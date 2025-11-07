import streamlit as st
from analyzers.analyzer import analyze_transcript  # Import main function
from utils.detectors import pre_check_callback, pre_check_interaction, pre_check_time_respect, pre_check_needs, pre_check_transfer  # Added pre_check_transfer

# UI Layout (Set config first)
st.set_page_config(page_title="QA Analysis Dashboard", page_icon="📊", layout="wide")

# Custom CSS for Tailwind-inspired styling (now after config)
st.markdown("""
<style>
body {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background-color: #f9fafb;
}
.stHeader {
    color: #1f2937;
    font-weight: 700;
    font-size: 2.5rem;
    margin-bottom: 1rem;
}
.stSubheader {
    color: #374151;
    font-weight: 600;
    font-size: 1.5rem;
    margin-top: 1rem;
}
.stMetric {
    background-color: #ffffff;
    padding: 1rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.stProgress {
    margin-top: 1rem;
}
.stExpander {
    background-color: #ffffff;
    border-radius: 0.5rem;
    margin-top: 0.5rem;
}
.stButton>button {
    background-color: #3b82f6;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
    font-weight: 500;
    transition: background-color 0.2s;
}
.stButton>button:hover {
    background-color: #2563eb;
}
.stTextArea>label {
    font-weight: 500;
    color: #374151;
}
</style>
""", unsafe_allow_html=True)

# Rest of the code remains unchanged...
st.header("QA Analysis Dashboard")
st.markdown("Analyze customer service transcripts with a beautiful, interactive dashboard. Paste a transcript or upload a file to see scores, reasoning, and visualizations.")

# Input Section
col1, col2 = st.columns([3, 1])
with col1:
    transcript = st.text_area("Paste Transcript Here", height=200, placeholder="Enter transcript in format: ( 0 s ): Speaker: Message...")
with col2:
    uploaded_files = st.file_uploader("Or Upload Transcript File (.txt)", type="txt", accept_multiple_files=True)  # New: Multiple for batch

# Analyze Button
model_select = st.selectbox("Select LLM Model", ["gpt-4o", "gpt-4o-mini"], index=0)  # Default gpt-4o
if st.button("Analyze Transcript"):
    transcripts = []
    if uploaded_files:
        transcripts = [f.read().decode("utf-8") for f in uploaded_files]
    if transcript:
        transcripts.append(transcript)
    
    if transcripts:
        results = []
        for t in transcripts:
            with st.spinner("Analyzing transcript..."):
                try:
                    result = analyze_transcript(t, model=model_select)  # New: Try-except
                    results.append(result)
                except Exception as e:
                    st.error(f"Analysis error for transcript: {str(e)}")
                    continue
        
        # Display Batch Results
        for idx, result in enumerate(results, 1):
            st.subheader(f"Transcript {idx} Results")
            
            # Overall Score and Progress (use .get() for safety)
            overall_scores = result.get('overall_scores', {})
            overall_total = overall_scores.get('total_score', 0)
            overall_max = overall_scores.get('max_possible_score', 45)  # Updated from 35 to 45
            overall_perc = overall_scores.get('percentage_score', 0)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Overall Score")
                st.metric("Total Score", f"{overall_total}/{overall_max}")
                st.progress(overall_perc / 100)
                st.write(f"Percentage: {overall_perc}%")
            
            with col2:
                st.subheader("Key Metrics")
                first_analysis = result.get('first_response_analysis', {})
                pre_calc = result.get('pre_calculated', {})
                first_score = first_analysis.get('score', 5 if pre_calc.get('within_2_minutes', False) and pre_check_callback(t) else 0)
                first_max = 5
                st.metric("First Response Score", f"{first_score}/{first_max}", help="Within 2 min + CBR request")
                
                verif_analysis = result.get('security_verification_analysis', {})
                pre_verif = result.get('pre_verification', {})
                verif_score = verif_analysis.get('score', 10 if pre_verif.get('all_obtained', False) and pre_verif.get('num_asked', 0) >= 3 else 0)
                verif_max = 10
                st.metric("Security Verification Score", f"{verif_score}/{verif_max}", help="Asked combo + provided all + aligned")
                
                needs_analysis = result.get('customer_needs_analysis', {})
                pre_reason = result.get('pre_reason', {})
                needs_score = needs_analysis.get('score', 5 if pre_reason.get('identified_reason', False) and pre_reason.get('restated_with_confirmation', False) else 0)
                needs_max = 5
                st.metric("Customer Needs Score", f"{needs_score}/{needs_max}", help="Identified reason + restated with confirmation")
                
                # New CX Metrics
                interaction_analysis = result.get('interaction_analysis', {})
                pre_interaction = result.get('pre_interaction', {})
                interaction_score = interaction_analysis.get('score', 5 if pre_interaction.get('all_met', False) else 0)
                st.metric("Interaction Responsibility Score", f"{interaction_score}/5", help="Proper language + responsibility + expectation")
                
                time_respect_analysis = result.get('time_respect_analysis', {})
                pre_time_respect = result.get('pre_time_respect', {})
                time_respect_score = time_respect_analysis.get('score', 10 if pre_time_respect.get('all_met', False) else 0)
                st.metric("Time Respect Score", f"{time_respect_score}/10", help="Check-ins + no idle")
                
                needs_ident_analysis = result.get('needs_identification_analysis', {})
                pre_needs = result.get('pre_needs', {})
                needs_ident_score = needs_ident_analysis.get('score', 5 if pre_needs.get('no_redundant_ask', False) else 0)
                st.metric("Needs Identification Score", f"{needs_ident_score}/5", help="No redundant asks")
                
                # New Transfer Metric
                transfer_analysis = result.get('transfer_analysis', {})
                pre_transfer = result.get('pre_transfer', {})
                transfer_score = transfer_analysis.get('score', 10 if pre_transfer.get('asked_voice', False) else 0)
                st.metric("Voice Services Question Score", f"{transfer_score}/10", help="Asked 'Do you need any voice services provisioned?'")
                
            # Detailed Reasoning
            st.subheader("Detailed Reasoning")
            
            with st.expander("First Response Analysis"):
                st.write(f"**Reasoning**: {first_analysis.get('reasoning', 'No LLM reasoning; based on pre-check.')}")
                st.write(f"**Response Time**: {first_analysis.get('response_time_seconds', pre_calc.get('response_time_seconds', 'N/A'))} seconds")
                st.write(f"**Within 2 Minutes**: {first_analysis.get('within_2_minutes', str(pre_calc.get('within_2_minutes', 'N/A')).lower())}")
                st.write(f"**Callback Requested**: {first_analysis.get('callback_requested', 'true' if pre_check_callback(t) else 'false')}")
            
            with st.expander("Security Verification Analysis"):
                st.write(f"**Reasoning**: {verif_analysis.get('reasoning', pre_verif.get('reasoning', 'N/A'))}")
                st.write(f"**Asked for Valid Combo**: {verif_analysis.get('agent_asked_for_combo', str(pre_verif.get('num_asked', 0) >= 3))}")
                st.write(f"**Number of Elements Asked**: {verif_analysis.get('num_elements_asked', pre_verif.get('num_asked', 'N/A'))}")
                st.write(f"**Customer Provided All**: {verif_analysis.get('customer_provided_all', str(pre_verif.get('all_obtained', 'N/A')))}")
                st.write(f"**Record Aligned**: {verif_analysis.get('record_aligned', str(not pre_verif.get('tech_pre_supplied', False)))}")
            
            with st.expander("Customer Expectations and Needs Analysis"):
                st.write(f"**Reasoning**: {needs_analysis.get('reasoning', pre_reason.get('reasoning', 'N/A'))}")
                st.write(f"**Identified Reason**: {needs_analysis.get('identified_reason', str(pre_reason.get('identified_reason', 'N/A')))}")
                st.write(f"**Restated with Confirmation**: {needs_analysis.get('restated_with_confirmation', str(pre_reason.get('restated_with_confirmation', 'N/A')))}")
            
            with st.expander("Customer Interaction and Accepting Responsibility"):
                st.write(f"**Reasoning**: {interaction_analysis.get('reasoning', 'N/A')}")
                st.write(f"**Proper Language**: {interaction_analysis.get('proper_language', 'N/A')}")
                st.write(f"**Accepts Responsibility**: {interaction_analysis.get('accepts_responsibility', 'N/A')}")
                st.write(f"**Sets Expectation**: {interaction_analysis.get('sets_expectation', 'N/A')}")
            
            with st.expander("Customer Experience/ Respectful of Customer's Time"):
                st.write(f"**Reasoning**: {time_respect_analysis.get('reasoning', 'N/A')}")
                st.write(f"**Check-ins Met**: {time_respect_analysis.get('check_ins_met', 'N/A')}")
                st.write(f"**No Idle**: {time_respect_analysis.get('no_idle', 'N/A')}")
            
            with st.expander("Identify Contact's Needs and Avoid Redundant Asks"):
                st.write(f"**Reasoning**: {needs_ident_analysis.get('reasoning', 'N/A')}")
                st.write(f"**No Redundant Ask**: {needs_ident_analysis.get('no_redundant_ask', 'N/A')}")
            
            # New Transfer Expander 
            with st.expander("Voice Services Question Analysis"):
                st.write(f"**Reasoning**: {transfer_analysis.get('reasoning', pre_transfer.get('reasoning', 'N/A'))}")
                st.write(f"**Asked Voice Services**: {transfer_analysis.get('asked_voice_services', str(pre_transfer.get('asked_voice', 'N/A')))}")
                    
                        
            # Score Breakdown Chart
            st.subheader("Score Breakdown")
            scores = {
                "First Response": (first_score / first_max * 100) if first_max else 0,
                "Security Verification": (verif_score / verif_max * 100) if verif_max else 0,
                "Customer Needs": (needs_score / needs_max * 100) if needs_max else 0,
                "Interaction Responsibility": (interaction_score / 5 * 100),
                "Time Respect": (time_respect_score / 10 * 100),
                "Needs Identification": (needs_ident_score / 5 * 100),
                "Proper Transfer": (transfer_score / 10 * 100)  # Added Proper Transfer
            }
            st.bar_chart(scores)
            
            # Debug Info (Optional) - Cleaned up
            with st.expander("Debug Information"):
                st.write("**Raw LLM Response**:")
                st.text(result.get('raw_response', 'N/A'))
                st.write("**Pre-Calculated Data**:")
                st.json(result.get('pre_calculated', {}))
                st.write("**Pre-Verification Data**:")
                st.json(result.get('pre_verification', {}))
                st.write("**Pre-Reason Data**:")
                st.json(result.get('pre_reason', {}))
                st.write("**Pre-Interaction Data**:")
                st.json(result.get('pre_interaction', {}))
                st.write("**Pre-Time Respect Data**:")
                st.json(result.get('pre_time_respect', {}))
                st.write("**Pre-Needs Data**:")
                st.json(result.get('pre_needs', {}))
                st.write("**Pre-Transfer Data**:")  # New
                st.json(result.get('pre_transfer', {}))
                st.write("**Sent LLM Prompt**:")
                st.text(result.get('sent_prompt', 'N/A'))
                if 'api_error' in result:
                    st.warning(f"API Error: {result['api_error']}")
                
    else:
        st.error("Please provide a transcript to analyze.")