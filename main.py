import tkinter as tk
from var_data import term1_courses_dict
from helper import open_chrome, open_pdf


def create_btn(frame, text, url):
    btn = None
    if url.startswith("https://"):
        btn = tk.Button(master=frame, text=text,
                        command=lambda: open_chrome(url))
    elif url.endswith(".pdf"):
        btn = tk.Button(master=frame, text=text, command=lambda: open_pdf(url))

    return btn


def create_course_frame(course_name, course_info):
    frame = tk.Frame()
    info_label = tk.Label(
        master=frame, text=course_name + " " +  course_info["course_code"])

    if course_info["course_outline_url"]:
        course_outline_btn = create_btn(
            frame, "Course outline", course_info["course_outline_url"])
    else:
        course_outline_btn = create_btn(
            frame, "Course outline", course_info["course_outline_path"])
    learnhub_btn = create_btn(frame, "Learning Hub",
                              course_info["learnhub_url"])

    info_label.pack(side=tk.LEFT, pady=10)
    course_outline_btn.pack(side=tk.LEFT, padx=15)
    learnhub_btn.pack(side=tk.LEFT, padx=15)

    if course_name == "Networking":
        netacad_btn = create_btn(frame, "Netacad", course_info["netacad_url"])
        netacad_btn.pack(side=tk.LEFT)

    if course_name == "Desktop":
        pcpro_btn = create_btn(frame, "PC Pro", course_info["pcpro_url"])
        pcpro_btn.pack(side=tk.LEFT)

    if course_name == "Linux":
        redhat_btn = create_btn(frame, "RedHat", course_info["redhat_url"])
        redhat_btn.pack(side=tk.LEFT)

    frame.pack()
    return frame


def main(window):
    courses_dict = term1_courses_dict
    frames = []
    for course_name, course_info in courses_dict.items():
        frame = create_course_frame(course_name, course_info)
        frames.append(frame)

    if not frames:
        print("What happened?")
        exit()


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Course Quick Access")
    main(window)
    window.mainloop()

