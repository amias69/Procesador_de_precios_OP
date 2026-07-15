from decimal import Decimal, InvalidOperation


def parse_price(value) -> Decimal | None:
    if value is None:
        return None

    text = str(value).strip().replace(",", ".")

    if text == "":
        return None

    try:
        return Decimal(text)
    except InvalidOperation:
        return None


def validate_price(value, field_name: str) -> list[str]:
    errors = []
    price = parse_price(value)

    if price is None:
        errors.append(f"{field_name} debe ser un valor numérico.")
        return errors

    if price <= 0:
        errors.append(f"{field_name} debe ser mayor que 0.")

    return errors


def format_price(value) -> str:
    price = parse_price(value)

    if price is None:
        raise ValueError("No se puede formatear un precio inválido.")

    return f"{price:.2f}"