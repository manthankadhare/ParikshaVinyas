KRUSHI / SPENDWISE — OVERLEAF PROJECT

What is included
- main.tex: Overleaf entry point. It uses the same InternshipReport.cls class file from your earlier Data Analytics Overleaf project as the formatting/template reference, and includes the supplied KRUSHI_STQA_REPORT_Original.pdf page-for-page. This preserves all 66 pages, screenshots, tables, and original visual layout.
- InternshipReport.cls: copied from your earlier Overleaf project.
- KRUSHI_STQA_REPORT_Original.pdf: the supplied source PDF.
- editable_text_draft.tex: companion editable text extraction in original page order. This is a draft, not a fully reconstructed semantic report; extracted line breaks, tables, and image placements may require manual editing.

How to use
1. Upload this ZIP to a new Overleaf project (New Project > Upload Project).
2. Set main.tex as the Main document if Overleaf does not select it automatically.
3. Compile with pdfLaTeX.

Important distinction
The main.tex route reproduces the supplied PDF exactly by embedding it. PDF text itself is not editable in this route. For editable report content, open editable_text_draft.tex and manually refine the extracted content, tables, and figures. The supplied reference class is retained for consistent future styling.
