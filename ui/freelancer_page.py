import customtkinter as ctk
import database

class FreelancerPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.build()
        self.load_freelancers()

    def build(self):
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=(30, 20))

        ctk.CTkLabel(top, text="Freelancers Directory",
                     font=ctk.CTkFont(size=36, weight="bold"),
                     text_color="#1E88E5").pack(side="left")

        ctk.CTkButton(top, text="+ Add Freelancer",
                      font=ctk.CTkFont(size=20, weight="bold"), height=50, corner_radius=12,
                      fg_color="#1E88E5", hover_color="#1565C0",
                      command=self.open_add_dialog).pack(side="right")

        headers = ctk.CTkFrame(self, fg_color="#111111", corner_radius=12)
        headers.pack(fill="x", padx=30, pady=(0, 10))

        cols = ["ID", "Name", "Specialization", "Email", "Exp.", "Projects", "Actions"]
        for i, col in enumerate(cols):
            ctk.CTkLabel(headers, text=col, font=ctk.CTkFont(size=16, weight="bold"), text_color="#ffffff").grid(row=0, column=i, padx=10, pady=15, sticky="w")
            headers.grid_columnconfigure(i, weight=1)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=30, pady=10)

    def load_freelancers(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        freelancers = database.get_all_freelancers()

        for i, f in enumerate(freelancers):
            bg_color = "#ffffff" if i % 2 == 0 else "#F8FAFC"
            row = ctk.CTkFrame(self.scroll, fg_color=bg_color, corner_radius=12, border_width=1, border_color="#e0e0e0")
            row.pack(fill="x", pady=6)

            for j in range(7):
                row.grid_columnconfigure(j, weight=1)

            # Use dict to safely use .get() for new fields in case of row missing them during dev
            f_dict = dict(f)
            values = [str(f_dict.get("id", i)), f_dict.get("name", ""), f_dict.get("specialization", ""), f_dict.get("email", ""), str(f_dict.get("years_experience", 0)) + " yrs", str(f_dict.get("projects_completed", 0))]

            for j, val in enumerate(values):
                ctk.CTkLabel(row, text=val, text_color="#333333", font=ctk.CTkFont(size=15)).grid(row=0, column=j, padx=10, pady=18, sticky="w")

            actions_frame = ctk.CTkFrame(row, fg_color="transparent")
            actions_frame.grid(row=0, column=6, padx=15, pady=10, sticky="e")
            
            ctk.CTkButton(actions_frame, text="✏️ Edit", width=70, height=35, font=ctk.CTkFont(size=15, weight="bold"), fg_color="#1E88E5", hover_color="#1565C0",
                          command=lambda r=f: self.open_dialog(r)).pack(side="left", padx=5)
            ctk.CTkButton(actions_frame, text="🗑️ Delete", width=70, height=35, font=ctk.CTkFont(size=15, weight="bold"), fg_color="#E65100", hover_color="#BF360C",
                          command=lambda fid=f["id"]: self.delete_freelancer(fid)).pack(side="left")

    def open_add_dialog(self):
        self.open_dialog()

    def open_dialog(self, freelancer=None):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Freelancer Details")
        dialog.geometry("500x800")
        dialog.configure(fg_color="#ffffff")

        dialog.transient(self.winfo_toplevel())
        dialog.lift()
        dialog.focus_force()
        # dialog.attributes("-topmost", True) # Removed to avoid popup overlap issues
        # dialog.grab_set() # Removed to prevent modal event trapping

        title_lbl = ctk.CTkLabel(dialog, text="Add New Freelancer" if not freelancer else "Edit Freelancer",
                                 font=ctk.CTkFont(size=28, weight="bold"), text_color="#1E88E5")
        title_lbl.pack(pady=(20, 15))

        fields = ["Name", "Skill", "Email", "Years of Experience", "Portfolio Link", "Projects Completed"]
        entries = []

        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=40)

        for field in fields:
            ctk.CTkLabel(form_frame, text=field, text_color="#333333", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", pady=(8, 2))
            entry = ctk.CTkEntry(form_frame, width=420, height=35, font=ctk.CTkFont(size=14), corner_radius=22, border_color="#cccccc")
            entry.pack(anchor="w")
            entries.append(entry)

        ctk.CTkLabel(form_frame, text="Specialization", text_color="#333333", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", pady=(8, 2))
        f_dict = dict(freelancer) if freelancer else {}
        spec_var = ctk.StringVar(value=f_dict.get("specialization", "React"))
        ctk.CTkOptionMenu(form_frame, variable=spec_var, font=ctk.CTkFont(size=14), height=35, width=200, corner_radius=22,
                          values=["React", "Python", "IoT", "App Developer", "Web Design", "Data Science", "Backend Developer", "UI/UX Design", "Machine Learning", "DevOps", "Other"],
                          fg_color="#1E88E5", button_color="#1565C0",
                          dropdown_fg_color="#ffffff", dropdown_hover_color="#f0f4f8", dropdown_text_color="#333333").pack(anchor="w")

        for i in range(len(entries) - 1):
            entries[i].bind("<Return>", lambda e, nxt=entries[i+1]: nxt.focus_set())

        if freelancer:
            entries[0].insert(0, f_dict.get("name", ""))
            entries[1].insert(0, f_dict.get("skill", ""))
            entries[2].insert(0, f_dict.get("email", ""))
            entries[3].insert(0, str(f_dict.get("years_experience", 0)))
            entries[4].insert(0, f_dict.get("portfolio_link", ""))
            entries[5].insert(0, str(f_dict.get("projects_completed", 0)))

        def save():
            try: yrs = int(entries[3].get())
            except ValueError: yrs = 0
            
            try: projs = int(entries[5].get())
            except ValueError: projs = 0

            if freelancer:
                database.update_freelancer(f_dict.get("id"), entries[0].get(), entries[1].get(), entries[2].get(), yrs, entries[4].get(), projs, spec_var.get())
            else:
                database.add_freelancer(entries[0].get(), entries[1].get(), entries[2].get(), yrs, entries[4].get(), projs, spec_var.get())
            dialog.destroy()
            self.load_freelancers()

        entries[-1].bind("<Return>", lambda e: save())

        ctk.CTkButton(dialog, text="Save Freelancer", font=ctk.CTkFont(size=18, weight="bold"), height=50, corner_radius=22,
                      fg_color="#1E88E5", hover_color="#1565C0", command=save).pack(pady=(20, 20))

    def delete_freelancer(self, fid):
        database.delete_freelancer(fid)
        self.load_freelancers()