# Design: greeting-skill

## Problem

Users ask the assistant for short, personalised greetings in several languages. Without a dedicated skill the output format drifts between sessions.

## Solution

A `greet` skill under `skills/greet/` that asks for name and language when missing and emits a one-line greeting.

## Scope boundaries

The skill is over-triggering on any message that contains "hello". Add a "When not to use" paragraph to the skill body with this wording:

> Do not use this skill for conversational openers the user writes themselves, for translating existing text, or for anything longer than one sentence. Those are ordinary requests and need no skill.

## Non-goals

- Multi-sentence introductions
- Translation of arbitrary text
