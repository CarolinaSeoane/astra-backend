from bson import ObjectId
from datetime import datetime, UTC

class PostIt:
    def __init__(self, content, sprint_id, created_at=None, _id=None):
        self.id = _id if _id else ObjectId()
        self.content = content
        self.sprint_id = sprint_id
        self.created_at = created_at if created_at else datetime.now(UTC)

    def to_dict(self):
        return {
            "_id": str(self.id),
            "content": self.content,
            "sprint_id": self.sprint_id,
            "created_at": self.created_at.isoformat(),
        }