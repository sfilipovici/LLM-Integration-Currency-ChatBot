# 💱 Currency-Math-LLM

An intelligent terminal-based currency conversion assistant powered by **OpenAI GPT** and the **Frankfurter API** for live exchange rates.

This mini project demonstrates how to:
- Use OpenAI GPT (GPT-4o or GPT-4.1) with **function/tool calling**
- Fetch **real-time currency exchange data** from an external API
- Build a natural conversation loop using **Python**
- Log responses for tracking and debugging

---

## 🚀 Features

- 🔁 Conversational terminal chatbot
- 🧠 GPT automatically calls a Python function when needed
- 🌐 Real-time conversion using `https://api.frankfurter.app`
- 🧾 Logging of all conversations to `response_log.json`
- ❌ No API key required for exchange rates

---

## 📸 Demo
<img width="1457" height="231" alt="Screenshot 2025-08-14 135123" src="https://github.com/user-attachments/assets/f55f4863-bb6b-4bc7-ab78-e5e33662cdc9" />


---

## 🧠 How It Works

- The user types a question like:  
  _"How much is 100 USD in EUR?"_
- GPT detects that a **currency conversion** is needed.
- GPT calls a function:  
  `convert_currency(amount, from_currency, to_currency)`
- The function uses the **Frankfurter API** to get a live rate.
- The result is passed back to GPT.
- GPT returns a natural language reply using the tool output.

---

## 📁 Project Structure

Currency-Math-LLM/

|- currencyMath.py # Main chatbot logic

|- response_monitor.py # Logs GPT responses

|- .env # OpenAI API key (not committed)

|_ response_log.json # Auto-generated log file



---

## 🔧 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/Currency-Math-LLM.git
cd Currency-Math-LLM
```

### 2. Create Virtual Environment 
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Dependencies
```bash
pip install openai python-dotenv requests
```

### 4. Create .env File
```bash
OPENAI_API_KEY=sk-your-openai-key
```

### ▶️ Run the Assistant
```bash
python currencyMath.py
```

___________________________

### 📈 Response Logging
```bash
response_log.json
```

#### Each entry includes:

1. Timestamp

2. Input prompt

3. Output from GPT

4. Model used

5. Token usage

___________________________

## 🧪 Example Queries
#### Convert 100 USD to GBP

#### How much is 12000 RON in EUR?

#### Please convert 300 CHF to CAD

_____________________________

### 📦 API Used

#### 💱 Frankfurter API (No key required)
#### 🤖 OpenAI API
