
import webbrowser
import os
import subprocess
import sys


def open_chrome(url):
    chrome_path = None

    # Attempt to locate the Chrome executable (platform dependent)
    if sys.platform.startswith('win'):
        # Windows paths (you can modify/add more if needed)
        possible_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                chrome_path = path
                break
    elif sys.platform.startswith('darwin'):
        # macOS
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif sys.platform.startswith('linux'):
        # Linux (assuming Chrome is in PATH)
        chrome_path = "google-chrome"

    # Open the URL in Chrome
    if chrome_path:
        try:
            subprocess.Popen([chrome_path, url])
        except Exception as e:
            print(f"Failed to open Chrome: {e}")
    else:
        print("Chrome executable not found.")


def open_pdf(relative_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(base_dir, relative_path)

    if not os.path.exists(pdf_path):
        print("PDF not found:", pdf_path)
        return
    
    os.startfile(pdf_path)
