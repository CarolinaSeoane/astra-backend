from app.db_connection import mongo
from bson import ObjectId
from app.models.story import Story

class Card:
    def __init__(self, story_id, title, team_id, sprint_id, assigned=None, category=None, _id=None):
        self._id = _id
        self.story_id = story_id  
        self.title = title         
        self.team_id = team_id          
        self.assigned = assigned    
        self.category = category    
        self.sprint_id = sprint_id  
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            story_id=data.get("story_id"),
            title=data.get("title"),
            team_id=data.get("team_id"),
            assigned=data.get("assigned"),
            category=data.get("category"),
            sprint_id=data.get("sprint_id"),
            _id=data.get("_id")
        )

    def to_dict(self):
        card_dict = {
            "story_id": self.story_id,
            "title": self.title,
            "team_id": self.team_id,
            "assigned": self.assigned,
            "category": self.category, 
            "sprint_id": self.sprint_id,
        }
        if self._id:
            card_dict["_id"] = self._id
        return card_dict
    
    @staticmethod
    def from_story_and_team(story, team_id):
        return {
            "title": story['title'],  
            "team_id": team_id,
            "sprint_id": str(story['sprint']['_id']),
            "story_id": str(story.get('_id')),  
            "category": "Backlog",
            "assigned": str(story['assigned_to']['_id'])
        }
    
    @staticmethod
    def create_card(card_data):
        try:

            card = Card(
                title=card_data['title'],
                team_id=card_data['team_id'],
                sprint_id=card_data.get('sprint_id'),
                story_id=card_data['story_id'],
                category=card_data.get('category', "Backlog"),
                assigned=card_data.get('assigned'),
            )
            
            card_dict = card.to_dict()
            result = mongo.db.cards.insert_one(card_dict)  
            card._id = str(result.inserted_id) 

            return card 
        except Exception as e:
            raise Exception(f"Failed to create card: {e}")
        
    @staticmethod
    def update_card(story_id, card_data):
        try:

            print("update storyID", story_id)
            print("update assignedID", card_data['assigned'])
            print("update sprintID", card_data['sprint_id'])
        
            result = mongo.db.cards.update_one(
                {"story_id": story_id}, 
                {"$set": {
                    "title": card_data['title'],
                    "assigned": card_data['assigned'],
                    "sprint_id": card_data['sprint_id'], 
                }}
            )
            return result.modified_count  
        except Exception as e:
            raise Exception(f"Failed to update card: {e}")
    
    @staticmethod
    def delete_card(story_id):
        try:
            story_document = Story.get_story_by_id(story_id)

            if not story_document:
                raise Exception("Story not found.")

            mongo_id = story_document["_id"]
            if isinstance(mongo_id, dict) and "$oid" in mongo_id:
                mongo_id = ObjectId(mongo_id["$oid"])
            else:
                mongo_id = ObjectId(mongo_id)  

            print("mongo_id:", mongo_id)

            result = mongo.db.cards.delete_one({"story_id": str(mongo_id)}) 

            if result.deleted_count == 0:
                raise Exception("No card found with the given mongo_id.")
            
            return result.deleted_count  
        except Exception as e:
            raise Exception(f"Failed to delete card: {e}")
        