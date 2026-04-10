from datetime import datetime

def validate_convert_date(date_str: str) -> int:
    """
    Valida uma data e retorna como INT YYYYMMDD.
    Aceita DD/MM/YYYY ou YYYY-MM-DD.
    """
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(date_str, fmt)
            return int(dt.strftime("%Y%m%d"))
        except ValueError:
            continue
    raise ValueError(f"Formato de data inválido: {date_str}")