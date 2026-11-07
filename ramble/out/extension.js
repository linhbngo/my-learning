"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
function activate(context) {
    // create a dedicate output channel for ramble extension
    const output = vscode.window.createOutputChannel('Ramble');
    // register a command to run ramble
    const command = vscode.commands.registerCommand('ramble.inspect', () => {
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
        }
        else {
            output.appendLine('No active text editor found.');
            output.show();
        }
    });
    // allow VSCode to clean up when the extension stops
    context.subscriptions.push(command, output);
}
function deactivate() {
    // no additional clean up needed for this extension
}
//# sourceMappingURL=extension.js.map