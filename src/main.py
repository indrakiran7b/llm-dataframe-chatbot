import os
os.environ.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")  # silence email prompt

import io
import contextlib
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_ollama import ChatOllama

# -------------------- Streamlit config & styles --------------------
st.set_page_config(page_title="DataChat", page_icon="💬", layout="wide")
st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
.code-wrap pre {white-space: pre-wrap;}
.kpi {border-radius: 16px; padding: 14px 16px; box-shadow: 0 1px 6px rgba(0,0,0,.08);}
</style>
""", unsafe_allow_html=True)

st.title("🤖 DataFrame Chatbot")

# Matplotlib sane defaults
plt.rcParams["figure.figsize"] = (8, 4)
plt.rcParams["axes.grid"] = True

# -------------------- Helpers --------------------
def read_data(file):
    return pd.read_csv(file) if file.name.lower().endswith(".csv") else pd.read_excel(file)

def _maybe_parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Parse any column whose name contains 'date' and sort by 'date' if present."""
    df = df.copy()
    for c in df.columns:
        if "date" in c:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    if "date" in df.columns:
        df = df.sort_values("date")
    return df

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # 1) drop duplicate + unnamed
    df = df.loc[:, ~df.columns.duplicated()]
    df = df.loc[:, ~df.columns.astype(str).str.match(r"^unnamed", case=False, na=False)]
    # 2) normalize names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^0-9a-zA-Z_]", "", regex=True)
        .str.lower()
    )
    # 3) numeric coercions
    for c in df.columns:
        if any(k in c for k in ["revenue", "price", "amount", "sales", "cost"]):
            df[c] = (
                df[c].astype(str)
                .str.replace(r"[,\$₹]", "", regex=True)
                .replace({"": None, "nan": None})
            )
            df[c] = pd.to_numeric(df[c], errors="coerce")
        if "discount" in c or c.endswith("_pct") or c.endswith("_percent"):
            s = df[c].astype(str).str.strip().str.replace("%", "", regex=False)
            df[c] = pd.to_numeric(s, errors="coerce") / 100.0
        if c in {"qty", "quantity", "count", "units"}:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    # 4) dates
    df = _maybe_parse_dates(df)
    return df

def get_llm():
    base = os.getenv("OLLAMA_HOST")  # e.g., "127.0.0.1:11434" or "http://127.0.0.1:11500"
    kwargs = {"model": "gemma2:2b", "temperature": 0}
    if base and not base.startswith("http"):  # allow host:port
        base = f"http://{base}"
    if base:
        kwargs["base_url"] = base
    return ChatOllama(**kwargs)

def extract_python_block(text: str) -> str | None:
    """Return the first ```python ... ``` block if present."""
    if not text:
        return None
    fence = "```"
    if "```python" in text:
        start = text.find("```python") + len("```python")
        end = text.find(fence, start)
        return text[start:end].strip() if end != -1 else text[start:].strip()
    return None

def _sanitize_llm_code(code: str) -> str:
    """Remove import lines; pd/df/plt/st are already provided."""
    lines = []
    for ln in code.splitlines():
        s = ln.strip()
        if s.startswith("import ") or s.startswith("from "):
            continue
        lines.append(ln)
    sanitized = "\n".join(lines).strip()
    # ensure reasonable layout even if LLM forgets
    if "plt.tight_layout()" not in sanitized:
        sanitized += "\nplt.tight_layout()"
    return sanitized

def execute_python_snippet(code: str, df: pd.DataFrame):
    """
    Execute LLM-provided python safely enough for analytics:
    - Provides pd, df, plt, st
    - Captures stdout/stderr and shows them
    - Renders active Matplotlib figures
    - If variable `result` is set to a DataFrame or Series, it is displayed
    """
    sanitized = _sanitize_llm_code(code)

    safe_globals = {
        "__builtins__": {"len": len, "range": range, "min": min, "max": max, "sum": sum, "print": print},
        "pd": pd,
        "df": df,   # cleaned + date-parsed df
        "plt": plt,
        "st": st
    }
    safe_locals = {}

    st.subheader("📜 Executed code")
    st.code(sanitized, language="python")

    buf_out, buf_err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        try:
            exec(sanitized, safe_globals, safe_locals)
        except Exception as e:
            st.error(f"Code execution error: {e}")

    stdout, stderr = buf_out.getvalue().strip(), buf_err.getvalue().strip()
    if stdout:
        st.caption("stdout:")
        st.code(stdout)
    if stderr:
        st.caption("stderr:")
        st.code(stderr)

    # Show `result` if set
    if "result" in safe_locals:
        res = safe_locals["result"]
        if isinstance(res, (pd.DataFrame, pd.Series)):
            st.subheader("🧮 Result")
            st.dataframe(res)
        else:
            st.write(res)

    # Render any active figures
    figs = list(map(plt.figure, plt.get_fignums()))
    for fig in figs:
        st.pyplot(fig)
    plt.close('all')

# -------------------- Sidebar --------------------
with st.sidebar:
    st.header("⚙️ Options")
    example = st.selectbox(
        "Examples",
        [
            "—",
            "Total revenue for region='north'",
            "Top 5 product by total revenue",
            "Average qty per region",
            "Bar chart: total revenue by product",
            "Line chart: daily revenue trend",
        ],
        index=0
    )
    st.markdown("Set `OLLAMA_HOST` to a different host:port if not default (11434).")
    st.text_input("OLLAMA_HOST", value=os.getenv("OLLAMA_HOST") or "", key="OLLAMA_HOST_IN_UI")
    use_example = st.button("Use example")

# -------------------- Session state --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "df" not in st.session_state:
    st.session_state.df = None

# -------------------- File upload --------------------
c1, c2 = st.columns([2, 1])
with c1:
    uploaded_file = st.file_uploader("Select a file...", type=["csv", "xlsx", "xls"])
with c2:
    if st.session_state.df is not None:
        st.metric("Rows", f"{len(st.session_state.df):,}")
        st.metric("Columns", f"{len(st.session_state.df.columns)}")

if uploaded_file:
    raw = read_data(uploaded_file)
    st.write("Raw preview:")
    st.dataframe(raw.head())
    st.session_state.df = clean_df(raw)
    st.write("Cleaned preview (columns normalized & dates parsed):")
    st.dataframe(st.session_state.df.head())
    st.caption(f"Columns: {', '.join(st.session_state.df.columns)}")

# -------------------- History render --------------------
for m in st.session_state.chat_history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# -------------------- Chat input --------------------
placeholder_text = "Ask LLM for analysis or plots…"
user_prompt = st.chat_input(placeholder=placeholder_text, key="chat_input")

# If user clicked "Use example" and input was empty, prefill with example
if use_example and (not user_prompt) and example != "—":
    user_prompt = example

if user_prompt:
    # propagate OLLAMA_HOST from UI if set
    if st.session_state.get("OLLAMA_HOST_IN_UI"):
        os.environ["OLLAMA_HOST"] = st.session_state["OLLAMA_HOST_IN_UI"]

    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    if st.session_state.df is None:
        msg = "Please upload a CSV/XLSX first. The DataFrame agent needs data to answer."
        st.error(msg)
        st.session_state.chat_history.append({"role": "assistant", "content": msg})
    else:
        # Prime with exact column names and plotting guidance
        system_hint = (
            "You are a data analyst. Use these exact DataFrame columns: "
            + ", ".join(st.session_state.df.columns)
            + ". Prefer vectorized pandas. "
            "Do NOT include any import statements; `pd`, `df`, `plt`, `st` are already available. "
            "If a chart is requested, return a Python code block using matplotlib (plt) and the existing DataFrame `df`. "
            "When plotting by date, assume `df['date']` is already datetime and sorted. "
            "Set axis labels and a short title. If you produce a table, assign it to a variable named `result`."
        )

        llm = get_llm()
        agent = create_pandas_dataframe_agent(
            llm,
            st.session_state.df,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            allow_dangerous_code=True,
        )

        try:
            result = agent.invoke(system_hint + "\n\nUser question: " + user_prompt)
            text = (result.get("output") or "").strip()
        except Exception as e:
            text = f"LLM/agent error: {e}"

        # Show raw LLM answer
        with st.chat_message("assistant"):
            st.markdown(text, help="Raw LLM output")
        st.session_state.chat_history.append({"role": "assistant", "content": text})

        # If there is a python code block, sanitize & execute it and render outputs
        code = extract_python_block(text)
        if code:
            execute_python_snippet(code, st.session_state.df)
