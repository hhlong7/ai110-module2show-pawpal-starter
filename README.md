# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output of `python main.py`:

```
Today's Schedule
----------------
  [ ] 07:30  Morning walk       Biscuit   30 min  high   daily
  [ ] 08:00  Feeding            Mochi     10 min  high   daily
  [ ] 08:00  Flea medicine      Mochi      5 min  high   weekly
  [ ] 12:15  Play session       Mochi     20 min  low    once
  [ ] 18:00  Evening walk       Biscuit   30 min  medium daily

WARNING: Conflict on 2026-10-20 at 08:00: Feeding (Mochi), Flea medicine (Mochi)

Mochi only
----------
  [ ] 08:00  Feeding            Mochi     10 min  high   daily
  [ ] 08:00  Flea medicine      Mochi      5 min  high   weekly
  [ ] 12:15  Play session       Mochi     20 min  low    once

Completed 'Morning walk'; next occurrence due 2026-10-21 (today is 2026-10-20)

Completed tasks
---------------
  [x] 07:30  Morning walk       Biscuit   30 min  high   daily
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
...........                                                              [100%]
11 passed in 0.02s
```

## 🧩 Implementation Summary

- `Task` (dataclass): description, `HH:MM` time, duration, priority, frequency, due date, completion flag.
- `Pet` (dataclass): name, species, list of tasks.
- `Owner`: holds pets; `get_all_tasks()` flattens every pet's tasks.
- `Scheduler`: takes an `Owner` and reads tasks through `owner.get_all_tasks()`, so it always sees all pets. It sorts, filters, builds today's schedule, completes recurring tasks and detects conflicts.
- `app.py` keeps the `Owner` in `st.session_state` so data survives Streamlit reruns. Run with `streamlit run app.py`.
- UML: `diagrams/uml.mmd`.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time`, `sort_by_priority` | `sorted()` with a lambda key; zero-padded `"HH:MM"` strings sort correctly as text |
| Filtering | `Scheduler.filter_tasks(pet_name, completed)` | Either filter optional; `None` means no filter |
| Conflict handling | `Scheduler.detect_conflicts` | Warning strings for pending tasks sharing a date and start time, across pets; never raises |
| Recurring tasks | `Task.mark_complete`, `Scheduler.mark_task_complete` | Daily = +1 day, weekly = +7 days via `timedelta`; next occurrence added to the same pet |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Enter the owner name and add one or more pets (name + species).
2. Schedule tasks for a pet: description, time, duration, priority, and repeat (once/daily/weekly).
3. If two pending tasks share a start time, a conflict warning appears.
4. View the schedule sorted by time; filter by pet and by pending/completed.
5. Click **Done** on a task; daily/weekly tasks automatically get a next occurrence.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
