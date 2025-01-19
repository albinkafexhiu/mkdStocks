from typing import List, Optional, Any
from sqlalchemy.orm import Session

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def execute_query(self, query: str, params: dict = None) -> List[Any]:
        try:
            result = self.db.execute(query, params or {})
            return result.fetchall()
        except Exception as e:
            print(f"Database error: {str(e)}")
            raise