# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

i started with the app flow as in adding a pet, schedule a task for them, and see the task in time order. there are four classes: task, pet, owner, and scheduler.

**b. Design changes**

i added a pet_name to task so the scheduler can filter and report by pet without going back to the owner. i also added a due_date for recurring tasks. i made the task.mark_complete() return the next occurrence for daily or weekly takss as well

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

the scheduler looks at due date, start time, priority and whether a task is completed. i decided time order matters most, because an owner reads their day from morning to night. priority can be used for sorting, but it doesnt reorder the daily schedule.

**b. Tradeoffs**

conflict detection only flags tasks with the same date and the exact same start time. it doesnt catch overlapping durations, so a 30-minute walk at 8:00 and a feeding at 8:15 aren’t flagged. i accepted this because it keeps the code simple and readable

---

## 3. AI Collaboration

**a. How you used AI**

i used claude for design brainstroming, drafting out the uml, and writing the tests as well as conencting the app all together.

**b. Judgment and verification**

it was suggesting me to convert the time to datetime instead of using hh:mm string with a lambda sort key. and also to verify their work, i have to run the test suite as well as main.py multiple times.

---

## 4. Testing and Verification

**a. What you tested**

i wrote 17 tests. They cover completing a task, adding a task to a pet, gathering tasks across pets, sorting by time and priority, filtering by pet and status, daily and weekly recurrence, and conflict detection. Edge cases include a pet with no tasks, two tasks at the same time, the same time on different days, and completing a recurring task twice. Writing that last test found a real bug that created a duplicate task, which I then fixed.

**b. Confidence**

im fairly confident, about 4 out of 5. The core logic is well tested. Next I would test overlapping durations, invalid time input, and duplicate pet names.

---

## 5. Reflection

**a. What went well**

Im most satisfied with building and checking the logic in the terminal first. By the time I connected the Streamlit UI, the classes already worked, so the wiring was easy.

**b. What you would improve**

n/a

**c. Key takeaway**

ai can write a lot of code quickly, but I still had to decide the structure, like which class owns what and how the scheduler gets its data, and I had to test its output instead of trusting it