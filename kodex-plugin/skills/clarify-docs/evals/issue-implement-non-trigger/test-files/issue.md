# Feature: optional greeting name

Read-only offline issue for https://github.example.invalid/acme/greeting/issues/23.

Allow `greet(name)` to return `Hello, <name>!`. Calling `greet()` without a name must continue returning `Hello, world!`. An empty string is a supplied name and should return `Hello, !`. No external dependencies are needed. Work only on the staged source; no live tracker access is available.
