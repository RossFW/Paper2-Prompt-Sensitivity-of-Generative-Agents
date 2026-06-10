# Paper 2: Prompt Sensitivity of Generative Agents

Dissertation chapter / Paper 2 of the three-paper dissertation *Epidemic
Modeling with Generative Agents* by Ross Williams (Virginia Tech).

How sensitive are generative-agent epidemic simulations to the *wording* of the
prompt? This paper varies persona phrasing, awareness framing, and related
prompt features in the GABM epidemic setting and measures how agent behavior
shifts — establishing that prompt design is itself a modeling choice.

> **Status:** Virginia Tech preliminary-examination paper (2023); not externally
> published. The simulation engine is the GABM epidemic model
> ([bear96/GABM-Epidemic](https://github.com/bear96/GABM-Epidemic),
> arXiv:2307.04986) run with modified prompts; see Paper 1
> ([Paper1-Epidemic-Generative-Agent-Based-Model](https://github.com/RossFW/Paper1-Epidemic-Generative-Agent-Based-Model)).

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

## Notes

- The `Regression Framework (Feb 2026)/` is the OLS comparison framework
  (`Mobility ~ NewCases + NewCases² + Treatment + Treatment×NewCases`) later
  reused as `prepare_comparison.py` in Paper 3.
- Simulation code is not duplicated here — see Paper 1 / bear96 above.
