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
