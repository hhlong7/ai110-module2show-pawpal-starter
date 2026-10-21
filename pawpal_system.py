"""PawPal+ logic layer: Task, Pet, Owner and Scheduler."""

from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from typing import Dict, List, Optional

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
RECURRENCE_DAYS = {"daily": 1, "weekly": 7}


@dataclass
class Task:
    """A single pet care activity."""

    description: str
    time: str = "08:00"  # "HH:MM", 24-hour
    duration_minutes: int = 15
    priority: str = "medium"  # low | medium | high
    frequency: str = "once"  # once | daily | weekly
    due_date: date = field(default_factory=date.today)
    completed: bool = False
    pet_name: str = ""  # set by Pet.add_task

    def mark_complete(self) -> Optional["Task"]:
        """Mark done; return the next occurrence for recurring tasks, else None."""
        if self.completed:  # already done: don't spawn a duplicate occurrence
            return None
        self.completed = True
        days = RECURRENCE_DAYS.get(self.frequency)
        if days is None:
            return None
        return replace(self, completed=False, due_date=self.due_date + timedelta(days=days))


@dataclass
class Pet:
    """A pet and the tasks that belong to it."""

    name: str
    species: str = "dog"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Detach a task from this pet."""
        self.tasks.remove(task)


@dataclass
class Owner:
    """A pet owner who manages several pets."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Find a pet by name (case-insensitive)."""
        return next((p for p in self.pets if p.name.lower() == name.lower()), None)

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all of the owner's pets."""
        return [t for pet in self.pets for t in pet.tasks]


class Scheduler:
    """The 'brain': organizes and manages tasks across all of an owner's pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Fetch tasks through the Owner so every pet is included."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort by due date then 'HH:MM' (zero-padded strings sort correctly)."""
        tasks = self.get_all_tasks() if tasks is None else tasks
        return sorted(tasks, key=lambda t: (t.due_date, t.time))

    def sort_by_priority(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort high-priority first, ties broken by time."""
        tasks = self.get_all_tasks() if tasks is None else tasks
        return sorted(tasks, key=lambda t: (PRIORITY_ORDER.get(t.priority, 3), t.due_date, t.time))

    def filter_tasks(
        self, pet_name: Optional[str] = None, completed: Optional[bool] = None
    ) -> List[Task]:
        """Filter by pet name and/or completion status (None means no filter)."""
        result = self.get_all_tasks()
        if pet_name is not None:
            result = [t for t in result if t.pet_name.lower() == pet_name.lower()]
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        return result

    def todays_schedule(self, today: Optional[date] = None) -> List[Task]:
        """Pending tasks due today, in time order."""
        today = today or date.today()
        due = [t for t in self.get_all_tasks() if t.due_date == today and not t.completed]
        return self.sort_by_time(due)

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Complete a task; if recurring, add the next occurrence to the same pet."""
        nxt = task.mark_complete()
        if nxt is not None:
            pet = self.owner.get_pet(task.pet_name)
            if pet is not None:
                pet.add_task(nxt)
        return nxt

    def detect_conflicts(self) -> List[str]:
        """Return warning strings for pending tasks sharing a date and start time.

        Lightweight by design: exact start-time matches only, never raises.
        """
        slots: Dict[tuple, List[Task]] = {}
        for t in self.get_all_tasks():
            if not t.completed:
                slots.setdefault((t.due_date, t.time), []).append(t)
        warnings = []
        for (day, time), group in sorted(slots.items()):
            if len(group) > 1:
                names = ", ".join(f"{t.description} ({t.pet_name})" for t in group)
                warnings.append(f"Conflict on {day} at {time}: {names}")
        return warnings
