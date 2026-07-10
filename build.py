#!/usr/bin/env python3
# build.py — books.json から index.html を生成する。実行: python3 build.py
import json, html, re, sys

D = json.load(open('books.json', encoding='utf-8'))
BOOKS = [b for b in D['books'] if b.get('visible')]
ENTRIES = D['entries']

SUB = {"Kindle出版":"出版で収入を作る","Claude活用":"話題のClaudeを使いこなす",
"AIツールの基本":"ChatGPT・NotebookLM・Obsidian","画像生成":"AIで絵・漫画・サムネ",
"note":"書く習慣から始める","占い・英語":"得意を副業にする","働き方・FIRE":"会社に頼らない人生",
"AI副業":"AIで新しい収入をつくる"}
TAG = {"Kindle出版":"出したい気持ちがあれば、もう半分は始まっています。",
"Claude活用":"話題のClaude、まずは肩の力を抜いて触ってみましょう。",
"AIツールの基本":"便利な道具を、ひとつずつ自分のものに。",
"画像生成":"絵が苦手でも大丈夫。言葉があれば描けます。",
"note":"うまく書けなくていい。まず一記事から。",
"占い・英語":"あなたの好きは、そのまま誰かの役に立ちます。",
"働き方・FIRE":"会社の外にも、道はちゃんとあります。",
"AI副業":"これまでの経験から、小さく始めていけます。"}
PICK_ORDER = ["最初の1冊","次に読む1冊","もっと深める1冊"]
TOP_LABEL = {0:"まず読む1冊",1:"次に読む1冊",2:"深める1冊"}
LABEL_CLS = {"最初の1冊":"lb-first","次に読む1冊":"lb-next","もっと深める1冊":"lb-deep",
"まず読む1冊":"lb-first","深める1冊":"lb-deep"}
AID = {e:f"e{i+1}" for i,e in enumerate(ENTRIES)}
esc = lambda s: html.escape(s, quote=True)

def pick_card(b, label):
    return f'''<a class="pick-card" data-title="{esc(b['title'])}" href="{esc(b['url'])}" target="_blank" rel="noopener">
<img src="{esc(b['cover'])}" alt="{esc(b['title'])} の表紙" loading="lazy">
<div class="pick-body"><span class="label {LABEL_CLS[label]}">{esc(label)}</span>
<h3>{esc(b['title'])}</h3><p>{esc(b['blurb'])}</p><span class="go">Amazonで見る →</span></div></a>'''

def grid_card(b):
    return f'''<a class="grid-card" data-title="{esc(b['title'])}" href="{esc(b['url'])}" target="_blank" rel="noopener">
<img src="{esc(b['cover'])}" alt="{esc(b['title'])} の表紙" loading="lazy">
<h4>{esc(b['title'])}</h4><p>{esc(b['blurb'])}</p></a>'''

parts = []
parts.append(f'''<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>あおいの本棚｜次に読む1冊が見つかる</title>
<meta name="description" content="AIアイデア工房の本を、テーマ別に選べる読者向けブックガイド。">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css"></head><body>
<header class="hero"><div class="wrap">
<p class="brand">あおいの本棚</p>
<h1>次に読む1冊が、<br>ここから見つかります。</h1>
<p class="lead">今のあなたに近いテーマを選んでください。<br class="sp">表紙をタップすると、そのままAmazonのページに飛べます。</p>
<nav class="entries" aria-label="テーマから選ぶ">''')
for e in ENTRIES:
    parts.append(f'<a class="entry-btn" href="#{AID[e]}"><strong>{esc(e)}</strong><span>{esc(SUB[e])}</span></a>')
parts.append('</nav></div></header>')

tops = sorted([b for b in BOOKS if b.get('top')], key=lambda x: x['order'])
parts.append('<section class="tone wrap-outer"><div class="wrap"><h2>今のあなたにおすすめ</h2><p class="tagline">はじめての方は、この3冊から。</p><div class="pick-row">')
for i,b in enumerate(tops):
    parts.append(pick_card(b, TOP_LABEL[i]))
parts.append('</div></div></section>')

for e in ENTRIES:
    eb = [b for b in BOOKS if b['entry']==e]
    picks = sorted([b for b in eb if b.get('pick')], key=lambda x: PICK_ORDER.index(x['pick']))
    parts.append(f'<section id="{AID[e]}" class="wrap-outer"><div class="wrap"><h2>{esc(e)}<small>{esc(SUB[e])}</small></h2><p class="tagline">{esc(TAG[e])}</p><div class="pick-row">')
    for b in picks:
        parts.append(pick_card(b, b['pick']))
    parts.append('</div></div></section>')

parts.append('<section class="tone wrap-outer"><div class="wrap"><h2>ぜんぶの本</h2><p class="tagline">もっと見たい方はこちらから。</p>')
for e in ENTRIES:
    eb = sorted([b for b in BOOKS if b['entry']==e], key=lambda x: x['order'])
    parts.append(f'<h3 class="genre-h">{esc(e)}</h3><div class="grid">')
    for b in eb:
        parts.append(grid_card(b))
    parts.append('</div>')
parts.append('</div></section>')

parts.append('''<footer><div class="wrap"><p class="f-brand">あおいの本棚</p>
<nav><a href="https://note.com/kurokawa_aoi" target="_blank" rel="noopener">note</a>
<a href="https://x.com/aoi_kurochan" target="_blank" rel="noopener">X</a>
<a href="https://aoi-kurochan.github.io/smart-fire-site/" target="_blank" rel="noopener">スマートFIRE読者ページ</a></nav>
</div></footer></body></html>''')

out = '\n'.join(parts)
open('index.html','w',encoding='utf-8').write(out)

# ---- 機械検証: 全カードの title / img / href が books.json と一致するか ----
truth = {b['title']:(b['cover'], b['url']) for b in BOOKS}
cards = re.findall(r'data-title="([^"]+)"[^>]*href="([^"]+)"[^>]*>\s*<img src="([^"]+)"', out)
errs = [t for t,u,c in ((html.unescape(t),u,c) for t,u,c in cards) if truth.get(t) != (c,u)]
n_grid = len(re.findall(r'grid-card', out)); n_pick = len(re.findall(r'pick-card', out))
print(f"カード検証: {len(cards)}枚中 不一致 {len(errs)} / 一覧{n_grid}冊 おすすめ枠{n_pick}枠")
if errs or n_grid != len(BOOKS): sys.exit("検証失敗: " + str(errs))
print("検証OK: 全カードで タイトル=表紙=リンク が books.json と一致")
