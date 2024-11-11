from bson import ObjectId
from app.models.configurations import CollectionNames
from app.services.mongoHelper import MongoHelper


POST_ITS_COL = CollectionNames.POST_ITS.value


class PostIt:
    def __init__(self, content, team_id, category, ceremony_id=None, _id=None):
        self._id = _id
        self.content = content
        self.team_id = team_id
        self.category = category
        self.ceremony_id = ceremony_id

    @classmethod
    def from_dict(cls, data):
        return cls(
            content=data.get("content"),
            team_id=data.get("team_id"),
            category=data.get("category"),
            ceremony_id=data.get("ceremony_id"),
            _id=data.get("_id")
        )

    def to_dict(self):
        post_it_dict = {
            "content": self.content,
            "team_id": self.team_id,
            "category": self.category,
            "ceremony_id": self.ceremony_id  
        }
        if self._id:
            post_it_dict["_id"] = self._id
        return post_it_dict

    @staticmethod
    def create_post_it(new_post_it):
        post_it_dict = new_post_it.to_dict()
        result = MongoHelper().create_document(POST_ITS_COL, post_it_dict)
        post_it_dict["_id"] = str(result.inserted_id)
        return post_it_dict

    @staticmethod
    def update_post_it(new_post_it, post_it_id):
        match = {
            "_id": ObjectId(post_it_id),
            "team_id": new_post_it.team_id,
            "ceremony_id": new_post_it.ceremony_id
        }
        update_operation = {
            "$set": {
                "content": new_post_it.content,
                "category": new_post_it.category
            }
        }

        result = MongoHelper().update_document(POST_ITS_COL, match, update_operation)

        if result.matched_count == 0:
            return None

        new_post_it._id = post_it_id
        return new_post_it.to_dict()

    @staticmethod
    def delete_post_it(post_it_id, team_id, ceremony_id):
        match = {
            "_id": ObjectId(post_it_id),
            "team_id": team_id,
            "ceremony_id": ceremony_id
        }
        result = MongoHelper().delete_element_from_collection(POST_ITS_COL, match)

        if result.deleted_count == 0:
            return None
        return post_it_id

    @staticmethod
    def get_post_its(team_id, ceremony_id):
        match = {
            "team_id": team_id,
            "ceremony_id": ceremony_id
        }
        post_its_cursor = MongoHelper().get_documents_by(POST_ITS_COL, match)
        post_its = list(post_its_cursor)
        for post_it in post_its:
            post_it['_id'] = str(post_it['_id']['$oid'])
        return post_its
