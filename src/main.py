import pandas as pd
import streamlit as st
from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_ollama import ChatOllama


# Streamlit Web Configuration

st.set_page_config(
    page_title="DataChat",
    page_icon="💬",
    layout="centered"
)


# Read the data file
def read_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)
    

# Streamlit page title
st.title("🤖 DataFrame Chatbot")


# Initialize chat history in streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
# Initialize df in session state
if "df" not in st.session_state:
    st.session_state.df = None
    

# File upload widget
uploaded_file = st.file_uploader("Select a file...", type=["csv","xlsx","xls"])

if uploaded_file:
    st.session_state.df = read_data(uploaded_file)
    st.write("Dataframe Preview: ")
    st.dataframe(st.session_state.df.head())
    

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        

# Input field for user's message
user_prompt = st.chat_input("Ask LLM...")

if user_prompt:
    # Add user's message to chat history
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role":"user", "content": user_prompt})
    
    #loading the LLM
    llm = ChatOllama(model="gemma2:2b", temperature=0)
    
    pandas_df_agent = create_pandas_dataframe_agent(
        llm,
        st.session_state.df,
        verbose=True,
        agentType = AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code = True
    )
    
    message = [
        {"role":"system", "content": "You're a helpful assistant"},
        *st.session_state.chat_history
    ]
    
    try:
        response = pandas_df_agent.invoke(user_prompt)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        assistant_response = "I'm sorry, I couldn't process your request. Please try rephrasing or check your data."


    assistant_response = response["output"]

    st.session_state.chat_history.append({"role":"assistant", "content": assistant_response})

    ## Display LLM Response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)



#[
#    {"role":"user","content":user_prompt},
#   {"role":"assistant","content":user_prompt},
#   {"role":"user","content":user_prompt},
#]