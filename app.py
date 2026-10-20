import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# Streamlit reruns this script on every click, so keep the Owner in session_state.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
owner: Owner = st.session_state.owner
scheduler = Scheduler(owner)

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.subheader("Add a pet")
with st.form("add_pet", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        if not pet_name.strip():
            st.error("Pet name is required.")
        elif owner.get_pet(pet_name):
            st.error(f"{pet_name} already exists.")
        else:
            owner.add_pet(Pet(pet_name.strip(), species))
            st.success(f"Added {pet_name}!")

if not owner.pets:
    st.info("Add a pet to start scheduling tasks.")
    st.stop()

st.subheader("Schedule a task")
with st.form("add_task", clear_on_submit=False):
    target = st.selectbox("Pet", [p.name for p in owner.pets])
    description = st.text_input("Task", value="Morning walk")
    c1, c2, c3, c4 = st.columns(4)
    when = c1.time_input("Time")
    duration = c2.number_input("Minutes", min_value=1, max_value=240, value=20)
    priority = c3.selectbox("Priority", ["low", "medium", "high"], index=2)
    frequency = c4.selectbox("Repeats", ["once", "daily", "weekly"])
    if st.form_submit_button("Add task"):
        owner.get_pet(target).add_task(
            Task(description, when.strftime("%H:%M"), int(duration), priority, frequency)
        )
        st.success(f"Scheduled '{description}' for {target}.")
        for warning in scheduler.detect_conflicts():
            st.warning(warning)

st.divider()
st.subheader("Today's schedule")

for warning in scheduler.detect_conflicts():
    st.warning(f"⚠️ {warning}")

view_pet = st.selectbox("Show pet", ["All"] + [p.name for p in owner.pets])
view_status = st.radio("Status", ["Pending", "Completed", "All"], horizontal=True)

tasks = scheduler.filter_tasks(
    pet_name=None if view_pet == "All" else view_pet,
    completed={"Pending": False, "Completed": True, "All": None}[view_status],
)
tasks = scheduler.sort_by_time(tasks)

if not tasks:
    st.info("No tasks match.")
for i, t in enumerate(tasks):
    col_a, col_b = st.columns([5, 1])
    col_a.write(
        f"**{t.time}** · {t.description} — {t.pet_name} "
        f"({t.duration_minutes} min, {t.priority}, {t.frequency}, due {t.due_date})"
    )
    if not t.completed and col_b.button("Done", key=f"done_{id(t)}"):
        nxt = scheduler.mark_task_complete(t)
        if nxt:
            st.toast(f"Next '{t.description}' scheduled for {nxt.due_date}")
        st.rerun()
