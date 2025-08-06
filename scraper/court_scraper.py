# court_scraper.py (final updated with SQLite logging)
import requests
from bs4 import BeautifulSoup
import re

# Map court complex to known est_code
COURT_COMPLEX_TO_EST_CODE = {
    "Court of Judicial Magistrate of First Class, Kurupam (Taluka)": "APVZ0C",
    "Court of Junior Civil Judge,, Cheepurupalli (Taluka)": "APVZ0C",
    "Court of Senior Civil Judge,, Bobbili (Taluka)": "APVZ0C",
    "Court of Junior Civil Judge,, Srungavarapukota (Taluka)": "APVZ0C",
    "Court of Junior Civil Judge,, GajapathiNagaram (Taluka)": "APVZ0C",
    "Court of Junior Civil Judge,, Kothavalasa (Taluka)": "APVZ0C",
    "Court of Junior Civil Judge,, Salur (Taluka)": "APVZ0C",
    "II Additional District Court,PVP": "APVZ0C",
    "PDJ Court VIZIANAGARAM": "APVZ0C",
}

def extract_by_exact_header(soup, label_text):
    rows = soup.select("table tr")
    for row in rows:
        headers = row.find_all("th")
        values = row.find_all("td")
        if len(headers) == len(values) and headers:
            for h, v in zip(headers, values):
                if h.get_text(strip=True) == label_text:
                    return v.get_text(strip=True)
    return "Not found"

def get_dynamic_tokens():
    url = "https://vizianagaram.dcourts.gov.in/case-status-search-by-case-number/"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        raise Exception("Failed to load court search page")

    soup = BeautifulSoup(resp.text, "html.parser")

    # Extract scid and captcha id from captcha image URL
    img = soup.find("img", {"src": re.compile("_siwp_captcha")})
    captcha_src = img["src"] if img else ""

    match = re.search(r"id=([a-z0-9]+)", captcha_src)
    scid = match.group(1) if match else ""

    return scid, captcha_src

def fetch_case_details(case_number, filing_year, captcha_value, court_complex):
    from .logger import log_query
    scid, _ = get_dynamic_tokens()

    url = "https://vizianagaram.dcourts.gov.in/wp-admin/admin-ajax.php"
    est_code = COURT_COMPLEX_TO_EST_CODE.get(court_complex, "APVZ0C")

    payload = {
        "service_type": "courtComplex",
        "est_code": est_code,
        "reg_no": case_number,
        "reg_year": filing_year,
        "scid": scid,
        "tok_183dc76e3fd2dfcc59fdb8edeb907a653e71c237": "2a2b9f6c4c0f4b8c2fdceb26e8941faf2f4866cd",
        "siwp_captcha_value": captcha_value,
        "es_ajax_request": "1",
        "submit": "Search",
        "action": "get_cases"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://vizianagaram.dcourts.gov.in/case-status-search-by-case-number/"
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        try:
            result = response.json()
            html = result.get("data", "")
            if "siwp_captcha" in html or "captcha" in html.lower():
                return {"error": "❌ Incorrect CAPTCHA. Please try again."}
            if "No records found" in html:
                return {"error": "❌ No records found for the given case number."}

            # Log to SQLite
            log_query(case_number, filing_year, court_complex, html)

            soup = BeautifulSoup(html, "html.parser")
            rows = soup.select("table tr")[1:]

            case_list = []
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 3:
                    case_no = cols[1].text.strip()
                    parties = cols[2].get_text(separator=" ").strip()
                    data_cno_tag = row.find("a", class_="viewCnrDetails")
                    case_id = data_cno_tag["data-cno"] if data_cno_tag else "N/A"

                    case_list.append({
                        "case_number": case_no,
                        "parties": parties,
                        "case_id": case_id
                    })

            return {"success": True, "cases": case_list}

        except Exception as e:
            return {"error": f"Failed to parse response: {str(e)}"}
    else:
        return {"error": f"Request failed with status {response.status_code}"}

def fetch_case_metadata(case_id):
    url = "https://vizianagaram.dcourts.gov.in/wp-admin/admin-ajax.php"
    payload = {
        "action": "get_cnr_details",
        "cino": case_id,
        "es_ajax_request": "1"
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://vizianagaram.dcourts.gov.in/case-status-search-by-case-number/"
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json().get("data", "")
            soup = BeautifulSoup(data, "html.parser")

            filing_date = extract_by_exact_header(soup, "Filing Date")
            hearing_date = extract_by_exact_header(soup, "First Hearing Date")
            case_status = extract_by_exact_header(soup, "Case Status")

            pdf_tag = soup.find("a", href=True, text=lambda x: x and "Order" in x)
            
            if pdf_tag:
                pdf_url = pdf_tag["href"]
                try:
                    pdf_check = requests.get(pdf_url, timeout=5)
                    if "orders is not uploaded" in pdf_check.text.lower():
                        pdf_link = "No PDF available"
                    else:
                        pdf_link = pdf_url
                except:
                    pdf_link = "No PDF available"
            else:
                pdf_link = "No PDF available"


            status_label = "Active" if case_status.lower() not in ["case disposed", "disposed"] else "Disposed"
            next_hearing = hearing_date if status_label == "Active" else "No upcoming hearing"

            return {
                "filing_date": filing_date,
                "next_hearing_date": next_hearing,
                "case_status": status_label,
                "pdf_link": pdf_link
            }

        except Exception as e:
            return {"error": f"Failed to parse metadata: {str(e)}"}
    else:
        return {"error": "⚠️ The court website is currently unavailable. Please try again later."}
