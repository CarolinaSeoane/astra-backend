class PostIt:
    def __init__(self, content, team_id, category):
        self.content = content
        self.team_id = team_id
        self.category = category

    def to_dict(self):
        return {
            "content": self.content,
            "team_id": self.team_id,
            "category": self.category
        }