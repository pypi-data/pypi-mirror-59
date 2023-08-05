# Diff cov lint

Linting and coverage reports for git diff only.

## Usage: 

```diff-cov-lint master new_branch --cov_report=coverage.xml --lint_report=pylint_output.txt```

Example output (the command above was run in `tests/repo` folder):
```
======================== DIFF COVERAGE ========================
FILE                                    COVERED STMTS   PERCENT
src/add.py                                    5     8     62.5%
src/modify.py                                 1     2     50.0%
===============================================================
TOTAL DIFF COV                                6    10     60.0%

========================== DIFF LINT ==========================
src/add.py:10:0 E0602: Undefined variable 'this_line_makes_no_sense' (undefined-variable)
```

Arguments:  

POSITIONAL ARGUMENTS  
    `TARGET_REF`
        Target branch in repo  
    `SOURCE_REF`
        Source branch in repo  

FLAGS  
    `--cov_report=COV_REPORT`  
        Path to coverage report in Cobertura (pytest-cov) format, If not stated, coverage report will not be produced.  
    `--lint_report=LINT_REPORT`  
        Path to pylint report. If not stated, linting report will not be produced.  
    `--repo_path=REPO_PATH`  
        Path to repo folder, defaults to "."