""" Module providing generic functions for opening links in browsers or PDF reader """

import webbrowser
import os
import subprocess
import sys


def open_link_in_browser(url) -> None:
    """ Open link in Chrome or default browser """
    chrome_path = None

    if sys.platform.startswith('win'):
        possible_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                chrome_path = path
                break

    if chrome_path:
        try:
            subprocess.Popen([chrome_path, url]) # pylint: disable=consider-using-with
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"Failed to open Chrome: {e}")
    else:
        print("Chrome executable not found, using default browser")
        try:
            # new=2 opens in a new tab, if possible. By default autoraise == True
            webbrowser.open(url, new=2) 
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"Failed to open browser: {e}")


def open_pdf(relative_path) -> None:
    """ Open PDF """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(base_dir, relative_path)

    if not os.path.exists(pdf_path):
        print("PDF not found:", pdf_path)
        return

    os.startfile(pdf_path)
