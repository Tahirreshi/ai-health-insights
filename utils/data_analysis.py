import pandas as pd
import numpy as np

def analyze_health_data(df):
    try:
        summary = df.describe(include='all').to_html(classes='table table-striped')
        missing = df.isnull().sum()
        missing_report = "<br>".join([f"{col}: {count} missing" for col, count in missing.items() if count > 0])

        return f"""
        <h4>🔍 Summary Statistics:</h4>
        {summary}
        <h4>⚠️ Missing Values:</h4>
        {missing_report if missing_report else 'None'}
        """
    except Exception as e:
        return f"Error analyzing data: {str(e)}"
def analyze_text(text):
    lines = text.splitlines()
    result = []

    name = ""
    for line in lines:
        if "name" in line.lower():
            name = line.strip()
            break
        elif not any(char.isdigit() for char in line) and len(line.strip()) > 2:
            name = line.strip()
            break

    abnormal_keywords = ["high", "low", "above", "below", "abnormal"]
    abnormal_findings = []
    for line in lines:
        if any(keyword in line.lower() for keyword in abnormal_keywords):
            abnormal_findings.append(line.strip())

    summary = ""
    if name:
        summary += f"<strong>Patient Name:</strong> {name}<br><br>"

    if abnormal_findings:
        summary += "<strong>Abnormal Findings:</strong><br>"
        for finding in abnormal_findings:
            summary += f"• {finding}<br>"
    else:
        summary += "No abnormal values detected."

    return summary
