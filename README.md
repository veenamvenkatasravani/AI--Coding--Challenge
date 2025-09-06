# 📧 AI-Powered Email Communication Assistant

An intelligent assistant that automatically retrieves support-related emails, categorizes them, prioritizes urgent ones, and generates context-aware responses using AI.
The project also includes a clean dashboard to display emails, insights, and analytics for faster customer support.

---

## 🚀 Features

* **Email Retrieval & Filtering**: Fetches emails (via IMAP/Gmail/Outlook APIs or sample dataset).
* **Categorization & Prioritization**:

  * Sentiment Analysis (Positive / Negative / Neutral).
  * Priority detection (Urgent / Not Urgent).
* **Context-Aware Auto-Responses**:

  * Uses LLMs (OpenAI / Hugging Face models) for draft replies.
  * Generates professional, empathetic, and contextual responses.
* **Information Extraction**:

  * Extracts phone numbers, alternate emails, and customer requirements.
* **Dashboard (Streamlit)**:

  * View filtered support emails.
  * Analytics & graphs (emails received, resolved, pending).
  * Preview & edit AI-generated replies.

---

## 🛠️ Tech Stack

* **Backend**: Python 3.10
* **Frontend**: Streamlit
* **AI/ML**: OpenAI GPT / Hugging Face (BERT, DistilBERT, T5)
* **Database**: SQLite / MongoDB (optional)
* **Visualization**: Plotly, Pandas
* **Email APIs**: IMAP, Gmail API, Outlook API

---

## 📂 Project Structure

```
AI-Email-Assistant/
│── app.py                 # Streamlit dashboard
│── email_fetcher.py       # Email fetching & filtering
│── processing.py          # Preprocessing & categorization
│── rag.py                 # Retrieval-Augmented-Generation logic
│── response_gen.py        # AI-based response generator
│── knowledge_base.json    # Knowledge base for RAG
│── requirements.txt       # Dependencies
│── .env.example           # Environment variables template
│── sample_emails.csv      # Sample dataset for testing
└── output/
    └── dashboard_screenshot.png  # Example output
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Email-Assistant.git
cd AI-Email-Assistant
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate   # On Mac/Linux
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Environment Variables

Create a `.env` file from `.env.example` and add:

```
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_password_or_app_password
OPENAI_API_KEY=your_openai_key
```

### 5️⃣ Run the Dashboard

```bash
python -m streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📊 Sample Output

### Dashboard Screenshot

https://github.com/veenamvenkatasravani/AI--Coding--Challenge/blob/main/output1.png?raw=true
https://github.com/veenamvenkatasravani/AI--Coding--Challenge/blob/main/output2.png?raw=true

---

## 📌 Future Improvements

* Multi-language support.
* Integration with CRM tools (Zendesk, Freshdesk).
* Automated sending of approved responses.
* Enhanced analytics dashboard with more visualizations.

---

## 👨‍💻 Author

Developed by **\[Veenam Venkata Sravani]** 🚀
Feel free to connect and contribute!
