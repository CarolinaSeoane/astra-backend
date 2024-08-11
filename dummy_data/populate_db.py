from bson import ObjectId
import datetime

from dummy_data.db_helper import DBHelper
from app.models.sprint import SprintStatus

class Populate:
    org1_id = ObjectId()
    org2_id = ObjectId()

    user1_id = ObjectId()
    user2_id = ObjectId()
    user3_id = ObjectId()
    user4_id = ObjectId()
    user5_id = ObjectId()
    user6_id = ObjectId()
    user7_id = ObjectId()
    
    username1 = "CarolinaSeoane"
    username2 = "BelenSeoane"
    username3 = "MariaJose"
    username4 = "JuanP"
    username5 = "Melisa"
    username6 = "Pedro07"
    username7 = "Nicolas"
    
    pfp1 = "6"
    pfp2 = "4"
    pfp3 = "3"
    pfp4 = "5"
    pfp5 = "10"
    pfp6 = "8"
    pfp7 = "9"

    team1_id = ObjectId()
    team2_id = ObjectId()

    epic1_id = ObjectId()
    epic1_title = "Mejoras del buscador"

    backlog_team1 = ObjectId() # Backlog is handled as a sprint
    sprint1_q1_team1 = ObjectId()
    sprint2_q1_team1 = ObjectId()
    sprint3_q1_team1 = ObjectId()
    sprint4_q1_team1 = ObjectId()
    sprint5_q1_team1 = ObjectId()
    sprint6_q1_team1 = ObjectId()

    sprint1_q2_team1 = ObjectId()
    sprint2_q2_team1 = ObjectId()
    sprint3_q2_team1 = ObjectId()
    sprint4_q2_team1 = ObjectId()
    sprint5_q2_team1 = ObjectId()
    sprint6_q2_team1 = ObjectId()

    sprint1_q3_team1 = ObjectId()
    sprint2_q3_team1 = ObjectId()
    sprint3_q3_team1 = ObjectId()
    sprint4_q3_team1 = ObjectId()
    sprint5_q3_team1 = ObjectId()
    sprint6_q3_team1 = ObjectId()

    backlog_team2 = ObjectId()

    def __init__(self):
        self.helper = DBHelper()

    def populate(self):
        self.helper.drop_db()
        self.populate_organizations()
        self.populate_users()
        self.populate_teams()
        self.populate_sprints()
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
            },
            {
                "_id": self.user3_id,
                "name": "Maria José",
                "surname": "Saenz",
                "username": self.username3,
                "email": "msaenz@gmail.com",
                "profile_picture": self.pfp3,
                "teams": [
                    {
                        "_id": self.team1_id,
                        "name": "Argo",
                    }
                ]
            },
            {
                "_id": self.user4_id,
                "name": "Juan",
                "surname": "Politi",
                "username": self.username4,
                "email": "juan.pol@gmail.com",
                "profile_picture": self.pfp4,
                "teams": [
                    {
                        "_id": self.team1_id,
                        "name": "Argo",
                    }
                ]
            },
            {
                "_id": self.user5_id,
                "name": "Melisa Camila",
                "surname": "León",
                "username": self.username5,
                "email": "melisa_leon@gmail.com",
                "profile_picture": self.pfp5,
                "teams": [
                    {
                        "_id": self.team1_id,
                        "name": "Argo",
                    }
                ]
            },
            {
                "_id": self.user6_id,
                "name": "Pedro",
                "surname": "Lombardo",
                "username": self.username6,
                "email": "pepilombardo@gmail.com",
                "profile_picture": self.pfp6,
                "teams": [
                    {
                        "_id": self.team1_id,
                        "name": "Argo",
                    }
                ]
            },
            {
                "_id": self.user7_id,
                "name": "Nicolás",
                "surname": "Justo",
                "username": self.username7,
                "email": "nic.justo@gmail.com",
                "profile_picture": self.pfp7,
                "teams": [
                    {
                        "_id": self.team1_id,
                        "name": "Argo",
                    }
                ]
            },
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
                    "sprint_set_up": {
                        "estimation_method": ["fibonacci"],
                        "sprint_duration": "2", # weeks
                        "sprint_begins_on": "mon"
                    },
                    "story_fields": ['title', 'description', 'creator', 'assigned_to', 'epic', 'sprint', 'points', 'type', 'estimation_method', 'tasks'],
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
                    },
                    {
                        "_id": self.user3_id,
                        "username": self.username3,
                        "email": "msaenz@gmail.com",
                        "profile_picture": self.pfp3,
                        "role": "Developer",
                        # "date": self.user2_id.generation_time
                    },
                    {
                        "_id": self.user4_id,
                        "username": self.username4,
                        "email": "juan.pol@gmail.com",
                        "profile_picture": self.pfp4,
                        "role": "Developer",
                        # "date": self.user2_id.generation_time
                    },
                    {
                        "_id": self.user5_id,
                        "username": self.username5,
                        "email": "melisa_leon@gmail.com",
                        "profile_picture": self.pfp5,
                        "role": "Developer",
                        # "date": self.user2_id.generation_time
                    },
                    {
                        "_id": self.user6_id,
                        "username": self.username6,
                        "email": "pepilombardo@gmail.com",
                        "profile_picture": self.pfp6,
                        "role": "Developer",
                        # "date": self.user2_id.generation_time
                    },
                    {
                        "_id": self.user7_id,
                        "username": self.username7,
                        "email": "nic.justo@gmail.com",
                        "profile_picture": self.pfp7,
                        "role": "Developer",
                        # "date": self.user2_id.generation_time
                    },
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
                    "sprint_set_up": {
                        "estimation_method": ["fibonacci"],
                        "sprint_duration": "3", # weeks
                        "sprint_begins_on": "mon",
                    },
                    "story_fields": ['title', 'description', 'acceptanceCriteria', 'creator', 'assigned_to', 'epic', 'sprint', 'points', 'tags', 'type', 'estimation_method', 'tasks'],
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
                "sprint": {
                    "_id": self.sprint1_q1_team1,
                    "name": "S1-Q1-2024"
                },
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
                "sprint": {
                    "_id": self.sprint1_q1_team1,
                    "name": "S1-Q1-2024"
                },
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
                "sprint": {
                    "_id": self.sprint1_q1_team1,
                    "name": "S1-Q1-2024"
                },
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

    def populate_sprints(self):
        sprints = [
            {
                "_id": self.backlog_team1,
                "name": 'Backlog',
                "target": 'COMPLETAR',
                "status": SprintStatus.ACTIVE.value,
                "team": self.team1_id
            },
            {
                "_id": self.sprint1_q1_team1,
                "name": 'S1-Q1-2024',
                "sprint_number": '1',
                "quarter": '1',
                "year": '2024',
                "name": "S1-Q1-2024",
                "start_date": datetime.datetime(2024, 1, 1),
                "end_date": datetime.datetime(2024, 1, 14),
                "status": SprintStatus.FINISHED.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint2_q1_team1,
                "name": 'S2-Q1-2024',
                "sprint_number": '2',
                "quarter": '1',
                "year": '2024',
                "start_date": datetime.datetime(2024, 1, 15),
                "end_date": datetime.datetime(2024, 1, 28),
                "status": SprintStatus.FINISHED.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint3_q1_team1,
                "name": 'S3-Q1-2024',
                "sprint_number": '3',
                "quarter": '1',
                "year": '2024',
                "start_date": datetime.datetime(2024, 1, 29),
                "end_date": datetime.datetime(2024, 2, 11),
                "status": SprintStatus.FINISHED.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint4_q1_team1,
                "name": 'S4-Q1-2024',
                "sprint_number": '4',
                "quarter": '1',
                "year": '2024',
                "start_date": datetime.datetime(2024, 2, 12),
                "end_date": datetime.datetime(2024, 2, 25),
                "status": SprintStatus.FINISHED.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint5_q1_team1,
                "name": 'S5-Q1-2024',
                "sprint_number": '5',
                "quarter": '1',
                "year": '2024',
                "start_date": datetime.datetime(2024, 2, 26),
                "end_date": datetime.datetime(2024, 3, 10),
                "status": SprintStatus.FINISHED.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint6_q1_team1,
                "name": 'S6-Q1-2024',
                "sprint_number": '6',
                "quarter": '1',
                "year": '2024',
                "start_date": datetime.datetime(2024, 3, 11),
                "end_date": datetime.datetime(2024, 3, 24),
                "status": SprintStatus.FINISHED.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint1_q2_team1,
                "name": 'S1-Q2-2024',
                "sprint_number": '1',
                "quarter": '2',
                "year": '2024',
                "start_date": datetime.datetime(2024, 3, 25),
                "end_date": datetime.datetime(2024, 4, 7),
                "status": SprintStatus.FINISHED.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint2_q2_team1,
                "name": 'S2-Q2-2024',
                "sprint_number": '2',
                "quarter": '2',
                "year": '2024',
                "start_date": datetime.datetime(2024, 4, 15),
                "end_date": datetime.datetime(2024, 4, 28),
                "status": SprintStatus.FINISHED.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint3_q2_team1,
                "name": 'S3-Q2-2024',
                "sprint_number": '3',
                "quarter": '2',
                "year": '2024',
                "start_date": datetime.datetime(2024, 4, 29),
                "end_date": datetime.datetime(2024, 5, 12),
                "status": SprintStatus.FINISHED.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint4_q2_team1,
                "name": 'S4-Q2-2024',
                "sprint_number": '4',
                "quarter": '2',
                "year": '2024',
                "start_date": datetime.datetime(2024, 5, 13),
                "end_date": datetime.datetime(2024, 5, 26),
                "status": SprintStatus.FINISHED.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint5_q2_team1,
                "name": 'S5-Q2-2024',
                "sprint_number": '5',
                "quarter": '2',
                "year": '2024',
                "start_date": datetime.datetime(2024, 5, 27),
                "end_date": datetime.datetime(2024, 6, 9),
                "status": SprintStatus.FINISHED.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint6_q2_team1,
                "name": 'S6-Q2-2024',
                "sprint_number": '6',
                "quarter": '2',
                "year": '2024',
                "start_date": datetime.datetime(2024, 6, 10),
                "end_date": datetime.datetime(2024, 6, 23),
                "status": SprintStatus.FINISHED.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint1_q3_team1,
                "name": 'S1-Q3-2024',
                "sprint_number": '1',
                "quarter": '3',
                "year": '2024',
                "start_date": datetime.datetime(2024, 6, 24),
                "end_date": datetime.datetime(2024, 7, 7),
                "status": SprintStatus.FINISHED.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint2_q3_team1,
                "name": 'S2-Q3-2024',
                "sprint_number": '2',
                "quarter": '3',
                "year": '2024',
                "start_date": datetime.datetime(2024, 7, 8),
                "end_date": datetime.datetime(2024, 7, 21),
                "status": SprintStatus.FINISHED.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint3_q3_team1,
                "name": 'S3-Q3-2024',
                "sprint_number": '3',
                "quarter": '3',
                "year": '2024',
                "start_date": datetime.datetime(2024, 7, 22),
                "end_date": datetime.datetime(2024, 8, 4),
                "status": SprintStatus.FINISHED.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint4_q3_team1,
                "name": 'S4-Q3-2024',
                "sprint_number": '4',
                "quarter": '3',
                "year": '2024',
                "start_date": datetime.datetime(2024, 8, 5),
                "end_date": datetime.datetime(2024, 8, 18),
                "status": SprintStatus.CURRENT.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint5_q3_team1,
                "name": 'S5-Q3-2024',
                "sprint_number": '5',
                "quarter": '3',
                "year": '2024',
                "start_date": datetime.datetime(2024, 8, 19),
                "end_date": datetime.datetime(2024, 9, 1),
                "status": SprintStatus.FUTURE.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.sprint6_q3_team1,
                "name": 'S6-Q3-2024',
                "sprint_number": '6',
                "quarter": '3',
                "year": '2024',
                "start_date": datetime.datetime(2024, 9, 2),
                "end_date": datetime.datetime(2024, 9, 15),
                "status": SprintStatus.FUTURE.value,
                "target": 'COMPLETAR',
                "team": self.team1_id
            },
            {
                "_id": self.backlog_team2,
                "name": 'Backlog',
                "target": 'COMPLETAR',
                "status": SprintStatus.ACTIVE.value,
                "team": self.team2_id
            },
        ]
        self.helper.post_to_collection("sprints", sprints)
        print("populated sprints")
