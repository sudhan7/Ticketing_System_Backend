# Devtrack

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

##Screenshots of testing API
<img width="1018" height="595" alt="Screenshot 2026-03-24 at 6 14 17 PM" src="https://github.com/user-attachments/assets/050bbde3-a83d-4205-9918-1cf80e8cabc7" />

<img width="1018" height="595" alt="Screenshot 2026-03-24 at 6 18 53 PM" src="https://github.com/user-attachments/assets/65f2b13c-b4e3-4ef4-96f8-21f94a07399a" />

<img width="1018" height="595" alt="Screenshot 2026-03-24 at 6 18 00 PM" src="https://github.com/user-attachments/assets/8733959f-681b-40a3-a86b-2cf868775be7" />

<img width="1018" height="672" alt="Screenshot 2026-03-24 at 6 33 49 PM" src="https://github.com/user-attachments/assets/80bcbf77-7a30-42ab-a76a-4b580f9c6004" />

<img width="1018" height="551" alt="Screenshot 2026-03-24 at 6 38 36 PM" src="https://github.com/user-attachments/assets/9d6a0d20-fdf9-4e53-b7a4-625c7eede789" />
