# LEAPPs Language Resources

## What this repo is
Shared language files used by the LEAPPs ecosystem, including LAVA and LEAPP tools.

## Who this is for
- Translators
- LEAPPs contributors
- Maintainers

## What is in this repo
- UI language strings
- Dynamic/runtime labels
- Artifact and column terminology

## Quick start
- Edit an existing language file
- Use _template to start a new language
- Open a pull request

## Important notes
- Do not remove keys unless discussed
- Empty values mean translation needed
- Artifact terms should preserve forensic meaning

## Documentation

- [Architecture](docs/architecture.md) — How this repo fits the LEAPPs ecosystem, file layout, namespaces, and templates.
- [Adding a language](docs/adding-a-language.md) — Copying templates, naming locale files, and submitting a pull request.
- [Artifact terms](docs/artifact-terms.md) — What artifact strings are, normalization goals, and translation guidance for forensic meaning.
- [Forensic terminology](docs/forensic-terminology.md) — Preferred terms, usage, deprecations, and rationale for naming consistency.
- [Key style guide](docs/key-style-guide.md) — Conventions for translation keys, plurals, and when tags change upstream.
- [Sync and merge](docs/sync-and-merge.md) — Canonical source rules, merging new keys from tools, conflicts, and orphan keys.