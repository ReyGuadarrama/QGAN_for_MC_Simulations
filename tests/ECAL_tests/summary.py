import json
import os

def read_json_files(directory):
    results = []
    # Read all files in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                results.append(data)
    return results

def format_scientific(value, key):
    # Define which keys should be formatted in scientific notation
    scientific_keys = {'FID', 'RMSE', 'disc_loss', 'gen_loss'}
    if key in scientific_keys:
        return f"{value:.3e}"  # Format as scientific notation with 3 decimal places
    return value

def generate_markdown_table(data):
    # Table headers
    headers = data[0].keys()
    markdown = "| " + " | ".join(headers) + " |\n"
    markdown += "|---" * len(headers) + "|\n"

    # Add data rows
    for entry in data:
        row = "| " + " | ".join(str(format_scientific(value, key)) for key, value in entry.items()) + " |"
        markdown += row + "\n"

    return markdown

def save_to_readme(markdown, introduction, filename="/home/reyguadarrama/GSoC/tests/ECAL_tests/README.md"):
    with open(filename, 'w') as file:
        file.write(introduction + "\n\n" + markdown)

# Use the defined functions to read, generate, and save the data
directory = "/home/reyguadarrama/GSoC/tests/ECAL_tests/log"
introduction_text = """
# **Summary of ECAL Channel Test Results**
---

This README file includes a summary of test results for the various parameters explored in our experiments.
Each entry in the table represents a specific configuration and its outcomes.
"""

data = read_json_files(directory)
markdown_table = generate_markdown_table(data)
save_to_readme(markdown_table, introduction_text)

print("The README.md has been updated with the results table.")
