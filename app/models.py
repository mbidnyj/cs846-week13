# User and Session Models

from dataclasses import dataclass, field
from typing import Optional
import uuid
import hashlib
import time

@dataclass
class User:
    username: str
    password_hash: str
    display_name: Optional[str] = None
    bio: Optional[str] = None

@dataclass
class Session:
    session_id: str
    username: str
    created_at: float = field(default_factory=lambda: time.time())

# In-memory storage
users = {}
sessions = {}

@dataclass
class Reply:
    reply_id: str
    author: str
    content: str
    created_at: float = field(default_factory=lambda: time.time())

@dataclass
class Post:
    post_id: str
    author: str
    content: str
    created_at: float = field(default_factory=lambda: time.time())
    updated_at: Optional[float] = None
    likes: set = field(default_factory=set)
    replies: list = field(default_factory=list)

posts = {}

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
