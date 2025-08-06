# 🏛️ Court Data Fetcher & Mini-Dashboard

A mini dashboard built using **Flask**, **BeautifulSoup**, and **SQLite** to fetch Indian district court case details from the Vizianagaram District Court website.

---

## ⚖️ Court Chosen

- **District**: Vizianagaram, Andhra Pradesh
- **Public URL**: [https://vizianagaram.dcourts.gov.in/case-status-search-by-case-number/](https://vizianagaram.dcourts.gov.in/case-status-search-by-case-number/)

---

## 🚀 Features

- Search cases using:
  - Court Complex
  - Case Number
  - Filing Year
  - CAPTCHA
- Auto-scroll to results or error
- Download PDF if available
- CAPTCHA refresh button
- SQLite logs of each query

---

## 🛠️ Setup Steps

### 📦 Requirements
```bash
pip install -r requirements.txt

python app.py

http://127.0.0.1:5000/

 ###CAPTCHA Strategy
CAPTCHA image is dynamically scraped on each page load

A reload button allows users to fetch a fresh CAPTCHA

Manual input only (no automation or breaking ethical limits)

Sample Environment Variables
Not used — all credentials and tokens are fetched dynamically within the script.



🧾 Technologies Used
Python 3

Flask

BeautifulSoup

SQLite

Bootstrap (for frontend styling)
