import os
import pandas as pd
from flask import Flask, render_template, request

from utils.data_analysis import analyze_health_data
from utils.groq_ai import get_health_advice, get_groq_response
from utils.ocr_handler import extract_text_from_image, format_as_html_table, parse_structured_medical_report
from utils.symptom_checker import match_symptoms

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis_result = ""
    ai_response = ""
    error_message = ""
    flagged = []

    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = file.filename.lower()
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            try:
                if filename.endswith('.csv'):
                    df = pd.read_csv(filepath)

                    investigation_columns = [col for col in df.columns if 'investigation' in col.lower() or 'test' in col.lower()]
                    name_columns = [col for col in df.columns if 'name' in col.lower()]
                    filtered_columns = name_columns + investigation_columns

                    if filtered_columns:
                        display_df = df[filtered_columns]
                    else:
                        display_df = df  

                    analysis_result = display_df.to_html(classes='table table-striped', index=False)
                    ai_response = get_health_advice(df)

                elif filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    extracted_text = extract_text_from_image(filepath)
                    flagged_results = parse_structured_medical_report(extracted_text)

                    if flagged_results:
                        analysis_result = format_as_html_table(flagged_results)
                    else:
                        analysis_result = "<p>No analyzable medical results found.</p>"

                    ai_response = get_health_advice(extracted_text)

                else:
                    error_message = "Unsupported file format. Please upload a CSV or image."

            except Exception as e:
                error_message = f"An error occurred while processing your file: {str(e)}"

        else:
            error_message = "No file selected. Please choose a file to upload."

    return render_template('index.html', result=analysis_result, ai=ai_response, error=error_message, flagged=flagged)

@app.route("/symptom-check", methods=["GET", "POST"])
def symptom_check():
    analysis_result = ""
    error_message = ""
    flagged = []

    if request.method == "POST":
        symptoms = request.form.get("symptoms", "").strip()

        if symptoms == "":
            error_message = "Please enter your symptoms."
            return render_template("index.html", result=analysis_result, ai="", error=error_message, flagged=flagged)

        matches = match_symptoms(symptoms)

        if matches:
            possible_conditions = matches[0]["conditions"]
            prompt = f"The user is experiencing: {symptoms}. Based on this, possible conditions are: {', '.join(possible_conditions)}. Explain them in simple terms with treatment/prevention advice."
            ai_response = get_groq_response(prompt)
        else:
            ai_response = "Sorry, no conditions matched. Please describe your symptoms in common terms like 'fever, cough'."

        return render_template("index.html", result=analysis_result, ai=ai_response, error=error_message, flagged=flagged)

    return render_template("index.html", result=analysis_result, ai=ai_response, error=error_message, flagged=flagged, form_type="upload")


if __name__ == '__main__':
    app.run(debug=True)
