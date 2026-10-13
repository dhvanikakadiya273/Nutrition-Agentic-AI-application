# 🥗 Nutrition Agentic AI Application

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![IBM WatsonX](https://img.shields.io/badge/IBM-WatsonX%20AI-0f62fe?logo=ibm)
![LangChain](https://img.shields.io/badge/LangChain-1.x-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.65-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-yellow)

An intelligent, conversational **Nutrition AI Agent** built with **IBM Bob** and **IBM WatsonX AI** that delivers personalised dietary advice, real-time nutritional information, AI-generated meal plans, calorie tracking, and evidence-based health recommendations.

> **Repository:** [github.com/dhvanikakadiya273/Nutrition-Agentic-AI-application](https://github.com/dhvanikakadiya273/Nutrition-Agentic-AI-application)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Sample Queries](#sample-queries)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**Nutrition Agentic AI Application** is a full-stack agentic AI solution powered by **IBM WatsonX** large language models (accessed via IBM Bob). It combines a multi-tool agent framework with a Streamlit web interface to provide an interactive, context-aware nutrition assistant.

The agent autonomously selects the right tool — food lookup, meal planner, calorie calculator, or diet advisor — based on the user's natural language query, returning structured, evidence-based answers in seconds.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Food Nutrition Lookup** | Detailed macro & micronutrient info for any food item |
| 🍽️ **AI Meal Planner** | Personalised weekly meal plans for 6 diet types |
| 🏋️ **Calorie Calculator** | Daily caloric needs via BMR / TDEE (Mifflin-St Jeor) |
| 💬 **Conversational AI** | Multi-turn dialogue with memory, powered by WatsonX LLM |
| 📊 **Diet Analysis** | Analyse meals and receive evidence-based suggestions |
| 🌿 **Dietary Support** | Vegan, vegetarian, gluten-free, diabetic, and keto diets |
| 🔒 **Secure Config** | Credentials stored in `.env`, never committed to git |

---

## 🏗️ Architecture

```
Nutrition-Agentic-AI-application/
│
├── agent.py                  # IBM Bob agentic loop — tool routing & LLM calls
├── app.py                    # Streamlit web UI (entry point)
├── requirements.txt          # Python package dependencies
├── .env.example              # Environment variable template (safe to commit)
├── .gitignore                # Git exclusions
├── README.md                 # This file
│
├── tools/                    # Individual agent tool modules
│   ├── __init__.py
│   ├── nutrition_lookup.py   # Food & nutrient search (built-in DB + USDA API)
│   ├── meal_planner.py       # Weekly meal plan generator (6 diet types)
│   └── calorie_calculator.py # BMR / TDEE calculator (Mifflin-St Jeor)
│
├── prompts/                  # System prompts
│   └── system_prompt.txt     # Agent persona and instruction template
│
└── config/                   # YAML configuration
    └── config.yaml           # Model ID, temperature, max tokens, tool settings
```

**Data Flow:**

```
User (Browser)
    ↓  HTTP
Streamlit UI  (app.py)
    ↓  Python call
IBM Bob Agent Core  (agent.py)
    ↓  ReAct tool-selection loop
Tool Modules  (tools/)
    ↓  LLM inference
IBM WatsonX AI  (Granite / LLaMA models)
    ↑  Structured response
User
```

---

## ✅ Prerequisites

| Requirement | Version / Notes |
|-------------|-----------------|
| Python | 3.9 or higher |
| pip | 23+ |
| Git | 2.x |
| IBM Cloud Account | [Sign up free](https://cloud.ibm.com/registration) |
| WatsonX API Key | [IBM Cloud IAM](https://cloud.ibm.com/iam/apikeys) |
| WatsonX Project ID | [WatsonX.ai](https://dataplatform.cloud.ibm.com) |

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/dhvanikakadiya273/Nutrition-Agentic-AI-application.git
cd Nutrition-Agentic-AI-application
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### 1. Copy the environment template

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

### 2. Edit `.env` with your IBM WatsonX credentials

```env
WATSONX_API_KEY=your_ibm_watsonx_api_key_here
WATSONX_PROJECT_ID=your_watsonx_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-13b-chat-v2
```

**Where to get your credentials:**

- **API Key** → [cloud.ibm.com/iam/apikeys](https://cloud.ibm.com/iam/apikeys) → click **Create**
- **Project ID** → [dataplatform.cloud.ibm.com](https://dataplatform.cloud.ibm.com) → open your WatsonX project → copy the Project ID
- **Region URL** → `https://us-south.ml.cloud.ibm.com` (Dallas) · `https://eu-de.ml.cloud.ibm.com` (Frankfurt)

> ⚠️ **Security:** `.env` is excluded by `.gitignore` and will **never** be committed to GitHub. Only `.env.example` (with placeholder values) is tracked.

---

## ▶️ Usage

### Run the Web Application

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### Run the Agent via CLI

```bash
python agent.py
```

### Run the Smoke Test (no API key needed)

```bash
python test_tools.py
```

---

## 📝 Sample Queries

Try asking the agent any of these:

```
"What are the macros in 100g of chicken breast?"
"Plan a 1800 calorie vegetarian diet for one week."
"I'm diabetic — what should I eat for breakfast?"
"How many calories do I need? I'm 70kg, 175cm, moderately active."
"Suggest a keto meal plan for weight loss."
"What vegan foods are high in iron?"
"Is brown rice healthier than white rice?"
"Give me a gluten-free dinner recipe under 500 calories."
```

---

## 📁 Project Structure

| File / Folder | Description |
|---------------|-------------|
| `agent.py` | IBM Bob agent — registers tools, system prompt, and WatsonX LLM |
| `app.py` | Streamlit UI — conversational chat interface |
| `tools/nutrition_lookup.py` | Tool: food nutrition data (built-in DB + optional USDA API) |
| `tools/meal_planner.py` | Tool: personalised meal plans (6 diet types, up to 7 days) |
| `tools/calorie_calculator.py` | Tool: BMR, TDEE, and caloric goal recommendations |
| `prompts/system_prompt.txt` | Agent persona and instruction template |
| `config/config.yaml` | Model ID, generation params, tool enable/disable flags |
| `.env.example` | Safe-to-commit credential template |
| `requirements.txt` | All Python dependencies |
| `test_tools.py` | Smoke test — runs all tools without WatsonX credentials |

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM Platform | IBM WatsonX AI (Granite / LLaMA) |
| Agent Framework | LangChain Classic (ReAct agent) |
| Web Interface | Streamlit 1.65 |
| Language | Python 3.9+ |
| Config | python-dotenv, PyYAML |
| Data | Pandas, NumPy |

---

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: describe your change"`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a **Pull Request** against `main`

Please follow the existing code style and add tests for any new tool modules.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

> Built with ❤️ using [IBM Bob](https://www.ibm.com/products/watsonx-ai) and IBM WatsonX AI.
