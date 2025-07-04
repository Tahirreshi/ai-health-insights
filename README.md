# 🏥 Smart Medical Report Analyzer & AI Health Advisor

A powerful Flask-based web application that helps users analyze their medical reports (CSV or image format) and receive personalized health advice using AI via the Groq API.


## 🚀 Features

- 📁 Upload CSV health data or image reports (like blood test screenshots).
- 🔍 OCR-powered extraction of medical data from images.
-  🩺 Check symptoms for possible health conditions  
- 📊 Automatic detection of key health indicators (e.g., cholesterol, hemoglobin).
- **Symptom Checker**  
  Enter symptoms (e.g. `fever, cough, headache`) and get a list of possible conditions using a built-in database.
- 🧠 Personalized AI-powered health suggestions using Groq API.
- 🧼 Clean and minimal web interface built with Flask.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Flask** – Web framework
- **Pandas & NumPy** – Data handling
- **Tesseract OCR (pytesseract)** – Extract text from medical report images
- **Groq API** – For AI-generated medical advice
- **dotenv** – For API key management
