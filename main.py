import customtkinter as ctk
import database
from ui.dashboard import DashboardPage
from ui.project_page import ProjectPage
from ui.freelancer_page import FreelancerPage
import os
from PIL import Image

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Freelance Project Tracker")
        self.geometry("1400x850") # Added much larger default resolution
        self.resizable(True, True)
        self.minsize(1200, 750)
        self.configure(fg_color="#f0f4f8")

        database.initialize_database()

        # =========== 1) SPLASH SCREEN ===========
        self.splash_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0)
        self.splash_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'splash_logo.png')
        try:
            pil_img = Image.open(logo_path)
            self.logo_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(400, 400))
            self.splash_label = ctk.CTkLabel(self.splash_frame, image=self.logo_img, text="")
            self.splash_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception:
            splash_font = ctk.CTkFont(family="Times New Roman", size=70, weight="bold", slant="italic")
            self.splash_label = ctk.CTkLabel(self.splash_frame, text="Freelance Project Tracker", font=splash_font, text_color="#1976D2")
            self.splash_label.place(relx=0.5, rely=0.5, anchor="center")

        self.after(3000, self.build_main_app)

    def build_main_app(self):
        self.splash_frame.destroy()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Sidebar ── (Increased width to 320 for bigger buttons)
        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=0, fg_color="#111111", border_width=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="Freelance\nTracker", font=ctk.CTkFont(size=38, weight="bold"), text_color="#ffffff")
        self.logo_label.pack(pady=(50, 60))

        # Prepare icons
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        os.makedirs(assets_dir, exist_ok=True)
        
        import urllib.request
        icon_urls = {
            "dashboard_icon.png": "https://img.icons8.com/ios-filled/100/ffffff/dashboard.png",
            "projects_icon.png": "https://img.icons8.com/ios-filled/100/ffffff/folder-invoices.png",
            "freelancer_icon.png": "https://img.icons8.com/ios-filled/100/ffffff/user.png"
        }
        icon_imgs = {}
        for filename, url in icon_urls.items():
            icon_path = os.path.join(assets_dir, filename)
            if not os.path.exists(icon_path):
                try:
                    urllib.request.urlretrieve(url, icon_path)
                except Exception:
                    pass
            try:
                pil_icon = Image.open(icon_path).resize((30, 30))
                icon_imgs[filename] = ctk.CTkImage(light_image=pil_icon, dark_image=pil_icon, size=(30, 30))
            except Exception:
                icon_imgs[filename] = None

        # Scaled up buttons
        btn_font = ctk.CTkFont(size=22, weight="bold")
        
        dash_img = icon_imgs.get("dashboard_icon.png")
        self.btn_dashboard = ctk.CTkButton(self.sidebar, text="  Dashboard", command=lambda: self.show_page("dashboard"),
                                           image=dash_img, fg_color="transparent", anchor="w", font=btn_font, text_color="#ffffff",
                                           hover_color="#1E88E5", corner_radius=12, height=60, compound="left")
        self.btn_dashboard.pack(fill="x", padx=25, pady=12)

        proj_img = icon_imgs.get("projects_icon.png")
        self.btn_projects = ctk.CTkButton(self.sidebar, text="  Projects", command=lambda: self.show_page("projects"),
                                          image=proj_img, fg_color="transparent", anchor="w", font=btn_font, text_color="#ffffff",
                                          hover_color="#1E88E5", corner_radius=12, height=60, compound="left")
        self.btn_projects.pack(fill="x", padx=25, pady=12)

        free_img = icon_imgs.get("freelancer_icon.png")
        self.btn_freelancers = ctk.CTkButton(self.sidebar, text="  Freelancers", command=lambda: self.show_page("freelancers"),
                                             image=free_img, fg_color="transparent", anchor="w", font=btn_font, text_color="#ffffff",
                                             hover_color="#1E88E5", corner_radius=12, height=60, compound="left")
        self.btn_freelancers.pack(fill="x", padx=25, pady=12)

        # ── Main Content Area ──
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.pages = {
            "dashboard": DashboardPage(self.main_frame),
            "projects": ProjectPage(self.main_frame),
            "freelancers": FreelancerPage(self.main_frame)
        }
        self.show_page("dashboard")

    def show_page(self, page_name):
        for page in self.pages.values():
            page.grid_remove()
        self.pages[page_name].grid(row=0, column=0, sticky="nsew")
        if page_name == "dashboard" and hasattr(self.pages[page_name], "refresh"):
            self.pages[page_name].refresh()

if __name__ == "__main__":
    app = App()
    app.mainloop()