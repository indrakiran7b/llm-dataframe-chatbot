# LLM DataFrame Chatbot

A Streamlit-based chatbot that lets you analyze and visualize data in CSV/XLSX files using LLMs (via Ollama).  
Upload your dataset, ask questions in natural language, and get answers with tables, plots, or KPIs.

---

## 🚀 Features
- Chat with your dataset using natural language
- Supports CSV, XLSX, XLS files
- Data cleaning & normalization (e.g., revenue as float, discount as %)
- Auto-generated plots (line, bar, etc.)
- Powered by Ollama LLMs (e.g., gemma2:2b)
- Interactive Streamlit UI

---

## ⚙️ Setup Instructions

### 1. Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/llm-dataframe-chatbot.git
cd llm-dataframe-chatbot
```

### 2. Create a virtual environment
```bash
python -m venv .venv
# On Linux/Mac
source .venv/bin/activate
# On Windows
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install & run Ollama
Download Ollama 👉 [https://ollama.ai](https://ollama.ai)

#### Start the Ollama server
```bash
ollama serve
```

#### Pull the model you want (default: gemma2:2b)
```bash
ollama pull gemma2:2b
```

#### ▶️ Run the app
```bash
streamlit run src/main.py
```

Open your browser: [http://localhost:8501](http://localhost:8501)

---

## 💡 Example Queries
Once you upload a dataset, try:
- Total revenue for region = 'north'
- Top 5 products by total revenue
- Average qty per region
- Bar chart: total revenue by product
- Line chart: daily revenue trend

---

## 📂 Project Structure
```bash
llm-dataframe-chatbot/
├── src/                # Streamlit app code
│   └── main.py
├── requirements.txt    # Python dependencies
├── setup.py            # Packaging setup
└── README.md           # Project documentation
```

