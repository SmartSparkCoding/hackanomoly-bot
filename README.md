# Hackanomoly

Hackanomoly is the Slack support bot used for Hack Club help workflows, with ticket routing, helper tooling, App Home dashboards, and automation.

## What It Does

### Ticket Lifecycle

- Creates a backend ticket whenever a new help message is posted.
- Posts a user-facing thread reply with a resolve button.
- Generates short ticket titles.
- Suggests and applies team tags for routing.
- Assigns tickets to helpers when helpers reply in-thread.

### Duplicate Guard

- Prevents repeat tickets from the same user within a short window.
- Uses relatedness checks to decide whether to close the newer ticket as a duplicate.
- Posts a summary and link to the original ticket when a duplicate is closed.

### App Home

- Dashboard
- Guide
- User Profiles
- Assigned Tickets
- Team Tags
- DM User (maintainer-only)
- My Stats

### Macros

Helper macros available in help threads:

- `?resolve` and aliases like `?close`
- `?reopen` and aliases like `?open`, `?unresolve`
- `?ai` and aliases like `?ask-ai`
- `?faq`
- `?identity`
- `?fraud`
- `?shipcertqueue` and related aliases
- `?thread`
- `?redirect` and aliases like `?admin`

### Scheduled Jobs

- Daily stats summary post.
- Fulfillment reminder post.
- Stale-ticket monitor.

## Scripts

Dummy data generator for performance testing:

```bash
uv run nephthys/scripts/add_dummy_data.py <num_records>
```

## License

MIT
