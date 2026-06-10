# Paper 2: Prompt Sensitivity of Generative Agents

Dissertation chapter / Paper 2 of the three-paper dissertation *Epidemic
Modeling with Generative Agents* by Ross Williams (Virginia Tech).

How sensitive are generative-agent epidemic simulations to the *wording* of the
prompt? This paper varies persona phrasing, awareness framing, and related
prompt features in the GABM epidemic setting and measures how agent behavior
shifts — establishing that prompt design is itself a modeling choice.

> **Status:** Virginia Tech preliminary-examination paper (2023); not externally published.

## Code & data provenance

- **Simulation engine — not in this repo.** The epidemic simulations were run with
  the **GABM epidemic model** ([bear96/GABM-Epidemic](https://github.com/bear96/GABM-Epidemic),
  arXiv:2307.04986), modified with the prompt-sensitivity variations studied here.
  That engine is also mirrored in **Paper 1**
  ([Paper1-Epidemic-Generative-Agent-Based-Model](https://github.com/RossFW/Paper1-Epidemic-Generative-Agent-Based-Model)).
  The simulation code is **not duplicated** in this repo.
- **Original raw outputs — partial.** Some of the original 2023 simulation files
  live on other machines. What's included here is the processed analysis data
  (`Graphs and Data/`), the manuscript, and a self-contained, reproducible
  regression (below).

## Repository layout

```
Writing/                         Manuscript + presentations
  ├── Williams, Ross Preliminary Exam.pdf / .docx   Canonical prelim document
  ├── Paper #2 Figures.docx
  └── RFW_*_Presentation.pptx                        Prelim + SoDA talks
Graphs and Data/                 Analysis workbooks + simulation runs
  ├── Prompt Sensitivity Analysis.xlsx
  ├── Name Sensitivity Analysis.xlsx
  ├── Paper2_data_for_analysis.xlsx
  └── Random Runs/
Regression Framework (Feb 2026)/ Dummy-variable OLS analysis scripts
  ├── regression_analysis.py, data_prep.py, run_analysis.py
  └── paper2_regression_results.xlsx
Literature Review from Park et al's paper.xlsx
```

## Reproducing the regression

`Regression Framework (Feb 2026)/` is a self-contained, dummy-variable OLS
comparison (`Mobility ~ NewCases + NewCases² + Treatment + Treatment×NewCases`).
Its input (`Graphs and Data/Paper2_data_for_analysis.xlsx`) is in this repo, so
the result (`paper2_regression_results.xlsx`) regenerates end-to-end:

```bash
cd "Regression Framework (Feb 2026)"
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python run_analysis.py        # reads ../Graphs and Data/, writes paper2_regression_results.xlsx
```

It analyzes the *Aware* and *Learn* prompt comparisons. (This same OLS framework
later became `prepare_comparison.py` in Paper 3.)
