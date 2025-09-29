# DataChat 💬

An interactive **Streamlit + LLM powered DataFrame chatbot**.  
Upload a CSV/Excel file and chat with your data — ask questions, request summaries, or generate charts (line plots, bar charts, etc.) using natural language.

---

## 🚀 Features
- Upload `.csv`, `.xlsx`, or `.xls` files
- Automatic data cleaning:
  - Drops duplicate/unnamed columns
  - Normalizes column names
  - Parses dates and numeric values
- LLM-powered Q&A using [Ollama](https://ollama.ai)
- Inline execution of Python code blocks returned by the LLM
- Supports Matplotlib visualizations directly inside Streamlit
- Example prompts in the sidebar for quick testing

---

## 🛠️ Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/YOUR_USERNAME/datachat.git
cd datachat
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt


▶️ Usage

Make sure Ollama
 is installed and running.
Example (serve gemma2:2b):

ollama serve
ollama pull gemma2:2b


Run the app:

streamlit run src/main.py


Open your browser at http://localhost:8501
.

📊 Example Queries

"Total revenue for region = 'north'"

"Top 5 products by total revenue"

"Bar chart of total revenue by product"

"Line chart: daily revenue trend"

🧩 Project Structure
datachat/
│── src/                 # Streamlit app code
│── requirements.txt     # Python dependencies
│── setup.py             # Packaging setup
│── README.md            # Project documentation
