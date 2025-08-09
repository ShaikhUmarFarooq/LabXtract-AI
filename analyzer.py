import fitz  # PyMuPDF
import pandas as pd
import re
import requests
import cohere
import os

# Setup Cohere API
COHERE_API_KEY = os.getenv("COHERE_API_KEY") or "YOUR_COHERE_API_KEY"
co = cohere.Client(COHERE_API_KEY)

# Logging helper
def log(msg):
    with open("output/logs.txt", "a") as f:
        f.write(msg + "\n")


def load_tests(csv_path):
    df = pd.read_csv(csv_path)
    tests = []
    for _, row in df.iterrows():
        try:
            aliases = [alias.strip().lower() for alias in str(row["aliases"]).split("|")]
            tests.append({
                "Test Name": str(row["Test Name"]).strip(),
                "aliases": aliases,
                "gender": str(row.get("gender", "any")).strip().lower(),
                "min": float(row["min"]),
                "max": float(row["max"]),
                "unit": str(row["unit"]).strip()
            })
        except Exception as e:
            log(f"❌ Error loading row: {row} - {e}")
    return tests


def extract_pdf_text(uploaded_file):
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    except Exception as e:
        log(f"❌ Error reading PDF: {e}")
        return ""


def generate_explanation(test_name, value, unit, status):
    prompt = (
        f"The blood test '{test_name}' shows a value of {value} {unit}, which is considered {status}.\n"
        f"Explain in simple terms what this might mean for the patient. Include causes, health risks, and what actions can be taken to improve it."
    )
    try:
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=250,
            temperature=0.5
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"⚠️ Explanation not available (API error: {str(e)})"


def analyze_text(text, all_tests, user_gender):
    text_lines = text.lower().split("\n")
    results = []
    matched_tests = set()

    for line in text_lines:
        line = line.strip()
        if not line or len(line) < 3:
            continue

        # Skip irrelevant lines
        skip_keywords = [
            "interpretation", "description", "suggestion", "advice",
            "verified by", "comment", "reference range", "method", "sample",
            "report generated", "note", "checked by", "remarks"
        ]
        if any(keyword in line for keyword in skip_keywords):
            continue

        # Clean special characters
        clean_line = re.sub(r"[^\w\s.%/+-]", " ", line)

        for test in all_tests:
            if test["Test Name"] in matched_tests:
                continue

            if test["gender"] != "any" and test["gender"] != user_gender:
                continue

            for alias in test["aliases"]:
                pattern = r"\b" + re.escape(alias) + r"\b"
                match = re.search(pattern, clean_line)
                if match:
                    alias_end = match.end()
                    rest_line = clean_line[alias_end:].strip()

                    # Extract value after alias only
                    number_match = re.search(r"[-+]?\d*\.\d+|\d+", rest_line)
                    if number_match:
                        try:
                            value = float(number_match.group())

                            if test["min"] <= value <= test["max"]:
                                status = "Normal"
                                explanation = ""  # skip explanation if normal
                            elif value < test["min"]:
                                status = "Low"
                                explanation = generate_explanation(test["Test Name"], value, test["unit"], "Low")
                            else:
                                status = "High"
                                explanation = generate_explanation(test["Test Name"], value, test["unit"], "High")

                            results.append({
                                "Test Name": test["Test Name"],
                                "Value": value,
                                "Unit": test["unit"],
                                "Normal Range": f"{test['min']} - {test['max']}",
                                "Status": status,
                                "Explanation": explanation
                            })

                            matched_tests.add(test["Test Name"])
                            break  # Go to next line
                        except:
                            continue
    return results
