import string
import secrets
import hashlib
import bcrypt
from passlib.context import CryptContext
from passlib.exc import InvalidHashError

# Use bcrypt directly to avoid passlib/bcrypt version compatibility issues
# Fallback to passlib for verification if needed

def generate_temporary_password():
        alphabet = string.ascii_letters + string.digits + string.punctuation
        temporary = ''.join(secrets.choice(alphabet) for _ in range(12))
        return temporary

def hash_password(password: str) -> str:
        """
        Hash a password using SHA256 + bcrypt.
        
        The password is first hashed with SHA256 to create a fixed-length
        input (64 bytes) for bcrypt, which has a 72-byte limit.
        """
        # SHA256 produces a 64-character hex string (64 bytes)
        prehash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        # Convert to bytes for bcrypt (SHA256 hex is 64 bytes, well under 72-byte limit)
        prehash_bytes = prehash.encode('utf-8')
        
        # Use bcrypt directly to avoid passlib version issues
        # Generate salt and hash
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(prehash_bytes, salt)
        # Return as string (bcrypt returns bytes)
        return hashed.decode('utf-8')

def verify_password(password: str, hash: str) -> bool:
        """
        Verify a password against a stored hash.
        
        Args:
            password: Plain text password to verify
            hash: Stored password hash (should be a valid bcrypt hash)
            
        Returns:
            True if password matches, False otherwise
            
        Raises:
            ValueError: If the hash is malformed or invalid
        """
        # Check if hash is None or empty
        if not hash:
            raise ValueError("Password hash is empty or None. User may need to reset their password.")
        
        # Check if hash looks like a valid bcrypt hash (starts with $2a$, $2b$, or $2y$)
        if not (hash.startswith('$2a$') or hash.startswith('$2b$') or hash.startswith('$2y$')):
            raise ValueError(
                f"Invalid password hash format. Expected bcrypt hash, but got: {hash[:20]}... "
                "User may need to reset their password."
            )
        
        try:
            # SHA256 hash the password first (same as in hash_password)
            prehash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            prehash_bytes = prehash.encode('utf-8')
            
            # Use bcrypt directly to verify
            hash_bytes = hash.encode('utf-8')
            return bcrypt.checkpw(prehash_bytes, hash_bytes)
        except (ValueError, Exception) as e:
            raise ValueError(
                f"Malformed password hash in database. User may need to reset their password. "
                f"Error: {str(e)}"
            )

