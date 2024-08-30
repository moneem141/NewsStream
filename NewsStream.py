import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required_packages = ["requests", "beautifulsoup4", "tkinter"]

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install(package)

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tkinter as tk
from tkinter import ttk
import webbrowser

# URLs
urls = {
    "The Business Standard": "https://www.tbsnews.net/bangla/",
    "The Daily Star": "https://bangla.thedailystar.net/",
    "BBC Bangla": "https://www.bbc.com/bengali",
    "Naya Diganta": "https://www.dailynayadiganta.com/"
}

# Defining tag selectors for each site
selectors = {
    "The Business Standard": ['h2', 'h3'],
    "The Daily Star": ['h3', 'h4'],
    "BBC Bangla": ['h3'],
    "Naya Diganta": ['h2']
}

def fetch_headlines(url, tags):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')

        headlines = soup.find_all(tags)
        results = []
        for headline in headlines[:5]:  # Limiting to top 5 headlines
            link = headline.find('a')
            if link:
                full_url = urljoin(url, link['href'])
                results.append((headline.get_text().strip(), full_url))
        return results

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def open_link(url):
    webbrowser.open_new(url)

def display_headlines():
    for widget in frame.winfo_children():
        widget.destroy()

    for site, url in urls.items():
        ttk.Label(frame, text=f"Headlines from {site}:", font=('Poppins', 14, 'bold')).pack(anchor='w', pady=5)
        headlines = fetch_headlines(url, selectors[site])
        for title, link in headlines:
            headline_label = ttk.Label(frame, text=title, font=('Poynter OS Display Nar SemiBold', 12), foreground='blue', cursor="hand2")
            headline_label.pack(anchor='w')
            headline_label.bind("<Button-1>", lambda e, url=link: open_link(url))

        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=10)

def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Tkinter setup
root = tk.Tk()
root.title("NewsStream")
root.geometry("600x400")

# Creating a scrollable frame
canvas = tk.Canvas(root)
frame = ttk.Frame(canvas)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0, 0), window=frame, anchor="nw")

frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Bind mouse wheel for scrolling

# Display the headlines on the GUI
display_headlines()

# Start the Tkinter main loop
root.mainloop()
