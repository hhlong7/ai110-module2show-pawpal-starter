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
python -m pytest
```

The 17 tests in `tests/test_pawpal.py` cover:

- **Happy paths:** completing a task, adding a task to a pet, collecting tasks across all pets, chronological sorting, filtering by pet and status, priority sorting, daily (+1 day) and weekly (+7 days) recurrence, and conflict detection across pets.
- **Edge cases:** an owner or pet with no tasks, one-off tasks that must not recur, completing a recurring task twice (no duplicate), same time on different days (no conflict), completed tasks ignored by conflict checks, and today's schedule excluding future and completed tasks.

Sample test output:

```
.................                                                        [100%]
17 passed in 0.03s
```

**Confidence level: ★★★★☆ (4/5).** The logic layer is well covered and the UI was smoke-tested with Streamlit's `AppTest`. Not yet covered: overlapping durations, invalid `HH:MM` input and duplicate pet names.

## ✨ Features

- **Multi-pet management:** one owner, many pets, each with its own tasks.
- **Sorting by time:** tasks are ordered by due date and `HH:MM` (also sortable by priority).
- **Filtering:** by pet name and/or pending vs. completed.
- **Daily and weekly recurrence:** completing a recurring task automatically schedules the next one.
- **Conflict warnings:** pending tasks that share a date and start time are flagged in the UI, never crashing the app.

## 🧩 Implementation Summary

- `Task` (dataclass): description, `HH:MM` time, duration, priority, frequency, due date, completion flag.
- `Pet` (dataclass): name, species, list of tasks.
- `Owner`: holds pets; `get_all_tasks()` flattens every pet's tasks.
- `Scheduler`: takes an `Owner` and reads tasks through `owner.get_all_tasks()`, so it always sees all pets. It sorts, filters, builds today's schedule, completes recurring tasks and detects conflicts.
- `app.py` keeps the `Owner` in `st.session_state` so data survives Streamlit reruns. Run with `streamlit run app.py`.
- UML: `diagrams/uml_final.mmd` (final), `diagrams/uml.mmd` (working copy).

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time`, `sort_by_priority` | `sorted()` with a lambda key; zero-padded `"HH:MM"` strings sort correctly as text |
| Filtering | `Scheduler.filter_tasks(pet_name, completed)` | Either filter optional; `None` means no filter |
| Conflict handling | `Scheduler.detect_conflicts` | Warning strings for pending tasks sharing a date and start time, across pets; never raises |
| Recurring tasks | `Task.mark_complete`, `Scheduler.mark_task_complete` | Daily = +1 day, weekly = +7 days via `timedelta`; next occurrence added to the same pet |

## 📸 Demo Walkthrough

**Main UI features:** add pets, schedule tasks (time, duration, priority, repeat), see a conflict banner, browse a sorted and filterable schedule table, and mark tasks complete.

**Example workflow:**

1. Enter the owner name and add a pet (e.g. Mochi, cat), then add a second pet.
2. Schedule a task for a pet: description, time, duration, priority, and repeat (once/daily/weekly).
3. Schedule a second task at the same time. A warning appears naming the clashing tasks.
4. View the schedule table, sorted by time; filter it by pet and by pending/completed.
5. Pick a daily task under **Mark a task complete**. It is checked off and tomorrow's occurrence is added automatically.

**Key Scheduler behaviors shown:** sorting by time, filtering, conflict warnings, and daily/weekly recurrence.

**CLI output** (`python main.py`):

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

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
