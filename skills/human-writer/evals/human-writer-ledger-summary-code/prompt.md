---
tags: [skill-creator]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

This repo is a small personal finance ledger. The existing module ledger/io.py is provided as ledger_io.py; read it for the house style. Add a new module ledger/summary.py with two functions: totals_by_category(rows) returning a dict mapping category to a Decimal total, and monthly_totals(rows) returning a dict mapping (year, month) tuples to a Decimal total. rows are the dicts produced by read_rows (keys date, desc, amt, cat); dates are strings in one of the DATE_FMTS formats from io.py; skip rows whose date does not parse.

Input files: ledger_io.py
