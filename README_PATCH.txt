SekigaharaWiki portrait 2x and experiment playlist — 4-file PATCH
==================================================================

Apply this patch only if the previous V2.8.0 cumulative Wiki update
(including portraits and wiki_commander_updates.py) has ALREADY been uploaded.
Extract at the repository root, preserving the docs/ paths.

Modified files:
- docs/assets/stylesheets/commander-portraits.css
- docs/assets/javascripts/commander-portraits.js
- docs/experiments/index.md
- docs/en/experiments/index.md

Portraits are displayed at up to 384 CSS px wide on spacious desktop
layouts and scale down without cropping on narrow screens. The experiment
playlist appears just before '実験一覧' / 'Experiment List'.
