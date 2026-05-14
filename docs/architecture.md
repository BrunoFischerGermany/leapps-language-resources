# Architecture

## Repo role
This repo is the shared source of truth for language resources.

## Consumers
- LAVA
- LEAPP tools
- Future LEAPPs ecosystem projects

## File layout
/locales/{language}/{namespace}_{language}.json

## Namespaces
- translation: general UI strings
- dynamic: runtime/expandable labels
- artifacts: artifact names, module names, and column labels

## Source language
English is the source language.

## Templates
_template contains empty-value files for creating new languages.