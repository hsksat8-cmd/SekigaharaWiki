# -*- coding: utf-8 -*-
"""MkDocs build-time commander data normalization (source: supplied roster)."""
from __future__ import annotations
import re

ROSTER = {'tokugawa-ieyasu': {'troops': 30000, 'expanded': False}, 'fukushima-masanori': {'troops': 6000, 'expanded': False}, 'kuroda-nagamasa': {'troops': 5400, 'expanded': False}, 'hosokawa-tadaoki': {'troops': 5000, 'expanded': False}, 'ii-naomasa': {'troops': 3600, 'expanded': False}, 'honda-tadakatsu': {'troops': 500, 'expanded': False}, 'todo-takatora': {'troops': 2500, 'expanded': False}, 'kyogoku-takatomo': {'troops': 3000, 'expanded': False}, 'asano-yoshinaga': {'troops': 6000, 'expanded': False}, 'ikeda-terumasa': {'troops': 4500, 'expanded': False}, 'yamauchi-kazutoyo': {'troops': 2400, 'expanded': False}, 'date-masamune': {'troops': 14100, 'expanded': True}, 'maeda-toshinaga': {'troops': 15100, 'expanded': True}, 'kato-kiyomasa': {'troops': 10000, 'expanded': True}, 'ishida-mitsunari': {'troops': 6000, 'expanded': False}, 'ukita-hideie': {'troops': 17000, 'expanded': False}, 'konishi-yukinaga': {'troops': 6000, 'expanded': False}, 'otani-yoshitsugu': {'troops': 600, 'expanded': False}, 'toda-shigemasa': {'troops': 1500, 'expanded': False}, 'hiratsuka-tamehiro': {'troops': 1500, 'expanded': False}, 'shimazu-yoshihiro': {'troops': 1500, 'expanded': False}, 'shima-sakon': {'troops': 1000, 'expanded': False}, 'mori-hidemoto': {'troops': 15000, 'expanded': False}, 'kikkawa-hiroie': {'troops': 3000, 'expanded': False}, 'kobayakawa-hideaki': {'troops': 15000, 'expanded': False}, 'wakizaka-yasuharu': {'troops': 1000, 'expanded': False}, 'kutsuki-mototsuna': {'troops': 600, 'expanded': False}, 'ogawa-suketada': {'troops': 2100, 'expanded': False}, 'akaza-naoyasu': {'troops': 600, 'expanded': False}, 'ankokuji-ekei': {'troops': 1800, 'expanded': False}, 'chosokabe-morichika': {'troops': 6600, 'expanded': False}, 'uesugi-kagekatsu': {'troops': 16000, 'expanded': True}, 'satake-yoshinobu': {'troops': 11300, 'expanded': True}, 'tachibana-muneshige': {'troops': 4500, 'expanded': True}, 'nabeshima-naoshige': {'troops': 10200, 'expanded': True}, 'niwa-nagashige': {'troops': 3700, 'expanded': True}}

def on_page_markdown(markdown, page, config, files):
    path = page.file.src_uri.replace('\\', '/')
    en = path.startswith('en/')
    # Commander profile content is normalized *before* Markdown rendering,
    # preserving each author's biographies and detailed notes.
    match = re.fullmatch(r'(?:en/)?commanders/(?:eastern|western)/([a-z0-9-]+)\.md', path)
    if match:
        slug = match.group(1)
        # Rename the existing stat without changing the underlying score.
        markdown = markdown.replace('統率', '規律').replace('Leadership', 'Discipline')
        if slug in ROSTER:
            info = ROSTER[slug]
            value = f"{info['troops']:,}"
            key = 'Troops' if en else '兵数'
            regex = r'(<tr><td>' + re.escape(key) + r'</td><td>)[^<]*(</td></tr>)'
            markdown = re.sub(regex, lambda m:m.group(1)+value+m.group(2),markdown,count=1)
            cat_key = 'Category' if en else '区分'
            cat_val = ('Additional commander for the fictional expanded map' if info['expanded'] else 'Core Sekigahara commander') if en else ('架空拡張マップ追加武将' if info['expanded'] else '関ヶ原基本武将')
            cat_regex = r'(<tr><td>' + re.escape(cat_key) + r'</td><td>)[^<]*(</td></tr>)'
            markdown = re.sub(cat_regex, lambda m:m.group(1)+cat_val+m.group(2),markdown,count=1)
    elif re.fullmatch(r'(?:en/)?commanders/user/user-commander-[123]\.md', path):
        markdown = markdown.replace('統率', '規律').replace('Leadership', 'Discipline')
    return markdown
