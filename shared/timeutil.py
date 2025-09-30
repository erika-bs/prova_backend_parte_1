from datetime import datetime, timezone

def iso_utc(value=None) -> str:
    if not value:
        return datetime.now(timezone.utc).isoformat()
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat()
    if isinstance(value, str):
        return value 
    raise ValueError("Esperado datetime ou string ISO")