import pandas as pd
import matplotlib.pyplot as plt
import os

def detect_gender_bias(df):
    if 'gender' not in df.columns or 'job_role' not in df.columns:
        return "Required columns 'gender' and 'job_role' not found."

    bias_result = {}
    job_roles = df['job_role'].unique()

    for role in job_roles:
        role_df = df[df['job_role'] == role]
        male_count = len(role_df[role_df['gender'].str.lower() == 'male'])
        female_count = len(role_df[role_df['gender'].str.lower() == 'female'])

        if male_count > female_count:
            bias_result[role] = "Bias towards Males"
        elif female_count > male_count:
            bias_result[role] = "Bias towards Females"
        else:
            bias_result[role] = "No Bias"

    return bias_result

def correct_gender_bias(df):
    if 'gender' not in df.columns or 'job_role' not in df.columns:
        return df, "Required columns not found."

    corrected_df = df.copy()
    new_rows = []

    for role in corrected_df['job_role'].unique():
        role_df = corrected_df[corrected_df['job_role'] == role]
        male_df = role_df[role_df['gender'].str.lower() == 'male']
        female_df = role_df[role_df['gender'].str.lower() == 'female']

        diff = len(male_df) - len(female_df)

        if diff > 0:
            sampled = female_df.sample(diff, replace=True)
            new_rows.append(sampled)
        elif diff < 0:
            sampled = male_df.sample(-diff, replace=True)
            new_rows.append(sampled)

    if new_rows:
        corrected_df = pd.concat([corrected_df] + new_rows, ignore_index=True)

    return corrected_df, "Bias correction applied: balanced gender count in each job role."

def generate_bias_report(original_df, corrected_df):
    original_count = original_df['gender'].value_counts().to_dict()
    corrected_count = corrected_df['gender'].value_counts().to_dict()

    report = {
        "Original Gender Distribution": original_count,
        "Corrected Gender Distribution": corrected_count
    }

    return report

def generate_bias_chart(original_df, corrected_df):
    original_count = original_df['gender'].value_counts()
    corrected_count = corrected_df['gender'].value_counts()

    labels = list(set(original_count.index.tolist() + corrected_count.index.tolist()))
    original_vals = [original_count.get(label, 0) for label in labels]
    corrected_vals = [corrected_count.get(label, 0) for label in labels]

    x = range(len(labels))
    width = 0.35

    plt.figure(figsize=(8, 5))
    plt.bar(x, original_vals, width=width, label='Original')
    plt.bar([i + width for i in x], corrected_vals, width=width, label='Corrected')

    plt.xlabel('Gender')
    plt.ylabel('Count')
    plt.title('Gender Distribution Before and After Bias Correction')
    plt.xticks([i + width / 2 for i in x], labels)
    plt.legend()

    chart_path = os.path.join('static', 'bias_chart.png')
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    return chart_path

def generate_bias_report(bias_summary, correction_summary, filepath="bias_report.txt"):
    with open(filepath, "w") as report_file:
        report_file.write("Bias Analysis Report\n")
        report_file.write("=====================\n\n")
        report_file.write("Bias Status by Job Title:\n\n")
        for job, status in bias_summary.items():
            report_file.write(f" - {job}: {status}\n")

        report_file.write("\nBias Correction Summary:\n\n")
        for key, value in correction_summary.items():
            report_file.write(f"{key}: {value}\n")

    return filepath

