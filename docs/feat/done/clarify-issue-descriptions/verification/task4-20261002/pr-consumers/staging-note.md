# Staging limitation

The first staging attempt failed before dispatch: the workstation's inherited Git
commit-signing configuration requested GPG-agent access outside the sandbox. No
behavioral agent ran against that incomplete fixture. Its temporary workspace and
partial exported evidence were preserved as `staging-attempt-1`.

The fresh staging attempt sets `commit.gpgsign=false` and `tag.gpgsign=false` on
the local synthetic Git commands only. It does not alter workstation Git settings.
