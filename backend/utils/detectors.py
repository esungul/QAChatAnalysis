import re
from typing import Dict, Any, Optional
import streamlit as st
from utils.parsers import parse_timestamp  # Import from sibling module

def pre_check_interaction(transcript: str) -> Dict[str, Any]:
    """Detect appropriate tone, communication, and context-dependent responsibility acceptance."""
    time_data = calculate_response_time(transcript)
    agent_id = time_data['first_agent_identifier'].lower() if time_data['first_agent_identifier'] else ''
    lines = [line.strip() for line in transcript.split('\n') if line.strip()]
    proper_language = True  # Assume true, flag if slang/profanity
    appropriate_tone = True  # Assume appropriate tone
    accepts_responsibility = False
    responsibility_context_present = False  # Flag if responsibility context exists in conversation
    sets_expectation = False
    
    st.write(f"Scanning for interaction quality...")
    
    for line in lines:
        match = re.match(r'\(\s*[^)]+\s*\):\s*([^:]+?):\s*(.*)', line)
        if not match:
            continue
        
        speaker, message = match.groups()
        speaker_lower = speaker.strip().rstrip(':').lower()
        msg_lower = message.lower()
        
        is_agent = speaker_lower == agent_id
        
        if is_agent:
            # Check for appropriate tone and communication
            if re.search(r'\bthanks?\b|\bplease\b|\bappreciate\b|\bhelp\b|\bassist\b', msg_lower, re.I):
                appropriate_tone = True
                st.write(f"Appropriate tone detected: '{message[:50]}...'")
            
            # Check for negative/inappropriate language
            if re.search(r'\bstupid\b|\bidiot\b|\brude\b|\bannoying\b|\bwhatever\b|\bnot my problem\b', msg_lower, re.I):
                appropriate_tone = False
                proper_language = False
                st.write(f"Inappropriate language detected: '{message[:50]}...'")
            
            # Check for expectation setting
            if re.search(r'\b(step|action|will take|process)\b.*(minute|time|soon|moment|while)\b', msg_lower, re.I):
                sets_expectation = True
                st.write(f"Expectation setting detected: '{message[:50]}...'")
            
            # Check for responsibility acceptance (only when context exists)
            if re.search(r'\bsorry\b|\bapologize\b|\binconvenience\b|\bwe will fix\b|\bour mistake\b|\bresponsibility\b', msg_lower, re.I):
                accepts_responsibility = True
                st.write(f"Responsibility acceptance detected: '{message[:50]}...'")
        
        # Check if responsibility context exists in the conversation (from customer or agent)
        if re.search(r'\bmistake\b|\berror\b|\bwrong\b|\bfault\b|\bissue\b.*company|\bproblem\b.*your', msg_lower, re.I):
            responsibility_context_present = True
            st.write(f"Responsibility context detected: '{message[:50]}...'")
    
    # Determine if all requirements are met
    # Core requirements: proper language and appropriate tone (MUST)
    core_requirements_met = proper_language and appropriate_tone
    
    # Responsibility is only required if context exists
    responsibility_required = responsibility_context_present
    responsibility_met = not responsibility_required or (responsibility_required and accepts_responsibility)
    
    # All met if core requirements + responsibility (if applicable) + expectation setting
    # But expectation setting is NOT mandatory - it's a nice-to-have but not required
    all_met = core_requirements_met and responsibility_met
    
    return {
        'proper_language': proper_language,
        'appropriate_tone': appropriate_tone,
        'accepts_responsibility': accepts_responsibility,
        'responsibility_context_present': responsibility_context_present,
        'sets_expectation': sets_expectation,
        'core_requirements_met': core_requirements_met,
        'responsibility_met': responsibility_met,
        'all_met': all_met,
        'reasoning': f"Language: {proper_language}; Tone: {appropriate_tone}; Responsibility context: {responsibility_context_present}; Responsibility accepted: {accepts_responsibility}; Expectation: {sets_expectation}"
    }

def pre_check_reason_identification(transcript: str) -> Dict[str, Any]:
    """Detect if agent identifies reason for contact and issue gets resolved."""
    time_data = calculate_response_time(transcript)
    agent_id = time_data['first_agent_identifier'].lower() if time_data['first_agent_identifier'] else ''
    lines = [line.strip() for line in transcript.split('\n') if line.strip()]
    identified_reason = False
    issue_resolved = False
    detected_issue = None
    resolution_indicators = []
    
    st.write(f"Scanning for reason identification and resolution...")
    
    for line in lines:
        match = re.match(r'\(\s*[^)]+\s*\):\s*([^:]+?):\s*(.*)', line)
        if not match:
            continue
        
        speaker, message = match.groups()
        speaker_clean = speaker.strip().rstrip(':')
        speaker_lower = speaker_clean.lower()
        msg_lower = message.lower()
        
        is_agent = (speaker_lower == agent_id) or (len(re.sub(r'[^a-zA-Z]', '', speaker_clean)) == 1 and not re.search(r'system', speaker_lower, re.I))
        
        # Detect identification of reason
        if is_agent:
            if re.search(r'reason for (contact|call|chat)|issue|problem|what can i help|how can i assist', msg_lower):
                identified_reason = True
                st.write(f"Reason identification detected: '{message[:50]}...'")
        
        # Detect specific issues
        if re.search(r'no dial tone|bad pin|no mss record|don\'t have IP|no ip|ip issue', msg_lower, re.I):
            detected_issue = message
            st.write(f"Specific issue detected: {detected_issue}")
        
        # Detect resolution indicators (from agent or technician)
        resolution_patterns = [
            r'problem (fixed|resolved|solved)',
            r'issue (fixed|resolved|solved)',
            r'working (now|fine)',
            r'resolved the (problem|issue)',
            r'fixed the (problem|issue)',
            r'completed.*successfully',
            r'good to go',
            r'all set',
            r'completed.*fix',
            r'resolved',
            r'fixed'
        ]
        
        for pattern in resolution_patterns:
            if re.search(pattern, msg_lower, re.I):
                resolution_indicators.append(message)
                issue_resolved = True
                st.write(f"Resolution indicator detected: '{message[:50]}...'")
                break

    # If reason is identified AND issue gets resolved in the chat, that's sufficient
    requirement_met = identified_reason and issue_resolved

    return {
        'identified_reason': identified_reason,
        'issue_resolved': issue_resolved,
        'requirement_met': requirement_met,
        'detected_issue': detected_issue,
        'resolution_indicators': resolution_indicators,
        'reasoning': f"Identified: {identified_reason}; Issue resolved in chat: {issue_resolved}; Requirement met: {requirement_met}"
    }


def pre_check_transfer(transcript: str) -> Dict[str, Any]:
    """Detect if agent asks voice services provisioned question."""
    time_data = calculate_response_time(transcript)
    agent_id = time_data['first_agent_identifier'].lower() if time_data['first_agent_identifier'] else ''
    lines = [line.strip() for line in transcript.split('\n') if line.strip()]
    asked_voice = False
    
    for line in lines:
        match = re.match(r'\(\s*[^)]+\s*\):\s*([^:]+?):\s*(.*)', line)
        if not match:
            continue
        
        speaker, message = match.groups()
        speaker_lower = speaker.strip().rstrip(':').lower()
        msg_lower = message.lower()
        
        is_agent = speaker_lower == agent_id
        
        if is_agent:
            # Check for voice services question
            if re.search(r'\bdo you need any voice services provisioned\b', msg_lower, re.I) or \
               re.search(r'\bvoice services.*provisioned\b', msg_lower, re.I) or \
               re.search(r'\bprovision.*voice services\b', msg_lower, re.I):
                asked_voice = True
                st.write(f"Asked voice services: '{message[:50]}...'")
                break  # Stop after first occurrence
    
    return {
        'asked_voice': asked_voice,
        'reasoning': f"Asked voice services: {asked_voice}"
    }

def pre_check_verification(transcript: str) -> Dict[str, Any]:
    """Enhanced: Detect customer provision (phone digits, confirmation 'Yes'). Check combos and if tech pre-supplied."""
    time_data = calculate_response_time(transcript)
    agent_id = time_data['first_agent_identifier'].lower() if time_data['first_agent_identifier'] else ''
    lines = [line.strip() for line in transcript.split('\n') if line.strip()]
    asked_account = False
    asked_phone = False
    asked_name = False
    asked_address = False
    customer_provided = {
        'account': False,
        'phone': False,
        'name': False,
        'address': False
    }
    tech_pre_supplied = False  # Flag if customer/tech provided info before agent ask
    
    st.write(f"Found {len(lines)} lines in transcript")
    st.write(f"Detected agent ID: '{agent_id}'")
    
    previous_line = None
    previous_msg_lower = None
    previous_was_agent = False
    
    for line in lines:
        match = re.match(r'\(\s*[^)]+\s*\):\s*([^:]+?):\s*(.*)', line)
        if not match:
            continue
        
        speaker, message = match.groups()
        speaker_clean = speaker.strip().rstrip(':')
        speaker_lower = speaker_clean.lower()
        speaker_len = len(re.sub(r'[^a-zA-Z]', '', speaker_clean))
        msg_lower = message.lower()
        
        is_agent = (speaker_lower == agent_id) or (speaker_len == 1 and not re.search(r'system', speaker_lower, re.I))
        if is_agent:
            if re.search(r'account number|account #', msg_lower):
                asked_account = True
                st.write(f"Agent ask account: '{message[:50]}...'")
            if re.search(r'telephone number|phone number', msg_lower):
                asked_phone = True
                st.write(f"Agent ask phone: '{message[:50]}...'")
            if re.search(r'name.*account', msg_lower):
                asked_name = True
                st.write(f"Agent ask name: '{message[:50]}...'")
            if re.search(r'service address|address.*account|address|street', msg_lower):
                asked_address = True
                st.write(f"Agent ask address: '{message[:50]}...'")
        
        elif not re.search(r'system', speaker_lower, re.I) and speaker_len > 1:
            st.write(f"Customer line: '{speaker}' - Msg starts: '{message[:50]}...'")
            # Check for pre-supply in customer messages
            if re.search(r'account #|sid|case #|\b\d{8,}\b', msg_lower):  # Account patterns
                customer_provided['account'] = True
                tech_pre_supplied = True
                st.write("-> Set account: True (pre-supplied)")
            if re.search(r'telephone|phone\s+\d|\b\d{10}\b', msg_lower):
                customer_provided['phone'] = True
                tech_pre_supplied = True
                st.write("-> Set phone: True (pre-supplied)")
            if re.search(r'\b[A-Z]{2,}\s+[A-Z]{2,}(\s+[A-Z]{2,})?\b', message):
                customer_provided['name'] = True
                tech_pre_supplied = True
                st.write("-> Set name: True (pre-supplied)")
            if re.search(r'address|street|city|state|zip', msg_lower):
                customer_provided['address'] = True
                tech_pre_supplied = True
                st.write("-> Set address: True (pre-supplied)")
            if previous_line and re.search(r'^\s*yes\s*$', msg_lower, re.I) and previous_was_agent and re.search(r'name|address|street|city|farmers|mutual|assn|st', previous_msg_lower, re.I):
                customer_provided['name'] = True
                customer_provided['address'] = True
                st.write("-> Set name/address: True (confirmation 'Yes')")
        
        previous_line = line
        previous_msg_lower = msg_lower
        previous_was_agent = is_agent
    
    # New: Determine asked/provided based on combos
    num_asked = sum([asked_name, asked_address, (asked_phone or asked_account)])
    combo1_obtained = customer_provided['name'] and customer_provided['address'] and customer_provided['phone']
    combo2_obtained = customer_provided['name'] and customer_provided['address'] and customer_provided['account']
    all_provided = combo1_obtained or combo2_obtained  # True if combo obtained (asked or pre-provided)
    
    st.write(f"Final provided flags: {customer_provided}")
    
    return {
        'asked_name': asked_name,
        'asked_address': asked_address,
        'asked_phone': asked_phone,
        'asked_account': asked_account,
        'num_asked': num_asked,
        'all_obtained': all_provided,
        'tech_pre_supplied': tech_pre_supplied,
        'reasoning': f"Asked {num_asked}/3 (with combo); Obtained all: {all_provided}; Pre-supplied: {tech_pre_supplied}"
    }

def pre_check_callback(transcript: str) -> bool:
    """Scan ALL agent messages for callback request phrases, including abbreviations like 'cbr'. Also detect if provided by customer if not asked."""
    time_data = calculate_response_time(transcript)
    agent_id = time_data['first_agent_identifier'].lower() if time_data['first_agent_identifier'] else ''
    if not agent_id:
        return False
    
    lines = [line.strip() for line in transcript.split('\n') if line.strip()]
    phrases = [
        r"contact number.*disconnected",
        r"callback number.*disconnected",
        r"phone number.*lose connection",
        r"disconnected\?",
        r"cbr",  # Detect 'cbr' as callback abbreviation
        r"call back.*number",  # Handle 'call back' expansion
        r"callback.*(number|phone)"  # Flexible for 'callback' variants
    ]
    
    asked = False
    provided = False
    
    for line in lines:
        match = re.match(r'\(\s*[^)]+\s*\):\s*([^:]+?):\s*(.*)', line)
        if not match:
            continue
        
        speaker, message = match.groups()
        speaker_clean = speaker.strip().rstrip(':')
        speaker_lower = speaker_clean.lower()
        msg_lower = message.lower()
        
        is_agent = (speaker_lower == agent_id) or (len(re.sub(r'[^a-zA-Z]', '', speaker_clean)) == 1 and not re.search(r'system', speaker_lower, re.I))
        
        if is_agent:
            for phrase in phrases:
                if re.search(phrase, msg_lower, re.I):
                    asked = True
                    st.write(f"Callback asked in agent message: '{message[:50]}...' (matched phrase: {phrase})")
                    return True
        else:  # Customer line
            if re.search(r'(cbr|callback|phone|contact|number)\s*(\:|\b)?\s*(\d{10}|\[PHONE\])', msg_lower, re.I):  # Refined: Detect 'CBR:' + number or masked
                provided = True
                st.write(f"Callback provided by customer: '{message[:50]}...'")
    
    return asked or provided


def pre_check_time_respect(transcript: str) -> Dict[str, Any]:
    """Check check-ins and idle time using timestamps."""
    lines = [line.strip() for line in transcript.split('\n') if line.strip()]
    timestamps = []
    is_chat = True  # Assume chat; detect call if voice keywords
    check_in_interval = 5 * 60 if is_chat else 3 * 60  # seconds
    idle_max = 299
    last_time = 0
    check_ins_met = True
    no_idle = True
    
    for line in lines:
        match = re.match(r'\(\s*([^)]+)\s*\):\s*([^:]+?):\s*(.*)', line)
        if match:
            timestamp_str = match.group(1)
            seconds = parse_timestamp(timestamp_str)
            if seconds is not None:
                timestamps.append(seconds)
                if seconds - last_time > idle_max:
                    no_idle = False
                last_time = seconds
    
    for i in range(1, len(timestamps)):
        if timestamps[i] - timestamps[i-1] > check_in_interval:
            check_ins_met = False
    
    all_met = check_ins_met and no_idle
    return {
        'check_ins_met': check_ins_met,
        'no_idle': no_idle,
        'all_met': all_met,
        'reasoning': f"Check-ins: {check_ins_met}; No idle: {no_idle}"
    }

def pre_check_needs(transcript: str) -> Dict[str, Any]:
    """Check no redundant asks, efficient flow."""
    time_data = calculate_response_time(transcript)
    agent_id = time_data['first_agent_identifier'].lower()
    lines = [line.strip() for line in transcript.split('\n') if line.strip()]
    provided_info = set()
    redundant_ask = False
    
    for line in lines:
        match = re.match(r'\(\s*[^)]+\s*\):\s*([^:]+?):\s*(.*)', line)
        if match:
            speaker, message = match.groups()
            speaker_lower = speaker.strip().rstrip(':').lower()
            msg_lower = message.lower()
            
            is_agent = speaker_lower == agent_id
            
            if not is_agent:
                if re.search(r'account|phone|name|address', msg_lower):
                    provided_info.add('info')
            else:
                if 'info' in provided_info and re.search(r'provide|what is|can you give', msg_lower):
                    redundant_ask = True
    
    all_met = not redundant_ask
    return {
        'no_redundant_ask': all_met,
        'reasoning': f"No redundant: {all_met}"
    }

def calculate_response_time(transcript: str) -> Dict[str, Any]:
    """Prioritize single-character speakers for agent ID, avoid skipping legitimate asks."""
    lines = [line.strip() for line in transcript.split('\n') if line.strip()]
    
    system_time = None
    first_agent_time = None
    first_agent_identifier = None
    first_agent_message = None
    
    for line in lines:
        match = re.match(r'\(\s*([^)]+)\s*\):\s*([^:]+?):\s*(.*)', line)
        if not match:
            continue
        
        timestamp_str, speaker, message = match.groups()
        seconds = parse_timestamp(timestamp_str)
        if seconds is None:
            continue
        
        speaker_clean = speaker.strip().rstrip(':')
        speaker_lower = speaker_clean.lower()
        speaker_len = len(re.sub(r'[^a-zA-Z]', '', speaker_clean))
        message_lower = message.lower()
        
        if system_time is None and 'system' in speaker_lower:
            system_time = seconds
            continue
        
        is_excluded = re.search(r'(customer|user|client|system)', speaker_lower, re.I)
        is_long_speaker = speaker_len > 1
        is_provision_like = (re.search(r'(customer phone|address:|name on|sid number|case #)', message_lower) or 
                             (re.search(r'\b[A-Z]{2,}\s+[A-Z]{2,}\b', message) and 
                              not re.search(r'thank you|hello|provide|the customer', message_lower, re.I)))
        
        if (system_time is not None and first_agent_time is None and
            not is_excluded and not is_long_speaker and not is_provision_like):
            
            first_agent_time = seconds
            first_agent_identifier = speaker_clean
            first_agent_message = message
            st.write(f"Identified agent: '{speaker_clean}' (len={speaker_len}, msg='{message[:30]}...')")
            break
    
    response_time = first_agent_time - system_time if system_time is not None and first_agent_time is not None else None
    
    return {
        'system_time_seconds': system_time,
        'first_agent_time_seconds': first_agent_time,
        'response_time_seconds': response_time,
        'within_2_minutes': response_time is not None and response_time <= 120,
        'first_agent_identifier': first_agent_identifier,
        'first_agent_message': first_agent_message
    }