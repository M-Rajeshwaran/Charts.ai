import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. CONFIGURATION & AI SETUP ---
st.set_page_config(page_title="charts.ai Pro", page_icon="📈", layout="wide")

# Securely get API Key from Streamlit Secrets or Sidebar
# To use Secrets, go to Streamlit Dashboard -> Settings -> Secrets
# And add: GOOGLE_API_KEY = "AIzaSyBtGBFWj-e4xhNOZvAa13q-eno9elpYJno"
api_key = st.secrets.get("GOOGLE_API_KEY") or st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.warning("Please provide an API Key to start.")

# --- 2. USER INTERFACE DESIGN ---
st.title("📈 charts.ai | Institutional Grade Analytics")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Strategy Configuration")
    mode = st.selectbox("Trading Mode", ["Scalping (1m-5m)", "Intraday (15m-1h)", "Swing (4h-Daily)"])
    strategy_type = st.radio("Primary Logic", ["SMC (Smart Money Concepts)", "ICT (Inner Circle Trader)", "Pure Price Action"])
    rr_target = st.slider("Target Risk/Reward Ratio", 1.5, 10.0, 3.0)
    
    st.info(f"System tuned for **{mode}** using **{strategy_type}**.")

# --- 3. CORE ANALYTICS ENGINE ---
uploaded_file = st.file_uploader("📤 Upload Real-Time Chart (Forex, Crypto, Indices)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Display the uploaded image professionally
    image = Image.open(uploaded_file)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🖼️ Uploaded Chart")
        st.image(image, use_container_width=True)

    with col2:
        st.subheader("🧠 AI Technical Analysis")
        if st.button("🚀 GENERATE PROFESSIONAL REPORT"):
            if not api_key:
                st.error("Missing API Key!")
            else:
                with st.spinner("Analyzing Market Structure, Liquidity, and Volume..."):
                    # The Professional Prompt
                    prompt = f"""
                    Act as an institutional Tier-1 bank trader. Analyze the attached chart for a {mode} setup.
                    Strategy: {strategy_type}. Minimum RR: {rr_target}.
                    
                    Provide a formal report in the following format:
                    
                    ### 📊 MARKET STRUCTURE
                    - **Current Bias:** (Bullish/Bearish/Neutral)
                    - **Key Levels:** (Supply/Demand zones identified)
                    - **Market Phase:** (Accumulation/Expansion/Retracement)
                    
                    ### 🎯 THE SETUP (PRECISION ENTRY)
                    - **Order Type:** (Limit/Market)
                    - **Entry Price:** (Be exact based on chart)
                    - **Stop Loss:** (Protecting the structure)
                    - **Take Profit (Primary):** (Targets 1, 2, and 3)
                    
                    ### ⚖️ RISK MANAGEMENT
                    - **Risk/Reward Ratio:** (Calculated based on Entry/SL/TP)
                    - **Confidence Score:** (0-100%)
                    - **Confluences:** (List 3 reasons for this trade)
                    """
                    
                    try:
                        response = model.generate_content([prompt, image])
                        st.success("Analysis Complete")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")

# --- 4. FOOTER ---
st.markdown("---")
st.caption("© 2026 charts.ai | Advanced Algorithmic Decision Support")
