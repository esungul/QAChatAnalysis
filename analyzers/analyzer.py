import json
import re
from typing import Dict, Any
from config import client  # Import global client
from analyzers.prompt_builder import build_smart_prompt
from utils.detectors import calculate_response_time, pre_check_verification, pre_check_reason_identification, pre_check_callback, pre_check_interaction, pre_check_time_respect, pre_check_needs, pre_check_transfer  # Added missing imports
from utils.masker import mask_sensitive_data  # Import for masking

def analyze_transcript(transcript: str, model: str = "gpt-4o-mini") -> Dict[str, Any]:
    result = {}  # Initialize result at the very beginning to avoid UnboundLocalError
    
    try:
        masked_transcript = mask_sensitive_data(transcript)  # Mask for security
        prompt = build_smart_prompt(masked_transcript)  # Use masked
        
        result['sent_prompt'] = prompt  # Add sent prompt for debug
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=800
        )
        
        response_text = response.choices[0].message.content.strip()
        result['raw_response'] = response_text  # Add raw response
        
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)
        
        if json_match:
            parsed = json.loads(json_match.group())
            result.update(parsed)
            
            # Updated sections list to include all KPIs
            sections = [
                'first_response_analysis', 
                'security_verification_analysis', 
                'customer_needs_analysis',
                'interaction_analysis',
                'time_respect_analysis',
                'needs_identification_analysis',
                'transfer_analysis'  # Added transfer analysis
            ]
            
            missing_sections = [sec for sec in sections if sec not in result]
            if missing_sections:
                result['partial_error'] = f"Missing sections: {missing_sections}"
            
            for section in sections:
                if section in result:
                    if 'score' not in result[section]:
                        result[section]['score'] = 0
                    else:
                        result[section]['score'] = int(result[section]['score'])
                    if 'reasoning' not in result[section]:
                        result[section]['reasoning'] = "No reasoning provided by LLM"
            
            # Calculate overall_scores if missing or update max possible score
            if 'overall_scores' not in result:
                total = sum(result.get(sec, {}).get('score', 0) for sec in sections)
                result['overall_scores'] = {
                    'total_score': total,
                    'max_possible_score': 45,  # Updated from 20 to 45 (added KPIs)
                    'percentage_score': round((total / 45) * 100)  # Updated denominator
                }
            else:
                # Update max possible score if it exists but is old value
                if result['overall_scores'].get('max_possible_score', 0) == 20:
                    result['overall_scores']['max_possible_score'] = 45
                    total = result['overall_scores']['total_score']
                    result['overall_scores']['percentage_score'] = round((total / 45) * 100)
        
        else:
            result['error'] = "No valid JSON found - Using pre-check fallbacks"
            
            # Fallback First Response
            pre_calc = calculate_response_time(transcript)
            cbr = pre_check_callback(transcript)
            first_score = 5 if pre_calc['within_2_minutes'] and cbr else 0
            result['first_response_analysis'] = {
                'response_time_seconds': pre_calc['response_time_seconds'],
                'within_2_minutes': str(pre_calc['within_2_minutes']).lower(),
                'callback_requested': str(cbr).lower(),
                'score': first_score,
                'max_score': 5,
                'reasoning': f"Fallback: Within time {pre_calc['within_2_minutes']}; CBR {cbr}"
            }
            
            # Fallback Verification
            pre_verif = pre_check_verification(transcript)
            verif_score = 10 if pre_verif['num_asked'] >= 3 and pre_verif['all_obtained'] else 0  # Fixed: all_obtained instead of all_provided
            result['security_verification_analysis'] = {
                'agent_asked_for_combo': str(pre_verif['num_asked'] >= 3).lower(),
                'num_elements_asked': pre_verif['num_asked'],
                'customer_provided_all': str(pre_verif['all_obtained']).lower(),  # Fixed: all_obtained
                'record_aligned': 'true',  # Assume true if provided; refine if needed
                'score': verif_score,
                'max_score': 10,
                'reasoning': f"Fallback: Asked {pre_verif['num_asked']}/3; Provided {pre_verif['all_obtained']}"  # Fixed: all_obtained
            }
            
            # Fallback Needs 
            # Fallback Needs
            pre_reason = pre_check_reason_identification(transcript)
            needs_score = 5 if pre_reason['identified_reason'] and pre_reason['issue_resolved'] else 0
            result['customer_needs_analysis'] = {
                'identified_reason': str(pre_reason['identified_reason']).lower(),
                'issue_resolved': str(pre_reason['issue_resolved']).lower(),
                'score': needs_score,
                'max_score': 5,
                'reasoning': f"Fallback: Identified {pre_reason['identified_reason']}; Issue resolved {pre_reason['issue_resolved']}"
            }
            
          

            # Fallback Interaction
            # Fallback Interaction
            pre_interaction = pre_check_interaction(transcript)
            # Agent gets 5 points if: appropriate tone AND (no responsibility context OR accepts responsibility when context exists)
            interaction_score = 5 if pre_interaction['all_met'] else 0
            result['interaction_analysis'] = {
                'appropriate_tone': str(pre_interaction['appropriate_tone']).lower(),
                'accepts_responsibility': str(pre_interaction['accepts_responsibility']).lower(),
                'responsibility_context_present': str(pre_interaction['responsibility_context_present']).lower(),
                'sets_expectation': str(pre_interaction['sets_expectation']).lower(),
                'score': interaction_score,
                'max_score': 5,
                'reasoning': f"Fallback: Tone {pre_interaction['appropriate_tone']}; Responsibility context {pre_interaction['responsibility_context_present']}; Responsibility accepted {pre_interaction['accepts_responsibility']}; All met: {pre_interaction['all_met']}"
            }
                        
            
            # Fallback Time Respect
            pre_time_respect = pre_check_time_respect(transcript)
            time_respect_score = 10 if pre_time_respect['all_met'] else 0
            result['time_respect_analysis'] = {
                'check_ins_met': str(pre_time_respect['check_ins_met']).lower(),
                'no_idle': str(pre_time_respect['no_idle']).lower(),
                'score': time_respect_score,
                'max_score': 10,
                'reasoning': f"Fallback: Check-ins {pre_time_respect['check_ins_met']}; No idle {pre_time_respect['no_idle']}"
            }
            
            # Fallback Needs Identification
            pre_needs = pre_check_needs(transcript)
            needs_ident_score = 5 if pre_needs['no_redundant_ask'] else 0
            result['needs_identification_analysis'] = {
                'no_redundant_ask': str(pre_needs['no_redundant_ask']).lower(),
                'score': needs_ident_score,
                'max_score': 5,
                'reasoning': f"Fallback: No redundant ask {pre_needs['no_redundant_ask']}"
            }
            
            # Fallback Transfer
            pre_transfer = pre_check_transfer(transcript)
            transfer_score = 10 if pre_transfer['asked_voice'] else 0
            result['transfer_analysis'] = {
                'asked_voice_services': str(pre_transfer['asked_voice']).lower(),
                'score': transfer_score,
                'max_score': 10,
                'reasoning': f"Fallback: Asked voice services: {pre_transfer['asked_voice']}"
            }
            
            
            # Overall from fallback scores
            total = first_score + verif_score + needs_score + interaction_score + time_respect_score + needs_ident_score + transfer_score
            result['overall_scores'] = {
                'total_score': total,
                'max_possible_score': 45,  # Updated from 20 to 45
                'percentage_score': round((total / 45) * 100)
            }
        
        # Add pre-data always
        result['pre_calculated'] = calculate_response_time(transcript)
        result['pre_verification'] = pre_check_verification(transcript)
        result['pre_reason'] = pre_check_reason_identification(transcript)
        result['pre_interaction'] = pre_check_interaction(transcript)
        result['pre_time_respect'] = pre_check_time_respect(transcript)
        result['pre_needs'] = pre_check_needs(transcript)
        result['pre_transfer'] = pre_check_transfer(transcript)  # Added pre_transfer data
        result['masked_transcript'] = masked_transcript
        
        return result
        
    except Exception as e:
        result['error'] = str(e)
        result['api_error'] = str(e)  # For debug
        
        # Add pre-data on error
        result['pre_calculated'] = calculate_response_time(transcript)
        result['pre_verification'] = pre_check_verification(transcript)
        result['pre_reason'] = pre_check_reason_identification(transcript)
        result['pre_interaction'] = pre_check_interaction(transcript)
        result['pre_time_respect'] = pre_check_time_respect(transcript)
        result['pre_needs'] = pre_check_needs(transcript)
        result['pre_transfer'] = pre_check_transfer(transcript)  # Added pre_transfer data on error
        
        return result