import pytesseract
from PIL import Image
import re

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, config='--psm 6') 
    return text

def parse_structured_medical_report(text):
    flagged = []
    lines = text.split('\n')

    for line in lines:
        line = line.strip()

        match = re.match(r'([A-Za-z\s]+)\s*(L|H)?\s*(\d+\.?\d*)\s*[%a-zA-Z/]*\s*(\d+\.?\d*)\s*-\s*(\d+\.?\d*)', line)
        if match:
            test_name = match.group(1).strip()
            flag = match.group(2) or ""
            value = float(match.group(3))
            ref_low = float(match.group(4))
            ref_high = float(match.group(5))

            result_flag = ""
            if value < ref_low:
                result_flag = "Low"
            elif value > ref_high:
                result_flag = "High"

            flagged.append({
                "Test": test_name,
                "Result": value,
                "Reference": f"{ref_low} - {ref_high}",
                "Flag": result_flag or flag or "Normal"
            })

    return flagged

def format_as_html_table(data):
    if not data:
        return "<p>No results to display.</p>"

    headers = data[0].keys()
    table = "<table class='table table-bordered'>"
    table += "<thead><tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr></thead><tbody>"

    for row in data:
        table += "<tr>" + "".join(f"<td>{row[h]}</td>" for h in headers) + "</tr>"

    table += "</tbody></table>"
    return table
