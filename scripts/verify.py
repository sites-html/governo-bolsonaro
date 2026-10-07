import json, datetime, re
from pathlib import Path
from urllib.parse import urlparse

root = Path(__file__).resolve().parents[1]
events = json.loads((root / 'events.json').read_text())
js = (root / 'events.js').read_text()
assert json.loads(js.removeprefix('window.ARCHIVE_EVENTS = ').rstrip().removesuffix(';')) == events
assert events == sorted(events, key=lambda e: (e['date'], e['id']))
assert events[-1]['date']=='2023-01-08' and 'Planalto' in events[-1]['title']
assert all('2019-01-01'<=e['date']<='2023-01-08' for e in events)
assert len({e['id'] for e in events}) == len(events)
required_months = {f'{y}-{m:02}' for y in range(2019,2024) for m in range(1,13) if f'{y}-{m:02}'<='2023-01'}
assert {e['date'][:7] for e in events} == required_months
categories = {'Democracia','Saúde','Economia','Meio ambiente','Governo','Direitos'}
for e in events:
    datetime.date.fromisoformat(e['date'])
    assert e['title'] and e['summary'] and e['sources']
    assert e['category'] in categories and e['importance'] in range(1,6)
    assert re.fullmatch(r'registro-[a-z0-9-]+',e['id'])
    for s in e['sources']:
        assert s['name'] and urlparse(s['url']).scheme == 'https' and urlparse(s['url']).netloc
        if s.get('published'): datetime.date.fromisoformat(s['published'] + ('-01' if len(s['published']) == 7 else ''))
    if e.get('image'):
        assert e['image']['credit'] and e['image']['alt']
        if e['image'].get('local'): assert (root / e['image']['local']).is_file()
    if e.get('video'):
        assert urlparse(e['video']['url']).scheme == 'https'
        assert e['video']['source']
        if 'youtube.com/watch' in e['video']['url'] or 'youtu.be/' in e['video']['url']: assert re.search(r'(youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]{11}',e['video']['url'])
assert len({e['rank'] for e in events if e.get('rank')}) == len([e for e in events if e.get('rank')])
for f in ['index.html','style.css','app.js','assets/favicon.svg','timeline-engine.js','README.md','pesquisa.md','.nojekyll']: assert (root / f).exists()
print(f'OK: {len(events)} registros; 49/49 meses; fontes, datas e mídia válidas; JSON/JS idênticos.')
