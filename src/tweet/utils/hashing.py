from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class HashPassword:
    """Utility class for hashing and verifying passwords."""
    
    @staticmethod
    def bcrypt(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hashed password."""
        return pwd_context.verify(plain_password, hashed_password)