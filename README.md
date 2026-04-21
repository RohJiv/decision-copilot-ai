# 🧩 AI Decision Copilot — Your Personal Business Strategist

An AI-powered decision support tool that analyses your business data, asks smart clarifying questions, runs what-if scenarios, and delivers confidence-scored recommendations with risk breakdown — built to help leaders make better decisions faster.

![Status](https://img.shields.io/badge/status-live-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![LangChain](https://img.shields.io/badge/framework-LangChain-yellow)

---

## 🎯 What It Does

Most decision-making tools show dashboards. This one thinks with you.

- Upload your business data (CSV or Excel)
- AI asks intelligent clarifying questions specific to your data
- Runs 3 what-if scenarios based on your context
- Delivers a recommended action with confidence score
- Identifies risks with severity levels and mitigations
- Tells you what NOT to do (equally important)
- Provides next steps and realistic timelines

---

## 💡 Why I Built This

Business leaders drown in data but struggle with decisions. Traditional BI tools answer "what happened" — they don't help you decide "what should I do next."

AI chatbots answer questions but don't run structured analysis. Decision Copilot bridges this gap — it's a thinking partner that uses your data to simulate outcomes before you commit.

This is the crown jewel of my 5-project portfolio — it combines everything: data analysis, scenario planning, risk assessment, and explainable recommendations.

---

## 🏗️ Architecture — 4-Step Guided Wizard

```
Step 1: DATA UPLOAD
├── Accept CSV or Excel
├── Auto-detect columns & types
└── Generate statistical summary
         ↓
Step 2: CLARIFYING QUESTIONS
├── AI generates 3 smart questions specific to data
├── User provides context
└── Feeds richer context to next step
         ↓
Step 3: SCENARIO ANALYSIS
├── Generate 3 what-if scenarios
├── Calculate impact scores (-100 to +100)
├── Assign risk levels (low/medium/high)
├── Estimate confidence (0-100%)
└── Visualise with interactive charts
         ↓
Step 4: FINAL RECOMMENDATION
├── AI Confidence gauge
├── Recommended action
├── Key insights & reasoning
├── Risks with mitigations
├── What NOT to do
└── Next steps & timeline
```

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📊 Data Upload | CSV or Excel with auto-type detection |
| ❓ Smart Questions | AI-generated questions specific to YOUR data |
| 🔮 Scenario Simulation | 3 what-if scenarios with quantified outcomes |
| 📈 Interactive Charts | Plotly-powered comparisons |
| 🎯 Confidence Gauge | Visual confidence score (0-100) |
| ⚠️ Risk Analysis | Each risk with severity and mitigation plan |
| 🚫 Anti-Pattern Detection | Tells you what NOT to do |
| 📋 Action Items | Prioritised next steps with timeline |
| 📥 Sample Data | Load synthetic business data for demo |

---

## 🛠️ Tech Stack

- **Framework:** LangChain
- **LLM:** OpenAI GPT-4 compatible APIs
- **Data Analysis:** Pandas
- **Visualisation:** Plotly (gauge, bar charts)
- **UI:** Streamlit multi-step wizard
- **Output Format:** Structured JSON

---

## 🚀 Run Locally

```bash
git clone https://github.com/RohJiv/decision-copilot-ai.git
cd decision-copilot-ai

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

# Set .env
# OPENAI_API_KEY=your_key_here

streamlit run app.py
```

---

## 📖 Example Use Case

**Input:** CSV with 5 products, revenue, costs, growth rates

**Question:** "Should I discontinue Product C?"

**Step 1 — Data Loaded:**
```
Product | Revenue | Growth% | Cost
Laptop  | 750k    | 12%     | 500k
Chair   | 360k    | 8%      | 180k
Product C | 175k  | -5%     | 125k  ← underperforming
...
```

**Step 2 — AI asks:**
- What's your target profit margin?
- Is there brand/strategic value in keeping Product C?
- What's your timeline for the decision?

**Step 3 — Scenarios:**
1. **Keep as-is** → Impact: -15, Risk: Medium, Confidence: 70%
2. **Discount 20%** → Impact: +25, Risk: Low, Confidence: 85%  ✅
3. **Discontinue** → Impact: -30, Risk: High (lose customers), Confidence: 60%

**Step 4 — Recommendation:**
"Discount Product C by 20% for 3 months before discontinuing. The 20% discount captures remaining demand while testing if product can recover. Discontinuing immediately loses ₹2.3L in annual recurring revenue and risks customer migration to competitors."

---

## 🎓 What I Learned Building This

- **Multi-step wizard UI patterns** in Streamlit
- **Complex state management** across steps
- **Pandas DataFrame analysis** at LLM context size
- **Multi-stage LLM chains** (3+ chained AI calls)
- **Interactive data visualisation** with Plotly
- **Confidence scoring** in AI outputs
- **Scenario modelling** patterns
- **Risk-mitigation thinking** in structured output
- **Progress indicators** for long multi-step workflows

---

## 💼 Real-World Applications

This decision support pattern powers:
- Strategic planning tools for executives
- Product portfolio rationalisation decisions
- Market expansion analysis
- Cost reduction scenario planning
- Investment allocation decisions
- Resource planning and forecasting

---

## 🧠 Why Decision Support Over Chat

Most AI products are chatbots. This is different:

| Chatbot | Decision Copilot |
|---------|------------------|
| Answers questions | Helps make decisions |
| Reactive | Structured process |
| Single response | Multi-scenario analysis |
| "What do you know?" | "What should I do?" |

This distinction matters for enterprise adoption. Executives don't want another chat window — they want structured decision frameworks augmented by AI.

---

## 🔐 Privacy Notes

- Data processed in-memory only — never stored
- CSV/Excel files held only during session
- No external data transmission
- All LLM calls use your own API key

---

## 👤 Author

**Phani Rajiv G**
Technical Program Manager | Cloud & AI Platforms
📍 Hyderabad, India
📧 phani.rg@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/phanirajivg)

This is the project I'm most proud of — it combines data analysis, AI reasoning, and product thinking into one tool.

---

## 📄 License

MIT License — free to use for learning.

---

⭐ If this sparked a decision-making idea for you, star the repo!
