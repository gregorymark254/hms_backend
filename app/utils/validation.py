import re

# Validates a phone number
def validate_phone(phone: str) -> (bool, str):
    phone = phone.strip()
    if phone.startswith('+'):
        phone = phone[1:]
    if phone.startswith('0'):
        phone = '254' + phone[1:]

    phone = re.sub(r'[^0-9]', '', phone)

    if len(phone) < 11 or len(phone) > 15:
        return False, phone

    return True, phone
