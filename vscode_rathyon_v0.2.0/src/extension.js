const vscode = require('vscode');

let decorations = [];
let timeout = null;
let extensionUri = null;

function clearDecorations() {
    for (const d of decorations) d.dispose();
    decorations = [];
}

function getColorForRole(name) {
    switch (name) {
        case 'start': return '#4CAF50'; // verde
        case 'step':  return '#2196F3'; // azul
        case 'end':   return '#F44336'; // vermelho
        default:      return null;      // herda (custom)
    }
}

function updateDecorations(editor) {
    clearDecorations();
    if (!editor || editor.document.languageId !== 'rathyon') return;
    if (!extensionUri) return;

    const config = vscode.workspace.getConfiguration('rathyon');
    if (!config.get('regionHighlightEnabled', true)) return;

    const lines = editor.document.getText().split('\n');
    const stack = [];
    const regions = [];
    const regionStartLines = [];

    for (let i = 0; i < lines.length; i++) {
        const startMatch = lines[i].match(/^(\s*)#tunel\s+(\w+)/);
        const endMatch = lines[i].match(/^\s*#toca\b/);
        if (startMatch) {
            const depth = stack.length + 1;
            stack.push({ name: startMatch[2], start: i, depth });
            regionStartLines.push({ line: i, depth });
        } else if (endMatch && stack.length > 0) {
            const top = stack.pop();
            regions.push({ name: top.name, start: top.start, end: i, depth: top.depth });
        }
    }
    while (stack.length > 0) {
        const top = stack.pop();
        regions.push({ name: top.name, start: top.start, end: lines.length - 1, depth: top.depth });
    }

    // 1) Fundo amarelo bem suave; aninhamento compõe alphas → gradiente natural
    if (regions.length > 0) {
        const bg = vscode.window.createTextEditorDecorationType({
            backgroundColor: 'rgba(255, 204, 0, 0.035)',
            isWholeLine: true,
        });
        decorations.push(bg);
        const ranges = regions.map(r => new vscode.Range(
            new vscode.Position(r.start, 0),
            new vscode.Position(r.end, (lines[r.end] || '').length)
        ));
        editor.setDecorations(bg, ranges);
    }

    // 2) Keywords em amarelo bold (#tunel / #toca / #vaparatunel)
    const kwDeco = vscode.window.createTextEditorDecorationType({
        color: '#FFCC00',
        fontWeight: 'bold',
    });
    decorations.push(kwDeco);
    const kwRanges = [];
    const kws = ['#tunel', '#toca', '#vaparatunel'];
    for (let i = 0; i < lines.length; i++) {
        for (const kw of kws) {
            let idx = lines[i].indexOf(kw);
            while (idx !== -1) {
                kwRanges.push(new vscode.Range(i, idx, i, idx + kw.length));
                idx = lines[i].indexOf(kw, idx + kw.length);
            }
        }
    }
    if (kwRanges.length > 0) editor.setDecorations(kwDeco, kwRanges);

    // 3) Nome da região (inclusive em #vaparatunel) colorido por papel
    const roleTypes = new Map();
    const roleRanges = new Map();
    for (let i = 0; i < lines.length; i++) {
        const mR = lines[i].match(/^(\s*)#tunel\s+(\w+)/);
        const mG = lines[i].match(/^(\s*)#vaparatunel\s+(\w+)/);
        const m = mR || mG;
        if (!m) continue;
        const kw = mR ? '#tunel' : '#vaparatunel';
        const nameStart = m[1].length + kw.length + 1;
        const nameEnd = nameStart + m[2].length;
        const color = getColorForRole(m[2]);
        if (!color) continue;
        if (!roleTypes.has(color)) {
            const deco = vscode.window.createTextEditorDecorationType({
                color: color,
                fontWeight: 'bold',
            });
            decorations.push(deco);
            roleTypes.set(color, deco);
            roleRanges.set(color, []);
        }
        roleRanges.get(color).push(new vscode.Range(i, nameStart, i, nameEnd));
    }
    for (const [color, ranges] of roleRanges) {
        editor.setDecorations(roleTypes.get(color), ranges);
    }

    // 4) Ícone no gutter na linha #tunel; cresce com a profundidade
    if (regionStartLines.length > 0) {
        const gutterTypes = new Map();
        for (const { depth } of regionStartLines) {
            const d = Math.min(depth, 5);
            if (!gutterTypes.has(d)) {
                const iconPath = vscode.Uri.joinPath(extensionUri, 'media', `region-${d}.svg`);
                const deco = vscode.window.createTextEditorDecorationType({
                    gutterIconPath: iconPath,
                    gutterIconSize: 'contain',
                });
                decorations.push(deco);
                gutterTypes.set(d, deco);
            }
        }
        for (const [depth, deco] of gutterTypes) {
            const ranges = regionStartLines
                .filter(r => Math.min(r.depth, 5) === depth)
                .map(r => new vscode.Range(r.line, 0, r.line, 0));
            editor.setDecorations(deco, ranges);
        }
    }
}

function activate(context) {
    extensionUri = context.extensionUri;
    if (vscode.window.activeTextEditor) {
        updateDecorations(vscode.window.activeTextEditor);
    }
    context.subscriptions.push(
        vscode.window.onDidChangeActiveTextEditor(ed => updateDecorations(ed)),
        vscode.workspace.onDidChangeTextDocument(e => {
            if (e.document === vscode.window.activeTextEditor?.document) {
                if (timeout) clearTimeout(timeout);
                timeout = setTimeout(() => updateDecorations(vscode.window.activeTextEditor), 150);
            }
        }),
        vscode.workspace.onDidChangeConfiguration(e => {
            if (e.affectsConfiguration('rathyon')) {
                updateDecorations(vscode.window.activeTextEditor);
            }
        })
    );
}

function deactivate() { clearDecorations(); }

module.exports = { activate, deactivate };