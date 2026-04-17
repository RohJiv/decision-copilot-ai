# decision_agent.py — AI Decision Copilot Core Logic

import os
import json
import pandas as pd
import io
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# ── Load and summarise uploaded data ─────────────────────────
def load_data(uploaded_file) -> tuple:
    try:
        filename = uploaded_file.name.lower()

        if filename.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            return None, "❌ Only CSV and Excel files supported"

        return df, None
    except Exception as e:
        return None, f"❌ Error loading file: {str(e)}"

def summarise_data(df: pd.DataFrame) -> str:
    summary = f"""
DATASET OVERVIEW:
- Rows: {len(df)}
- Columns: {len(df.columns)}
- Column names: {list(df.columns)}

COLUMN TYPES:
{df.dtypes.to_string()}

SAMPLE DATA (first 5 rows):
{df.head().to_string()}

BASIC STATISTICS:
{df.describe().to_string()}

MISSING VALUES:
{df.isnull().sum().to_string()}
"""
    return summary

# ── Step 1: Ask smart clarifying questions ────────────────────
def generate_clarifying_questions(data_summary: str) -> list:
    prompt = ChatPromptTemplate.from_template("""
You are an expert business analyst and decision advisor.

You have been given this dataset:
{data_summary}

Generate 3 smart clarifying questions to understand:
1. What decision the user is trying to make
2. What constraints they have
3. What success looks like to them

Return ONLY a JSON array — no markdown, no explanation:
[
    "question 1",
    "question 2", 
    "question 3"
]

Make questions specific to the actual data columns and values shown.
Return ONLY valid JSON array.
""")

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"data_summary": data_summary})

    try:
        result = result.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    except:
        return [
            "What specific decision are you trying to make with this data?",
            "What constraints or limitations should I consider?",
            "What does success look like for you in this situation?"
        ]

# ── Step 2: Run what-if scenarios ─────────────────────────────
def run_scenarios(
    df: pd.DataFrame,
    data_summary: str,
    decision_question: str,
    user_answers: str
) -> dict:

    prompt = ChatPromptTemplate.from_template("""
You are an expert business analyst running what-if scenarios.

DATASET:
{data_summary}

DECISION QUESTION: {question}

USER CONTEXT: {answers}

Run 3 different what-if scenarios relevant to this decision.
For each scenario calculate likely outcomes based on the data.

Return ONLY a JSON object — no markdown, no explanation:
{{
    "scenarios": [
        {{
            "name": "Scenario name",
            "description": "What this scenario does",
            "assumptions": ["assumption 1", "assumption 2"],
            "predicted_outcome": "what happens",
            "impact_score": 0,
            "risk_level": "low/medium/high",
            "confidence": 0
        }}
    ]
}}

impact_score is -100 to +100 (negative = bad, positive = good)
confidence is 0-100

Return ONLY valid JSON.
""")

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({
        "data_summary":    data_summary,
        "question":        decision_question,
        "answers":         user_answers
    })

    try:
        result = result.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    except:
        return {"scenarios": []}

# ── Step 3: Generate final recommendation ─────────────────────
def generate_recommendation(
    data_summary:      str,
    decision_question: str,
    user_answers:      str,
    scenarios:         dict
) -> dict:

    prompt = ChatPromptTemplate.from_template("""
You are an expert business advisor making a final recommendation.

DATASET SUMMARY:
{data_summary}

DECISION QUESTION: {question}

USER CONTEXT: {answers}

SCENARIOS ANALYSED:
{scenarios}

Based on all of the above give a final recommendation.

Return ONLY a JSON object — no markdown, no explanation:
{{
    "recommended_action": "clear specific action to take",
    "confidence_score": 0,
    "reasoning": "detailed explanation of why this is best",
    "key_insights": ["insight 1", "insight 2", "insight 3"],
    "risks": [
        {{"risk": "risk description", "severity": "low/medium/high", "mitigation": "how to handle"}}
    ],
    "do_not_do": "what to avoid and why",
    "next_steps": ["step 1", "step 2", "step 3"],
    "timeline": "recommended timeline to implement"
}}

confidence_score is 0-100.
Be specific, honest and data-driven.
Return ONLY valid JSON.
""")

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({
        "data_summary": data_summary,
        "question":     decision_question,
        "answers":      user_answers,
        "scenarios":    json.dumps(scenarios, indent=2)
    })

    try:
        result = result.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    except:
        return {
            "recommended_action": "Unable to parse recommendation",
            "confidence_score":   0,
            "reasoning":          result,
            "key_insights":       [],
            "risks":              [],
            "do_not_do":          "",
            "next_steps":         [],
            "timeline":           "Unknown"
        }