def encrypt(message, key):
    
    cipher = []
    for character in message.upper():
        if character.isalpha():
            cipher.append(chr((ord(character) + ord(key.upper())) % 26 + 65))
        else:
            cipher.append(character)
    return "".join(cipher)

def decrypt(cipher, key):
    
    message = []
    for character in cipher.upper():
        if character.isalpha():
            message.append(chr((ord (character) - ord(key.upper())) % 26 + 65))
        else:
            message.append(character)
    return "".join(message)

print decrypt(encrypt("B ONJOuR", "B"), "b")