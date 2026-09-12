---
name: greet
description: Greet the user by name in their preferred language. Use when the user asks for a greeting or a one-line introduction message.
---

# Greet

## Overview

Produces a single-line greeting addressed to the user by name, in the language they prefer. Defaults to English when no language is given.

## Workflow

1. If the name or language is missing, ask for it in one message.
2. Emit exactly one line: the greeting, the name, and nothing else.
