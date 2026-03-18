import customtkinter as ctk
import database
from tkcalendar import DateEntry

class ProjectPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.build()
        self.load_projects()

    def build(self):
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=(30, 20))

        ctk.CTkLabel(top, text="Projects Management",
                     font=ctk.CTkFont(size=36, weight="bold"),
                     text_color="#1E88E5").pack(side="left")

        ctk.CTkButton(top, text="+ Add Project",
                      font=ctk.CTkFont(size=20, weight="bold"), height=50, corner_radius=12,
                      fg_color="#1E88E5", hover_color="#1565C0",
                      command=self.open_add_dialog).pack(side="right")

        headers = ctk.CTkFrame(self, fg_color="#111111", corner_radius=12)
        headers.pack(fill="x", padx=30, pady=(0, 10))

        cols = ["ID", "Project Name", "Client", "Freelancer", "Deadline", "Status", "Payment", "Actions"]
        for i, col in enumerate(cols):
            ctk.CTkLabel(headers, text=col, font=ctk.CTkFont(size=18, weight="bold"), text_color="#ffffff").grid(row=0, column=i, padx=20, pady=15, sticky="w")
            headers.grid_columnconfigure(i, weight=1)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=30, pady=10)

    def load_projects(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        projects = database.get_all_projects()

        for i, project in enumerate(projects):
            bg_color = "#ffffff" if i % 2 == 0 else "#F8FAFC"
            row = ctk.CTkFrame(self.scroll, fg_color=bg_color, corner_radius=12, border_width=1, border_color="#e0e0e0")
            row.pack(fill="x", pady=6)

            for j in range(8):
                row.grid_columnconfigure(j, weight=1)

            values = [str(project["id"]), project["project_name"], project["client_name"], project["freelancer"], project["deadline"], project["status"], project["payment_status"]]

            for j, val in enumerate(values):
                color = "#333333"
                if val == "Completed": color = "#2E7D32"
                elif val == "Pending": color = "#E65100"
                elif val == "Paid":    color = "#2E7D32"
                elif val == "Unpaid":  color = "#E65100"

                ctk.CTkLabel(row, text=val, text_color=color, font=ctk.CTkFont(size=16, weight="bold" if j in [5,6] else "normal")).grid(row=0, column=j, padx=20, pady=18, sticky="w")

            actions_frame = ctk.CTkFrame(row, fg_color="transparent")
            actions_frame.grid(row=0, column=7, padx=15, pady=10, sticky="e")
            
            ctk.CTkButton(actions_frame, text="✏️ Edit", width=70, height=35, font=ctk.CTkFont(size=15, weight="bold"), fg_color="#1E88E5", hover_color="#1565C0",
                          command=lambda p=project: self.open_dialog(p)).pack(side="left", padx=5)
            ctk.CTkButton(actions_frame, text="🗑️ Delete", width=70, height=35, font=ctk.CTkFont(size=15, weight="bold"), fg_color="#E65100", hover_color="#BF360C",
                          command=lambda pid=project["id"]: self.delete_project(pid)).pack(side="left")

    def open_add_dialog(self):
        self.open_dialog()

    def open_dialog(self, project=None):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Project Details")
        dialog.geometry("550x750")
        dialog.configure(fg_color="#ffffff")

        dialog.transient(self.winfo_toplevel())
        dialog.lift()
        dialog.focus_force()
        # dialog.attributes("-topmost", True) # Removed to fix tkcalendar popup issue
        # dialog.grab_set() # Removed because it traps tkcalendar click events

        title_lbl = ctk.CTkLabel(dialog, text="Add New Project" if not project else "Edit Project",
                                 font=ctk.CTkFont(size=28, weight="bold"), text_color="#1E88E5")
        title_lbl.pack(pady=(30, 20))

        fields = ["Project Name", "Client Name", "Freelancer"]
        entries = []

        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=40)

        for field in fields:
            ctk.CTkLabel(form_frame, text=field, text_color="#333333", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(15, 5))
            entry = ctk.CTkEntry(form_frame, width=450, height=45, font=ctk.CTkFont(size=16), corner_radius=22, border_color="#cccccc")
            entry.pack(anchor="w")
            entries.append(entry)

        # Date Entry with ttkcalendar
        ctk.CTkLabel(form_frame, text="Deadline", text_color="#333333", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(15, 5))
        date_entry = DateEntry(form_frame, width=38, background='#1E88E5', foreground='white', borderwidth=2,
                               font=('Helvetica', 14), date_pattern='yyyy-mm-dd')
        date_entry.pack(anchor="w")
        
        # Status dropdown
        ctk.CTkLabel(form_frame, text="Status", text_color="#333333", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(15, 5))
        status_var = ctk.StringVar(value=project["status"] if project else "Pending")
        ctk.CTkOptionMenu(form_frame, variable=status_var, font=ctk.CTkFont(size=16), height=45, width=200, values=["Pending", "In Progress", "Completed"],
                          fg_color="#1E88E5", button_color="#1565C0", corner_radius=22,
                          dropdown_fg_color="#ffffff", dropdown_hover_color="#f0f4f8", dropdown_text_color="#333333").pack(anchor="w")

        # Payment dropdown
        ctk.CTkLabel(form_frame, text="Payment Status", text_color="#333333", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(15, 5))
        payment_var = ctk.StringVar(value=project["payment_status"] if project else "Unpaid")
        ctk.CTkOptionMenu(form_frame, variable=payment_var, font=ctk.CTkFont(size=16), height=45, width=200, values=["Unpaid", "Paid"],
                          fg_color="#1E88E5", button_color="#1565C0", corner_radius=22,
                          dropdown_fg_color="#ffffff", dropdown_hover_color="#f0f4f8", dropdown_text_color="#333333").pack(anchor="w")

        for i in range(len(entries) - 1):
            entries[i].bind("<Return>", lambda e, nxt=entries[i+1]: nxt.focus_set())
        
        if project:
            entries[0].insert(0, project["project_name"])
            entries[1].insert(0, project["client_name"])
            entries[2].insert(0, project["freelancer"])
            if project["deadline"]:
                try:
                    date_entry.set_date(project["deadline"])
                except Exception:
                    pass

        def save():
            if project:
                database.update_project(project["id"], entries[0].get(), entries[1].get(), entries[2].get(),
                                        date_entry.get(), status_var.get(), payment_var.get())
            else:
                database.add_project(entries[0].get(), entries[1].get(), entries[2].get(),
                                     date_entry.get(), status_var.get(), payment_var.get())
            dialog.destroy()
            self.load_projects()

        entries[-1].bind("<Return>", lambda e: save())

        ctk.CTkButton(dialog, text="Save Project", font=ctk.CTkFont(size=18, weight="bold"), height=50, corner_radius=22,
                      fg_color="#1E88E5", hover_color="#1565C0", command=save).pack(pady=(30, 20))

    def delete_project(self, pid):
        database.delete_project(pid)
        self.load_projects()