from __future__ import annotations

from dataclasses import dataclass

from . import ast
from .errors import Diagnostic
from .tokens import Span, Token, TokenType


class ParseError(Diagnostic):
    pass


@dataclass
class Parser:
    tokens: list[Token]
    source: str
    filename: str | None = None

    def __post_init__(self) -> None:
        self._i = 0
        self._line_starts = self._compute_line_starts(self.source)

    # ---------- Public API ----------

    def parse_program(self) -> ast.Program:
        try:
            self._skip_newlines()
            items: list[ast.Expr] = []
            start = self._peek().span.start

            while not self._check(TokenType.EOF):
                expr = self._parse_expr()
                items.append(expr)

                # Top-level requires line breaks between expressions.
                if not (self._check(TokenType.NEWLINE) or self._check(TokenType.EOF)):
                    self._error_here(
                        "Expected end of line after expression; use a newline to separate top-level forms"
                    )
                self._skip_newlines()

            end = self._peek().span.end
            return ast.Program(items=items, span=Span(start, end))
        except ParseError:
            raise
        except RecursionError:
            # Provide a clean, user-facing error when Python recursion is exhausted.
            tok = self._peek()
            pos = tok.span.start
            ctx = self._line_text(pos.line)
            raise ParseError(
                error_type="syntax",
                message="Maximum parse depth exceeded",
                line=pos.line,
                column=pos.column,
                filename=self.filename,
                source=self.source,
                context_line=ctx,
            )
        except Exception as e:
            # Defensive: convert internal parser failures into a user-facing ParseError.
            tok = self._peek()
            pos = tok.span.start
            ctx = self._line_text(pos.line)
            raise ParseError(
                error_type="syntax",
                message=f"Internal parser error: {type(e).__name__}: {e}",
                line=pos.line,
                column=pos.column,
                filename=self.filename,
                source=self.source,
                context_line=ctx,
            )

    # ---------- Expressions (precedence climbing) ----------

    def _parse_expr(self) -> ast.Expr:
        return self._parse_dispatch()

    def _parse_dispatch(self) -> ast.Expr:
        expr = self._parse_or()
        while self._match(TokenType.DISPATCH):
            # value ▷ ⟪ ... ⟫
            self._consume(
                TokenType.LDBLOCK, "Expected ⟪ after ▷ to start dispatch arms"
            )
            arms: list[ast.DispatchArm] = []
            self._skip_newlines()
            while not (self._check(TokenType.RDBLOCK) or self._check(TokenType.EOF)):
                self._consume(TokenType.DISPATCH, "Expected ▷ to start a dispatch arm")
                pat = self._parse_pattern()
                self._consume(
                    TokenType.FAT_ARROW, "Expected ⇒ after dispatch arm pattern"
                )
                self._skip_newlines()
                arm_expr = self._parse_expr()
                arms.append(
                    ast.DispatchArm(
                        pattern=pat,
                        expr=arm_expr,
                        span=Span(pat.span.start, arm_expr.span.end),
                    )
                )
                self._skip_newlines()
            if self._check(TokenType.EOF):
                self._error_here("Expected ⟫ to close dispatch")
            end_tok = self._consume(TokenType.RDBLOCK, "Expected ⟫ to close dispatch")
            expr = ast.Dispatch(
                value=expr, arms=arms, span=Span(expr.span.start, end_tok.span.end)
            )
        return expr

    def _parse_or(self) -> ast.Expr:
        expr = self._parse_and()
        while self._match(TokenType.OR):
            op = self._previous().lexeme
            right = self._parse_and()
            expr = ast.Binary(
                op=op,
                left=expr,
                right=right,
                span=Span(expr.span.start, right.span.end),
            )
        return expr

    def _parse_and(self) -> ast.Expr:
        expr = self._parse_compare()
        while self._match(TokenType.AND):
            op = self._previous().lexeme
            right = self._parse_compare()
            expr = ast.Binary(
                op=op,
                left=expr,
                right=right,
                span=Span(expr.span.start, right.span.end),
            )
        return expr

    def _parse_compare(self) -> ast.Expr:
        expr = self._parse_add()
        while self._match(
            TokenType.EQ,
            TokenType.NEQ,
            TokenType.LT,
            TokenType.LTE,
            TokenType.GT,
            TokenType.GTE,
        ):
            op = self._previous().lexeme
            right = self._parse_add()
            expr = ast.Binary(
                op=op,
                left=expr,
                right=right,
                span=Span(expr.span.start, right.span.end),
            )
        return expr

    def _parse_add(self) -> ast.Expr:
        expr = self._parse_mul()
        while self._match(TokenType.PLUS, TokenType.MINUS, TokenType.CONCAT):
            op = self._previous().lexeme
            right = self._parse_mul()
            expr = ast.Binary(
                op=op,
                left=expr,
                right=right,
                span=Span(expr.span.start, right.span.end),
            )
        return expr

    def _parse_mul(self) -> ast.Expr:
        expr = self._parse_prefix()
        while self._match(TokenType.MUL, TokenType.DIV, TokenType.MOD):
            op = self._previous().lexeme
            right = self._parse_prefix()
            expr = ast.Binary(
                op=op,
                left=expr,
                right=right,
                span=Span(expr.span.start, right.span.end),
            )
        return expr

    def _parse_prefix(self) -> ast.Expr:
        if self._match(TokenType.NOT, TokenType.MINUS):
            op_tok = self._previous()
            rhs = self._parse_call()  # call binds tighter than prefix in SuayLang spec
            return ast.Unary(
                op=op_tok.lexeme, expr=rhs, span=Span(op_tok.span.start, rhs.span.end)
            )
        return self._parse_call()

    def _parse_call(self) -> ast.Expr:
        expr = self._parse_variant()
        while self._match(TokenType.CALL):
            rhs = self._parse_call_arg()
            expr = ast.Call(
                func=expr, arg=rhs, span=Span(expr.span.start, rhs.span.end)
            )
        return expr

    def _parse_call_arg(self) -> ast.Expr:
        # Allow prefix operators in call arguments (e.g. f · -7) without
        # making call-chains right-associative.
        if self._match(TokenType.NOT, TokenType.MINUS):
            op_tok = self._previous()
            rhs = self._parse_variant()
            return ast.Unary(
                op=op_tok.lexeme, expr=rhs, span=Span(op_tok.span.start, rhs.span.end)
            )
        return self._parse_variant()

    def _parse_variant(self) -> ast.Expr:
        # Variant constructor: tag•payload, where tag is IDENT.
        if self._check(TokenType.IDENT) and self._check_next(TokenType.BULLET):
            tag_tok = self._advance()
            self._advance()  # •
            payload = self._parse_primary()
            return ast.VariantExpr(
                tag=tag_tok.value if isinstance(tag_tok.value, str) else tag_tok.lexeme,
                payload=payload,
                span=Span(tag_tok.span.start, payload.span.end),
            )
        return self._parse_primary()

    def _parse_primary(self) -> ast.Expr:
        if self._match(TokenType.INT):
            t = self._previous()
            return ast.IntLit(value=int(t.value), span=t.span)
        if self._match(TokenType.DEC):
            t = self._previous()
            return ast.DecLit(value=float(t.value), span=t.span)
        if self._match(TokenType.STRING):
            t = self._previous()
            return ast.TextLit(value=str(t.value), span=t.span)
        if self._match(TokenType.UNIT):
            t = self._previous()
            return ast.UnitLit(span=t.span)
        if self._match(TokenType.TRUE):
            t = self._previous()
            return ast.BoolLit(value=True, span=t.span)
        if self._match(TokenType.FALSE):
            t = self._previous()
            return ast.BoolLit(value=False, span=t.span)

        # Cycle: ⟲ seed ▷ ⟪ ... ⟫
        if self._match(TokenType.CYCLE):
            start_tok = self._previous()
            self._skip_newlines()
            # Important: the ▷ after the seed belongs to the cycle syntax,
            # so we must parse the seed *without* consuming dispatch.
            seed = self._parse_or()
            self._consume(TokenType.DISPATCH, "Expected ▷ after ⟲ seed")
            self._consume(TokenType.LDBLOCK, "Expected ⟪ to start cycle arms")
            arms: list[ast.CycleArm] = []
            self._skip_newlines()
            while not (self._check(TokenType.RDBLOCK) or self._check(TokenType.EOF)):
                self._consume(TokenType.DISPATCH, "Expected ▷ to start a cycle arm")
                pat = self._parse_pattern()
                self._consume(TokenType.FAT_ARROW, "Expected ⇒ after cycle arm pattern")
                if self._match(TokenType.CONTINUE):
                    mode = "continue"
                elif self._match(TokenType.FINISH):
                    mode = "finish"
                else:
                    self._error_here("Expected ↩ or ↯ after ⇒ in cycle arm")
                self._skip_newlines()
                arm_expr = self._parse_expr()
                arms.append(
                    ast.CycleArm(
                        pattern=pat,
                        mode=mode,
                        expr=arm_expr,
                        span=Span(pat.span.start, arm_expr.span.end),
                    )
                )
                self._skip_newlines()
            if self._check(TokenType.EOF):
                self._error_here("Expected ⟫ to close cycle")
            end_tok = self._consume(TokenType.RDBLOCK, "Expected ⟫ to close cycle")
            return ast.Cycle(
                seed=seed, arms=arms, span=Span(start_tok.span.start, end_tok.span.end)
            )

        # Lambda: ⌁(p1 p2 ...) body
        if self._match(TokenType.LAMBDA):
            start_tok = self._previous()
            self._consume(TokenType.LPAREN, "Expected ( after ⌁")
            params: list[ast.Pattern] = []
            self._skip_newlines()
            while not self._check(TokenType.RPAREN):
                params.append(self._parse_pattern())
                self._skip_separators_in_listlike()
                if self._check(TokenType.RPAREN):
                    break
            self._consume(TokenType.RPAREN, "Expected ) to close parameter list")
            self._skip_newlines()
            body = self._parse_expr()
            return ast.Lambda(
                params=params, body=body, span=Span(start_tok.span.start, body.span.end)
            )

        # Block: ⟪ ... ⟫
        if self._match(TokenType.LDBLOCK):
            start_tok = self._previous()
            items: list[ast.Expr] = []
            self._skip_newlines()
            while not (self._check(TokenType.RDBLOCK) or self._check(TokenType.EOF)):
                items.append(self._parse_expr())
                # Inside blocks, require line breaks between forms.
                if not (
                    self._check(TokenType.NEWLINE) or self._check(TokenType.RDBLOCK)
                ):
                    self._error_here("Expected end of line after block expression")
                self._skip_newlines()
            if self._check(TokenType.EOF):
                self._error_here("Expected ⟫ to close block")
            end_tok = self._consume(TokenType.RDBLOCK, "Expected ⟫ to close block")
            if not items:
                self._raise_at_span(
                    Span(start_tok.span.start, end_tok.span.end),
                    "Empty block ⟪ ⟫ is not allowed",
                )
            return ast.Block(
                items=items, span=Span(start_tok.span.start, end_tok.span.end)
            )

        # Tuple: (e1 e2 ...)
        if self._match(TokenType.LPAREN):
            start_tok = self._previous()
            items: list[ast.Expr] = []
            saw_comma = False
            self._skip_newlines()
            while not self._check(TokenType.RPAREN):
                items.append(self._parse_expr())
                # Track commas so we can distinguish grouping: (expr) vs 1-tuple: (expr,)
                if self._match(TokenType.COMMA):
                    saw_comma = True
                    self._skip_newlines()
                    continue
                # newlines also separate items in tuple literals
                if self._match(TokenType.NEWLINE):
                    self._skip_newlines()
                    continue
                if self._check(TokenType.RPAREN):
                    break
            end_tok = self._consume(TokenType.RPAREN, "Expected ) to close tuple")
            # Grouping: (expr) is just expr. A 1-tuple must be written as (expr,).
            if len(items) == 1 and not saw_comma:
                return items[0]
            return ast.TupleExpr(
                items=items, span=Span(start_tok.span.start, end_tok.span.end)
            )

        # List: [e1 e2 ...]
        if self._match(TokenType.LBRACK):
            start_tok = self._previous()
            items: list[ast.Expr] = []
            self._skip_newlines()
            while not self._check(TokenType.RBRACK):
                if self._check(TokenType.ELLIPSIS):
                    self._error_here(
                        "⋯ (ellipsis) is only allowed in list patterns, not list expressions"
                    )
                items.append(self._parse_expr())
                self._skip_separators_in_listlike()
                if self._check(TokenType.RBRACK):
                    break
            end_tok = self._consume(TokenType.RBRACK, "Expected ] to close list")
            return ast.ListExpr(
                items=items, span=Span(start_tok.span.start, end_tok.span.end)
            )

        # Map: ⟦ k ↦ v , ... ⟧
        if self._match(TokenType.LDBRACK):
            start_tok = self._previous()
            entries: list[tuple[ast.Expr, ast.Expr]] = []
            self._skip_newlines()
            while not self._check(TokenType.RDBRACK):
                key = self._parse_expr()
                self._consume(TokenType.ARROW_MAP, "Expected ↦ after map key")
                val = self._parse_expr()
                entries.append((key, val))
                self._skip_separators_in_listlike()
                if self._check(TokenType.RDBRACK):
                    break
            end_tok = self._consume(TokenType.RDBRACK, "Expected ⟧ to close map")
            return ast.MapExpr(
                entries=entries, span=Span(start_tok.span.start, end_tok.span.end)
            )

        # Binding: name ← expr
        if self._check(TokenType.IDENT) and self._check_next(TokenType.ARROW_BIND):
            name_tok = self._advance()
            self._advance()  # ←
            self._skip_newlines()
            val = self._parse_expr()
            return ast.Binding(
                name=str(name_tok.value),
                value=val,
                span=Span(name_tok.span.start, val.span.end),
            )

        # Mutation: name ⇐ expr
        if self._check(TokenType.IDENT) and self._check_next(TokenType.ARROW_SET):
            name_tok = self._advance()
            self._advance()  # ⇐
            self._skip_newlines()
            val = self._parse_expr()
            return ast.Mutation(
                name=str(name_tok.value),
                value=val,
                span=Span(name_tok.span.start, val.span.end),
            )

        if self._match(TokenType.IDENT):
            t = self._previous()
            return ast.Name(value=str(t.value), span=t.span)

        self._error_here("Expected an expression")

    # ---------- Patterns ----------

    def _parse_pattern(self) -> ast.Pattern:
        return self._parse_pattern_variant()

    def _parse_pattern_variant(self) -> ast.Pattern:
        # tag•payload
        if self._check(TokenType.IDENT) and self._check_next(TokenType.BULLET):
            tag_tok = self._advance()
            self._advance()  # •
            payload = self._parse_pattern_atom()
            return ast.PVariant(
                tag=str(tag_tok.value),
                payload=payload,
                span=Span(tag_tok.span.start, payload.span.end),
            )
        return self._parse_pattern_atom()

    def _parse_pattern_atom(self) -> ast.Pattern:
        if self._match(TokenType.UNDERSCORE):
            t = self._previous()
            return ast.PWildcard(span=t.span)

        if self._match(TokenType.INT):
            t = self._previous()
            return ast.PInt(value=int(t.value), span=t.span)
        if self._match(TokenType.DEC):
            t = self._previous()
            return ast.PDec(value=float(t.value), span=t.span)
        if self._match(TokenType.STRING):
            t = self._previous()
            return ast.PText(value=str(t.value), span=t.span)
        if self._match(TokenType.UNIT):
            t = self._previous()
            return ast.PUnit(span=t.span)
        if self._match(TokenType.TRUE):
            t = self._previous()
            return ast.PBool(value=True, span=t.span)
        if self._match(TokenType.FALSE):
            t = self._previous()
            return ast.PBool(value=False, span=t.span)

        if self._match(TokenType.LPAREN):
            start = self._previous()
            items: list[ast.Pattern] = []
            saw_comma = False
            self._skip_newlines()
            while not self._check(TokenType.RPAREN):
                items.append(self._parse_pattern())
                if self._match(TokenType.COMMA):
                    saw_comma = True
                    self._skip_newlines()
                    continue
                if self._match(TokenType.NEWLINE):
                    self._skip_newlines()
                    continue
                if self._check(TokenType.RPAREN):
                    break
            end = self._consume(TokenType.RPAREN, "Expected ) to close tuple pattern")
            # Grouping in patterns: (p) is just p. A 1-tuple pattern is (p,).
            if len(items) == 1 and not saw_comma:
                return items[0]
            return ast.PTuple(items=items, span=Span(start.span.start, end.span.end))

        if self._match(TokenType.LBRACK):
            start = self._previous()
            items: list[ast.Pattern] = []
            tail: ast.Pattern | None = None
            self._skip_newlines()
            while not self._check(TokenType.RBRACK):
                if self._match(TokenType.ELLIPSIS):
                    tail = self._parse_pattern_atom()
                    if not isinstance(tail, (ast.PName, ast.PWildcard)):
                        self._raise_at_span(
                            tail.span, "List tail after ⋯ must be a name or _"
                        )
                    self._skip_newlines()
                    break
                items.append(self._parse_pattern())
                self._skip_separators_in_listlike()
                if self._check(TokenType.RBRACK):
                    break
            end = self._consume(TokenType.RBRACK, "Expected ] to close list pattern")
            return ast.PList(
                items=items, tail=tail, span=Span(start.span.start, end.span.end)
            )

        if self._match(TokenType.IDENT):
            t = self._previous()
            return ast.PName(name=str(t.value), span=t.span)

        self._error_here("Expected a pattern")

    # ---------- Helpers ----------

    def _skip_newlines(self) -> None:
        while self._match(TokenType.NEWLINE):
            pass

    def _skip_separators_in_listlike(self) -> None:
        # Inside (), [], ⟦⟧, allow commas and/or newlines between items.
        while True:
            if self._match(TokenType.COMMA):
                continue
            if self._match(TokenType.NEWLINE):
                continue
            break

    def _match(self, *types: TokenType) -> bool:
        if self._check(*types):
            self._advance()
            return True
        return False

    def _consume(self, typ: TokenType, message: str) -> Token:
        if self._check(typ):
            return self._advance()
        self._error_here(message)

    def _check(self, *types: TokenType) -> bool:
        if self._is_at_end():
            return TokenType.EOF in types
        return self._peek().type in types

    def _check_next(self, typ: TokenType) -> bool:
        if self._i + 1 >= len(self.tokens):
            return False
        return self.tokens[self._i + 1].type == typ

    def _advance(self) -> Token:
        if not self._is_at_end():
            self._i += 1
        return self._previous()

    def _peek(self) -> Token:
        return self.tokens[self._i]

    def _previous(self) -> Token:
        return self.tokens[self._i - 1]

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _error_here(self, message: str) -> None:
        tok = self._peek()
        pos = tok.span.start
        ctx = self._line_text(pos.line)
        found = tok.lexeme if tok.lexeme else tok.type.value
        full = f"{message} (got {found})"
        raise ParseError(
            error_type="syntax",
            message=full,
            line=pos.line,
            column=pos.column,
            filename=self.filename,
            source=self.source,
            context_line=ctx,
        )

    def _raise_at_span(self, span: Span, message: str) -> None:
        pos = span.start
        ctx = self._line_text(pos.line)
        raise ParseError(
            error_type="syntax",
            message=message,
            line=pos.line,
            column=pos.column,
            filename=self.filename,
            source=self.source,
            context_line=ctx,
        )

    @staticmethod
    def _compute_line_starts(s: str) -> list[int]:
        starts = [0]
        for i, ch in enumerate(s):
            if ch == "\n":
                starts.append(i + 1)
        return starts

    def _line_text(self, line: int) -> str | None:
        if line <= 0 or line > len(self._line_starts):
            return None
        start = self._line_starts[line - 1]
        end = self.source.find("\n", start)
        if end == -1:
            end = len(self.source)
        return self.source[start:end]
