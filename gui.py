import tkinter as tk
from tkcalendar import DateEntry
from datetime import date
from logic import load_projects, save_projects

class KanbanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kanban Project Tracker")
        self.root.geometry("900x530")
        self.root.configure(bg="#f0f0f0")

        self.columns = ["To Do", "In Progress", "Done"]
        self.column_frames = {}
        self.projects = load_projects()

        for i, title in enumerate(self.columns):
            frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RIDGE)
            frame.place(x=20 + i * 300, y=90, width=280, height=400)

            label = tk.Label(frame, text=title, bg="#ffffff", font=("Arial", 14, "bold"))
            label.pack(pady=10)

            self.column_frames[title] = frame

        header = tk.Label(
            self.root,
            text="Kanban Project Tracker",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0"
        )
        header.pack(pady=10)

        add_button = tk.Button(
            self.root,
            text="➕ Add New Project",
            command=self.show_add_project_popup,
            font=("Arial", 12),
            bg="#4caf50",
            fg="white",
            padx=10,
            pady=5
        )
        add_button.place(x=700, y=20)

        self.filter_var = tk.BooleanVar(value=False)
        filter_check = tk.Checkbutton(
            self.root,
            text="🔍 Show only due this week",
            variable=self.filter_var,
            command=self.render_all_projects,
            bg="#f0f0f0"
        )
        filter_check.place(x=20, y=60)

        self.render_all_projects()

    def show_add_project_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add New Project")
        popup.geometry("300x300")

        tk.Label(popup, text="Project Title:").pack(pady=5)
        title_entry = tk.Entry(popup, width=30)
        title_entry.pack()

        tk.Label(popup, text="Description:").pack(pady=5)
        desc_entry = tk.Entry(popup, width=30)
        desc_entry.pack()

        tk.Label(popup, text="Due Date (optional):").pack(pady=5)
        due_entry = DateEntry(popup, width=27, background='darkblue', foreground='white',
                              borderwidth=2, date_pattern="yyyy-mm-dd")
        due_entry.pack()

        user_selected_date = tk.BooleanVar(value=False)

        def mark_user_changed(*args):
            user_selected_date.set(True)

        due_entry.bind("<<DateEntrySelected>>", mark_user_changed)

        def submit():
            title = title_entry.get()
            desc = desc_entry.get()
            due_date = due_entry.get_date().strftime("%Y-%m-%d") if user_selected_date.get() else ""

            if title.strip():
                new_project = {
                    "title": title,
                    "description": desc,
                    "due_date": due_date,
                    "status": "To Do"
                }
                self.projects.append(new_project)
                save_projects(self.projects)
                self.render_all_projects()
                popup.destroy()

        submit_btn = tk.Button(popup, text="Add Project", command=submit, bg="#2196f3", fg="white")
        submit_btn.pack(pady=15)

    def show_edit_popup(self, index):
        popup = tk.Toplevel(self.root)
        popup.title("Edit Project")
        popup.geometry("300x300")

        tk.Label(popup, text="Project Title:").pack(pady=5)
        title_entry = tk.Entry(popup, width=30)
        title_entry.insert(0, self.projects[index]["title"])
        title_entry.pack()

        tk.Label(popup, text="Description:").pack(pady=5)
        desc_entry = tk.Entry(popup, width=30)
        desc_entry.insert(0, self.projects[index]["description"])
        desc_entry.pack()

        tk.Label(popup, text="Due Date (optional):").pack(pady=5)
        due_entry = DateEntry(popup, width=27, background='darkblue', foreground='white',
                              borderwidth=2, date_pattern="yyyy-mm-dd")
        due_entry.pack()

        current_due = self.projects[index].get("due_date", "").strip()
        user_selected_date = tk.BooleanVar(value=False)

        if current_due:
            due_entry.set_date(current_due)
        else:
            due_entry.set_date(date.today())

        def mark_user_changed(*args):
            user_selected_date.set(True)

        due_entry.bind("<<DateEntrySelected>>", mark_user_changed)

        def submit():
            self.projects[index]["title"] = title_entry.get()
            self.projects[index]["description"] = desc_entry.get()

            if current_due and not user_selected_date.get():
                self.projects[index]["due_date"] = current_due
            elif not current_due and not user_selected_date.get():
                self.projects[index]["due_date"] = ""
            else:
                self.projects[index]["due_date"] = due_entry.get_date().strftime("%Y-%m-%d")

            save_projects(self.projects)
            self.render_all_projects()
            popup.destroy()

        tk.Button(popup, text="Update", command=submit, bg="#ff9800", fg="white").pack(pady=15)

    def add_project_card(self, project, index):
        status = project["status"]
        column = self.column_frames[status]

        card = tk.Frame(column, bg="#e0f7fa", bd=1, relief=tk.SOLID)
        card.pack(pady=5, padx=5, fill="x")

        title_lbl = tk.Label(card, text=project["title"], font=("Arial", 12, "bold"), bg="#e0f7fa")
        title_lbl.pack(anchor="w", padx=5, pady=2)

        desc_lbl = tk.Label(card, text=project["description"], font=("Arial", 10), bg="#e0f7fa", wraplength=250,
                            justify="left")
        desc_lbl.pack(anchor="w", padx=5, pady=2)

        due = project.get("due_date", "").strip()
        if due:
            try:
                due_obj = date.fromisoformat(due)
                is_overdue = due_obj < date.today()
                due_color = "#d32f2f" if is_overdue else "#555"
            except ValueError:
                due_color = "#555"

            due_lbl = tk.Label(card, text=f"Due: {due}", font=("Arial", 9, "italic"), bg="#e0f7fa", fg=due_color)
            due_lbl.pack(anchor="w", padx=5, pady=2)

        btn_frame = tk.Frame(card, bg="#e0f7fa")
        btn_frame.pack(anchor="e", padx=5, pady=5)

        col_index = self.columns.index(status)

        if col_index > 0:
            left_btn = tk.Button(btn_frame, text="←", command=lambda: self.move_project(index, -1))
            left_btn.pack(side="left", padx=1)

        if col_index < len(self.columns) - 1:
            right_btn = tk.Button(btn_frame, text="→", command=lambda: self.move_project(index, 1))
            right_btn.pack(side="left", padx=1)

        edit_btn = tk.Button(btn_frame, text="✏️", command=lambda: self.show_edit_popup(index))
        edit_btn.pack(side="left", padx=1)

        delete_btn = tk.Button(btn_frame, text="🗑️", command=lambda: self.delete_project(index))
        delete_btn.pack(side="left", padx=1)

    def move_project(self, index, direction):
        current_status = self.projects[index]["status"]
        col_index = self.columns.index(current_status)
        new_status = self.columns[col_index + direction]

        self.projects[index]["status"] = new_status
        save_projects(self.projects)
        self.render_all_projects()

    def delete_project(self, index):
        del self.projects[index]
        save_projects(self.projects)
        self.render_all_projects()

    def render_all_projects(self):
        for frame in self.column_frames.values():
            for widget in frame.winfo_children()[1:]:
                widget.destroy()

        for status in self.columns:
            if self.filter_var.get():
                today = date.today()
                end_of_week = today.replace(day=today.day + (6 - today.weekday()))
                def is_due_this_week(p):
                    try:
                        due = date.fromisoformat(p.get("due_date", ""))
                        return today <= due <= end_of_week
                    except ValueError:
                        return False
                filtered = [p for p in self.projects if p["status"] == status and is_due_this_week(p)]
            else:
                filtered = [p for p in self.projects if p["status"] == status]

            def sort_key(p):
                try:
                    return date.fromisoformat(p.get("due_date", "9999-12-31"))
                except ValueError:
                    return date.max

            filtered.sort(key=sort_key)

            for project in filtered:
                self.add_project_card(project, self.projects.index(project))
