import customtkinter as ctk
import database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.build()

    def build(self):
        title = ctk.CTkLabel(self, text="Dashboard Overview", font=ctk.CTkFont(size=36, weight="bold"), text_color="#1E88E5")
        title.grid(row=0, column=0, sticky="w", padx=15, pady=(0, 25))

        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 25))
        for i in range(4): self.top_frame.grid_columnconfigure(i, weight=1, uniform="kpi")

        self.middle_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.middle_frame.grid(row=2, column=0, sticky="nsew", padx=0, pady=(0, 25))
        self.middle_frame.grid_columnconfigure(0, weight=2)
        self.middle_frame.grid_columnconfigure(1, weight=1)
        self.middle_frame.grid_rowconfigure(0, weight=1)
        
        self.chart_frame = ctk.CTkFrame(self.middle_frame, fg_color="#ffffff", corner_radius=20, border_width=1, border_color="#e0e0e0")
        self.chart_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        self.deadlines_frame = ctk.CTkFrame(self.middle_frame, fg_color="#ffffff", corner_radius=20, border_width=1, border_color="#e0e0e0")
        self.deadlines_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 0))

        self.bottom_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=20, border_width=1, border_color="#e0e0e0")
        self.bottom_frame.grid(row=3, column=0, sticky="nsew", padx=0, pady=(0, 0))
        
        self.refresh()

    def refresh(self):
        stats = database.get_dashboard_stats()
        deadlines = database.get_upcoming_deadlines(limit=4)
        recent = database.get_recent_projects(limit=5)

        for w in self.top_frame.winfo_children() + self.chart_frame.winfo_children() + self.deadlines_frame.winfo_children() + self.bottom_frame.winfo_children():
            w.destroy()

        cards_data = [
            ("Total Projects", stats["total"], "#E3F2FD", "#1565C0"),
            ("Completed", stats["completed"], "#E8F5E9", "#2E7D32"),
            ("In Progress", stats["in_progress"], "#F3E5F5", "#6A1B9A"),
            ("Pending", stats["pending"], "#FFF3E0", "#E65100")
        ]

        for i, (label, val, bg_color, txt_color) in enumerate(cards_data):
            card = ctk.CTkFrame(self.top_frame, fg_color=bg_color, corner_radius=18, height=140)
            card.grid(row=0, column=i, sticky="nsew", padx=(0, 20) if i < 3 else (0,0))
            card.grid_propagate(False)

            ctk.CTkLabel(card, text=str(val), font=ctk.CTkFont(size=52, weight="bold"), text_color=txt_color).pack(pady=(25, 0))
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=18, weight="bold"), text_color=txt_color).pack(pady=(5, 20))

        # Chart
        ctk.CTkLabel(self.chart_frame, text="Project Status Distribution", font=ctk.CTkFont(size=22, weight="bold"), text_color="#333333").pack(pady=(20, 0))
        # Increase figure size and remove tight text overlapping
        fig, ax = plt.subplots(figsize=(6, 4.5), facecolor="#ffffff")
        labels = ['Completed', 'In Progress', 'Pending']
        sizes = [stats["completed"], stats["in_progress"], stats["pending"]]
        colors = ['#81c784', '#ba68c8', '#ffb74d']
        
        if sum(sizes) == 0:
            sizes = [1]; labels = ['No Projects']; colors = ['#e0e0e0']

        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%' if sum(sizes) > 0 else '', colors=colors, startangle=140, textprops={'color':"#222222", 'fontsize':12, 'weight':'bold'})
        fig.patch.set_facecolor('#ffffff')
        ax.axis('equal')  

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)
        plt.close(fig)

        # Deadlines
        ctk.CTkLabel(self.deadlines_frame, text="Upcoming Deadlines", font=ctk.CTkFont(size=22, weight="bold"), text_color="#333333").pack(pady=(20, 15), anchor="w", padx=25)
        if not deadlines:
            ctk.CTkLabel(self.deadlines_frame, text="No upcoming deadlines.", text_color="#777777", font=ctk.CTkFont(size=16)).pack(pady=10, padx=25, anchor="w")
        else:
            for proj, date, sts in deadlines:
                row_f = ctk.CTkFrame(self.deadlines_frame, fg_color="#F8FAFC", corner_radius=10)
                row_f.pack(fill="x", padx=20, pady=6)
                ctk.CTkLabel(row_f, text=proj, font=ctk.CTkFont(size=16, weight="bold"), text_color="#333333").pack(side="left", padx=15, pady=10)
                ctk.CTkLabel(row_f, text=date, font=ctk.CTkFont(size=15), text_color="#E65100").pack(side="right", padx=15, pady=10)

        # Recent
        ctk.CTkLabel(self.bottom_frame, text="Recent Projects", font=ctk.CTkFont(size=22, weight="bold"), text_color="#333333").pack(pady=(20, 10), anchor="w", padx=25)
        hdr_f = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        hdr_f.pack(fill="x", padx=25, pady=5)
        ctk.CTkLabel(hdr_f, text="PROJECT NAME", font=ctk.CTkFont(size=15, weight="bold"), text_color="#888888", width=450, anchor="w").pack(side="left")
        ctk.CTkLabel(hdr_f, text="CLIENT", font=ctk.CTkFont(size=15, weight="bold"), text_color="#888888", width=200, anchor="w").pack(side="left")
        ctk.CTkLabel(hdr_f, text="STATUS", font=ctk.CTkFont(size=15, weight="bold"), text_color="#888888", width=150, anchor="e").pack(side="right")

        if not recent:
            ctk.CTkLabel(self.bottom_frame, text="No recent projects.", text_color="#777777", font=ctk.CTkFont(size=16)).pack(pady=10, padx=25, anchor="w")
        else:
            for i, (proj, client, sts) in enumerate(recent):
                bg_color = "#ffffff" if i % 2 == 0 else "#F8FAFC"
                row_f = ctk.CTkFrame(self.bottom_frame, fg_color=bg_color, corner_radius=10)
                row_f.pack(fill="x", padx=20, pady=4)
                ctk.CTkLabel(row_f, text=proj, font=ctk.CTkFont(size=18), text_color="#333333", width=450, wraplength=430, anchor="w", justify="left").pack(side="left", padx=10, pady=8)
                ctk.CTkLabel(row_f, text=client, font=ctk.CTkFont(size=18), text_color="#666666", width=200, wraplength=180, anchor="w", justify="left").pack(side="left")
                sts_col = "#2E7D32" if sts == "Completed" else ("#E65100" if sts == "Pending" else "#6A1B9A")
                ctk.CTkLabel(row_f, text=sts, font=ctk.CTkFont(size=16, weight="bold"), text_color=sts_col, width=150, anchor="e").pack(side="right", padx=10)