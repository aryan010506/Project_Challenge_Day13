"""
Project 13 — Basic Web Scraper (GUI)
Authors: Aryan Sunil & Swara Gharat
Dependencies: pip install requests beautifulsoup4
"""

import tkinter as tk
from tkinter import messagebox, ttk
import requests
from bs4 import BeautifulSoup

def scrape_website():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return
    
    try:
        result_box.delete(*result_box.get_children())
        status_label.config(text="Scraping...")
        root.update()

        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        page_title = soup.title.string if soup.title else "No Title Found"
        title_var.set(f"Page Title: {page_title}")

        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href')
            text = link.get_text(strip=True)
            result_box.insert("", "end", values=(text if text else "[No Text]", href))

        status_label.config(text=f"Found {len(links)} links")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to scrape website.\n\n{e}")
        status_label.config(text="")

# ---------- GUI ---------- #
root = tk.Tk()
root.title("Project 13 - Basic Web Scraper")
root.geometry("800x500")
root.config(bg="#111")

title = tk.Label(root, text="Basic Web Scraper", font=("Arial", 16, "bold"), bg="#111", fg="#1DB954")
title.pack(pady=10)

url_frame = tk.Frame(root, bg="#111")
url_frame.pack(pady=10)

url_label = tk.Label(url_frame, text="Enter URL:", font=("Arial", 12), bg="#111", fg="white")
url_label.grid(row=0, column=0, padx=5)

url_entry = tk.Entry(url_frame, width=50, font=("Arial", 12))
url_entry.grid(row=0, column=1, padx=5)

scrape_btn = tk.Button(root, text="Scrape Website", font=("Arial", 12, "bold"),
                       bg="#1DB954", fg="black", command=scrape_website, padx=20, pady=5)
scrape_btn.pack(pady=10)

title_var = tk.StringVar(value="Page Title: -")
title_label = tk.Label(root, textvariable=title_var, font=("Arial", 12, "bold"), bg="#111", fg="white")
title_label.pack(pady=5)

columns = ("Text", "Link")
result_box = ttk.Treeview(root, columns=columns, show="headings")
result_box.heading("Text", text="Link Text")
result_box.heading("Link", text="URL")
result_box.pack(fill="both", expand=True, padx=10, pady=10)

status_label = tk.Label(root, text="", font=("Arial", 10), bg="#111", fg="gray")
status_label.pack(side="bottom", pady=5)

footer = tk.Label(root, text="Day 13 of 30-Day Coding Challenge | Aryan Sunil & Swara Gharat",
                  font=("Arial", 9), bg="#111", fg="gray")
footer.pack(side="bottom", pady=2)

root.mainloop()
