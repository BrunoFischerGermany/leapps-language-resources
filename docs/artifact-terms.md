# Artifact Terms

## What artifact strings are
**Artifact** names, **module** names, and **column headers** extracted from LEAPP outputs. Note that some module or artifact names may not need to be translated. App names should only get translated if it would be appropriate to the local language. Empty tag values will default to English.

- `Microsoft Teams` probably doesn't get translated
- `Teams Messages` might get partially translated
- `Call History` could probably be fully translated

## Why column headers might be different
Column headers have come from many modules written over time by different contributors. There has been no requirement or push for consistency before now. Going forward we need to bring some normalization into the terms used to reduce translation efforts.

## Normalization goals
Where it makes sense, we should consolidate similar meaning column headers into a single value.
An example:
- time stamp → Timestamp
- Timestamp → Timestamp
- Date → Timestamp

## Translation guidance
- Preserve forensic meaning
    - Something like `Accessed Time` should not be changed to simply `Timestamp`
- Prefer consistent terminology
    - We can build a terminology guide
- Do not over-localize technical terms
- Ask when context is unclear

## Header extraction process
A script scans LEAPP artifact definitions to build each tool list for review.

## Manual review
Extracted terms may require consolidation before being added.