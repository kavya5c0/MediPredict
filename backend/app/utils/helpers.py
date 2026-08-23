import os
from datetime import datetime
from typing import Optional

def ensure_directory_exists(path: str):
    """Ensure a directory exists, create if it doesn't"""
    os.makedirs(path, exist_ok=True)

def get_timestamp() -> str:
    """Get current timestamp as string"""
    return datetime.utcnow().isoformat()

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove path separators and special characters
    filename = filename.replace('/', '_').replace('\\', '_')
    filename = ''.join(c for c in filename if c.isalnum() or c in '._-')
    return filename

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"
