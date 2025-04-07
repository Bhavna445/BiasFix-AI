# BiasFix-AI
# Developed by Bhavna Choudhary
# A tool to detect and correct gender bias in datasets

from flask import Flask, render_template, request, send_from_directory
import os
import pandas as pd
from gender_bias import (
    detect_gender_bias,
    correct_gender_bias,
    generate_bias_chart,
    generate_bias_report,
)
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"csv"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route("/")
def upload_file():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return "No file part"
    file = request.files["file"]
    if file.filename == "":
        return "No selected file"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        df = pd.read_csv(filepath)

        corrected_df, bias_result = correct_gender_bias(df)

        # Save corrected file
        corrected_filename = "corrected_" + filename
        corrected_path = os.path.join(app.config["UPLOAD_FOLDER"], corrected_filename)
        corrected_df.to_csv(corrected_path, index=False)

        # Generate and save chart
        chart_path = generate_bias_chart(df, corrected_df)

        # Generate and save bias report
        report = generate_bias_report(df, corrected_df)
        report_path = os.path.join("bias_report.txt")
        with open(report_path, "w") as f:
            f.write(report)

        # Read bias report to display in HTML
        with open(report_path, "r") as f:
            bias_report_text = f.read()

        # Preview table (first 5 rows)
        table_html = df.head().to_html(classes="table table-bordered", index=False)

        return render_template(
            "result.html",
            bias_result=bias_result,
            chart_path=chart_path,
            table_html=table_html,
            corrected_filename=corrected_filename,
            bias_report_text=bias_report_text
        )

    return "Invalid file format"

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.run(debug=True)

