#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rewrite Japanese commander biographies in original Markdown, without browser JS."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((Path(__file__).parent/'commander_biographies.json').read_text(encoding='utf-8'))
NOTE='注：性格・心情・動機の記述には、史実や伝承を踏まえたゲーム制作上の解釈を含みます。本人の実際の発言や内面を断定するものではありません。'
TARGET={'簡単な経歴','人となり','人物とその背景','史実とゲーム表現','人となりと歴史的背景'}
HEADING=re.compile(r'(?m)^## ([^\r\n]+)[ \t]*$')
def rewrite(source,profile):
    matches=list(HEADING.finditer(source))
    positions=[i for i,m in enumerate(matches) if m.group(1).strip() in TARGET]
    if not positions: raise ValueError('紹介欄がありません')
    # A per-section replacement preserving all unrelated content, even when
    # other sections occur between the original biography sections.
    blocks=[(matches[i].start(), matches[i+1].start() if i+1<len(matches) else len(source)) for i in positions]
    output=[];pos=0
    replacement=(
      '## 簡単な経歴\n\n'+profile['biography'].strip()+'\n\n'
      '## 人となり\n\n'+profile['character'].strip()+'\n\n'
      '## 人物とその背景\n\n'+profile['background'].strip()+'\n\n'
      '!!! note "人物解釈について"\n    '+NOTE+'\n\n'
    )
    for i,(left,right) in enumerate(blocks):
        output.append(source[pos:left])
        if i==0: output.append(replacement)
        pos=right
    output.append(source[pos:])
    return ''.join(output).rstrip()+'\n'
def main():
    pending=[]; seen=set()
    for person in DATA:
        slug=person['slug']
        paths=[ROOT/'docs'/'commanders'/side/(slug+'.md') for side in ('eastern','western')]
        existing=[p for p in paths if p.is_file()]
        if len(existing)!=1: raise ValueError('武将ファイルの照合に失敗: '+person['name'])
        path=existing[0]
        if path in seen: raise ValueError('武将ファイルの重複: '+str(path))
        seen.add(path)
        original=path.read_text(encoding='utf-8-sig')
        if not re.search(r'^# '+re.escape(person['name'])+r'\s*$',original,re.M):
            raise ValueError('武将名の不一致: '+str(path))
        updated=rewrite(original,person)
        # safety/idempotence validations
        assert rewrite(updated,person)==updated
        for heading in ('簡単な経歴','人となり','人物とその背景'):
            assert updated.count('## '+heading+'\n')==1
        assert '## 史実とゲーム表現\n' not in updated
        if updated!=original: pending.append((path,updated))
    if len(DATA)!=36: raise ValueError('資料は36人分必要です')
    # Avoid partial changes if any file cannot be processed.
    for path,body in pending: path.write_text(body,encoding='utf-8',newline='\n')
    print('武将36人を検証しました。書き換えファイル数:',len(pending))
if __name__=='__main__':main()
