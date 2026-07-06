<img src="assets/readme-cover.svg" alt="Prompt Pack Lint cover" width="100%" />

# Prompt Pack Lint

Lint reusable prompt packs for metadata, variables, and risky instruction patterns.

![stack](https://img.shields.io/badge/stack-Python-be185d?style=flat-square) ![python](https://img.shields.io/badge/python-3.11-4b5563?style=flat-square) ![license](https://img.shields.io/badge/license-MIT-2563eb?style=flat-square) ![ci](https://img.shields.io/badge/ci-GitHub%20Actions-16a34a?style=flat-square)

| Question | Answer |
| --- | --- |
| What is it? | A focused Python utility for prompt operations. |
| How does it run? | `prompt-pack-lint` |
| Why keep it small? | Easier review, easier tests, fewer moving parts. |

## Command

```bash
python -m pip install -e ".[dev]"
prompt-pack-lint --help
python -m prompt_pack_lint --help
```

## Verify

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest
python -m prompt_pack_lint --help
```
