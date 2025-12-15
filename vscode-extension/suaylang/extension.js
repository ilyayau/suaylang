const path = require('path');
const vscode = require('vscode');
const { LanguageClient } = require('vscode-languageclient/node');

let client;

function activate(context) {
  const pythonPath = vscode.workspace
    .getConfiguration()
    .get('suay.server.pythonPath', 'python3');

  const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
  const workspaceRoot = workspaceFolder ? workspaceFolder.uri.fsPath : process.cwd();

  const serverOptions = {
    command: pythonPath,
    args: ['-m', 'suaylang.lsp_server'],
    options: {
      cwd: workspaceRoot,
      env: {
        ...process.env,
        PYTHONPATH: workspaceRoot + (process.env.PYTHONPATH ? path.delimiter + process.env.PYTHONPATH : '')
      }
    },
  };

  const clientOptions = {
    documentSelector: [{ scheme: 'file', language: 'suay' }]
  };

  client = new LanguageClient('suaylang', 'SuayLang', serverOptions, clientOptions);
  context.subscriptions.push(client.start());
}

function deactivate() {
  if (!client) {
    return undefined;
  }
  return client.stop();
}

module.exports = {
  activate,
  deactivate
};
