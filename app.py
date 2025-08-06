from flask import Flask, render_template, request
from scraper.court_scraper import fetch_case_details, fetch_case_metadata, get_dynamic_tokens

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    case_list = []
    error = None

    # Get fresh CAPTCHA image URL every time page loads
    try:
        scid, captcha_url = get_dynamic_tokens()
    except Exception as e:
        captcha_url = None
        error = f"Failed to load CAPTCHA: {str(e)}"

    if request.method == "POST":
        try:
            court_complex = request.form["court_complex"]
            case_type = request.form.get("case_type", "")  # optional
            case_number = request.form["case_number"]
            filing_year = request.form["filing_year"]
            captcha = request.form["captcha"]

            result = fetch_case_details(case_number, filing_year, captcha, court_complex)

            if "error" in result:
                error = result["error"]
            elif result.get("success") and result.get("cases"):
                for case in result["cases"]:
                    case_id = case["case_id"]
                    metadata = fetch_case_metadata(case_id)
                    case.update(metadata)
                    case_list.append(case)
            else:
                error = "No records found for the given details."

        except Exception as e:
            error = f"Unexpected error: {str(e)}"

    return render_template("index.html", case_list=case_list, error=error, captcha_url=captcha_url)

if __name__ == "__main__":
    app.run(debug=True)
