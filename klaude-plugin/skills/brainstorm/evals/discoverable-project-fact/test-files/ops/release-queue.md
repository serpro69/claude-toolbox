# Release queue operating note

Current limit: one concurrent deployment (`max_concurrent_deployments = 1`).

All deployments share the staging database migration lock. The limit prevents two deployments from contending for that lock; parallel deployment safety has not been established.

Recent queue waits reach ten minutes. We have not measured what fraction of deployment time holds the migration lock. This note records the current setup, not a decision to change concurrency.
