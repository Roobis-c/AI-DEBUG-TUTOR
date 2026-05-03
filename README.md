# 🧠 Conversational AI Code Debugger

A smart, conversational AI-powered debugging assistant built using **Streamlit** and **LangChain**. This tool helps developers understand errors and solve problems without directly giving code solutions — encouraging deeper learning and problem-solving skills.

---

## 🚀 Features

* 💬 ChatGPT-like conversational UI using Streamlit
* 🧠 Context-aware responses with session memory
* 🔍 Intelligent intent classification:

  * **DEBUG** → Explains errors and fixes conceptually
  * **APPROACH** → Provides algorithmic thinking steps
* 🚫 Strict no-code policy (enforced via guardrails)
* ⚡ Powered by Gemini (Google Generative AI)

---

## 🏗️ Tech Stack

* Python
* Streamlit
* LangChain
* Google Generative AI (Gemini)
* dotenv

---

## 📂 Project Structure

```
project/
│── main.py
│── .env

```

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/ai-code-debugger.git
cd ai-code-debugger
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your API key in `.env`:

```
GOOGLE_API_KEY=your_api_key_here
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 🧩 How It Works

1. User inputs a problem or bug
2. AI classifies the intent (Debug / Approach)
3. Routes to the correct prompt chain
4. Uses chat history for context
5. Ensures no code is generated using guardrails

---

## 🎯 Use Cases

* Debugging errors conceptually
* Learning problem-solving approaches
* Interview preparation
* Practicing algorithms without copy-paste coding

---

## 📌 Future Improvements

* Code explanation mode
* Multi-language support
* Error log parsing
* Voice-based debugging assistant

---

## 🤝 Contributing

Feel free to fork, improve, and submit PRs!

---

