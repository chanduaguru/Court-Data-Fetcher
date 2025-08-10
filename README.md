# ⚖️ Court-Data Fetcher & Mini-Dashboard

A Flask-based web app to fetch **Indian Court Case Details** from the Vizianagaram District Court official site, bypassing dynamic CAPTCHA and extracting details such as **case parties, filing date, hearing date, case status, and PDF orders**.  

This project is built as part of the Think Act Rise Foundation Internship **Task 1**.

---

## 🚀 Features

- 🎯 **Court Complex Dropdown** – Select from predefined court locations.
- 📅 **Filing Year Input/Dropdown** – Type manually or pick from last 30 years (optional).
- 🆔 **Case Number Search** – Fetch details instantly.
- 🔄 **Dynamic CAPTCHA** – Automatically fetched & refreshable with one click.
- 📂 **PDF Order Links** – Download latest available orders/judgments.
- 💾 **SQLite Logging** – Stores every query and raw HTML response for analysis.
- 📜 **Error Handling** – User-friendly messages for "No Records Found", incorrect inputs, or site downtime.
- ⬇️ **Auto-Scroll to Results** – Smoothly jumps to matched cases section.

---

## 🖼️ Screenshots

### 1️⃣ Home Page – Search Form
<img width="1837" height="860" alt="Screenshot 2025-08-06 180409" src="https://github.com/user-attachments/assets/37db04ad-b1d1-4161-b7c8-4e9b1e618365" />

### 2️⃣ Search Results – Case List
<img width="1208" height="2131" alt="127 0 0 1_5000_" src="https://github.com/user-attachments/assets/05f4bb24-b400-4c3c-95bc-16ac8c3a2f0f" />

### 3️⃣ PDF Order Download
<img width="1524" height="541" alt="Screenshot 2025-08-10 112000" src="https://github.com/user-attachments/assets/5bbbf09e-7966-4b96-a760-c8ed753b763d" />

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask  
- **Frontend:** HTML, Bootstrap 5, JavaScript  
- **Database:** SQLite  
- **Scraping:** BeautifulSoup4, Requests  

---

## 🧩 CAPTCHA Strategy

The official court site generates a **dynamic CAPTCHA image** with a unique `scid` token each time the page loads.  
Our approach:
1. Request the search page and parse the `scid` & CAPTCHA image URL.
2. Display the CAPTCHA dynamically in our form.
3. On search, send `scid` + user-entered CAPTCHA to the court's backend API.
4. Refresh button generates a fresh CAPTCHA without reloading the whole app.

---

## 📂 Project Structure
Court-Data-Dashboard/
│
├── app.py # Flask app entry
├── court_scraper.py # Scraping logic & CAPTCHA handling
├── logger.py # SQLite logging
├── templates/
│ └── index.html # Main UI template
├── static/
│ ├── favicon.ico # App favicon
│ └── screenshots/ # Place your screenshots here
├── queries.db # SQLite database
├── LICENSE # MIT License
└── README.md # This file
---
## ⚙️ Setup Instructions

### 
1️⃣ Clone the Repo
```bash
git clone https://github.com/yourusername/Court-Data-Fetcher.git
cd Court-Data-Fetcher
2️⃣ Create a Virtual Environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run the App
python app.py

Then open http://127.0.0.1:5000/ in your browser.

##🔑 Sample .env Variables
(Create a .env file in the project root for sensitive keys if needed)

ini
Copy
Edit
FLASK_ENV=development
SECRET_KEY=your_secret_key
---
```
##🤝 Acknowledgments
Vizianagaram District Court Website – Official source of data.

Think Act Rise Foundation – Internship project guidelines.

BeautifulSoup4 – For HTML parsing.

Bootstrap – For responsive UI.
---

## 📝 Disclaimer

This project was developed by **Aguru Chandu** as part of the Think Act Rise Foundation internship.  
Some assistance was taken from **AI-powered tools** such as ChatGPT for:
- Code structuring & debugging
- Documentation formatting
- UI/UX improvement suggestions

All final implementation, testing, and integration were done by me.
