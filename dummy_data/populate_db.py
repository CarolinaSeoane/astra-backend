from bson import ObjectId

from dummy_data.db_helper import DBHelper

class Populate:
    org1_id = ObjectId()
    org2_id = ObjectId()

    user1_id = ObjectId()
    username1 = "CarolinaSeoane"
    pfp1 = "2"
    user2_id = ObjectId()
    username2 = "BelenSeoane"
    pfp2 = "5"

    team1_id = ObjectId()

    epic1_id = ObjectId()
    epic1_title = "Mejoras del Buscador"

    def __init__(self):
        self.helper = DBHelper()

    def populate(self):
        self.helper.drop_db()
        self.populate_organizations()
        self.populate_users()
        self.populate_teams()
        self.populate_epics()
        self.populate_stories()

    def populate_organizations(self):
        organizations = [
            {
                "_id": self.org1_id, 
                "name": "Google",
                "logo": "google.jpg",
                "epics": [self.epic1_id]
            },
            {   
                "_id": self.org2_id,
                "name": "Astra",
                "logo": "astra.jpg",
                "epics": []
            }
        ]
        self.helper.post_to_collection("organizations", organizations)
        print("populated organizations")

    def populate_users(self):
        users = [
            {
                "_id": self.user1_id,
                "name": "Carolina",
                "surname": "Seoane",
                "username": self.username1,
                "email": "carolina.b.seoane@gmail.com",
                "profile_picture": self.pfp1,
                "teams": [
                    {
                        "team": self.team1_id,
                        "name": "Argo",
                        "icon": "argo.jpg"
                    },
                ]
            },

            {
                "_id": self.user2_id,
                "name": "Belen",
                "surname": "Seoane",
                "username": self.username2,
                "email": "seoane.m.b@gmail.com",
                "profile_picture": self.pfp2,
                "teams": [
                    {
                        "team": self.team1_id,
                        "name": "Argo",
                        "icon": "argo.jpg"
                    },
                ]
            }
        ]
        self.helper.post_to_collection("users", users)
        print("populated users")
    
    def populate_teams(self):
        teams = [
            {
                "_id": self.team1_id,
                "name": "Argo",
                "logo": "argo.jpg",
                "organization": self.org1_id,
                "team_settings": {
                    "sprint_duration": "2",
                    "sprint_begins_on": 0,
                    "estimation_method": ["Fibonacci"],
                    "mandatory_story_fields": ["acceptance_criteria", "title", "description", "story_points"],
                    "permits": [
                        {
                            "role": "Product Owner",
                            "options": {
                                "edit_story": True,
                                "delete_story": False,
                                "add_team_members": False,
                                "join_standup": False,
                                "all_time_metrics": True
                            }
                        },
                        {
                            "role": "Developer",
                            "options": {
                                "create_story": True,
                                "edit_story": True
                            }
                        }
                    ]
                },
                "members": [
                    {
                        "user": self.user1_id,
                        "role": "Developer",
                        "date": self.user1_id.generation_time
                    },
                    {
                        "user": self.user2_id,
                        "role": "Scrum Master",
                        "date": self.user2_id.generation_time
                    }
                ]
            }
        ]
        self.helper.post_to_collection("teams", teams)
        print("populated teams")
    
    def populate_epics(self):
        epics = [
            {
                "_id": self.epic1_id,
                "title": self.epic1_title,
                "description": "Mejorar la precision del buscador para mejorar la experiencia de los usuarios.",
                "sprints": "1,2",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1
                },
                "priority": "High"
            }
        ]
        self.helper.post_to_collection("epics", epics)
        print("populated epics")

    def populate_stories(self):
        stories = [
            {
                "title": "Mejorar la busqueda de acuerdo a busquedas recientes",
                "description": "Como usuario quiero que el buscador tenga en cuenta mis busquedas recientes para obtener resultados mas precisos",
                "acceptance_criteria": "La busqueda devuelve resultados mas precisos segun el historial del usuario",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1
                },
                "assigned_to": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                },
                "sprint": "1",
                "story_points": "5",
                "tags": ["Buscador"],
                "priority": "Medium",
                "type": "Feature",
                "estimation_method": "Fibonacci",
                "tasks": [
                    {
                        "title": "Revisar implementacion de libreria",
                        "description": "Ajustar parametros de la libreria de busqueda",
                        "app": "GOOGLE-SEARCH",
                        "status": "Doing"
                    }
                ],
                "team": self.team1_id
            }
        ]
        self.helper.post_to_collection("stories", stories)
        print("populated stories")
