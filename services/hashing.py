from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher:
    @staticmethod
    def get_hash(value: str) -> str:
        return pwd_context.hash(value)
    
    @staticmethod
    def verify(value: str, hashed_value: str) -> str:
        return pwd_context.verify(value, hashed_value)