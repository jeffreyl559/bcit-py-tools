import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, PhotoImage
from data import term1_courses_dict as COURSES_DICT
from helper import open_link_in_browser, open_pdf


class MainApplication():

    # Constructor, ran automatically when an new object of a class is created. Initial state set.
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("CISA Stuff")
        logo = PhotoImage(file="assets/desktop.png")
        self.window.iconphoto(False, logo)

        # Ttk Notebook widget manages a collection of windows and displays a single one at a time. Each child window is associated with a tab.
        self.notebook = ttk.Notebook(self.window)
        self.course_tab = ttk.Frame(self.notebook)
        self.toolbox_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.course_tab, text="Courses")
        self.notebook.add(self.toolbox_tab, text="Toolbox (Beta)")
        self.notebook.pack(expand=1, fill="both")

        # All Frames - Rectangular container for grouping and organizing aother widgets such as Labels
        self.frames = []
        for course_name, course_info in COURSES_DICT.items():
            frame = self.create_course_frame(
                self.course_tab, course_name, course_info)
            self.frames.append(frame)

        self.last_allowed_tab = 0
        self.authenticated_tabs = set()
        self.password = "costco"
        self.bind_events()

        self.center_window(self.window)

        # Tkinter event loop - Keeps window open, listens for interaction, updates GUI
        self.window.mainloop()

    def create_course_frame(self, parent_frame, course_name: str, course_info: dict) -> tk.Frame:
        """ Create frame for course """
        frame = tk.Frame(parent_frame, bd=1, relief='groove')

        info_label = tk.Label(frame, text=course_name + " " +
                              course_info["course_code"], font=("Helvetica", 12, "bold"))
        info_label.pack(pady=(10, 5))

        btn_frame = tk.Frame(frame)
        btn_frame.pack(anchor="w")

        instructor_contact_btn = self.create_popup_btn(btn_frame, "Contact info", dict(
            name=course_info["instructor"], email=course_info["email"], office_hours=course_info["office_hours"]))
        instructor_contact_btn.pack(side=tk.LEFT, padx=15)

        outline_url_or_path = course_info["course_outline_url"] or course_info["course_outline_path"]
        course_outline_btn = self.create_btn(
            btn_frame, "Course outline", outline_url_or_path)
        course_outline_btn.pack(side=tk.LEFT, padx=15)

        learnhub_btn = self.create_btn(btn_frame, "Learning Hub",
                                       course_info["learnhub_url"])
        learnhub_btn.pack(side=tk.LEFT, padx=10, pady=5)

        if course_info.get("alt_platform_name") and course_info.get("alt_platform_url"):
            alt_platform_btn = self.create_btn(
                btn_frame, course_info["alt_platform_name"], course_info["alt_platform_url"])
            alt_platform_btn.pack(side=tk.LEFT, padx=10, pady=5)

        frame.pack(pady=15, fill="x")
        return frame

    def create_btn(self, frame: tk.Frame, btn_text: str, destination_link) -> tk.Button:
        """ Create button where a click will open to a website or file """
        if destination_link.startswith("https://"):
            return tk.Button(frame, text=btn_text,
                             command=lambda: open_link_in_browser(destination_link))
        elif destination_link.endswith(".pdf"):
            return tk.Button(frame, text=btn_text, command=lambda: open_pdf(destination_link))

        return tk.Button(frame, text=btn_text, state=tk.DISABLED)

    def create_popup_btn(self, frame, btn_text: str, popup_text: str) -> tk.Button:
        """ Create popup button with text inside the window """
        return tk.Button(frame, text=btn_text, command=lambda: self.open_popup(popup_text))

    def center_window(self, window) -> None:
        """ Center window horizontally and vertically """
        window.update_idletasks()  # Update geometry

        # Get screen size after widgets are drawn
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Get window size
        window_width = window.winfo_width()
        window_height = window.winfo_height()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        window.geometry(f"+{x}+{y}")

    def open_popup(self, info) -> None:
        """ Open popup containing instructor email and office location & hours """
        dialog = tk.Toplevel(self.window)
        dialog.title("Instructor Contact and Office Hours")
        # Make it modal relative to the root window
        dialog.transient(self.window)
        dialog.grab_set()  # Grab focus and prevent interaction with other windows
        label = ttk.Label(
            dialog, text=f"Email: {info["email"]}\nOffice Hours: {info["office_hours"]}")
        label.pack(padx=15, pady=10)

        label2 = ttk.Label(
            dialog, text=f"All info is subject to change")
        label2.pack(pady=(0, 5))

        ok_button = ttk.Button(dialog, text="OK", command=dialog.destroy)
        ok_button.pack()

        self.center_window(dialog)
        self.window.wait_window(dialog)  # Wait until the dialog is closed

    def bind_events(self):
        # Mouse clicks
        self.notebook.bind("<Button-1>", self.on_tab_click)
        # Keyboard navigation or programmatic tab changes
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def ask_password(self):
        """ Ask user for password """
        self.window.update_idletasks()  # Update geometry
        pwd = simpledialog.askstring(
            "Password Required", "Enter password:", show="*")
        return pwd

    def on_tab_click(self, event):
        """ Intercept mouse clicks on tabs """
        x, y = event.x, event.y
        try:
            clicked_tab = self.notebook.index(f"@{x},{y}")
        except tk.TclError:
            return
        tab_text = self.notebook.tab(clicked_tab, "text")

        if tab_text == "Toolbox (Beta)" and clicked_tab not in self.authenticated_tabs:
            pwd = self.ask_password()
            if pwd == self.password:
                self.authenticated_tabs.add(clicked_tab)
            else:
                messagebox.showerror("Access Denied", "Incorrect password!")
                return "break"  # Prevent tab switch

    def on_tab_changed(self, event):
        """ Intercept programmatic/tab-change events (keyboard navigation) """
        selected_tab = self.notebook.index(self.notebook.select())
        tab_text = self.notebook.tab(selected_tab, "text")

        if tab_text == "Toolbox (Beta)" and selected_tab not in self.authenticated_tabs:
            pwd = self.ask_password()
            if pwd == self.password:
                self.authenticated_tabs.add(selected_tab)
                self.last_allowed_tab = selected_tab
            else:
                messagebox.showerror("Access Denied", "Incorrect password!")
                self.notebook.select(self.last_allowed_tab)
        else:
            self.last_allowed_tab = selected_tab


if __name__ == "__main__":
    app = MainApplication()
