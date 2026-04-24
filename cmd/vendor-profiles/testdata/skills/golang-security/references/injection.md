# SQL Injection Prevention

## Parameterized Queries

Always use prepared statements or query builders that support parameter binding.

```go
rows, err := db.Query("SELECT * FROM users WHERE id = ?", userID)
```

## Command Injection

Never construct shell commands from user input. Use exec.Command with separate arguments.
