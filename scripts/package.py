"""Gera uma prévia HTML autônoma e o ZIP publicável, sem dependências externas."""
from pathlib import Path
import json, base64, urllib.parse, zipfile, mimetypes
root = Path(__file__).resolve().parents[1]
out = root.parent
html = (root/'index.html').read_text()
css = (root/'style.css').read_text()
app = (root/'app.js').read_text()
engine = (root/'timeline-engine.js').read_text()
category_script = (root/'categories.js').read_text()
events = json.loads((root/'events.json').read_text())
for e in events:
    if e.get('image', {}).get('local'):
        data = (root/e['image']['local']).read_bytes()
        mime = mimetypes.guess_type(e['image']['local'])[0] or 'image/jpeg'
        e['image']['local'] = 'data:' + mime + ';base64,' + base64.b64encode(data).decode()
mdurl = 'data:text/markdown;charset=utf-8,' + urllib.parse.quote((root/'pesquisa.md').read_text())
jsonurl = 'data:application/json;charset=utf-8,' + urllib.parse.quote((root/'events.json').read_text())
app = app.replace('href="pesquisa.md"', 'href="'+mdurl+'"').replace('href="events.json"', 'href="'+jsonurl+'"')
html = html.replace('<link rel="stylesheet" href="style.css">', '<style>'+css+'</style>')
icon = base64.b64encode((root/'assets/favicon.svg').read_bytes()).decode()
html = html.replace('href="assets/favicon.svg"', 'href="data:image/svg+xml;base64,'+icon+'"')
html = html.replace('<script src="categories.js"></script>', '<script>'+category_script+'</script>')
html = html.replace('<script src="timeline-engine.js"></script>', '<script>'+engine+'</script>')
html = html.replace('<script src="events.js"></script>', '<script>window.ARCHIVE_EVENTS = '+json.dumps(events,ensure_ascii=False).replace('</','<\\/')+';</script>')
html = html.replace('<script src="app.js"></script>', '<script>'+app+'</script>')
html = html.replace('href="pesquisa.md"', 'href="'+mdurl+'"')
(out/'memoria-publica.html').write_text(html)
with zipfile.ZipFile(out/'memoria-publica-github.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(root.rglob('*')):
        if f.is_file() and '__pycache__' not in f.parts:
            z.write(f,Path('memoria-publica')/f.relative_to(root))
with zipfile.ZipFile(out/'memoria-publica-github.zip') as z:
    assert z.testzip() is None
    print(f'Pacote íntegro: {len(z.namelist())} arquivos.')
print('Prévia HTML gerada com imagens e código incorporados.')
