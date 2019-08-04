# Encruption Module

from Crypto.Cipher import AES

key = b"%&498Ks&FI&^%GHk"
cipher = AES.new(key)

def pad(s):
    return s + ((16 - len(s) % 16) * '{')

def encrypt(plainText):
    global cipher, key
    return cipher.encrypt(pad(plainText))

def decrypt(encryptedText):
    global cipher
    dec = cipher.decrypt(encryptedText).decode('utf-8')
    l = dec.count('{')
    return dec[:len(dec)-l]

'''
msg = input(" > ")
e = encrypt(msg)
print("Encrypted : ", e)
print("Decrypted : ", decrypt(e))
'''

