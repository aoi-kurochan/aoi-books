#!/usr/bin/env python3
"""books.json から本番用 index.html を生成する。"""
import html
import json
import re
import sys
from collections import Counter

with open("books.json", encoding="utf-8") as f:
    data = json.load(f)

books = [book for book in data["books"] if book.get("visible")]
esc = lambda value: html.escape(str(value), quote=True)

GOALS = [
    ("publish", "本を出版したい", "書きたい気持ちを、1冊の形にする", "01"),
    ("learn", "AIを学びたい", "ChatGPTやClaudeの基本をやさしく知る", "02"),
    ("work", "AIを仕事や副業に活かしたい", "AIに仕事を任せ、できることを増やす", "03"),
    ("create", "画像や動画を作りたい", "画像・漫画・動画・ゲームをAIと作る", "04"),
    ("share", "SNS・noteで発信したい", "書くことや発信を小さく始める", "05"),
    ("skill", "得意を副業にしたい", "占い・英語などの経験を仕事につなげる", "06"),
    ("life", "働き方や収入を変えたい", "会社だけに頼らない選択肢を持つ", "07"),
]

GOAL_BY_ORDER = {
    **{n: "publish" for n in [1, 2, 3, 29]},
    **{n: "learn" for n in [4, 5, 7, 10, 11, 12, 13]},
    **{n: "work" for n in [6, 8, 9, 30, 34, 36]},
    **{n: "create" for n in [14, 15, 16, 17, 32, 33, 35]},
    **{n: "share" for n in [18, 19, 31]},
    **{n: "skill" for n in [20, 21, 22, 23, 24]},
    **{n: "life" for n in [25, 26, 27, 28]},
}

AUDIENCE = {
    "publish": "自分の本を出したい人",
    "learn": "AIの基本から知りたい人",
    "work": "AIを仕事や副業で使いたい人",
    "create": "AIでものづくりをしたい人",
    "share": "SNSやnoteで発信したい人",
    "skill": "好きや得意を副業にしたい人",
    "life": "働き方と収入を見直したい人",
}

def series_for(book):
    title = book["title"].lower()
    result = []
    if "chatgpt" in title:
        result.append("chatgpt")
    if "claude" in title:
        result.append("claude")
    if "kindle" in title:
        result.append("kindle")
    if "kimi" in title:
        result.append("kimi")
    return result

def card(book):
    goal = GOAL_BY_ORDER[book["order"]]
    labels = " ".join(series_for(book)) or "other"
    return f'''<a class="book-card" data-title="{esc(book['title'])}" data-series="{labels}" href="{esc(book['url'])}" target="_blank" rel="noopener">
      <div class="cover-wrap"><img src="{esc(book['cover'])}" alt="{esc(book['title'])} の表紙" loading="lazy"></div>
      <div class="book-copy">
        <p class="book-kicker">こんな人へ</p>
        <p class="audience">{esc(AUDIENCE[goal])}</p>
        <h3>{esc(book['title'])}</h3>
        <p class="outcome"><span>読んだあと</span>{esc(book['blurb'])}</p>
        <span class="amazon">Amazonで見る <b>→</b></span>
      </div>
    </a>'''

if set(GOAL_BY_ORDER) != {b["order"] for b in books}:
    raise SystemExit("分類されていない本、または余分な分類があります")

series_counts = Counter(s for b in books for s in series_for(b))
hero_books = [next(b for b in books if b["order"] == n) for n in [33, 34, 25]]

parts = [f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>あおいの本棚｜次に読む1冊が見つかる</title>
<meta name="description" content="黒川葵の本を、やりたいことや使いたいAIから選べるブックガイド。">
<meta property="og:title" content="あおいの本棚｜次に読む1冊が見つかる">
<meta property="og:description" content="黒川葵の本を、やりたいことや使いたいAIから選べるブックガイド。">
<meta property="og:image" content="https://aoi-kurochan.github.io/aoi-books/ogp.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://aoi-kurochan.github.io/aoi-books/ogp.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&family=Noto+Serif+JP:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css"></head><body>
<header class="hero"><div class="paper-noise"></div><div class="wrap hero-grid">
  <div class="hero-copy">
    <p class="brand"><span>✦</span> あおいの本棚</p>
    <p class="eyebrow">BOOK GUIDE BY AOI KUROKAWA</p>
    <h1>次に読む1冊を<br><em>選べます。</em></h1>
    <p class="lead">やりたいことや、使いたいAIから選んでください。<br>今のあなたに合う本をご案内します。</p>
    <a class="hero-cta" href="#guide">やりたいことから選ぶ <span>↓</span></a>
  </div>
  <div class="hero-books" aria-label="本棚の一部">
    <span class="halo"></span>
    <img class="cover cover-a" src="{esc(hero_books[0]['cover'])}" alt="">
    <img class="cover cover-b" src="{esc(hero_books[1]['cover'])}" alt="">
    <img class="cover cover-c" src="{esc(hero_books[2]['cover'])}" alt="">
  </div>
</div></header>

<main id="guide">
<section class="guide wrap">
  <div class="section-intro">
    <p class="section-label">FIND YOUR NEXT BOOK</p>
    <h2>何を始めたいですか？</h2>
    <p>テーマ名ではなく、今の目的に近いものを選んでください。</p>
  </div>
  <nav class="goal-grid" aria-label="やりたいことから選ぶ">''']

for key, title, subtitle, number in GOALS:
    parts.append(f'''<a class="goal-card goal-{key}" href="#{key}">
      <span class="goal-number">{number}</span>
      <strong>{esc(title)}</strong><small>{esc(subtitle)}</small>
      <span class="goal-meta"><b>→</b></span>
    </a>''')

parts.append('''</nav>
  <div class="series-box">
    <div><p class="series-label">使いたいAIやシリーズが決まっている方へ</p><p class="series-note">同じ本を重複表示せず、該当する本だけに絞れます。</p></div>
    <div class="series-buttons" role="group" aria-label="シリーズで絞り込む">
      <button class="filter active" data-filter="all">すべて</button>
      <button class="filter" data-filter="chatgpt">ChatGPT</button>
      <button class="filter" data-filter="claude">Claude</button>
      <button class="filter" data-filter="kimi">Kimi</button>
      <button class="filter" data-filter="kindle">Kindle出版</button>
    </div>
  </div>
</section>''')

for key, title, subtitle, number in GOALS:
    goal_books = sorted((b for b in books if GOAL_BY_ORDER[b["order"]] == key), key=lambda b: b["order"])
    parts.append(f'''<section id="{key}" class="shelf shelf-{key}" data-goal="{key}"><div class="wrap">
      <div class="shelf-head"><div><p class="shelf-number">SHELF {number}</p><h2>{esc(title)}</h2><p>{esc(subtitle)}</p></div></div>
      <div class="book-grid">''')
    parts.extend(card(book) for book in goal_books)
    parts.append('</div></div></section>')

parts.append('''</main>
<footer><div class="wrap"><p class="footer-brand">あおいの本棚</p><p>あなたの「やってみたい」に、やさしい最初の1冊を。</p>
<nav aria-label="関連リンク"><a href="https://note.com/kurokawa_aoi" target="_blank" rel="noopener">note</a><a href="https://x.com/aoi_kurochan" target="_blank" rel="noopener">X</a><a href="https://aoi-kurochan.github.io/smart-fire-site/" target="_blank" rel="noopener">スマートFIRE読者ページ</a></nav>
</div></footer>
<script src="app.js"></script></body></html>''')

out = "\n".join(parts)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(out)

truth = {b["title"]: (b["cover"], b["url"]) for b in books}
cards = re.findall(r'class="book-card" data-title="([^"]+)"[^>]*href="([^"]+)"[^>]*>\s*<div class="cover-wrap"><img src="([^"]+)"', out)
errors = [title for title, url, cover in ((html.unescape(t), u, c) for t, u, c in cards) if truth.get(title) != (cover, url)]
if errors or len(cards) != len(books) or len(truth) != len(books):
    sys.exit(f"カード検証失敗: 件数={len(cards)} 不一致={errors}")

print(f"生成・検証OK: {len(books)}冊 / 目的別{len(GOALS)}棚 / ChatGPT {series_counts['chatgpt']}冊 / Claude {series_counts['claude']}冊 / Kimi {series_counts['kimi']}冊")
