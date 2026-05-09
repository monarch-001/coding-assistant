import aiosqlite
import json
from datetime import datetime
from typing import List, Dict, Any

class MemoryManager:
    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = db_path

    async def initialize(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS threads (
                    id TEXT PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    thread_id TEXT,
                    role TEXT,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(thread_id) REFERENCES threads(id)
                )
            """)
            await db.commit()

    async def create_thread(self, thread_id: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("INSERT OR IGNORE INTO threads (id) VALUES (?)", (thread_id,))
            await db.commit()

    async def add_message(self, thread_id: str, role: str, content: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO messages (thread_id, role, content) VALUES (?, ?, ?)",
                (thread_id, role, content)
            )
            await db.commit()

    async def get_messages(self, thread_id: str) -> List[Dict[str, str]]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT role, content FROM messages WHERE thread_id = ? ORDER BY created_at ASC",
                (thread_id,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [{"role": row[0], "content": row[1]} for row in rows]
