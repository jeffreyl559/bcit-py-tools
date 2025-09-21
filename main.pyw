import tkinter as tk
from tkinter import ttk
from data import term1_courses_dict
from helper import open_chrome, open_pdf


def create_btn(frame, text, url):
    if not url:
        return tk.Button(frame, text=text, state=tk.DISABLED)

    if url.startswith("https://"):
        return tk.Button(frame, text=text,
                         command=lambda: open_chrome(url))
    elif url.endswith(".pdf"):
        return tk.Button(frame, text=text, command=lambda: open_pdf(url))

    return tk.Button(frame, text=text, state=tk.DISABLED)


def create_popup_btn(window, frame, text, info):
    return tk.Button(frame, text=text, command=lambda: open_popup(window, info))


def open_popup(window, info):
    dialog = tk.Toplevel(window)
    center_window(dialog)
    dialog.title("Instructor Contact and Office Hours")
    dialog.transient(window)  # Make it modal relative to the root window
    dialog.grab_set()      # Grab focus and prevent interaction with other windows
    label = ttk.Label(
        dialog, text=f"Email: {info["email"]}\nOffice Hours: {info["office_hours"]}")
    label.pack(padx=15, pady=15)

    label2 = ttk.Label(
        dialog, text=f"All info is subject to change")
    label2.pack(pady=5)

    ok_button = ttk.Button(dialog, text="OK", command=dialog.destroy)
    ok_button.pack()

    window.wait_window(dialog)  # Wait until the dialog is closed


def create_course_frame(window, course_name, course_info):
    frame = tk.Frame(master=window, bd=1, relief='groove')

    info_label = tk.Label(
        master=frame, text=course_name + " " + course_info["course_code"], font=("Helvetica", 12, "bold"))
    info_label.pack(pady=(10, 5))

    btn_frame = tk.Frame(master=frame)
    btn_frame.pack(anchor="w")

    instructor_contact_btn = create_popup_btn(window, btn_frame, "Contact info", dict(
        name=course_info["instructor"], email=course_info["email"], office_hours=course_info["office_hours"]))

    instructor_contact_btn.pack(side=tk.LEFT, padx=15)

    outline_url_or_path = course_info["course_outline_url"] or course_info["course_outline_path"]
    course_outline_btn = create_btn(
        btn_frame, "Course outline", outline_url_or_path)
    course_outline_btn.pack(side=tk.LEFT, padx=15)

    learnhub_btn = create_btn(btn_frame, "Learning Hub",
                              course_info["learnhub_url"])
    learnhub_btn.pack(side=tk.LEFT, padx=10, pady=5)

    if course_info.get("alt_platform_name") and course_info.get("alt_platform_url"):
        alt_platform_btn = create_btn(
            btn_frame, course_info["alt_platform_name"], course_info["alt_platform_url"])
        alt_platform_btn.pack(side=tk.LEFT, padx=10, pady=5)

    frame.pack(pady=15, fill="x")
    return frame

# https://www.geeksforgeeks.org/python/how-to-center-a-window-on-the-screen-in-tkinter/
def center_window(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window.winfo_reqwidth()) // 2
    y = (screen_height - window.winfo_reqheight()) // 2
    window.geometry(f"+{x}+{y}")


def center_window_horizontally(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    dialog_width = window.winfo_width()
    x = (screen_width // 2) - (dialog_width // 2)
    y = int(screen_height * 0.15)
    window.geometry(f"+{x}+{y}")


def main(window):
    courses_dict = term1_courses_dict

    frames = []
    for course_name, course_info in courses_dict.items():
        frame = create_course_frame(window, course_name, course_info)
        frames.append(frame)

    window.update_idletasks()


if __name__ == "__main__":
    window = tk.Tk()
    window.title("CISA Toolbox")
    window.minsize(500, 200)
    center_window_horizontally(window)
    notebook = ttk.Notebook(window)

    course_tab = ttk.Frame(notebook)
    toolbox_tab = ttk.Frame(notebook)

    notebook.add(course_tab, text="Courses")
    notebook.add(toolbox_tab, text="Toolbox (Beta)")
    notebook.tab(toolbox_tab, state="disabled")
    notebook.pack(expand=1, fill="both")

    main(course_tab)
    window.mainloop()
