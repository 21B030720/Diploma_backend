import os


def upload_to(instance, prefix, filename):
    path = os.path.join(prefix, filename)
    return path


def only_digits_phone_number(phone_number: str):
    new_phone = ''.join(number for number in phone_number if number.isdigit())
    if new_phone:
        new_phone = '7' + new_phone[1:]
    return new_phone


def convert_phone_number(phone_number: str):
    return f'+{phone_number[0]} {phone_number[1:4]} {phone_number[4:7]} {phone_number[7:9]} {phone_number[9:11]}'
