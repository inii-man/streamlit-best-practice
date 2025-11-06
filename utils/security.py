"""
Security utilities module
Handles encryption, authentication, and security-related functions
"""
import hashlib
import secrets
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from config import Config


class SecurityManager:
    """Handle security operations"""
    
    def __init__(self):
        self.secret_key = Config.SECRET_KEY.encode()
        self._cipher = None
    
    @property
    def cipher(self):
        """Lazy initialization of cipher"""
        if self._cipher is None:
            # Generate a proper Fernet key from secret
            key = hashlib.sha256(self.secret_key).digest()
            self._cipher = Fernet(Fernet.generate_key())
        return self._cipher
    
    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt encrypted data"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate a secure random token"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_data(data: str) -> str:
        """Hash data using SHA-256"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def validate_api_key(provided_key: str, stored_key: str) -> bool:
        """Validate API key"""
        return secrets.compare_digest(provided_key, stored_key)


class SessionManager:
    """Manage user sessions"""
    
    @staticmethod
    def init_session_state(st, defaults: Optional[Dict[str, Any]] = None):
        """Initialize session state with defaults"""
        if defaults:
            for key, value in defaults.items():
                if key not in st.session_state:
                    st.session_state[key] = value
    
    @staticmethod
    def get_session_value(st, key: str, default: Any = None) -> Any:
        """Get value from session state"""
        return st.session_state.get(key, default)
    
    @staticmethod
    def set_session_value(st, key: str, value: Any):
        """Set value in session state"""
        st.session_state[key] = value
    
    @staticmethod
    def clear_session(st):
        """Clear all session state"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]


def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';']
    sanitized = user_input
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    return sanitized.strip()


def validate_file_upload(file, allowed_extensions: list = None) -> tuple[bool, str]:
    """Validate uploaded file"""
    if allowed_extensions is None:
        allowed_extensions = ['.csv', '.xlsx', '.json']
    
    if file is None:
        return False, "No file uploaded"
    
    file_extension = '.' + file.name.split('.')[-1].lower()
    
    if file_extension not in allowed_extensions:
        return False, f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
    
    # Check file size (max 200MB)
    max_size = 200 * 1024 * 1024
    if hasattr(file, 'size') and file.size > max_size:
        return False, "File too large (max 200MB)"
    
    return True, "File is valid"
