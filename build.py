#!/usr/bin/env python3
"""Static site generator for clementquintard.com.

Run `python3 build.py` (needs: pip install markdown). Output goes to site/, which is what gets deployed.
Content: posts/*.md (blog), pubs.json (publications), page-research.md (background page), img/, cv.pdf.
--artifact: write index.html without a document skeleton (used only for Claude artifact previews)."""
import json, re, html, os, sys, shutil, datetime, glob
from markdown import markdown

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SRC, 'site')
ARTIFACT = '--artifact' in sys.argv
UP = 'https://www.clementquintard.com/wp-content/uploads/'

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Schibsted+Grotesk:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap">'

def head(title, rel, desc=''):
    s = f'<title>{html.escape(title)}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
    if desc: s += f'<meta name="description" content="{html.escape(desc)}">\n'
    s += FONTS + f'\n<link rel="stylesheet" href="{rel}style.css">\n'
    return s

def nav(rel, home):
    h = home
    return f'''<header class="nav"><div class="wrap">
<a class="brand" href="{h}">Clément <em>Quintard</em></a>
<nav><ul>
<li><a href="{h}#research">Research</a></li>
<li><a href="{h}#publications">Publications</a></li>
<li><a href="{h}#blog">Blog</a></li>
<li><a href="{h}#contact">Contact</a></li>
</ul></nav></div></header>'''

TOTOP = '<a href="#" class="totop" id="totop" aria-label="Back to top" hidden><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M12 5l-7 7h4v7h6v-7h4z" fill="currentColor"/></svg></a>'
FOOT = TOTOP + '<footer><div class="wrap"><span>© Clément Quintard {y}</span><span>Vancouver, BC</span></div></footer>'.format(y=datetime.date.today().year)

MATHJAX = '<script>window.MathJax={tex:{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["$$","$$"]]}};</script><script async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js"></script>'

def page(body, title, rel='', desc='', skeleton=True):
    inner = head(title, rel, desc) + body + f'\n<script src="{rel}site.js"></script>'
    if '$$' in body or '\\(' in body: inner += MATHJAX
    if not skeleton: return inner
    return '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + inner.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '', 1) + '\n</body></html>'

# ---------- content ----------
# Each post is posts/<slug>.md: a front matter block (title, date, image, excerpt) then the body,
# written in Markdown or HTML. Images live in img/ and are referenced as img/<file>.
pubs = json.load(open(os.path.join(SRC, 'pubs.json')))

def read_post(path):
    raw = open(path, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n', raw, re.S)
    meta = dict(line.split(':', 1) for line in m.group(1).splitlines() if ':' in line)
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    body = raw[m.end():]
    body_html = body if meta.get('format') == 'html' else markdown(body, extensions=['tables', 'fenced_code', 'md_in_html'])
    body_html = body_html.replace('<table', '<div class="tbl"><table').replace('</table>', '</table></div>') if '<div class="tbl">' not in body_html else body_html
    body_html = re.sub(r'<a href="(http[^"]+)"(?![^>]*target)', r'<a href="\1" target="_blank" rel="noopener"', body_html)
    body_html = body_html.replace(' target="_blank" rel="noopener" target="_blank" rel="noreferrer noopener"', ' target="_blank" rel="noopener"')
    return {
        'slug': os.path.splitext(os.path.basename(path))[0],
        'title': meta.get('title', ''), 'date': meta.get('date', ''),
        'image': meta.get('image', ''), 'alt': meta.get('alt', ''),
        'excerpt': meta.get('excerpt', ''), 'html': body_html,
        'lang': meta.get('lang', 'en'), 'translation_of': meta.get('translation_of', ''),
    }

all_posts = sorted((read_post(p) for p in glob.glob(os.path.join(SRC, 'posts', '*.md'))), key=lambda p: p['date'], reverse=True)
posts = [p for p in all_posts if not p['translation_of']]          # listed on the home page
by_slug = {p['slug']: p for p in all_posts}
translations = {p['translation_of']: p for p in all_posts if p['translation_of']}

FLAG_FR = '<svg viewBox="0 0 3 2" width="21" height="14" aria-hidden="true"><rect width="1" height="2" fill="#0055a4"/><rect x="1" width="1" height="2" fill="#fff"/><rect x="2" width="1" height="2" fill="#ef4135"/></svg>'
FLAG_EN = '<svg viewBox="0 0 60 40" width="21" height="14" aria-hidden="true"><rect width="60" height="40" fill="#012169"/><path d="M0 0L60 40M60 0L0 40" stroke="#fff" stroke-width="8"/><path d="M0 0L60 40M60 0L0 40" stroke="#c8102e" stroke-width="3"/><path d="M30 0V40M0 20H60" stroke="#fff" stroke-width="12"/><path d="M30 0V40M0 20H60" stroke="#c8102e" stroke-width="7"/></svg>'

def lang_switch(p):
    # link from an article to its other-language version, shown as a flag
    other = translations.get(p['slug']) or (by_slug.get(p['translation_of']) if p['translation_of'] else None)
    if not other: return ''
    if other['lang'] == 'fr':
        return f'<a class="lang" href="{other["slug"]}.html" hreflang="fr" lang="fr" title="Lire en français">{FLAG_FR} Lire en français</a>'
    return f'<a class="lang" href="{other["slug"]}.html" hreflang="en" lang="en" title="Read in English">{FLAG_EN} Read in English</a>'

MOIS = ['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre']
def fmt_date(d, lang='en'):
    dt = datetime.date.fromisoformat(d)
    if lang == 'fr': return f"{dt.day} {MOIS[dt.month-1]} {dt.year}"
    return dt.strftime('%B %-d, %Y')

# ---------- home ----------
def pub_li(p):
    url = p.get('url') or (f"https://doi.org/{p['doi']}" if p.get('doi') else '')
    cls = ' class="patent"' if p['type'] == 'Patent' else (' class="lead"' if p['lead'] else '')
    tag = f'<span class="tag">{p["type"]}</span>' if p['type'] not in ('Article', 'Patent') else ''
    if p.get('status'): tag += f'<span class="tag st">{p["status"]}</span>'
    t = f'<a href="{url}" target="_blank" rel="noopener">{html.escape(p["title"])}</a>' if url else html.escape(p["title"])
    venue = f' · <i>{html.escape(p["venue"])}</i>' if p.get('venue') and not p.get('status') else ''
    return f'<li{cls}><div class="yr">{p["year"]}</div><div><p class="t">{t}{tag}</p><div class="m">{html.escape(p["authors"])}{venue}</div></div></li>'

def post_card(p, rel=''):
    return f'''<li class="rv"><a class="card" href="{rel}posts/{p['slug']}.html">
<div class="img"><img src="{p['image']}" alt="{html.escape(p['alt'])}" loading="lazy"></div>
<div class="d">{fmt_date(p['date'])}</div>
<h3>{html.escape(p['title'])}</h3>
<p>{html.escape(p['excerpt'][:150])}</p></a></li>'''

rel_cv = 'cv.pdf'
home_body = f'''{nav('', 'index.html')}
<section class="hero"><canvas id="vasc" aria-hidden="true"></canvas><div class="wrap">
<p class="eyebrow"><b>Postdoctoral fellow</b> · Penninger lab · University of British Columbia</p>
<h1>Clément <em>Quintard</em></h1>
<p class="lede">I build microfluidic systems where stem cell-derived organoids are fed by their own blood vessels and visited by their own immune cells. The aim is human tissue models that are good enough to replace animals in drug development, and complex enough to be worth the trouble.</p>
<p class="lede">Outside the lab I am curious about most things. The <a href="#blog">blog</a> is where that goes: science, nature, sport, and whatever I happen to be thinking of.</p>
<div class="links"><a href="#publications">Publications</a><a href="{rel_cv}" target="_blank" rel="noopener">CV (PDF)</a><a href="https://scholar.google.com/citations?user=WsRDHysAAAAJ" target="_blank" rel="noopener">Google Scholar</a><a href="https://github.com/ClementQuintard" target="_blank" rel="noopener"><svg class="gh" viewBox="0 0 16 16" width="15" height="15" aria-hidden="true"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg> GitHub</a><a href="https://x.com/c_quintard" target="_blank" rel="noopener">X</a></div>
</div></section>

<section class="block" id="research"><div class="wrap">
<div class="idx"><span class="dot" aria-hidden="true"></span>Research</div>
<div class="body rv">
<h2>Vascularized and immunized <em>organoids-on-chip</em></h2>
<div class="prose">
<p>I am a postdoctoral fellow in the lab of <a href="https://en.wikipedia.org/wiki/Josef_Penninger" target="_blank" rel="noopener">Josef Penninger</a> at the University of British Columbia. My research sits at the interface of stem cell biology, organoid engineering and microfluidics, with a focus on developing functionally vascularized and immunized organoids-on-chip.</p>
<p>Before Vancouver, I did my PhD at CEA Grenoble, engineering vascularized organoids-on-chip with new microfluidic strategies. That work led to two first-author papers and a patent, and to a lasting interest in standardization, because organs-on-chip will only be adopted by industry if they become standardized and easy to use. I trained in physics at École Normale Supérieure Paris-Saclay, then in microfluidics at Institut Pierre-Gilles de Gennes, with research stays at Harvard and in an industrial collaboration with Sanofi.</p>
<p>AI tools have become part of my daily research, from analysis pipelines to experimental design. Bringing human microphysiological systems and AI together is, to me, one of the most promising directions for biology and drug discovery in the coming years.</p>
</div>
<ul class="focus">
<li><b>Microfluidic platforms</b><span>Improving throughput and scalability of organoid-on-chip systems.</span></li>
<li><b>Fully stem cell-derived models</b><span>Vessels, stroma and parenchyma from the same iPSC line, for physiological relevance.</span></li>
<li><b>Immune components</b><span>Immune cell trafficking and interactions inside microphysiological systems.</span></li>
<li><b>New vascularization strategies</b><span>Beyond blood vessels, for heart, pancreas, lung, brain and cancer models.</span></li>
</ul>
<a class="more" href="research.html">Full background and CV →</a>
</div></div></section>

<section class="block" id="publications"><div class="wrap">
<div class="idx"><span class="dot" aria-hidden="true"></span>Publications</div>
<div class="body rv">
<h2>Selected <em>papers</em> and patents</h2>
<ul class="pubs">
{''.join(pub_li(p) for p in pubs if p['type'] != 'Patent')}
</ul>
<h3 class="sub">Patents</h3>
<ul class="pubs">
{''.join(pub_li(p) for p in pubs if p['type'] == 'Patent')}
</ul>
<a class="more" href="https://scholar.google.com/citations?user=WsRDHysAAAAJ" target="_blank" rel="noopener">All publications on Google Scholar →</a>
</div></div></section>

<section class="block" id="blog"><div class="wrap">
<div class="idx"><span class="dot" aria-hidden="true"></span>Blog</div>
<div class="body">
<h2 class="rv">Notes on science and <em>everything else</em></h2>
<ul class="posts">
{''.join(post_card(p) for p in posts)}
</ul>
</div></div></section>

<section class="block" id="contact"><div class="wrap">
<div class="idx"><span class="dot" aria-hidden="true"></span>Contact</div>
<div class="body rv">
<h2>Get in <em>touch</em></h2>
<div class="contact">
<div><div class="k">Email</div><div class="v"><a href="mailto:clement.quintard@gmail.com">clement.quintard@gmail.com</a></div></div>
<div><div class="k">Google Scholar</div><div class="v"><a href="https://scholar.google.com/citations?user=WsRDHysAAAAJ" target="_blank" rel="noopener">Clément Quintard</a></div></div>
<div><div class="k">GitHub</div><div class="v"><a href="https://github.com/ClementQuintard" target="_blank" rel="noopener"><svg class="gh" viewBox="0 0 16 16" width="15" height="15" aria-hidden="true"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg> ClementQuintard</a></div></div>
<div><div class="k">X</div><div class="v"><a href="https://x.com/c_quintard" target="_blank" rel="noopener">@c_quintard</a></div></div>
<div><div class="k">Lab</div><div class="v"><a href="https://lsi.ubc.ca/people/josef-penninger/" target="_blank" rel="noopener">Penninger lab, UBC</a></div></div>
</div>
</div></div></section>
{FOOT}'''

# ---------- research page ----------
research_md = open(os.path.join(SRC, 'page-research.md')).read()
research_md = research_md.split('# Research', 1)[1]
research_html = markdown(research_md)
research_html = re.sub(r'<a href="(http[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', research_html)
research_body = f'''{nav('', 'index.html')}
<main class="article"><div class="wrap">
<a class="back" href="index.html#research">← Back</a>
<div class="d">Background</div>
<h1>From physics to <em>organoids-on-chip</em></h1>
<p class="d"><a href="{rel_cv}" target="_blank" rel="noopener">Download CV (PDF) →</a></p>
<div class="prose">{research_html}</div>
</div></main>{FOOT}'''

# ---------- write ----------
os.makedirs(os.path.join(OUT, 'posts'), exist_ok=True)
shutil.copy(os.path.join(SRC, 'style.css'), OUT)
shutil.copy(os.path.join(SRC, 'site.js'), OUT)
shutil.copytree(os.path.join(SRC, 'img'), os.path.join(OUT, 'img'), dirs_exist_ok=True)
shutil.copy(os.path.join(SRC, 'cv.pdf'), OUT)
if os.path.isdir(os.path.join(SRC, 'video')): shutil.copytree(os.path.join(SRC, 'video'), os.path.join(OUT, 'video'), dirs_exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w').write(page(home_body, 'Clément Quintard', '', 'Clément Quintard, postdoctoral fellow at UBC working on vascularized and immunized organoids-on-chip, and a blog on science and everything else.', skeleton=not ARTIFACT))
open(os.path.join(OUT, 'research.html'), 'w').write(page(research_body, 'Background · Clément Quintard', ''))
for p in all_posts:
    back = '← Tous les billets' if p['lang'] == 'fr' else '← All posts'
    body = f'''{nav('../', '../index.html')}
<main class="article" lang="{p['lang']}"><div class="wrap">
<div class="topbar"><a class="back" href="../index.html#blog">{back}</a>{lang_switch(p)}</div>
<div class="d">{fmt_date(p['date'], p['lang'])}</div>
<h1>{html.escape(p['title'])}</h1>
{f'<img class="hero-img" src="{p["image"]}" alt="{html.escape(p["alt"])}">' if p['image'] else ''}
<div class="prose">{p['html']}</div>
</div></main>{FOOT}'''
    body = body.replace('src="img/', 'src="../img/').replace('href="img/', 'href="../img/').replace('src="video/', 'src="../video/')
    out = page(body, p['title'] + ' · Clément Quintard', '../', p['excerpt'][:160])
    if p['lang'] != 'en': out = out.replace('<html lang="en">', f'<html lang="{p["lang"]}">', 1)
    open(os.path.join(OUT, 'posts', p['slug'] + '.html'), 'w').write(out)
nf = f'''{nav('', 'index.html')}
<main class="article"><div class="wrap"><div class="d">404</div><h1>Nothing <em>here</em></h1><p class="prose">That page does not exist. <a href="index.html">Back to the home page</a>.</p></div></main>{FOOT}'''
open(os.path.join(OUT, '404.html'), 'w').write(page(nf, 'Not found · Clément Quintard', ''))
print('built', len(all_posts), 'pages,', len(posts), 'listed ->', OUT)
