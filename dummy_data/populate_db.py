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
    team2_id = ObjectId()

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
        self.populate_story_fields()

    def populate_organizations(self):
        organizations = [
            {
                "_id": self.org1_id, 
                "name": "Google",
                "epics": [self.epic1_id]
            },
            {   
                "_id": self.org2_id,
                "name": "IBM",
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
                        "_id": self.team1_id,
                        "name": "Argo",
                    },
                    {
                        "_id": self.team2_id,
                        "name": "Flyers",
                    }
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
                        "_id": self.team1_id,
                        "name": "Argo"
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
                "organization": self.org1_id,
                "team_settings": {
                    "ceremonies": {
                        "planning": {
                            "days": [1], # Tuesday
                            "when": "beginnig", # "beginning" or "end"
                            "time": "10:00" # "HH:MM
                        },
                        "standup": {
                            "days": [0, 2, 3], # Monday, Wednesday, Thursday
                            "when": "every_week",
                            "time": "09:30" # "HH:MM
                        },
                        "retrospective": {
                            "days": [1], # Tuesday
                            "when": "end", # "beginning" or "end"
                            "time": "10:00" # "HH:MM
                        }
                    },
                    "team": {
                        "estimation_method": ["Fibonacci"],
                        "sprint_duration": "2", # weeks
                        "sprint_begins_on": 0, # Monday
                    },
                    "mandatory_story_fields": ["acceptance_criteria", "title", "description", "estimation"],
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
                        "_id": self.user1_id,
                        "username": self.username1,
                        "email": "carolina.b.seoane@gmail.com",
                        "profile_picture": self.pfp1,
                        "role": "Developer",
                        # "date": self.user1_id.generation_time
                    },
                    {
                        "_id": self.user2_id,
                        "username": self.username2,
                        "email": "seoane.m.b@gmail.com",
                        "profile_picture": self.pfp2,
                        "role": "Scrum Master",
                        # "date": self.user2_id.generation_time
                    }
                ]
            },
            {
                "_id": self.team2_id,
                "name": "Flyers",
                "organization": self.org1_id, 
                "team_settings": {
                    "ceremonies": {
                        "planning": {
                            "days": [1], # Tuesday
                            "when": "beginnig", # "beginning" or "end"
                            "time": "10:00" # "HH:MM
                        },
                        "standup": {
                            "days": [0, 2, 3], # Monday, Wednesday, Thursday
                            "when": "every_week",
                            "time": "09:30" # "HH:MM
                        },
                        "retrospective": {
                            "days": [1], # Tuesday
                            "when": "end", # "beginning" or "end"
                            "time": "10:00" # "HH:MM
                        }
                    },
                    "team": {
                        "estimation_method": ["Fibonacci"],
                        "sprint_duration": "3", # weeks
                        "sprint_begins_on": 0, # Monday
                    },
                    "mandatory_story_fields": ["title", "description", "estimation", "sprint"],
                    "permits": [
                        {
                            "role": "Product Owner",
                            "options": {
                                "edit_story": False,
                                "delete_story": False,
                                "add_team_members": False,
                                "join_standup": True,
                                "all_time_metrics": True
                            }
                        },
                        {
                            "role": "Developer",
                            "options": {
                                "create_story": False,
                                "edit_story": False
                            }
                        }
                    ]
                },
                "members": [
                    {
                        "_id": self.user1_id,
                        "username": self.username1,
                        "email": "carolina.b.seoane@gmail.com",
                        "profile_picture": self.pfp1,
                        "role": "Scrum Master",
                        "date": self.user1_id.generation_time
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
                "story_id": "ARGO-1",
                "title": "Mejorar el buscador teniendo en cuenta búsquedas recientes",
                "description": "Como usuario quiero que el buscador tenga en cuenta mis búsquedas recientes para obtener resultados más precisos",
                "acceptance_criteria": "La búsqueda devuelve resultados más precisos según el historial del usuario",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                },
                "sprint": "1",
                "estimation": "5",
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
                    },
                    {
                        "title": "Guardar busquedas recientes en cache",
                        "description": "Guardar las busquedas de las ultimas 24 horas en cache",
                        "app": "GOOGLE-SEARCH",
                        "status": "Done"
                    },
                    {
                        "title": "Agregar parametro de precision al endpoint /search",
                        "description": "Agregar parametro precision como entrada que tome un int",
                        "app": "GOOGLE-SEARCH",
                        "status": "Done"
                    }
                ],
                "team": self.team1_id
            },
            {
                "story_id": "ARGO-2",
                "title": "Cambiar color del botón de Login",
                "description": "Como usuario quiero que el color del buscador cambie para que sea accesible",
                "acceptance_criteria": "El botón de Login se visualiza con el color #1D4ED8",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2
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
                "estimation": "1",
                "tags": ["UX", "Accesibilidad"],
                "priority": "Medium",
                "type": "Feature",
                "estimation_method": "Fibonacci",
                "tasks": [
                    {
                        "title": "Modificar valor de font-color",
                        "description": "En el archivo de configuración modificar el valor de la propiedad font-color",
                        "app": "GOOGLE-UI",
                        "status": "Not Started"
                    }
                ],
                "team": self.team1_id
            },
            {
                "story_id": "ARGO-3",
                "title": "Solicitar pruebas de performance del MS user",
                "description": "Como usuario quiero que el microservicio pase por pruebas de performance para asegurar su buen rendimiento",
                "acceptance_criteria": "Pruebas de performance pasan con resultado satisfactorio",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                },
                "sprint": "1",
                "estimation": "3",
                "tags": ["QA", "Performance"],
                "priority": "Medium",
                "type": "Feature",
                "estimation_method": "Fibonacci",
                "tasks": [
                    {
                        "title": "Solicitar pruebas de performance para GET /user/id",
                        "description": "Crear ticket para pedir prueba de performance",
                        "app": "MS USER",
                        "status": "Done"
                    }
                ],
                "team": self.team1_id # change to _id?
            }
        ]
        self.helper.post_to_collection("stories", stories)
        print("populated stories")

    def populate_story_fields(self):
        story_fields = [{
            "fields": [
                {
                    "value": 'title',
                    "label": 'Title',
                    "modifiable": 0,
                    "description": 'The title of the story or task.'
                },
                {
                    "value": 'description',
                    "label": 'Description',
                    "modifiable": 0,
                    "description": 'A detailed description of the story or task.'
                },
                {
                    "value": 'acceptanceCriteria',
                    "label": 'Acceptance Criteria',
                    "modifiable": 1,
                    "description": 'The conditions that must be met for the story to be accepted.'
                },
                {
                    "value": 'creator',
                    "label": 'Creator',
                    "modifiable": 0,
                    "description": 'The person who created the story or task.'
                },
                {
                    "value": 'assigned_to',
                    "label": 'Assigned To',
                    "modifiable": 0,
                    "description": 'The person responsible for completing the story or task.'
                },
                {
                    "value": 'epic',
                    "label": 'Epic',
                    "modifiable": 1,
                    "description": 'The larger body of work that this story or task belongs to.'
                },
                {
                    "value": 'sprint',
                    "label": 'Sprint',
                    "modifiable": 0,
                    "description": 'The sprint in which the story or task is being worked on.'
                },
                {
                    "value": 'points',
                    "label": 'Story Points',
                    "modifiable": 0,
                    "description": 'The estimated effort required to complete the story or task.'
                },
                {
                    "value": 'tags',
                    "label": 'Tags',
                    "modifiable": 1,
                    "description": 'Keywords associated with the story or task for categorization.'
                },
                {
                    "value": 'priority',
                    "label": 'Priority',
                    "modifiable": 1,
                    "description": 'The importance level of the story or task.'
                },
                {
                    "value": 'type',
                    "label": 'Type',
                    "modifiable": 1,
                    "description": 'The classification of the story or task (e.g., bug, feature, chore).'
                },
                {
                    "value": 'estimation_method',
                    "label": 'Estimation Method',
                    "modifiable": 0,
                    "description": 'The method used to estimate the effort for the story or task.'
                },
                {
                    "value": 'tasks',
                    "label": 'Tasks',
                    "modifiable": 0,
                    "description": 'The sub-tasks that need to be completed to finish the story.'
                }
            ]
        }]
        self.helper.post_to_collection("story_fields", story_fields)
        print("populated story_fields")
