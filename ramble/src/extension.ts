import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {

    // create a dedicate output channel for ramble extension
    const output = vscode.window.createOutputChannel('Ramble');

    // register a command to run ramble
    const command = vscode.commands.registerCommand('ramble.inspect',
        () => {
            // get the active text editor
            const editor = vscode.window.activeTextEditor;
            if (editor) {
                const document = editor.document; // get the document of the active text editor
                const fileName = document.fileName; // get the file name of the document
                const language = document.languageId; // get the language of the document
                const sourceCode = document.getText(); // get the source code of the document

                // log the information to the output channel
                output.appendLine(`File Name: ${fileName}`);
                output.appendLine(`Language: ${language}`);
                output.appendLine(`Source Code:\n${sourceCode}`);
                output.show();

            } else {
                output.appendLine('No active text editor found.');
                output.show();
            }
        }
    );

    // allow VSCode to clean up when the extension stops
    context.subscriptions.push(command, output);
}

export function deactivate(): void {
    // no additional clean up needed for this extension
}