# Local CI

Run `bash .ci/local.sh`; `--check` runs only guard/syntax checks. Logs stay in `.ci/logs/`; nonzero status reports failures or incomplete coverage.

This is a GitHub training exercise. The four original Markdown predicates (header, image, fenced code, and unchecked task item) are preserved in `check-lesson.py` and tested with positive/negative cases. `local.sh` runs those checker tests, then checks the current course step against `index.md`. You can supply `--step 1|2|3|4 --file /path/to/your/local/index.md` without changing the course metadata.

The current default branch records step 4 but has no `index.md`; the local command correctly returns incomplete status (2) until a learner supplies that file. This is a pre-existing incomplete course state, not a passing application test suite. Course state updates, branch creation, issue/PR updates and merges are manual; the archived bots are never invoked locally.

Original workflow files are recoverable under `archived-workflows/`. Existing remote logs/artifacts and retention settings are unchanged. Do not restore archived YAML into `.github/workflows`.
