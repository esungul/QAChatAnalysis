from typing import Dict, Any
from utils.detectors import calculate_response_time, pre_check_callback, pre_check_verification, pre_check_reason_identification, pre_check_interaction, pre_check_time_respect, pre_check_needs, pre_check_transfer

def build_smart_prompt(transcript: str) -> str:
    time_data = calculate_response_time(transcript)
    callback_flag = pre_check_callback(transcript)
    verif_data = pre_check_verification(transcript)
    reason_data = pre_check_reason_identification(transcript)
    interaction_data = pre_check_interaction(transcript)
    time_respect_data = pre_check_time_respect(transcript)
    needs_data = pre_check_needs(transcript)
    transfer_data = pre_check_transfer(transcript)
    
    return f"""You are a strict QA analyst for customer service chats. Analyze the ENTIRE transcript following these EXACT rules. Use pre-calculated data for objectivity.

PRE-CALCULATED DATA (do not override):
- System message at: {time_data['system_time_seconds']} seconds
- First agent response at: {time_data['first_agent_time_seconds']} seconds
- Response time: {time_data['response_time_seconds']} seconds
- Within 2 minutes: {time_data['within_2_minutes']}
- Agent identifier: {time_data['first_agent_identifier']}
- Callback obtained (asked by agent or provided by customer in ANY msg, including abbrevs like 'cbr' for callback): {callback_flag}
- Verification pre-check: Asked phone: {verif_data['asked_phone']}, Account: {verif_data['asked_account']}, Name: {verif_data['asked_name']}, Address: {verif_data['asked_address']}; Num asked: {verif_data['num_asked']}/3; Customer provided all via combo: {verif_data['all_obtained']}; Tech pre-supplied: {verif_data['tech_pre_supplied']}
- Reason pre-check: Identified reason: {reason_data['identified_reason']}; Issue resolved in chat: {reason_data['issue_resolved']}; Requirement met: {reason_data['requirement_met']}; Detected issue: {reason_data['detected_issue'] or 'None'}
- Interaction pre-check: Proper language: {interaction_data['proper_language']}; Appropriate tone: {interaction_data['appropriate_tone']}; Accepts responsibility: {interaction_data['accepts_responsibility']}; Responsibility context present: {interaction_data['responsibility_context_present']}; Sets expectation: {interaction_data['sets_expectation']}; Core requirements met: {interaction_data['core_requirements_met']}; Responsibility met: {interaction_data['responsibility_met']}; All met: {interaction_data['all_met']}
- Time respect pre-check: Check-ins met: {time_respect_data['check_ins_met']}; No idle: {time_respect_data['no_idle']}; All met: {time_respect_data['all_met']}
- Needs pre-check: No redundant ask: {needs_data['no_redundant_ask']}
- Transfer pre-check: Asked voice services: {transfer_data['asked_voice']}

RULES (STRICT - no leniency):
1. FIRST RESPONSE TIME (5 points):
   - Must respond within 120 seconds AND obtain CBR (asked by agent or provided by customer) using ONE of these exact/similar phrases in ANY agent message or customer provision: "Could you please provide a contact number in case we get disconnected?", "May I have a callback number in case we get disconnected?", "Please provide a phone number in case we lose connection", "may i have your cbr please", or variants like "call back number" implying disconnection safety, or customer gives phone number.
   - Scoring: 5 = within 2min + CBR obtained (anywhere, asked or provided, per pre-check); 0 = neither or only one.

2. ACCOUNT VERIFICATION (10 points):
   - Ensure the record accessed aligns with the information given by the contact (no mismatches or guesses; confirm alignment via provisions/confirmations).
   - Obtain ONE of these combos (asked by agent or provided by technician/customer): (Name on Account + Service Address + Telephone Number) OR (Name on Account + Service Address + Account Number).
   - If not pre-supplied (check pre-supply flag), agent must ASK using phrasing close to: "Could you please provide the customer's account number or telephone number, and the name and address associated with the account?"
   - Scan ALL agent messages for asks. Customer must PROVIDE all in the combo (detect keywords like 'Account #: XXXX', 'Telephone #: XXXX', 'Name: XXX', 'Address: XXX', or confirm with 'Yes' after agent ask).
   - CRITICAL: If not pre-supplied, agent must ASK (don't assume). No credit if agent provides/guesses info without ask. Use EXACT phrasing or very close if asked.
   - Acceptable customer info: Account # (e.g., 12345678), Telephone # (e.g., 555-1234 or 10-digit), Name (e.g., John Smith or FARMERS MUTUAL INSURANCE ASSN), Address (e.g., 123 Main St, City, State, Zip), or 'Yes' confirming agent-provided name/address.
   - Scoring: 10 = Combo obtained (asked or provided) + customer provided all in combo (including via 'Yes') + record aligns; 0 = Any failure (e.g., missing combo, mismatch, improper phrasing if asked).
   - IMPORTANT: If pre-check shows all provided and pre-supplied true, score 10 if alignment confirmed.

3. CUSTOMER EXPECTATIONS AND NEEDS (5 points):
   - Identify the reason for the contact (e.g., No dial tone, bad pin, no MSS record, customer doesn't have IP, etc.).
   - The issue must be resolved during the chat (either by agent actions or technician providing solution).
   - NO NEED for agent to demonstrate understanding through restatement if the problem gets fixed.
   - Scoring: 5 = Reason identified + Issue resolved in chat; 0 = Missing identification OR issue not resolved.

4. CUSTOMER INTERACTION AND ACCEPTING RESPONSIBILITY (5 points):
   - Use appropriate verbiage/tone during contact (MUST - no slang, profanity, or negative language).
   - Accept responsibility ONLY WHERE APPLICABLE (when company/department errors are mentioned in conversation).
   - Setting expectations is RECOMMENDED but NOT REQUIRED for scoring.
   - Scoring breakdown:
     - Appropriate tone and language: REQUIRED (2.5 points)
     - Accepts responsibility WHEN CONTEXT EXISTS: REQUIRED (2.5 points)
     - If no responsibility context exists, agent gets full 5 points for appropriate tone/language
   - Scoring: 
       5 = Appropriate tone/language + (Accepts responsibility IF context exists)
       0 = Inappropriate tone/language OR (responsibility context exists AND agent doesn't accept responsibility)

5. CUSTOMER EXPERIENCE/ RESPECTFUL OF CUSTOMER'S TIME (10 points):
   - Check in with the tech every 5 minutes on chat and 3 minutes on call. Maintain control of the chat/call and guide the conversation. TAC Agent should refrain from distracting activities and should not sit idle without reason for over 5 minute.
   - Scoring: 10 = All met per pre-check (check-ins met, no idle); 0 = Any failure.

6. IDENTIFY CONTACT'S NEEDS AND AVOID REDUNDANT ASKS (5 points):
   - Identify the contact's needs and avoid asking for information that has been provided in the transcript, chat history, or accessible on the account. Have efficient chat/call flow. Avoid repeating information that the contact already understands.
   - Scoring: 5 = No redundant asks per pre-check; 0 = Any failure.

7. PROPER TRANSFER/VOICE SERVICES QUESTION (10 points):
   - Agent must ask about voice services provisioning using phrases like: "Do you need any voice services provisioned?", "voice services provisioned", or "provision voice services".
   - Scoring: 10 = Asked voice services question; 0 = Not asked.

ENFORCEMENT:
- Base on pre-checks but refine if nuances (e.g., 'Yes' confirmations, 10-digit phone as account).
- If reason is identified and chat shows problem is fixed (by agent OR technician), give full marks.
- If no responsibility context exists in conversation, don't penalize for lack of responsibility acceptance.
- Reasoning must explain matches to rules/phrases.
- Use EXACT key names as in the structure (e.g., 'within_2_minutes', not 'response_within_2_minutes').

TRANSCRIPT:
{transcript}

Respond with ONLY valid JSON in this EXACT structure (no extra text):
{{
  "first_response_analysis": {{
    "response_time_seconds": {time_data['response_time_seconds']},
    "within_2_minutes": {str(time_data['within_2_minutes']).lower()},
    "callback_requested": "true or false based on transcript and pre-check",
    "score": number (0 or 5),
    "max_score": 5,
    "reasoning": "Brief explanation with phrase evidence"
  }},
  "security_verification_analysis": {{
    "agent_asked_for_combo": "true or false",
    "num_elements_asked": {verif_data['num_asked']},
    "customer_provided_all": "true or false",
    "record_aligned": "true or false",
    "score": number (0 or 10),
    "max_score": 10,
    "reasoning": "Brief explanation with detected asks/provisions, combo used, phrasing match, and alignment"
  }},
  "customer_needs_analysis": {{
    "identified_reason": "true or false",
    "issue_resolved": "true or false",
    "score": number (0 or 5),
    "max_score": 5,
    "reasoning": "Brief explanation with identified reason and resolution evidence"
  }},
  "interaction_analysis": {{
    "appropriate_tone": "true or false",
    "accepts_responsibility": "true or false",
    "responsibility_context_present": "true or false",
    "sets_expectation": "true or false",
    "score": number (0 or 5),
    "max_score": 5,
    "reasoning": "Brief explanation with tone evidence and responsibility context analysis"
  }},
  "time_respect_analysis": {{
    "check_ins_met": "true or false",
    "no_idle": "true or false",
    "score": number (0 or 10),
    "max_score": 10,
    "reasoning": "Brief explanation with timestamp evidence"
  }},
  "needs_identification_analysis": {{
    "no_redundant_ask": "true or false",
    "score": number (0 or 5),
    "max_score": 5,
    "reasoning": "Brief explanation with evidence"
  }},
  "transfer_analysis": {{
    "asked_voice_services": "true or false",
    "score": number (0 or 10),
    "max_score": 10,
    "reasoning": "Brief explanation with phrase evidence"
  }},
  "overall_scores": {{
    "total_score": sum of all,
    "max_possible_score": 45,
    "percentage_score": (total / 45 * 100) rounded to nearest int
  }}
}}"""