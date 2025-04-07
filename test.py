from bias_check import detect_gender_bias, correct_gender_bias, generate_bias_report

# Input CSV
file_path = 'sample.csv'

# Step 1: Detect gender bias
bias_result = detect_gender_bias(file_path)
print(bias_result)

# Step 2: Correct gender bias and save
corrected_df = correct_gender_bias(file_path, 'corrected_sample.csv')
print("Bias correction completed. See corrected_sample.csv")

# Step 3: Generate bias comparison report
generate_bias_report(file_path, 'corrected_sample.csv')
print("Bias report generated in bias_report.txt")

