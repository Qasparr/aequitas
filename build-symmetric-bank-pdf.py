#!/usr/bin/env python3
"""Build the Symmetric Credit Union proposal PDF from its Markdown twin.

Epigraph: "The rich ruleth over the poor, and the borrower is servant
to the lender." — Proverbs 22:7 (KJV)
Date: 2026-10-05 (Monday). 93.
Authorship: Johnathan 'Qasparr' (Kasparr) Monroe, Keeper of the Secret Treasure.
Method: Scientific Illuminism.

MECHANISM: read the Markdown source, walk it line by line, and pour it
into a styled letter-size PDF via fpdf2 — headings sized by depth,
blockquotes indented and italic, body text justified.
DOCTRINE: the doctrinal pipeline (build-doctrinal-pdfs.py) is built for
the law-library manuscripts with tables; this proposal has no tables, so
a small dedicated pour keeps the tool honest — one document, one script,
no dead code paths.
"""
import re
from fpdf import FPDF

import os
_HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(_HERE, "Aequitas-Proposal.md")
OUT = os.path.join(_HERE, "Aequitas-Proposal.pdf")
TITLE = "Aequitas — A Proposal for the Symmetric Credit Union"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"


class ProposalPDF(FPDF):
    # MECHANISM: footer on every page after the first — title + page number.
    # DOCTRINE: the first page is the title page; numbering it would be noise.
    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"{TITLE}  |  {self.page_no() - 1}", align="C")


def main():
    md = open(SRC, encoding="utf-8").read()
    pdf = ProposalPDF(format="Letter")
    pdf.set_margins(25.4, 25.4, 25.4)  # one-inch margins, the formal standard
    pdf.set_auto_page_break(True, margin=25.4)
    pdf.add_font("DejaVu", "", SERIF)
    pdf.add_font("DejaVu", "B", SERIF_B)
    # MECHANISM: no italic face ships on this host — blockquotes render in
    #   the regular face, distinguished by indentation alone.
    # DOCTRINE: say what the box can do, not what the brochure promised.
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)

    in_quote = False
    for line in md.split("\n"):
        s = line.rstrip()
        # MECHANISM: headings — '# ' is the title, '## ' a section.
        # DOCTRINE: size carries hierarchy so the eye never needs the '#'.
        if s.startswith("# "):
            pdf.set_font("DejaVu", "B", 20)
            pdf.multi_cell(0, 9, s[2:].strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
        elif s.startswith("## "):
            pdf.ln(3)
            pdf.set_font("DejaVu", "B", 14)
            pdf.multi_cell(0, 8, s[3:].strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        # MECHANISM: '>' lines are blockquotes — indented, italic.
        elif s.startswith(">"):
            if not in_quote:
                pdf.set_x(pdf.l_margin + 10)
                in_quote = True
            pdf.set_font("DejaVu", "", 10)
            text = s.lstrip("> ").strip()
            if text:
                pdf.multi_cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")
            else:
                in_quote = False
                pdf.ln(2)
        # MECHANISM: bold-only lines ('**...**') are sub-heads or rulings.
        elif re.fullmatch(r"\*\*.+\*\*", s):
            pdf.ln(2)
            pdf.set_font("DejaVu", "B", 11)
            pdf.multi_cell(0, 7, s.strip("*").strip(),
                           new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        elif not s.strip():
            if in_quote:
                in_quote = False
            pdf.ln(3)
        # MECHANISM: horizontal rules become breathing room, not a drawn line.
        # DOCTRINE: whitespace is the divider in a formal document.
        elif s.strip() == "---":
            pdf.ln(4)
        else:
            if in_quote:
                in_quote = False
            pdf.set_font("DejaVu", "", 10.5)
            # MECHANISM: strip inline bold markers for the pour — emphasis
            #   is carried by the sentence, not the typeface, in print.
            # DOCTRINE: honest simplification, stated here, not hidden.
            text = s.replace("**", "")
            pdf.multi_cell(0, 6, text, new_x="LMARGIN", new_y="NEXT",
                           align="J")

    pdf.output(OUT)
    print(f"wrote {OUT} ({pdf.page_no()} pages)")


if __name__ == "__main__":
    main()

# "Live, Love, and let Love, Live." — 93.
