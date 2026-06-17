from pwdlib import PasswordHash # library for hashing passwords

password_hash = PasswordHash.recommended()


class Hash():
    def encrypt(password:str): # ye function password ko hash karega aur usko return karega taki usko database me store kar sake
        return password_hash.hash(password)
    

    def verify(hashed_password,plain_password): # ye function hashed password ko verify karega aur agar password match karega to true return karega aur agar password match nahi karega to false return karega
     return password_hash.verify(plain_password,hashed_password)