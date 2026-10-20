# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Core actions: add a pet, schedule a task for a pet, and see today's tasks in time order (with conflict warnings).
Four classes: `Task` (one activity: description, time, duration, priority, frequency, status), `Pet` (name, species, its tasks), `Owner` (holds pets; `get_all_tasks()` flattens them) and `Scheduler` (the logic layer that sorts, filters, completes recurring tasks and detects conflicts). `Task` and `Pet` are dataclasses to keep them light.

**b. Design changes**

Two changes. (1) I added `pet_name` to `Task` (set in `Pet.add_task`) so the Scheduler can filter and report by pet without walking back to the owner. (2) `Task.mark_complete()` returns the next occurrence for recurring tasks instead of the Scheduler duplicating tasks itself; `Scheduler.mark_task_complete` then attaches it to the right pet. I also added a `due_date` so recurrence has something to advance.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers due date, start time, priority and completion status. Time ordering matters most because a daily plan is read chronologically; priority is available through `sort_by_priority` but does not reorder the daily schedule.

**b. Tradeoffs**

Conflict detection only flags tasks with the exact same date and start time; it ignores overlapping durations (a 30-min walk at 08:00 and a feeding at 08:15 are not flagged). That keeps the code simple and readable and never blocks the user, which suits a casual pet-care app; duration-overlap checking is the next improvement.

## 3. AI Collaboration

**a. How you used AI**

I used an AI coding assistant (Claude) as a design partner and implementer. In Phase 1 it helped me list the building blocks and draft the Mermaid class diagram. In Phase 2 it turned the UML into dataclass skeletons and then full code, and wrote the `main.py` demo and pytest tests. In Phase 3 it showed me how `st.session_state` keeps the `Owner` alive across Streamlit reruns. In Phase 4 it helped with the sort key, recurrence with `timedelta`, and conflict detection.

The most helpful prompts were specific about structure, such as "the Scheduler must get tasks through `Owner.get_all_tasks()`, not from a single pet," and ones that asked for a lightweight approach, such as conflict detection that returns a warning instead of crashing. Vague prompts gave generic code; constrained prompts gave code I could check.

**b. Judgment and verification**

When I asked for a simpler, more Pythonic version of `detect_conflicts`, the suggestion was to collapse it into a `collections.Counter` or `itertools.groupby` one-liner over (date, time) keys. It was shorter, but it only reports *that* a clash exists, not *which* tasks and pets clash, and the warning message needs that. I kept the explicit `setdefault` loop because it is easier to read and gives the owner a useful message.

I similarly kept `HH:MM` strings with a lambda sort key instead of parsing every time into `datetime`: zero-padded strings already sort correctly.

I verified the AI's code by running `main.py` with tasks added out of order and with a deliberate same-time conflict, checking the output by eye, and by the pytest suite (11 passing tests). I also smoke-tested the Streamlit app with `streamlit.testing.v1.AppTest`: adding a pet and a task.

## 4. Testing and Verification

**a. What you tested**

Task completion, task addition, owner-wide task retrieval, chronological sorting, filtering by pet/status, daily and weekly recurrence (and none for one-off tasks), conflict detection (including that completed tasks don't conflict), and an empty owner. These cover the behaviors the UI depends on.

**b. Confidence**

Fairly confident (11 passing tests plus a Streamlit AppTest smoke run). Next edge cases: overlapping durations, invalid `HH:MM` input, month/year rollover for weekly tasks, and duplicate pet names.

## 5. Reflection

**a. What went well**

The CLI-first workflow: verifying the logic in `main.py` and tests before touching the UI made the Streamlit wiring trivial.

**b. What you would improve**

Add duration-aware conflict detection, task editing/deleting in the UI, and persistence (JSON) so data survives restarts.

**c. Key takeaway**

Design the data flow first (Scheduler reads via Owner); clear boundaries between logic and UI made both AI-generated and hand-written code easier to check.
