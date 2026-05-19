import sqlite3
import os
from pathlib import Path

class RAGMemory:
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Default to data/chat.db relative to the project root
            self.db_path = Path(__file__).parent.parent.parent.parent / "data" / "chat.db"
        else:
            self.db_path = Path(db_path)
            
        # Ensure the directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rag_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT,
                query TEXT,
                answer TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def add_history(self, thread_id: str, query: str, answer: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO rag_history (thread_id, query, answer) VALUES (?, ?, ?)",
            (thread_id, query, answer)
        )
        conn.commit()
        conn.close()

    def get_history(self, thread_id: str, limit: int = 5) -> str:
        if not thread_id:
            return ""
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT query, answer FROM rag_history WHERE thread_id = ? ORDER BY timestamp DESC LIMIT ?",
            (thread_id, limit)
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return ""

        history_str = "\nPrevious Conversation History:\n"
        # Reverse to show in chronological order
        for q, a in reversed(rows):
            history_str += f"User: {q}\nAI: {a}\n"
        
        return history_str
