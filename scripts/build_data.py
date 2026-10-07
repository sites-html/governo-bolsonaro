"""Regenera o JS para abertura local e a lista de pesquisa a partir de events.json."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
events = json.loads((root / 'events.json').read_text())
(root / 'events.js').write_text('window.ARCHIVE_EVENTS = ' + json.dumps(events, ensure_ascii=False, indent=2) + ';\n')
months = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
lines = ['# Memória pública — pesquisa de 2019 a 2023', '', f'{len(events)} registros. Cobertura de janeiro de 2019 até 8 de janeiro de 2023 (49 meses). Pesquisa inicial em 5 de outubro de 2026.', '',
'## Escopo e método', '',
'Recorte crítico do governo Jair Bolsonaro (1º/01/2019–31/12/2022), de integrantes da administração, de Flávio Bolsonaro e de atos relacionados até a invasão de 8 de janeiro de 2023. Não se atribui automaticamente ao presidente toda ação de ministros, familiares, apoiadores ou servidores. Os resumos e títulos são editoriais e originais; links permitem consultar os textos das fontes.', '',
'Datas priorizam o acontecimento. Reportagens posteriores podem revelar fatos de anos anteriores. Para divulgação de indicadores ou denúncia pública, registra-se esse ato, com notas sobre o período de referência ou a data original. Quando desconhecida, a data original não é inventada. Os estados de denúncia, investigação e decisão são identificados; atos descobertos posteriormente registram expressamente essa condição. Anulações conhecidas e a condenação posterior na trama golpista aparecem em notas específicas.', '',
'## Destaques: seleção editorial, não ranking medido de engajamento', '',
'Não foi obtida uma série comparável de interações negativas em redes sociais de 2019 a 2023. Portanto não seria correto alegar um ranking por engajamento. A lista abaixo é uma hierarquia editorial explícita: prioridade para ataques à democracia e crises de alcance humano amplo, seguida por declarações e episódios institucionais centrais. Repercussão nacional/internacional é indicada somente onde fontes a documentam. A importância 1–5 é editorial: 5 = episódio central ou de amplo alcance; 4 = controvérsia nacional relevante; 3 = episódio contextual; 2 = desdobramento limitado; 1 = registro complementar. Não é uma escala científica e não é calculada com curtidas.', '']
ranked = sorted((e for e in events if e.get('rank')), key=lambda e: e['rank'])
for e in ranked:
    lines += [f"{e['rank']}. **{e['date']} — {e['title']}** (importância editorial {e['importance']}/5).", f"   {e.get('prominence', 'Prioridade editorial por alcance e relação com a narrativa histórica.')}"]
lines += ['', '### Métricas pontuais encontradas', '']
for e in events:
    if e.get('engagement'):
        lines += [f"- **{e['date']}**: {e['engagement']['text']}", f"  Fonte: {e['engagement']['sourceUrl']}"]
lines += ['', 'Essas métricas medem fenômenos e janelas diferentes. Não devem ser colocadas em um ranking quantitativo comum.', '', '## Cronologia mensal', '']
last = None
for e in events:
    ym = e['date'][:7]
    if ym != last:
        lines += [f"### {months[int(ym[5:])-1].capitalize()} de {ym[:4]}", '']
        last = ym
    lines += [f"#### {e['date']} — {e['title']}", '', f"Tema: {e['category']}. Classificação do registro: {e['status']}. Importância editorial: {e['importance']}/5.", '', e['summary'], '']
    if e.get('dateNote'): lines += ['Sobre a data: ' + e['dateNote'], '']
    if e.get('update'): lines += ['Desdobramento posterior: ' + e['update'], '']
    for s in e['sources']: lines += [f"- [{s['name']}]({s['url']})" + (f" — publicação: {s['published']}" if s.get('published') else '')]
    if e.get('image'):
        i = e['image']
        lines += [f"- Imagem: {i['credit']}. {i.get('context','')} Origem: {i.get('sourceUrl',i['url'])}", f"  Condições de reprodução: {i.get('license','consultar fonte')} {i.get('licenseUrl','')}"]
    if e.get('video'): lines += [f"- [Vídeo — {e['video'].get('source','fonte')}]({e['video']['url']})"]
    lines += ['']
lines += ['## Limites da pesquisa', '', 'Busca extensiva inicial, sem pretensão de exaustividade absoluta. Cobertura mensal não significa equivalência de gravidade. Não se fez atribuição causal exclusiva ao governo de todos os indicadores econômicos e ambientais. URLs foram encontradas em busca e fontes consultadas, mas algumas páginas históricas, vídeos e portais podem ter acesso restrito, mudar ou retornar erro. O projeto não inclui contagens fabricadas de engajamento, nem reproduz integralmente reportagens.']
(root / 'pesquisa.md').write_text('\n'.join(lines) + '\n')
print(f'Gerados events.js e pesquisa.md com {len(events)} registros.')
