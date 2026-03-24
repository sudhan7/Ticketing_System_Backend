# Ticketing_System_Backend | # Devtrack

A Django-based issue tracking API that stores data in flat JSON files.

---

## Setup & Run

```bash
conda activate devtrack
pip install -r requirements.txt
python manage.py runserver
```

Server runs at `http://localhost:8000`

---

## Endpoints

### Reporters

| Method | URL | Description |
|--------|-----|-------------|
| `POST` | `/api/reporters/` | Create a new reporter |
| `GET` | `/api/reporters/all/` | List all reporters |
| `GET` | `/api/reporters/<id>/` | Get a reporter by ID |

**POST `/api/reporters/`**
```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com",
  "team": "Backend"
}
```

---

### Issues

| Method | URL | Description |
|--------|-----|-------------|
| `POST` | `/api/issues/` | Create a new issue |
| `GET` | `/api/issues/all/` | List all issues |
| `GET` | `/api/issues/<id>/` | Get an issue by ID |
| `GET` | `/api/issues/status/<status>/` | Filter issues by status |

Valid statuses: `open`, `in_progress`, `resolved`, `closed`
Valid priorities: `low`, `medium`, `high`, `critical`

**POST `/api/issues/`**
```json
{
  "id": 1,
  "title": "Login button not working",
  "description": "Users on iOS 17 cannot tap the login button",
  "status": "open",
  "priority": "critical",
  "reporter_id": 1,
  "created_at": "2026-03-24T10:00:00"
}
```

Response includes a `describe` field derived from the issue's priority class:
- `critical` → `"[URGENT] Login button not working — needs immediate attention"`
- `low` → `"Login button not working — low priority, handle when time allows"`
- `medium` / `high` → `"Login button not working [high]"`

---

## Design Decision

**Subclass dispatch based on priority**

Instead of handling priority with conditionals scattered through the codebase, the `create_issue` view instantiates a different class (`CriticalIssue`, `LowPriorityIssue`, or base `Issue`) based on the incoming `priority` field. Each class overrides `describe()` to return a priority-appropriate message.

This keeps priority-specific behaviour encapsulated in the model layer and makes it easy to add new priority types (e.g. `UrgentIssue`) without touching the view logic.
