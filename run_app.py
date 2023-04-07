import os
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open_new("http://localhost:8501")

if __name__ == '__main__':
    Timer(1, open_browser).start()
    os.system("streamlit run microbiology_app.py")
