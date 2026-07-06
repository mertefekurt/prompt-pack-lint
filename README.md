# Prompt Pack Lint

> Lint reusable prompt packs for metadata, variables, and risky instruction patterns

## Snapshot

<img src="assets/readme-cover.svg" alt="Prompt Pack Lint cover" width="100%" />

| Part | Notes |
| --- | --- |
| Area | model quality |
| Entry | `prompt-pack-lint` |
| Main files | .github/, examples/, src/, tests/ |

## Use

```bash
git clone https://github.com/mertefekurt/prompt-pack-lint.git
cd prompt-pack-lint
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
prompt-pack-lint --help
```

## Notes

This project stays useful when the output is easy to read and the setup is easy to throw away after a quick check.
