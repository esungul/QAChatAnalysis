import re

def mask_sensitive_data(transcript: str) -> str:
    """Mask PII in transcript for security before LLM/API call."""
    # Mask phones (10-digit or similar)
    transcript = re.sub(r'\b\d{10}\b', '[PHONE]', transcript)
    # Mask names (capitalized words pattern; refine if needed)
    transcript = re.sub(r'\b[A-Z]{2,}\s+[A-Z]{2,}(\s+[A-Z]{2,})?\b', '[NAME]', transcript)
    # Mask addresses (refined to require street indicators, avoid timestamps like '1 m 30 s')
    transcript = re.sub(r'\d+\s+[A-Z0-9\s]+(?:ST|AVE|RD|BLVD|DR|LN|CT|PL|WAY|CIR|STREET|AVENUE|ROAD|BOULEVARD|DRIVE|LANE|COURT|PLACE|WAY|CIRCLE)\b', '[ADDRESS]', transcript, flags=re.I)
    # Mask accounts/SIDs (8+ digits, but avoid if in timestamp context)
    transcript = re.sub(r'\b(?! \s*[m s]\b)\d{8,}\b', '[ACCOUNT]', transcript)
    # Add more patterns as needed (e.g., emails: r'\b[\w\.-]+@[\w\.-]+\.\w+\b' -> '[EMAIL]')
    return transcript