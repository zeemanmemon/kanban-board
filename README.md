🗂️ KanbanBoard – A Visual Project Tracker (Tkinter)
====================================================

**KanbanBoard** is a lightweight desktop app to visually manage your projects and tasks using the Kanban method.

Built with Python and Tkinter, it lets you quickly organize tasks across columns like **To Do**, **In Progress**, and **Done** — with features like due dates, editing, filtering, and visual indicators for overdue tasks.

* * *

🚀 Features
-----------

* ➕ Add new tasks with title, description, and optional due date
* ✏️ Edit or 🗑️ delete existing tasks
* ➡️ Move tasks between columns (To Do → In Progress → Done)
* 📅 Select due dates with a calendar picker (`tkcalendar`)
* 🔴 Highlight overdue tasks in red
* 📊 Sort tasks by due date
* 🔍 Quick filter: Show only tasks due **this week**
* 🔒 Local storage with `data.json` (no internet required)

* * *

🛠️ Requirements
----------------

* Python 3.x
* [tkcalendar](https://pypi.org/project/tkcalendar/)

    pip install tkcalendar

* * *

🧰 How to Run
-------------

1.  Clone the repo or copy the files into a folder
2.  Ensure you have `main.py`, `gui.py`, `logic.py`, and `data.json`
3.  Run the app:

    python main.py

* * *

📁 File Structure
-----------------

kanban-board/
├── main.py           # App entry point
├── gui.py            # GUI layout and logic
├── logic.py          # Load/save project data
├── data.json         # Project data storage
└── README.md         # This file
    

* * *

🧠 Future Ideas
--------------------------

* ⏳ Drag-and-drop task movement
* 📥 Import/export tasks to CSV
* 🎨 Tagging or color labels
* 📈 Dashboard summary view

* * *

👨‍💻 Made With
---------------

* Python
* Tkinter
* tkcalendar
