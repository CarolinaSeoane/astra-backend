class PostIt:
    def __init__(self, content, team_id, category, _id=None):

        self._id = _id
        self.content = content
        self.team_id = team_id
        self.category = category
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            content=data.get("content"),
            team_id=data.get("team_id"),
            category=data.get("category"),
            _id=data.get("_id")
        )
    def to_dict(self):
        post_it_dict = {
            "content": self.content,
            "team_id": self.team_id,
            "category": self.category
        }
        if self._id:
            post_it_dict["_id"] = self._id
        return post_it_dict