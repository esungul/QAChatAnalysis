import re
from typing import Optional

def parse_timestamp(timestamp_str: str) -> Optional[int]:
    """Parse timestamp formats like '0 s', '1 m 28 s', '120' into seconds."""
    try:
        clean_ts = re.sub(r'[^\d\s m s]', '', timestamp_str).strip()
        parts = re.findall(r'(\d+)\s*(m|s)', clean_ts)
        
        if not parts:
            digits = re.findall(r'\d+', clean_ts)
            if digits:
                return int(digits[0])
            return None
        
        total = 0
        for num, unit in parts:
            total += int(num) * (60 if unit == 'm' else 1)
        return total
    except:
        return None