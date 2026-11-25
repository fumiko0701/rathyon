const vscode = require('vscode');

let decorations = [];
let timeout = null;
let extensionUri = null;

const KEYWORD_COLOR = '#FFCC00';
const QUEIJO_PALETTE = ['#F29F05', '#F28705', '#BF4904'];
const RESERVED_COLORS = {
    'entrada':  '#4CAF50',
    'passagem': '#FFCC00',
    'saida':    '#F44336'
};

function clearDecorations() {
    for (const d of decorations) d.dispose();
    decorations = [];
}

function hashString(s) {
    let h = 0;
    for (let i = 0; i < s.length; i++) {
        h = ((h << 5) - h + s.charCodeAt(i)) | 0;
    }
    return Math.abs(h);
}

function colAfter(match, prefixLen) {
    // Retorna a coluna onde começa o nome (captura 3), pulando espaços
    const leading = match[1].length;
    const kw = prefixLen;
    const between = match[0].slice(leading + kw);
    const sp = between.match(/^\s+/);
    return leading + kw + (sp ? sp[0].length : 0);
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
    const keywordRanges = [];
    const reservedRanges = { entrada: [], passagem: [], saida: [] };
    const customRanges = [];

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];

        const startM = line.match(/^(\s*)(#tunel)\s+(\w+)/);
        if (startM) {
            const depth = stack.length + 1;
            const name = startM[3];
            stack.push({ name, start: i, depth });
            regionStartLines.push({ line: i, depth });

            keywordRanges.push({ line: i, start: startM[1].length, len: 6 }); // #tunel
            const nameCol = colAfter(startM, 6);
            if (RESERVED_COLORS[name]) {
                reservedRanges[name].push({ line: i, start: nameCol, len: name.length });
            } else {
                customRanges.push({ line: i, start: nameCol, len: name.length, name });
            }
            continue;
        }

        const gotoM = line.match(/^(\s*)(#vaparatunel)\s+(\w+)/);
        if (gotoM) {
            const name = gotoM[3];
            keywordRanges.push({ line: i, start: gotoM[1].length, len: 12 }); // #vaparatunel
            const nameCol = colAfter(gotoM, 12);
            if (RESERVED_COLORS[name]) {
                reservedRanges[name].push({ line: i, start: nameCol, len: name.length });
            } else {
                customRanges.push({ line: i, start: nameCol, len: name.length, name });
            }
            continue;
        }

        const endM = line.match(/^(\s*)(#toca)\b/);
        if (endM) {
            keywordRanges.push({ line: i, start: endM[1].length, len: 5 }); // #toca
            if (stack.length > 0) {
                const top = stack.pop();
                regions.push({ name: top.name, start: top.start, end: i, depth: top.depth });
            }
        }
    }

    while (stack.length > 0) {
        const top = stack.pop();
        regions.push({ name: top.name, start: top.start, end: lines.length - 1, depth: top.depth });
    }

    // 1) Fundo amarelo suave nas regioes
    if (regions.length > 0) {
        const bg = vscode.window.createTextEditorDecorationType({
            backgroundColor: 'rgba(255, 204, 0, 0.035)',
            isWholeLine: true,
        });
        decorations.push(bg);
        editor.setDecorations(bg, regions.map(r => new vscode.Range(
            new vscode.Position(r.start, 0),
            new vscode.Position(r.end, (lines[r.end] || '').length)
        )));
    }

    // 2) Keywords (#tunel / #vaparatunel / #toca) -> amarelo forte bold
    if (keywordRanges.length > 0) {
        const kwDeco = vscode.window.createTextEditorDecorationType({
            color: KEYWORD_COLOR,
            fontWeight: 'bold',
        });
        decorations.push(kwDeco);
        editor.setDecorations(kwDeco, keywordRanges.map(k =>
            new vscode.Range(k.line, k.start, k.line, k.start + k.len)));
    }

    // 3) Nomes reservados (entrada=verde, passagem=amarelo, saida=vermelho)
    for (const name of ['entrada', 'passagem', 'saida']) {
        const items = reservedRanges[name];
        if (items.length === 0) continue;
        const deco = vscode.window.createTextEditorDecorationType({
            color: RESERVED_COLORS[name],
            fontWeight: 'bold',
        });
        decorations.push(deco);
        editor.setDecorations(deco, items.map(r =>
            new vscode.Range(r.line, r.start, r.line, r.start + r.len)));
    }

    // 4) Nomes customizados -> paleta queijo deterministica por hash
    if (customRanges.length > 0) {
        const groups = new Map();
        for (const c of customRanges) {
            const color = QUEIJO_PALETTE[hashString(c.name) % QUEIJO_PALETTE.length];
            if (!groups.has(color)) groups.set(color, []);
            groups.get(color).push(c);
        }
        for (const [color, items] of groups) {
            const deco = vscode.window.createTextEditorDecorationType({
                color: color,
                fontWeight: 'bold',
            });
            decorations.push(deco);
            editor.setDecorations(deco, items.map(c =>
                new vscode.Range(c.line, c.start, c.line, c.start + c.len)));
        }
    }

    // 5) Gutter icons
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