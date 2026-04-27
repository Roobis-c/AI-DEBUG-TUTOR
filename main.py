import os
import re
import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ------------------ SETUP ------------------
load_dotenv()

st.set_page_config(page_title="AI Code Debugger", layout="centered")
st.title("🧠 Conversational AI Code Debugger")

# ------------------ LLM ------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.3
)

parser = StrOutputParser()

# ------------------ SESSION MEMORY ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Convert chat history into text format
def get_history():
    return "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages]
    )

# ------------------ PROMPTS ------------------
classifier_prompt = ChatPromptTemplate.from_template("""
Classify the user input into:
1. DEBUG
2. APPROACH

Return only one word.

Input:
{input}
""")

debug_prompt = ChatPromptTemplate.from_template("""
Conversation so far:
{history}

You are an AI debugging assistant. Respond in medium-length (not too long or too short)
STRICT RULES:
- DO NOT provide corrected code
- DO NOT rewrite the code
- ONLY explain:
    1. What the error is
    2. Why it occurs
    3. How to fix it conceptually

User input:
{input}
""")

approach_prompt = ChatPromptTemplate.from_template("""
Conversation so far:
{history}

You are an algorithm mentor.Respond in medium-length (not too long or too short)

STRICT RULES:
- DO NOT write full code
- ONLY provide:
    - Approach
    - Step-by-step logic

Problem:
{input}
""")

# ------------------ CHAINS ------------------
classifier_chain = classifier_prompt | llm | parser
debug_chain = debug_prompt | llm | parser
approach_chain = approach_prompt | llm | parser

# ------------------ GUARDRAILS ------------------
def contains_code(text):
    patterns = [
        r"\bdef\b", r"\bclass\b", r"{.*}", r";",
        r"#include", r"console\.log"
    ]
    return any(re.search(p, text) for p in patterns)

def enforce_no_code(response, chain, user_input, history):
    if contains_code(response):
        stricter_input = user_input + "\n\nREMINDER: DO NOT provide code."
        return chain.invoke({
            "input": stricter_input,
            "history": history
        })
    return response

# ------------------ DISPLAY CHAT ------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ------------------ INPUT ------------------
user_input = st.chat_input("Describe your bug or problem...")

if user_input:

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    try:
        history = get_history()

        # Step 1: classify
        intent = classifier_chain.invoke({
            "input": user_input
        }).strip().upper()

        # Step 2: route
        if intent == "DEBUG":
            response = debug_chain.invoke({
                "input": user_input,
                "history": history
            })
            response = enforce_no_code(response, debug_chain, user_input, history)

        else:
            response = approach_chain.invoke({
                "input": user_input,
                "history": history
            })
            response = enforce_no_code(response, approach_chain, user_input, history)

        # Store assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        with st.chat_message("assistant"):
            st.write(response)

    except Exception as e:
        st.error(f"Error: {str(e)}")