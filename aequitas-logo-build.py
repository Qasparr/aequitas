#!/usr/bin/env python3
"""Cut the Aequitas mark: the eye at the heart of the scales.

Epigraph: "The rich ruleth over the poor, and the borrower is servant
to the lender." — Proverbs 22:7 (KJV)
Date: 2026-10-05 (Monday). 93.
Authorship: Johnathan 'Qasparr' (Kasparr) Monroe, Keeper of the Secret Treasure.
Method: Scientific Illuminism.

MECHANISM: emit a one-color silhouette SVG — the balanced scales with the
all-seeing eye set at the fulcrum, the pivot the whole beam turns on.
DOCTRINE: the pupil is cut with fill-rule="evenodd", not painted white,
so the mark stays honest on any ground — transparency, not theater.
v3: the eye moved from above the beam to its middle, per the author's
ruling — awareness as the fulcrum of balance.
"""
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(_HERE, "aequitas-logo.svg")

# -- geometry ---------------------------------------------------------------
BEAM_Y = 200                     # top of the beam
EX, EY = 256, BEAM_Y + 9         # eye center: the fulcrum, mid-beam
ALMOND_HW, PUPIL_R = 70, 16
PAN_Y = BEAM_Y + 140

# MECHANISM: one path, two subpaths (almond + pupil circle), evenodd rule —
#   the pupil becomes a true hole, transparent on any background.
eye = (
    f"M{EX-ALMOND_HW},{EY} Q{EX},{EY-52} {EX+ALMOND_HW},{EY} "
    f"Q{EX},{EY+52} {EX-ALMOND_HW},{EY} Z "
    f"M{EX-PUPIL_R},{EY} a{PUPIL_R},{PUPIL_R} 0 1,0 {2*PUPIL_R},0 "
    f"a{PUPIL_R},{PUPIL_R} 0 1,0 {-2*PUPIL_R},0 Z"
)

scales = f"""
    <rect x="244" y="{BEAM_Y+46}" width="24" height="188"/>
    <rect x="176" y="{BEAM_Y+234}" width="160" height="22" rx="2"/>
    <rect x="156" y="{BEAM_Y+256}" width="200" height="18" rx="2"/>
    <path d="M64,{PAN_Y} Q112,{PAN_Y+62} 160,{PAN_Y} Z"/>
    <path d="M344,{PAN_Y} Q392,{PAN_Y+62} 440,{PAN_Y} Z"/>"""

hangers = []
for hx, px in ((112, (72, 112, 152)), (400, (352, 400, 448))):
    for ex in px:
        hangers.append(
            f'<line x1="{hx}" y1="{BEAM_Y+18}" x2="{ex}" y2="{PAN_Y}"/>')

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 500" role="img" aria-label="Aequitas — the eye at the heart of the scales">
  <!-- AEQUITAS mark, v3: the eye in the middle of the scales. One color, transparent ground. -->
  <g fill="#000000">
    <rect x="88" y="{BEAM_Y}" width="336" height="18" rx="2"/>
    <path d="{eye}" fill-rule="evenodd"/>
    {scales}
  </g>
  <g stroke="#000000" stroke-width="7" stroke-linecap="round">
    {''.join('    ' + h + chr(10) for h in hangers)}
  </g>
</svg>
"""

with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT}")

# "Live, Love, and let Love, Live." — 93.
