# app.py — AI Decision Copilot UI

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from decision_agent import (
    load_data,
    summarise_data,
    generate_clarifying_questions,
    run_scenarios,
    generate_recommendation
)
# Works locally (from .env) AND on Railway (from environment variables)
def get_api_key():
    # Try Streamlit secrets first (production)
    try:
        return st.secrets["GROQ_API_KEY"]
    except:
        # Fall back to .env (local development)
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv("GROQ_API_KEY")
# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="🧩 Decision Copilot",
    page_icon="🧩",
    layout="wide"
)

# ── Initialize session state ──────────────────────────────────
for key in ["step", "df", "data_summary", "questions",
            "answers", "scenarios", "recommendation"]:
    if key not in st.session_state:
        st.session_state[key] = None

if st.session_state["step"] is None:
    st.session_state["step"] = 1

# ── Title ─────────────────────────────────────────────────────
st.title("🧩 AI Decision Copilot")
st.caption("Upload your data → AI asks smart questions → Runs scenarios → Recommends best decision")

# ── Progress bar ──────────────────────────────────────────────
steps = ["Upload Data", "Answer Questions", "View Scenarios", "Final Decision"]
current_step = st.session_state["step"]

cols = st.columns(len(steps))
for i, (col, step_name) in enumerate(zip(cols, steps), 1):
    if i < current_step:
        col.success(f"✅ {step_name}")
    elif i == current_step:
        col.info(f"▶️ {step_name}")
    else:
        col.markdown(f"⏳ {step_name}")

st.divider()

# ══════════════════════════════════════════════════════════════
# STEP 1 — Upload Data
# ══════════════════════════════════════════════════════════════
if st.session_state["step"] == 1:
    st.subheader("📊 Step 1 — Upload Your Data")

    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Upload CSV or Excel file",
            type=["csv", "xlsx", "xls"]
        )

        if uploaded_file:
            df, error = load_data(uploaded_file)

            if error:
                st.error(error)
            else:
                st.success(f"✅ Loaded {len(df)} rows × {len(df.columns)} columns")
                st.dataframe(df.head(10), use_container_width=True)

                if st.button("🚀 Analyse This Data", type="primary", use_container_width=True):
                    with st.spinner("🧠 Understanding your data..."):
                        summary = summarise_data(df)
                        questions = generate_clarifying_questions(summary)

                    st.session_state["df"]           = df
                    st.session_state["data_summary"] = summary
                    st.session_state["questions"]    = questions
                    st.session_state["step"]         = 2
                    st.rerun()

    with col2:
        st.info("""
**How the Decision Copilot works:**

1️⃣ **Upload** your business data (sales, costs, metrics)

2️⃣ **Answer** 3 smart questions about your decision

3️⃣ **Review** AI-generated what-if scenarios

4️⃣ **Get** a clear recommendation with confidence score

**Works with any business decision:**
- Should I expand to a new market?
- Which product should I discontinue?
- Where should I cut costs?
- Which investment gives best ROI?
        """)

        st.markdown("**📥 Don't have data? Use sample:**")
        if st.button("Load Sample Sales Data"):
            sample = pd.DataFrame({
                "Product":  ["Laptop Pro", "Smartphone X", "Earbuds", "Chair", "Desk"],
                "Revenue":  [750000, 500000, 175000, 360000, 500000],
                "Units":    [10, 20, 50, 30, 20],
                "Cost":     [500000, 300000, 87500, 180000, 250000],
                "Growth%":  [12, -5, 25, 8, 15],
                "Returns%": [2, 8, 3, 1, 2]
            })
            summary   = summarise_data(sample)
            questions = generate_clarifying_questions(summary)

            st.session_state["df"]           = sample
            st.session_state["data_summary"] = summary
            st.session_state["questions"]    = questions
            st.session_state["step"]         = 2
            st.rerun()

# ══════════════════════════════════════════════════════════════
# STEP 2 — Answer Clarifying Questions
# ══════════════════════════════════════════════════════════════
elif st.session_state["step"] == 2:
    st.subheader("❓ Step 2 — Answer These Questions")
    st.caption("Help the AI understand your decision context")

    questions = st.session_state["questions"]
    answers   = []

    with st.form("questions_form"):
        for i, q in enumerate(questions, 1):
            answer = st.text_area(
                f"Question {i}: {q}",
                height=80,
                key=f"q{i}"
            )
            answers.append(f"Q{i}: {q}\nA{i}: {answer}")

        col1, col2 = st.columns([1, 1])
        with col1:
            back = st.form_submit_button("← Back")
        with col2:
            next_btn = st.form_submit_button(
                "Run Scenarios →",
                type="primary",
                use_container_width=True
            )

    if back:
        st.session_state["step"] = 1
        st.rerun()

    if next_btn:
        combined_answers = "\n\n".join(answers)
        with st.spinner("🔄 Running what-if scenarios..."):
            scenarios = run_scenarios(
                st.session_state["df"],
                st.session_state["data_summary"],
                questions[0],
                combined_answers
            )

        st.session_state["answers"]   = combined_answers
        st.session_state["scenarios"] = scenarios
        st.session_state["step"]      = 3
        st.rerun()

# ══════════════════════════════════════════════════════════════
# STEP 3 — View Scenarios
# ══════════════════════════════════════════════════════════════
elif st.session_state["step"] == 3:
    st.subheader("📊 Step 3 — What-If Scenarios")

    scenarios = st.session_state["scenarios"].get("scenarios", [])

    if not scenarios:
        st.error("No scenarios generated. Please go back and try again.")
    else:
        # Scenario cards
        cols = st.columns(len(scenarios))
        for i, (col, scenario) in enumerate(zip(cols, scenarios)):
            with col:
                impact = scenario.get("impact_score", 0)
                risk   = scenario.get("risk_level", "medium")
                conf   = scenario.get("confidence", 0)

                color = "🟢" if impact > 20 else "🔴" if impact < -20 else "🟡"
                risk_color = "🔴" if risk == "high" else "🟡" if risk == "medium" else "🟢"

                st.markdown(f"### {color} {scenario.get('name', f'Scenario {i+1}')}")
                st.caption(scenario.get("description", ""))

                st.metric("Impact Score", f"{impact}/100")
                st.metric("Risk Level",   f"{risk_color} {risk.title()}")
                st.metric("Confidence",   f"{conf}%")

                st.markdown("**Predicted Outcome:**")
                st.info(scenario.get("predicted_outcome", ""))

                with st.expander("📋 Assumptions"):
                    for assumption in scenario.get("assumptions", []):
                        st.markdown(f"• {assumption}")

        # Impact comparison chart
        st.divider()
        st.subheader("📈 Scenario Comparison")

        names   = [s.get("name", f"Scenario {i+1}") for i, s in enumerate(scenarios)]
        impacts = [s.get("impact_score", 0) for s in scenarios]
        confs   = [s.get("confidence", 0) for s in scenarios]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Impact Score",
            x=names,
            y=impacts,
            marker_color=["green" if i > 0 else "red" for i in impacts]
        ))
        fig.add_trace(go.Scatter(
            name="Confidence %",
            x=names,
            y=confs,
            mode="lines+markers",
            yaxis="y2",
            line=dict(color="blue", width=2)
        ))
        fig.update_layout(
            yaxis=dict(title="Impact Score"),
            yaxis2=dict(title="Confidence %", overlaying="y", side="right"),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)

    # Navigation
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back"):
            st.session_state["step"] = 2
            st.rerun()
    with col2:
        if st.button("Get Final Recommendation →", type="primary", use_container_width=True):
            with st.spinner("🧠 Generating final recommendation..."):
                recommendation = generate_recommendation(
                    st.session_state["data_summary"],
                    st.session_state["questions"][0],
                    st.session_state["answers"],
                    st.session_state["scenarios"]
                )
            st.session_state["recommendation"] = recommendation
            st.session_state["step"]           = 4
            st.rerun()

# ══════════════════════════════════════════════════════════════
# STEP 4 — Final Recommendation
# ══════════════════════════════════════════════════════════════
elif st.session_state["step"] == 4:
    st.subheader("🎯 Step 4 — Final Recommendation")

    rec   = st.session_state["recommendation"]
    score = rec.get("confidence_score", 0)

    # Confidence gauge
    color = "green" if score >= 70 else "orange" if score >= 40 else "red"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "AI Confidence Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar":  {"color": color},
            "steps": [
                {"range": [0,  40],  "color": "#ffcccc"},
                {"range": [40, 70],  "color": "#fff3cc"},
                {"range": [70, 100], "color": "#ccffcc"}
            ]
        }
    ))
    fig.update_layout(height=250)
    st.plotly_chart(fig, use_container_width=True)

    # Recommendation box
    st.success(f"### ✅ Recommended Action\n\n{rec.get('recommended_action', '')}")
    st.markdown(f"**💡 Reasoning:** {rec.get('reasoning', '')}")

    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🔍 Key Insights")
        for insight in rec.get("key_insights", []):
            st.markdown(f"💡 {insight}")

        st.divider()
        st.subheader("⚠️ Do NOT Do This")
        st.error(rec.get("do_not_do", ""))

    with col2:
        st.subheader("🚨 Risks & Mitigations")
        for risk in rec.get("risks", []):
            severity = risk.get("severity", "medium")
            icon     = "🔴" if severity == "high" else "🟡" if severity == "medium" else "🟢"
            with st.expander(f"{icon} {risk.get('risk', '')}"):
                st.markdown(f"**Mitigation:** {risk.get('mitigation', '')}")

        st.divider()
        st.subheader("📋 Next Steps")
        for i, step in enumerate(rec.get("next_steps", []), 1):
            st.markdown(f"{i}. {step}")

    st.divider()
    st.info(f"⏱️ **Recommended Timeline:** {rec.get('timeline', 'Unknown')}")

    # Start over
    if st.button("🔄 Analyse New Data", use_container_width=True):
        for key in ["step", "df", "data_summary", "questions",
                    "answers", "scenarios", "recommendation"]:
            st.session_state[key] = None
        st.session_state["step"] = 1
        st.rerun()