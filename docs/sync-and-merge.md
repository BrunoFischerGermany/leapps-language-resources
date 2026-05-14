# Sync and Merge Process

## Core rule
The shared repo is the canonical source for translations.

## Adding keys from tools
Tools may scan their own source and contribute newly discovered keys.

## Merge behavior
- Existing shared translations are preserved
- New keys are added from source tools
- Keys are not deleted automatically

## Conflict behavior
- Existing shared value wins by default
- Human review resolves wording conflicts
- Cleanup happens through review, not automatic deletion

## Orphan keys
We will build a manual review process to evaluate potentially unused keys. This needs to be done carefully since multiple tools will share these files.