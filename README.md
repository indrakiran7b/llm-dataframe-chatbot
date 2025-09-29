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
2. Create a virtual environment
bash
Copy code
python -m venv .venv
# On Linux/Mac
source .venv/bin/activate
# On Windows
.venv\Scripts\activate
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
4. Install & run Ollama
Download Ollama: 👉 https://ollama.ai

Start the Ollama server:

bash
Copy code
ollama serve
Pull the model you want (default: gemma2:2b):

bash
Copy code
ollama pull gemma2:2b
▶️ Run the app
Launch Streamlit:

bash
Copy code
streamlit run src/main.py
Open your browser: http://localhost:8501

💡 Example Queries
Once you upload a dataset, try:

Total revenue for region = 'north'

Top 5 products by total revenue

Average qty per region

Bar chart of total revenue by product

Line chart: daily revenue trend

📂 Project Structure
bash
Copy code
llm-dataframe-chatbot/
│── src/                 # Streamlit app code
│   └── main.py
│── requirements.txt     # Python dependencies
│── setup.py             # Packaging setup
│── README.md            # Project documentation
