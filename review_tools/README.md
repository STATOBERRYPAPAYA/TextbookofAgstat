# Verification evidence

The selected scripts and reports in this directory document numerical and structural checks of the textbook. Run R scripts from the repository root with R and the packages used by the book (including agricolae) installed. Python checks use the standard library unless stated otherwise.

`verify_numeric_core.R`, `verify_final_examples.R`, `verify_design_examples.R`, `verify_detailed_additions.R`, `verify_uniformity.R`, `check_ancova.R`, `check_calculations.R` and `check_appendices.R` cover the calculations named in their reports. `verify_duncan.R` compares the traditional monotone Duncan range convention for df at least 2, rather than asserting a facsimile transcription of every published table. `verify_design_layouts.py` checks treatment counts and Latin-square permutations; its introductory diagram construction is deterministic.

`check_source_integrity.py`, `audit_structure.py`, `audit_numeric_equalities.py`, `audit_table_arithmetic.py` and `audit_rendered_html.py` provide limited automated checks, not a proof that every statement is correct or that every browser layout is overflow-free. See `../DETAILED_CHAPTER_REVIEW.md` for the editorial reading, corrections and qualifications.

Downloaded source PDFs, local snapshots, repeated build directories and temporary editing scripts are intentionally excluded from Git. The Gomez source PDF needed by `verify_gomez_adjustment.py` is available at the reference URL recorded in `gomez_adjustment_verified.json`; its checksum is recorded there. No copyrighted reference PDF is distributed with the book.

The print PDF was not proofed in this review, at the author's request. ISBN and the previously flagged quotation attributions remain author items.

The external-review additions have a separate numeric script and CSV, including the new percentile/decile, combined-SD, reverse-regression and graphical exercises. Local editorial reports remain with the author rather than being distributed as part of the public book.
