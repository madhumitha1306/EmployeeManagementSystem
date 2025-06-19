from hashlib import sha256

class Hash:
    @staticmethod
    def bcrypt(password: str):
        return sha256(password.encode()).hexdigest()

    @staticmethod
    def verify(hashed_password: str, plain_password: str):
        return hashed_password == sha256(plain_password.encode()).hexdigest()