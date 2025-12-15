from __future__ import annotations

import json
import os
import sys
import threading
from dataclasses import dataclass
from typing import Any
from urllib.parse import unquote, urlparse

from .lexer import LexError, Lexer
from .parser import ParseError, Parser
from .tokens import Token, TokenType


# ----------------------------
# LSP / JSON-RPC transport
# ----------------------------


def _read_exact(n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = sys.stdin.buffer.read(n - len(buf))
        if not chunk:
            return b""
        buf += chunk
    return buf


def _read_message() -> dict[str, Any] | None:
    # Headers: "Content-Length: <n>\r\n" ... "\r\n" then JSON payload.
    headers: dict[str, str] = {}
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        line = line.decode("utf-8", errors="replace").strip()
        if line == "":
            break
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    if "content-length" not in headers:
        return None
    n = int(headers["content-length"])
    raw = _read_exact(n)
    if not raw:
        return None
    return json.loads(raw.decode("utf-8"))


def _send(payload: dict[str, Any]) -> None:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(data)}\r\n\r\n".encode("ascii"))
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()


def _respond(req_id: Any, result: Any) -> None:
    _send({"jsonrpc": "2.0", "id": req_id, "result": result})


def _respond_error(
    req_id: Any, code: int, message: str, data: Any | None = None
) -> None:
    err: dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    _send({"jsonrpc": "2.0", "id": req_id, "error": err})


def _notify(method: str, params: Any) -> None:
    _send({"jsonrpc": "2.0", "method": method, "params": params})


# ----------------------------
# URI / position helpers
# ----------------------------


def _uri_to_path(uri: str) -> str:
    if uri.startswith("file://"):
        p = urlparse(uri)
        path = unquote(p.path)
        return path
    return uri


def _lsp_pos_to_offset(text: str, line0: int, ch0: int) -> int:
    # LSP positions are 0-based. Treat character as Python codepoint index.
    if line0 < 0:
        return 0
    lines = text.splitlines(keepends=True)
    if line0 >= len(lines):
        return len(text)
    line_text = lines[line0]
    # Clamp within the line (excluding newline)
    raw_line = line_text.rstrip("\n").rstrip("\r")
    ch0 = max(0, min(ch0, len(raw_line)))
    return sum(len(lines[i]) for i in range(line0)) + ch0


def _pos_in_span(line1: int, col1: int, tok: Token) -> bool:
    # Token spans are half-open [start, end)
    s = tok.span.start
    e = tok.span.end
    if (line1, col1) < (s.line, s.column):
        return False
    if (line1, col1) >= (e.line, e.column):
        return False
    return True


def _span_to_lsp_range(span) -> dict[str, Any]:
    return {
        "start": {"line": span.start.line - 1, "character": span.start.column - 1},
        "end": {"line": span.end.line - 1, "character": span.end.column - 1},
    }


# ----------------------------
# Indexing (definitions/symbols/hover)
# ----------------------------


@dataclass(frozen=True)
class DefInfo:
    name: str
    kind: str  # "function" | "binding"
    name_span: Any
    full_span: Any
    params_text: str | None = None


@dataclass
class DocState:
    uri: str
    text: str
    version: int | None
    tokens: list[Token] | None = None
    defs: dict[str, list[DefInfo]] | None = None


def _index_document(
    uri: str, text: str
) -> tuple[list[dict[str, Any]], list[Token] | None, dict[str, list[DefInfo]] | None]:
    # Returns (diagnostics, tokens, defs). On lex/parse error, tokens/defs may be partial.
    diagnostics: list[dict[str, Any]] = []

    try:
        tokens = Lexer(text, filename=_uri_to_path(uri)).tokenize()
    except LexError as e:
        prefix = getattr(e, "error_type", "lexical")
        diagnostics.append(
            {
                "range": {
                    "start": {"line": e.line - 1, "character": e.column - 1},
                    "end": {"line": e.line - 1, "character": e.column},
                },
                "severity": 1,
                "source": "suay",
                "message": f"{prefix} error: {e.message}",
            }
        )
        return diagnostics, None, None

    try:
        Parser(tokens, text, filename=_uri_to_path(uri)).parse_program()
    except ParseError as e:
        prefix = getattr(e, "error_type", "syntax")
        diagnostics.append(
            {
                "range": {
                    "start": {"line": e.line - 1, "character": e.column - 1},
                    "end": {"line": e.line - 1, "character": e.column},
                },
                "severity": 1,
                "source": "suay",
                "message": f"{prefix} error: {e.message}",
            }
        )
        # Still return tokens; defs can still be built best-effort.

    defs = _extract_defs(text, tokens)
    return diagnostics, tokens, defs


def _extract_defs(text: str, tokens: list[Token]) -> dict[str, list[DefInfo]]:
    defs: dict[str, list[DefInfo]] = {}

    def add(di: DefInfo) -> None:
        defs.setdefault(di.name, []).append(di)

    i = 0
    while i < len(tokens) - 2:
        t0 = tokens[i]
        t1 = tokens[i + 1]
        # IDENT ← ...
        if t0.type == TokenType.IDENT and t1.type == TokenType.ARROW_BIND:
            name = str(t0.value)
            kind = "binding"
            params_text: str | None = None

            # function if next non-newline token is ⌁
            j = i + 2
            while j < len(tokens) and tokens[j].type == TokenType.NEWLINE:
                j += 1
            if j < len(tokens) and tokens[j].type == TokenType.LAMBDA:
                kind = "function"
                params_text = _extract_lambda_params(text, tokens, j)

            full_span = tokens[j].span if j < len(tokens) else t0.span
            add(
                DefInfo(
                    name=name,
                    kind=kind,
                    name_span=t0.span,
                    full_span=full_span,
                    params_text=params_text,
                )
            )
        i += 1

    # Sort by occurrence.
    for name, lst in defs.items():
        defs[name] = sorted(lst, key=lambda d: d.name_span.start.offset)
    return defs


def _extract_lambda_params(
    text: str, tokens: list[Token], lambda_index: int
) -> str | None:
    # lambda token is at lambda_index. Find next LPAREN .. matching RPAREN.
    i = lambda_index + 1
    while i < len(tokens) and tokens[i].type == TokenType.NEWLINE:
        i += 1
    if i >= len(tokens) or tokens[i].type != TokenType.LPAREN:
        return None
    start = tokens[i].span.start.offset

    depth = 0
    while i < len(tokens):
        if tokens[i].type == TokenType.LPAREN:
            depth += 1
        elif tokens[i].type == TokenType.RPAREN:
            depth -= 1
            if depth == 0:
                end = tokens[i].span.end.offset
                return text[start:end]
        i += 1
    return None


def _find_ident_at(tokens: list[Token], line0: int, ch0: int) -> Token | None:
    line1 = line0 + 1
    col1 = ch0 + 1
    for t in tokens:
        if t.type == TokenType.IDENT and _pos_in_span(line1, col1, t):
            return t
    return None


def _pick_def(
    defs: dict[str, list[DefInfo]], name: str, before_offset: int
) -> DefInfo | None:
    lst = defs.get(name)
    if not lst:
        return None
    # Pick the nearest definition occurring before the cursor.
    best = None
    for d in lst:
        if d.name_span.start.offset <= before_offset:
            best = d
        else:
            break
    return best or lst[0]


# ----------------------------
# Server
# ----------------------------


class SuayLspServer:
    def __init__(self) -> None:
        self._docs: dict[str, DocState] = {}
        self._lock = threading.Lock()
        self._shutdown = False

    def run(self) -> None:
        while True:
            msg = _read_message()
            if msg is None:
                return
            self._handle(msg)

    def _handle(self, msg: dict[str, Any]) -> None:
        method = msg.get("method")
        req_id = msg.get("id")
        params = msg.get("params") or {}

        if method == "initialize":
            result = {
                "capabilities": {
                    "textDocumentSync": 1,  # Full sync
                    "definitionProvider": True,
                    "documentSymbolProvider": True,
                    "hoverProvider": True,
                }
            }
            _respond(req_id, result)
            return

        if method == "initialized":
            return

        if method == "shutdown":
            self._shutdown = True
            _respond(req_id, None)
            return

        if method == "exit":
            raise SystemExit(0 if self._shutdown else 1)

        if method == "textDocument/didOpen":
            td = params.get("textDocument", {})
            uri = td.get("uri")
            text = td.get("text", "")
            version = td.get("version")
            if uri:
                self._update_doc(uri, text, version)
            return

        if method == "textDocument/didChange":
            td = params.get("textDocument", {})
            uri = td.get("uri")
            version = td.get("version")
            changes = params.get("contentChanges") or []
            if uri and changes:
                # Full sync: take the full text.
                text = changes[0].get("text", "")
                self._update_doc(uri, text, version)
            return

        if method == "textDocument/didClose":
            td = params.get("textDocument", {})
            uri = td.get("uri")
            if uri:
                with self._lock:
                    self._docs.pop(uri, None)
                _notify(
                    "textDocument/publishDiagnostics", {"uri": uri, "diagnostics": []}
                )
            return

        if method == "textDocument/definition":
            try:
                _respond(req_id, self._on_definition(params))
            except Exception as e:
                _respond_error(req_id, -32603, f"internal error: {e}")
            return

        if method == "textDocument/documentSymbol":
            try:
                _respond(req_id, self._on_document_symbols(params))
            except Exception as e:
                _respond_error(req_id, -32603, f"internal error: {e}")
            return

        if method == "textDocument/hover":
            try:
                _respond(req_id, self._on_hover(params))
            except Exception as e:
                _respond_error(req_id, -32603, f"internal error: {e}")
            return

        # Unknown request with id
        if req_id is not None:
            _respond_error(req_id, -32601, f"Method not found: {method}")

    def _update_doc(self, uri: str, text: str, version: int | None) -> None:
        diagnostics, tokens, defs = _index_document(uri, text)
        with self._lock:
            self._docs[uri] = DocState(
                uri=uri, text=text, version=version, tokens=tokens, defs=defs
            )
        _notify(
            "textDocument/publishDiagnostics", {"uri": uri, "diagnostics": diagnostics}
        )

    def _get_doc(self, uri: str) -> DocState | None:
        with self._lock:
            return self._docs.get(uri)

    def _on_definition(self, params: dict[str, Any]) -> Any:
        td = params.get("textDocument", {})
        uri = td.get("uri")
        pos = params.get("position", {})
        if not uri:
            return None

        doc = self._get_doc(uri)
        if not doc or not doc.tokens or not doc.defs:
            return None

        tok = _find_ident_at(doc.tokens, pos.get("line", 0), pos.get("character", 0))
        if tok is None:
            return None

        name = str(tok.value)
        before = _lsp_pos_to_offset(
            doc.text, pos.get("line", 0), pos.get("character", 0)
        )
        di = _pick_def(doc.defs, name, before)
        if di is None:
            return None

        return {
            "uri": uri,
            "range": _span_to_lsp_range(di.name_span),
        }

    def _on_document_symbols(self, params: dict[str, Any]) -> Any:
        td = params.get("textDocument", {})
        uri = td.get("uri")
        if not uri:
            return []
        doc = self._get_doc(uri)
        if not doc or not doc.defs:
            return []

        out: list[dict[str, Any]] = []
        for name, defs_list in doc.defs.items():
            # Prefer first occurrence for symbol list.
            d = defs_list[0]
            kind = 12 if d.kind == "function" else 13  # Function or Variable
            out.append(
                {
                    "name": name,
                    "kind": kind,
                    "range": _span_to_lsp_range(d.full_span),
                    "selectionRange": _span_to_lsp_range(d.name_span),
                }
            )
        # Sort for stable UI
        out.sort(key=lambda s: s["name"])
        return out

    def _on_hover(self, params: dict[str, Any]) -> Any:
        td = params.get("textDocument", {})
        uri = td.get("uri")
        pos = params.get("position", {})
        if not uri:
            return None
        doc = self._get_doc(uri)
        if not doc or not doc.tokens:
            return None

        tok = _find_ident_at(doc.tokens, pos.get("line", 0), pos.get("character", 0))
        if tok is None:
            return None
        name = str(tok.value)

        builtins = {
            "say": "builtin: say · x → ø (prints)",
            "hear": "builtin: hear · prompt → Text (read a line from stdin)",
            "text": "builtin: text · x → Text (stringify)",
            "abs": "builtin: abs · n → Num",
            "count": "builtin: count · x → Int (length of Text/List/Tuple/Map)",
            "at": "builtin: at · xs · i → value (index Text/List/Tuple)",
            "take": "builtin: take · xs · n → xs (prefix of Text/List)",
            "drop": "builtin: drop · xs · n → xs (suffix of Text/List)",
            "keys": "builtin: keys · map → List (map keys)",
            "has": "builtin: has · map · key → Bool (map contains key)",
            "put": "builtin: put · map · key · val → Map (returns new map)",
            "map": "builtin: map · f · [a] → [b]",
            "fold": "builtin: fold · f · init · [a] → b",
            "link": "builtin: link · path · name → value (load module by file path)",
        }

        if name in builtins:
            contents = builtins[name]
        elif doc.defs and name in doc.defs:
            d = doc.defs[name][0]
            if d.kind == "function":
                sig = d.params_text or "(?)"
                contents = f"function {name}{sig}"
            else:
                contents = f"binding {name}"
        else:
            contents = f"name {name}"

        return {
            "contents": {
                "kind": "markdown",
                "value": f"```suay\n{contents}\n```",
            }
        }


def main() -> None:
    # Ensure UTF-8 on stdout.
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    SuayLspServer().run()


if __name__ == "__main__":
    main()
