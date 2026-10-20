"""CLI demo for the PawPal+ logic layer."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(title: str, tasks) -> None:
    print(title)
    print("-" * len(title))
    if not tasks:
        print("  (nothing scheduled)")
    for t in tasks:
        mark = "x" if t.completed else " "
        print(
            f"  [{mark}] {t.time}  {t.description:<18} {t.pet_name:<8} "
            f"{t.duration_minutes:>3} min  {t.priority:<6} {t.frequency}"
        )
    print()


def main() -> None:
    owner = Owner("Jordan")
    mochi, biscuit = Pet("Mochi", "cat"), Pet("Biscuit", "dog")
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    # Added deliberately out of order
    biscuit.add_task(Task("Evening walk", "18:00", 30, "medium", "daily"))
    mochi.add_task(Task("Feeding", "08:00", 10, "high", "daily"))
    biscuit.add_task(Task("Morning walk", "07:30", 30, "high", "daily"))
    mochi.add_task(Task("Flea medicine", "08:00", 5, "high", "weekly"))  # conflict
    mochi.add_task(Task("Play session", "12:15", 20, "low"))

    scheduler = Scheduler(owner)

    print_schedule("Today's Schedule", scheduler.todays_schedule())

    for warning in scheduler.detect_conflicts():
        print(f"WARNING: {warning}")
    print()

    print_schedule("Mochi only", scheduler.filter_tasks(pet_name="Mochi"))

    walk = next(t for t in scheduler.get_all_tasks() if t.description == "Morning walk")
    nxt = scheduler.mark_task_complete(walk)
    print(f"Completed '{walk.description}'; next occurrence due {nxt.due_date} (today is {date.today()})\n")

    print_schedule("Completed tasks", scheduler.filter_tasks(completed=True))


if __name__ == "__main__":
    main()
