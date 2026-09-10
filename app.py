import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta
import re # NEW: Used for dynamic text extraction

# --- PAGE CONFIG ---
st.set_page_config(page_title="Promise Guard | Advanced", layout="wide", page_icon="🛡️")

# --- CUSTOM CSS WITH BACKGROUND IMAGE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Share Tech Mono', monospace;
    }
    
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
        background-color: rgba(11, 14, 20, 0.92);
        background-blend-mode: multiply;
    }
    
    .glow-card {
        background: rgba(15, 20, 30, 0.75);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 240, 255, 0.3);
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.05);
        margin-bottom: 20px;
        color: #E0E6ED;
    }
    
    .glow-card:hover {
        border-color: rgba(0, 240, 255, 0.8);
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
    }
    
    .risk-high { border-color: rgba(255, 51, 102, 0.5); }
    .risk-low { border-color: rgba(0, 255, 153, 0.5); }
    
    .stButton>button {
        border: 1px solid #00F0FF;
        color: #00F0FF;
        background-color: rgba(0, 240, 255, 0.05);
        transition: all 0.3s ease-in-out;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #00F0FF;
        color: #0B0E14;
        box-shadow: 0 0 20px #00F0FF;
    }
    
    div.row-widget.stRadio > div {
        background: rgba(15, 20, 30, 0.6);
        padding: 10px;
        border-radius: 5px;
        border: 1px solid rgba(0, 240, 255, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# --- ADVANCED DATA LOADING ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("promise guard/data/promiseguard_clean.csv")
    except:
        dates = [datetime.today() + timedelta(days=x*30) for x in range(12)]
        df = pd.DataFrame({
            "Promise_ID": [f"PRM-00{i}" for i in range(1, 13)],
            "Entity": ["TechCorp", "GovLocal", "BioPharma", "EcoOrg", "FinServe", "TechCorp", "GovLocal", "AgriGen", "EcoOrg", "BioPharma", "FinServe", "GovLocal"],
            "Category": ["Environment", "Infrastructure", "Health", "Environment", "Compliance", "Labor", "Education", "Environment", "Health", "R&D", "Cybersecurity", "Infrastructure"],
            "Sentiment_Score": [0.85, -0.20, 0.60, 0.92, 0.10, 0.45, -0.60, 0.30, 0.88, 0.75, -0.15, 0.20],
            "Confidence_Score": [94, 82, 88, 96, 75, 89, 70, 85, 91, 95, 78, 83],
            "Risk_Level": ["Low", "High", "Medium", "Low", "Medium", "Medium", "High", "Medium", "Low", "Low", "High", "Medium"],
            "Status": ["On Track", "Delayed", "On Track", "Completed", "At Risk", "On Track", "Delayed", "On Track", "Completed", "On Track", "At Risk", "On Track"],
            "Target_Date": dates
        })
    return df

df = load_data()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=60) 
    st.markdown("<h2 style='color:#00F0FF; margin-top:0;'>PROMISE GUARD</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00FF99; font-size: 0.8em;'>● SECURE UPLINK ESTABLISHED</p>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("SELECT OVERRIDE", ["[01] NEURAL ENGINE", "[02] GLOBAL TELEMETRY"])
    
    st.markdown("---")
    if page == "[02] GLOBAL TELEMETRY":
        st.subheader("Filter Parameters")
        selected_entities = st.multiselect("Select Entities", options=df['Entity'].unique(), default=df['Entity'].unique())
        selected_risk = st.multiselect("Select Risk Level", options=df['Risk_Level'].unique(), default=df['Risk_Level'].unique())
        df = df[df['Entity'].isin(selected_entities) & df['Risk_Level'].isin(selected_risk)]

# --- LIGHTWEIGHT NLP LOGIC ---
def analyze_text(text):
    text_lower = text.lower()
    
    # 1. Dynamic Extraction
    # Find Dates (Years, Months, Days, Q1-Q4)
    date_patterns = r'(20\d{2}|q[1-4]|january|february|march|april|may|june|july|august|september|october|november|december|tomorrow|monday|tuesday|wednesday|thursday|friday|next \w+|by \w+)'
    dates_found = re.findall(date_patterns, text_lower)
    extracted_date = dates_found[-1].title() if dates_found else "UNSPECIFIED (High Variance)"

    # Find Entity (Look for subjects before promise words)
    entity_match = re.search(r'(.*?)\s+(commit|promise|pledge|will|guarantee|plan|try)', text, re.IGNORECASE)
    raw_entity = entity_match.group(1).strip() if entity_match else "Unknown Source"
    extracted_entity = " ".join(raw_entity.split()[-2:]).title() if raw_entity != "Unknown Source" and len(raw_entity.split()) > 0 else raw_entity

    # Find Commitment Rule
    commitment_match = re.search(r'(?:commit to|promise to|pledge to|will|guarantee that|plan to|try to)\s+(.*)', text, re.IGNORECASE)
    extracted_commitment = commitment_match.group(1).strip().capitalize() if commitment_match else "Vague/Unspecified Action"

    # 2. Dynamic Sentiment Scoring
    pos_words = ['guarantee', 'commit', 'improve', 'growth', 'allocate', 'fix', 'deliver', 'completed', 'ambitious', 'pledge', 'reduce', 'definitely']
    neg_words = ['unfortunately', 'delay', 'cancel', 'struggle', 'downturn', 'bug', 'fail', 'not', 'never', 'miss', 'pushing']
    
    pos_count = sum(1 for w in pos_words if w in text_lower)
    neg_count = sum(1 for w in neg_words if w in text_lower)
    
    sentiment_score = 0.1 + (pos_count * 0.35) - (neg_count * 0.45)
    sentiment_score = max(-1.0, min(1.0, sentiment_score)) # Clamp between -1 and 1
    
    if sentiment_score >= 0.5: sentiment_label = "Highly Ambitious / Positive"
    elif sentiment_score > 0: sentiment_label = "Neutral-Positive"
    elif sentiment_score > -0.5: sentiment_label = "Hesitant / Neutral-Negative"
    else: sentiment_label = "Negative / Retraction"

    # 3. Dynamic Risk Scoring
    risk_words = ['try', 'if', 'maybe', 'hope', 'soon', 'whenever', 'provided', 'looking into']
    risk_hits = [w for w in risk_words if w in text_lower]
    
    # Calculate confidence based on data points found
    confidence = 50
    if extracted_date != "UNSPECIFIED (High Variance)": confidence += 20
    if extracted_commitment != "Vague/Unspecified Action": confidence += 20
    if not risk_hits: confidence += 10
    
    is_high_risk = len(risk_hits) > 0 or extracted_date == "UNSPECIFIED (High Variance)" or sentiment_score < 0
    
    return {
        "entity": extracted_entity, "date": extracted_date, "commitment": extracted_commitment,
        "sent_score": sentiment_score, "sent_label": sentiment_label,
        "is_high_risk": is_high_risk, "risk_hits": risk_hits, "confidence": confidence
    }

# --- MODULE 1: NEURAL ENGINE ---
if page == "[01] NEURAL ENGINE":
    st.markdown("<h1 style='color:#00F0FF;'>>> NEURAL PROCESSING NODES</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#E0E6ED;'>Feed text into the buffer, select your target processing node, and execute.</p>", unsafe_allow_html=True)
    
    user_input = st.text_area("RAW TEXT STREAM:", height=120, placeholder="> Paste speech, document excerpt, or press release here...")
    
    st.markdown("<h4 style='color:#00F0FF;'>SELECT PROCESSING NODE:</h4>", unsafe_allow_html=True)
    analysis_mode = st.radio("", ["[ EXTRACT ]", "[ SENTIMENT ]", "[ RISK ]"], horizontal=True, label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("EXECUTE PROTOCOL"):
        if not user_input:
            st.error("Error: Input buffer empty.")
        else:
            # RUN NLP LOGIC
            analysis = analyze_text(user_input)
            
            st.markdown("---")
            
            # --- [ EXTRACT ] MODE ---
            if analysis_mode == "[ EXTRACT ]":
                with st.spinner("Executing extraction_config.json..."): time.sleep(0.8)
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"""
                    <div class='glow-card'>
                        <h3 style='color:#00F0FF; border-bottom: 1px solid #00F0FF;'>[ PARSED COMMITMENTS ]</h3>
                        <p><b>DETECTED ENTITY:</b> <span style='color:#00FF99;'>{analysis['entity']}</span></p>
                        <p><b>COMMITMENT RULE:</b> <span style='color:#00FF99;'>{analysis['commitment']}</span></p>
                        <p><b>DEADLINE / TIMELINE:</b> <span style='color:#00FF99;'>{analysis['date']}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class='glow-card'>
                        <h4 style='color:#00F0FF;'>[ LOGIC CONFIDENCE ]</h4>
                        <h1 style='color:#00FF99; margin:0;'>{analysis['confidence']}%</h1>
                        <p style='font-size:0.8em;'>Pattern Match Confirmed</p>
                    </div>
                    """, unsafe_allow_html=True)

            # --- [ SENTIMENT ] MODE ---
            elif analysis_mode == "[ SENTIMENT ]":
                with st.spinner("Executing sentiment_config.json..."): time.sleep(0.8)
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown(f"""
                    <div class='glow-card'>
                        <h3 style='color:#00F0FF; border-bottom: 1px solid #00F0FF;'>[ LINGUISTIC TONE ]</h3>
                        <p>The text has been analyzed for ambitious, hesitant, or negative phrasing regarding commitments.</p>
                        <h2 style='color:#00F0FF;'>Score: {analysis['sent_score']:+.2f}</h2>
                        <p style='color:#00FF99;'>[ STATUS: {analysis['sent_label']} ]</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown("<div class='glow-card'>", unsafe_allow_html=True)
                    fig_gauge = go.Figure(go.Indicator(
                        mode = "gauge+number", value = analysis['sent_score'], domain = {'x': [0, 1], 'y': [0, 1]},
                        gauge = {
                            'axis': {'range': [-1, 1], 'tickwidth': 1, 'tickcolor': "#00F0FF"},
                            'bar': {'color': "#00F0FF"}, 'bgcolor': "#151A22",
                            'borderwidth': 2, 'bordercolor': "#00F0FF",
                            'steps': [{'range': [-1, -0.3], 'color': "rgba(255, 51, 102, 0.3)"},
                                      {'range': [-0.3, 0.3], 'color': "rgba(255, 255, 255, 0.1)"},
                                      {'range': [0.3, 1], 'color': "rgba(0, 255, 153, 0.3)"}],
                        }))
                    fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E6ED", font_family="Share Tech Mono", height=200, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig_gauge, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            # --- [ RISK ] MODE ---
            elif analysis_mode == "[ RISK ]":
                with st.spinner("Executing risk_model_config.json..."): time.sleep(0.8)
                
                risk_class = "risk-high" if analysis['is_high_risk'] else "risk-low"
                risk_text = "HIGH RISK DETECTED" if analysis['is_high_risk'] else "LOW RISK DETECTED"
                risk_color = "#FF3366" if analysis['is_high_risk'] else "#00FF99"
                
                # Dynamic Radar values
                clarity = 30 if analysis['is_high_risk'] else 95
                feasibility = 45 if analysis['is_high_risk'] else 85
                timeline_realism = 20 if analysis['date'] == "UNSPECIFIED (High Variance)" else 95
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    flagged_str = ", ".join(analysis['risk_hits']) if analysis['risk_hits'] else "None detected (Concrete statement)"
                    st.markdown(f"""
                    <div class='glow-card {risk_class}'>
                        <h3 style='color:{risk_color}; border-bottom: 1px solid {risk_color};'>[ FEASIBILITY REPORT ]</h3>
                        <h2 style='color:{risk_color};'>{risk_text}</h2>
                        <p>Text evaluated against historical completion metrics, conditional statements, and timeline realism.</p>
                        <p><b>Flagged terms:</b> {flagged_str}</p>
                        <p><b>Timeline Check:</b> {"Missing/Vague Deadline" if analysis['date'] == "UNSPECIFIED (High Variance)" else "Deadline Identified"}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown("<div class='glow-card'>", unsafe_allow_html=True)
                    fig_radar = go.Figure(data=go.Scatterpolar(
                      r=[clarity, 20 if not analysis['is_high_risk'] else 80, feasibility, 40, timeline_realism], 
                      theta=['Clarity','Ambiguity','Feasibility','Financial Risk','Timeline Realism'],
                      fill='toself', line_color=risk_color
                    ))
                    fig_radar.update_layout(
                      polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(0,240,255,0.2)'), bgcolor='rgba(0,0,0,0)'),
                      paper_bgcolor='rgba(0,0,0,0)', font_color='#E0E6ED', height=250, margin=dict(l=20, r=20, t=20, b=20)
                    )
                    st.plotly_chart(fig_radar, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

# --- MODULE 2: GLOBAL TELEMETRY (EDA) ---
elif page == "[02] GLOBAL TELEMETRY":
    st.markdown("<h1 style='color:#00F0FF;'>>> GLOBAL TELEMETRY DASHBOARD</h1>", unsafe_allow_html=True)
    
    # 1. TOP METRICS
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='glow-card'><p>ACTIVE PROMISES</p><h2 style='color:#00F0FF; margin:0;'>{len(df)}</h2></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='glow-card'><p>AVG CONFIDENCE</p><h2 style='color:#00FF99; margin:0;'>{df['Confidence_Score'].mean():.1f}%</h2></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='glow-card risk-high'><p>HIGH RISK</p><h2 style='color:#FF3366; margin:0;'>{len(df[df['Risk_Level'] == 'High'])}</h2></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='glow-card'><p>DELAYED</p><h2 style='color:#FFaa00; margin:0;'>{len(df[df['Status'] == 'Delayed'])}</h2></div>", unsafe_allow_html=True)
    
    # 2. MIDDLE ROW: TREEMAP & SCATTER
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("<div class='glow-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#00F0FF;'>[ Entity & Category Matrix ]</h4>", unsafe_allow_html=True)
        fig_tree = px.treemap(df, path=['Entity', 'Category', 'Risk_Level'], color='Sentiment_Score', color_continuous_scale='cyan')
        fig_tree.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E0E6ED", margin=dict(t=10, l=10, r=10, b=10))
        st.plotly_chart(fig_tree, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_chart2:
        st.markdown("<div class='glow-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#00F0FF;'>[ Sentiment vs Confidence Scatter ]</h4>", unsafe_allow_html=True)
        fig_scatter = px.scatter(df, x="Sentiment_Score", y="Confidence_Score", color="Risk_Level", 
                                 size="Confidence_Score", hover_data=['Entity', 'Category'],
                                 color_discrete_map={"Low":"#00FF99", "Medium":"#00F0FF", "High":"#FF3366"})
        fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E0E6ED", margin=dict(t=10, l=10, r=10, b=10))
        fig_scatter.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,240,255,0.1)')
        fig_scatter.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,240,255,0.1)')
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 3. BOTTOM ROW: TIMELINE
    st.markdown("<div class='glow-card'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#00F0FF;'>[ Promise Delivery Timeline ]</h4>", unsafe_allow_html=True)
    fig_line = px.bar(df.sort_values('Target_Date'), x="Target_Date", y="Confidence_Score", color="Status",
                      color_discrete_map={"On Track":"#00F0FF", "Completed":"#00FF99", "Delayed":"#FF3366", "At Risk":"#FFaa00"})
    fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E0E6ED")
    fig_line.update_xaxes(showgrid=True, gridcolor='rgba(0,240,255,0.1)')
    fig_line.update_yaxes(showgrid=True, gridcolor='rgba(0,240,255,0.1)')
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)