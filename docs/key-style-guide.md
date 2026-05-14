# Key Style Guide

## General keys
Use stable keys that describe meaning, not exact English text. Use `_` as word separator.

## Key Names
Column header values are written as plain english in the LEAPP tools. During processing, the header gets sanitized to be safe for SQL. Essentially, lower cased, symbols removed, and spaces replaced with `_` character. The key names should reflect the SQL sanitized version of the header for proper matchup.

Examples:
- `Accessed Timestamp` becomes `accessed_timestamp`
- `Speed (mi/hr)` becaomes `speed_mi_hr`

## Flat keys
Keys are flat strings. Dots are part of the key and used to group similar tags.

## Plural keys
These keys are responsive to an input value, so output can be `row` or `rows` based on provided value. Some languages use only `_one` and `_other` suffixes, but some languages also use a `_many` suffix. If the `_many` suffix is included in the tag list but doesn't make sense for the language, it can be made as a duplicate of the `_other` tag.

## Do not create new keys or rename keys
Tags are created in the tool repo. They are then merged into this repo as the shared resource. If there is reason to rename or create a new tag, open an issue to discuss.

## Empty values
Empty string means untranslated, and will default to showing the english version of the tag value.