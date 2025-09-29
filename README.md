# 📊 DataChat — LLM DataFrame Chatbot

An interactive **Streamlit + Ollama + Pandas** powered chatbot for exploring CSV/Excel data.  
Upload your dataset, ask natural-language questions, and get instant **answers, tables, and charts**.

---

## ✨ Features
- Upload `.csv`, `.xlsx`, or `.xls` files
- Automatic data cleaning:
  - Drops duplicate/unnamed columns
  - Normalizes column names
  - Parses dates & numeric values
- Ask questions in plain English:
  - Aggregations (sum, avg, counts…)
  - Filtering, grouping, pivoting
  - Table summaries
- Built-in charting:
  - Line, bar, scatter, etc. via Matplotlib
- Example queries in the sidebar for quick testing
- Runs completely **locally** with [Ollama](https://ollama.ai)

---

## 🛠️ Setup

### 1. Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/llm-dataframe-chatbot.git
cd llm-dataframe-chatbot

## 2. Create a virtual environment
  python -m venv .venv
  # On Linux/Mac
  source .venv/bin/activate
  # On Windows
  .venv\Scripts\activate

## 3. Install dependencies
  pip install -r requirements.txt

## 4. Install & run Ollama
  Download Ollama 👉 https://ollama.ai
  ### Start the Ollama server:
    ollama serve
  ### Pull the model you want (default: gemma2:2b):
    ollama pull gemma2:2b
##▶️ Run the app
  ### Launch Streamlit:
    streamlit run src/main.py
Open your browser: http://localhost:8501



