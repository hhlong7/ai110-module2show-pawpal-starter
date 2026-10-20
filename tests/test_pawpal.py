from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def make_owner():
    owner = Owner("Jordan")
    mochi, biscuit = Pet("Mochi", "cat"), Pet("Biscuit", "dog")
    owner.add_pet(mochi)
    owner.add_pet(biscuit)
    return owner, mochi, biscuit


def test_task_completion_changes_status():
    task = Task("Feeding")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet("Mochi")
    pet.add_task(Task("Feeding"))
    pet.add_task(Task("Play"))
    assert len(pet.tasks) == 2
    assert pet.tasks[0].pet_name == "Mochi"


def test_owner_gets_tasks_from_all_pets():
    owner, mochi, biscuit = make_owner()
    mochi.add_task(Task("Feeding"))
    biscuit.add_task(Task("Walk"))
    assert len(owner.get_all_tasks()) == 2


def test_sort_by_time_orders_chronologically():
    owner, mochi, biscuit = make_owner()
    mochi.add_task(Task("Late", "18:00"))
    biscuit.add_task(Task("Early", "07:30"))
    mochi.add_task(Task("Mid", "12:15"))
    ordered = Scheduler(owner).sort_by_time()
    assert [t.description for t in ordered] == ["Early", "Mid", "Late"]


def test_filter_by_pet_and_status():
    owner, mochi, biscuit = make_owner()
    a, b = Task("A"), Task("B")
    mochi.add_task(a)
    biscuit.add_task(b)
    a.mark_complete()
    s = Scheduler(owner)
    assert s.filter_tasks(pet_name="mochi") == [a]
    assert s.filter_tasks(completed=False) == [b]


def test_daily_task_creates_next_day_occurrence():
    owner, mochi, _ = make_owner()
    task = Task("Feeding", frequency="daily")
    mochi.add_task(task)
    nxt = Scheduler(owner).mark_task_complete(task)
    assert nxt.due_date == date.today() + timedelta(days=1)
    assert nxt.completed is False
    assert nxt in mochi.tasks and len(mochi.tasks) == 2


def test_weekly_task_recurs_in_seven_days():
    owner, mochi, _ = make_owner()
    task = Task("Bath", frequency="weekly")
    mochi.add_task(task)
    assert Scheduler(owner).mark_task_complete(task).due_date == date.today() + timedelta(days=7)


def test_one_off_task_does_not_recur():
    owner, mochi, _ = make_owner()
    task = Task("Vet visit")
    mochi.add_task(task)
    assert Scheduler(owner).mark_task_complete(task) is None
    assert len(mochi.tasks) == 1


def test_conflict_detected_across_pets():
    owner, mochi, biscuit = make_owner()
    mochi.add_task(Task("Feeding", "08:00"))
    biscuit.add_task(Task("Walk", "08:00"))
    warnings = Scheduler(owner).detect_conflicts()
    assert len(warnings) == 1 and "08:00" in warnings[0]


def test_no_conflict_when_times_differ_or_task_done():
    owner, mochi, biscuit = make_owner()
    done = Task("Feeding", "08:00")
    mochi.add_task(done)
    biscuit.add_task(Task("Walk", "08:00"))
    done.mark_complete()
    assert Scheduler(owner).detect_conflicts() == []


def test_empty_owner_is_safe():
    s = Scheduler(Owner("Nobody"))
    assert s.todays_schedule() == [] and s.detect_conflicts() == []
