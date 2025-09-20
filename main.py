import tkinter as tk
from var_data import term1_courses_dict
from helper import open_chrome, open_pdf


def create_btn(frame, text, url):
    if not url:
        return tk.Button(frame, text=text, state=tk.DISABLED)

    if url.startswith("https://"):
        return tk.Button(frame, text=text,
                         command=lambda: open_chrome(url))
    elif url.endswith(".pdf"):
        return tk.Button(frame, text=text, command=lambda: open_pdf(url))

    # Fallback for any other unexpected string
    return tk.Button(frame, text=text, state=tk.DISABLED)


def create_course_frame(window, course_name, course_info):
    frame = tk.Frame(master=window, bd=1, relief='solid')

    # Course name label
    info_label = tk.Label(
        master=frame, text=course_name + " " + course_info["course_code"])
    info_label.pack(pady=(10, 5))

    # Button row
    btn_frame = tk.Frame(master=frame)
    btn_frame.pack(anchor="w")

    outline_url_or_path = course_info["course_outline_url"] or course_info["course_outline_path"]
    course_outline_btn = create_btn(
        btn_frame, "Course outline", outline_url_or_path)
    course_outline_btn.pack(side=tk.LEFT, padx=15)

    learnhub_btn = create_btn(btn_frame, "Learning Hub",
                              course_info["learnhub_url"])
    learnhub_btn.pack(side=tk.LEFT, padx=10, pady=5)

    if course_name == "Networking":
        netacad_btn = create_btn(btn_frame, "Netacad",
                                 course_info["netacad_url"])
        netacad_btn.pack(side=tk.LEFT, padx=10, pady=5)

    if course_name == "Desktop":
        pcpro_btn = create_btn(btn_frame, "PC Pro", course_info["pcpro_url"])
        pcpro_btn.pack(side=tk.LEFT, padx=10, pady=5)

    if course_name == "Linux":
        redhat_btn = create_btn(btn_frame, "RedHat", course_info["redhat_url"])
        redhat_btn.pack(side=tk.LEFT, padx=10, pady=5)

    frame.pack(pady=15, fill="x")

    bottom_border_frame = tk.Frame(frame, height=1) # 2 pixels thick, black color
    bottom_border_frame.pack(fill="x") # Fill horizontally
    return frame


def main(window):
    courses_dict = term1_courses_dict

    frames = []
    for course_name, course_info in courses_dict.items():
        frame = create_course_frame(window, course_name, course_info)
        frames.append(frame)

    window.update_idletasks()


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Course Quick Access")
    window.minsize(500, 200)

    main(window)
    window.mainloop()
