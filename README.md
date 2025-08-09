🔬🩺 LabXtract AI
AI-Powered Medical Lab Report Analyzer

📌 Overview
LabXtract AI is an AI-powered tool that automatically reads, analyzes, and explains lab test reports in simple language. It highlights abnormal values, explains possible causes & risks using AI (Cohere LLM), and provides recommendations for better health.

✨ Features
✅ Extracts values from PDF medical lab reports
✅ Detects normal, low, and high results based on standard reference ranges
✅ Explains medical terms & health implications using Cohere AI
✅ Supports multiple lab test types (Blood, Liver, Kidney, Thyroid, Lipid, etc.)
✅ Option to download detailed AI-generated report in PDF
✅ Congratulates the user if all results are normal
✅ Clean, modern UI

🛠 Tech Stack
Python 🐍

Streamlit (Web App UI)

PyMuPDF (fitz) (PDF text extraction)

Pandas (Data handling)

Cohere AI API (LLM-based explanations)

📂 Project Structure
bash
Copy
Edit
LabXtract-AI/
│── analyzer.py        # Core logic for analyzing reports
│── app.py             # Streamlit web app
│── normal_ranges.csv  # Reference ranges for lab tests
│── requirements.txt   # Required Python packages
│── README.md          # Project documentation
🚀 How to Run Locally
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/ShaikhUmarFarooq/LabXtract-AI.git
cd LabXtract-AI
2️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Add Your Cohere API Key
Edit analyzer.py and replace:

python
Copy
Edit
COHERE_API_KEY = "your_api_key_here"
with your actual Cohere API key.

4️⃣ Run the App
bash
Copy
Edit
streamlit run app.py
📊 How It Works
Upload your PDF lab report

The app extracts test names & values

Matches them with normal ranges from CSV

Uses AI to explain abnormal values

Generates a detailed downloadable report

🖼 Sample Output
(![alt text](<Screenshot 2025-08-09 212629-1.jpg>))
![alt text](<Screenshot 2025-08-09 212543-1.jpg>)

📜 License
This project is licensed under the MIT License.

👨‍💻 Author
Shaikh Umar Farooq
💡 AI & Machine Learning Enthusiast
https://github.com/ShaikhUmarFarooq
https://www.linkedin.com/in/shaikh-umar-farooq-492a1831a/

⭐ Support
If you like this project, consider giving it a star ⭐ on GitHub!