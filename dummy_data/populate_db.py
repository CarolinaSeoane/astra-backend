from bson import ObjectId
import datetime

from dummy_data.db_helper import DBHelper
from app.models.sprint import SprintStatus
from app.models.story import Type, Priority
from app.models.epic import Color
from app.models.member import Role

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
    epic2_id = ObjectId()
    epic1_title = "Mejoras del buscador"
    epic2_title = "Migracion de ordernes a base NoSql"

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
        self.populate_epic_fields()
        self.populate_permissions()
        self.populate_estimation_methods()

    def populate_organizations(self):
        organizations = [
            {
                "_id": self.org1_id, 
                "name": "Google"
            },
            {   
                "_id": self.org2_id,
                "name": "IBM"
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
                            "days": ["tue"],
                            "when": "beginning", # "beginning" or "end"
                            "time": "10:00" # "HH:MM
                        },
                        "standup": {
                            "days": ["mon", "wed", "thu"],
                            "when": "every",
                            "time": "09:30" # "HH:MM
                        },
                        "retrospective": {
                            "days": ["tue"],
                            "when": "end", # "beginning" or "end"
                            "time": "10:00" # "HH:MM
                        }
                    },
                    "sprint_set_up": {
                        "estimation_method": ["fibonacci"],
                        "sprint_duration": "2", # weeks
                        "sprint_begins_on": "mon"
                    },
                    "story_fields": ['title', 'description', 'creator', 'assigned_to', 'epic', 'sprint', 'estimation', 'story_type', 'estimation_method', 'tasks'],
                    "permits": [
                        {
                            "role": Role.PRODUCT_OWNER.value,
                            "options": ["edit_story", "add_team_members", "join_standup", "all_time_metrics"]
                        },
                        {
                            "role": Role.DEV.value,
                            "options": ["create_story", "edit_story"]
                        }
                    ]
                },
                "members": [
                    {
                        "_id": self.user1_id,
                        "username": self.username1,
                        "email": "carolina.b.seoane@gmail.com",
                        "profile_picture": self.pfp1,
                        "role": Role.DEV.value,
                        # "date": self.user1_id.generation_time
                    },
                    {
                        "_id": self.user2_id,
                        "username": self.username2,
                        "email": "seoane.m.b@gmail.com",
                        "profile_picture": self.pfp2,
                        "role": Role.SCRUM_MASTER.value,
                        # "date": self.user2_id.generation_time
                    },
                    {
                        "_id": self.user3_id,
                        "username": self.username3,
                        "email": "msaenz@gmail.com",
                        "profile_picture": self.pfp3,
                        "role": Role.DEV.value,
                        # "date": self.user2_id.generation_time
                    },
                    {
                        "_id": self.user4_id,
                        "username": self.username4,
                        "email": "juan.pol@gmail.com",
                        "profile_picture": self.pfp4,
                        "role": Role.DEV.value,
                        # "date": self.user2_id.generation_time
                    },
                    {
                        "_id": self.user5_id,
                        "username": self.username5,
                        "email": "melisa_leon@gmail.com",
                        "profile_picture": self.pfp5,
                        "role": Role.DEV.value,
                        # "date": self.user2_id.generation_time
                    },
                    {
                        "_id": self.user6_id,
                        "username": self.username6,
                        "email": "pepilombardo@gmail.com",
                        "profile_picture": self.pfp6,
                        "role": Role.DEV.value,
                        # "date": self.user2_id.generation_time
                    },
                    {
                        "_id": self.user7_id,
                        "username": self.username7,
                        "email": "nic.justo@gmail.com",
                        "profile_picture": self.pfp7,
                        "role": Role.DEV.value,
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
                            "days": ["tu"],
                            "when": "beginning", # "beginning" or "end"
                            "time": "10:00" # "HH:MM
                        },
                        "standup": {
                            "days": ["mon", "wed", "thu"],
                            "when": "every",
                            "time": "09:30" # "HH:MM
                        },
                        "retrospective": {
                            "days": ["tue"],
                            "when": "end", # "beginning" or "end"
                            "time": "10:00" # "HH:MM
                        }
                    },
                    "sprint_set_up": {
                        "estimation_method": ["fibonacci"],
                        "sprint_duration": "3", # weeks
                        "sprint_begins_on": "mon",
                    },
                    "story_fields": ['title', 'description', 'acceptanceCriteria', 'creator', 'assigned_to', 'epic', 'sprint', 'estimation', 'tags', 'story_type', 'estimation_method', 'tasks'],
                    "permits": [
                        {
                            "role": Role.PRODUCT_OWNER.value,
                            "options": ["edit_story", "delete_story", "join_standup", "all_time_metrics"]
                        },
                        {
                            "role": Role.DEV.value,
                            "options": ["create_story", "edit_story"]
                        }
                    ]
                },
                "members": [
                    {
                        "_id": self.user1_id,
                        "username": self.username1,
                        "email": "carolina.b.seoane@gmail.com",
                        "profile_picture": self.pfp1,
                        "role": Role.SCRUM_MASTER.value,
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
                "team": {
                    "_id": self.team1_id,
                    "name": "Argo",
                },
                "priority": Priority.HIGH.value,
                "organization": self.org1_id,
                "color": Color.YELLOW.value
            },
            {
                "_id": self.epic2_id,
                "title": self.epic2_title,
                "description": "Migrar el schema Ordenes a MongoDB",
                "team": {
                    "_id": self.team2_id,
                    "name": "Flyers",
                },
                "priority": Priority.HIGH.value,
                "organization": self.org1_id,
                "color": Color.PURPLE.value
            }
        ]
        self.helper.post_to_collection("epics", epics)
        print("populated epics")

    def populate_stories(self):
        stories = [
            {
                "story_id": "ARGO-000001",
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
                    "_id": self.sprint4_q3_team1,
                    "name": "S4-Q3-2024"
                },
                "estimation": "5",
                "tags": ["Buscador"],
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
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
                "story_id": "ARGO-000002",
                "title": "Cambiar color del botón de Buscar",
                "description": "Como usuario quiero que el color del boton del buscador cambie para que sea accesible",
                "acceptance_criteria": "El botón de Buscar se visualiza con el color #1D4ED8",
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
                    "_id": self.sprint4_q3_team1,
                    "name": "S4-Q3-2024"
                },
                "estimation": "1",
                "tags": ["UX", "Accesibilidad"],
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
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
                "story_id": "ARGO-000003",
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
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
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
            },
            {
                "story_id": "ARGO-000004",
                "title": "Arreglar click en botón Buscar",
                "description": "Como usuario quiero que al hacer click en el botón buscar no aumente el tamaño del input field",
                "acceptance_criteria": "El tamaño del input field permanece constante",
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
                    "_id": self.sprint5_q3_team1,
                    "name": "S5-Q3-2024"
                },
                "estimation": "1",
                "tags": ["Frontend"],
                "priority": Priority.LOW.value,
                "story_type": Type.BUGFIX.value,
                "estimation_method": "Fibonacci",
                "tasks": [
                    {
                        "title": "Modificar componente buscador",
                        "description": "Eliminar propiedad de width en el componente buscador",
                        "status": "Doing"
                    }
                ],
                "team": self.team1_id # change to _id?
            }
        ]
        self.helper.post_to_collection("stories", stories)
        print("populated stories")

    def populate_story_fields(self):
        story_fields = [
            {
                "value": 'title',
                "label": 'Title',
                "modifiable": 0,
                "description": 'The title of the story or task.',
                "section": 'general',
                "type": "input_field",
                "order": 1
            },
            {
                "value": 'description',
                "label": 'Description',
                "modifiable": 0,
                "description": 'A detailed description of the story or task.',
                "section": 'general',
                "type": "text_area",
                "order": 2
            },
            {
                "value": 'acceptanceCriteria',
                "label": 'Acceptance criteria',
                "modifiable": 1,
                "description": 'The conditions that must be met for the story to be accepted.',
                "section": 'additional_information',
                "type": "text_area"
            },
            {
                "value": 'creator',
                "label": 'Creator',
                "modifiable": 0,
                "description": 'The person who created the story or task.',
                "section": "users",
                "type": "user"
            },
            {
                "value": 'assigned_to',
                "label": 'Assigned To',
                "modifiable": 0,
                "description": 'The person responsible for completing the story or task.',
                "section": 'users',
                "type": "dropdown"
            },
            {
                "value": 'epic',
                "label": 'Epic',
                "modifiable": 1,
                "description": 'The larger body of work that this story or task belongs to.',
                "section": 'general',
                "type": "dropdown",
                "order": 4
            },
            {
                "value": 'sprint',
                "label": 'Sprint',
                "modifiable": 0,
                "description": 'The sprint in which the story or task is being worked on.',
                "section": 'general',
                "type": "dropdown",
                "order": 5
            },
            {
                "value": 'estimation',
                "label": 'Estimation',
                "modifiable": 0,
                "description": 'The estimated effort required to complete the story or task.',
                "section": 'estimation',
                "type": "select",
                "order": 1
            },
            {
                "value": 'tags',
                "label": 'Tags',
                "modifiable": 1,
                "description": 'Keywords associated with the story or task for categorization.',
                "section": 'additional_information',
                "type": "hidden"
            },
            {
                "value": 'priority',
                "label": 'Priority',
                "modifiable": 1,
                "description": 'The importance level of the story or task.',
                "section": 'additional_information',
                "type": "select"
            },
            {
                "value": 'story_type',
                "label": 'Story type',
                "modifiable": 1,
                "description": 'The classification of the story or task (e.g., bug, feature, chore).',
                "section": 'general',
                "type": "select",
                "order": 3
            },
            {
                "value": 'tasks',
                "label": 'Tasks',
                "modifiable": 0,
                "description": 'The sub-tasks that need to be completed to finish the story.',
                "section": 'tasks',
                "type": "task",
                "components": [
                    {
                        "value": 'task_0_title',
                        "label": 'Task title',
                        "modifiable": 0,
                        "description": 'The title of the task.',
                        "section": 'task',
                        "type": "input_field",
                        "order": 1
                    },
                    {
                        "value": 'task_0_description',
                        "label": 'Task description',
                        "modifiable": 0,
                        "description": 'A detailed description of the task.',
                        "section": 'task',
                        "type": "text_area",
                        "order": 2
                    },
                ]
            },
            {
                "value": 'story_id',
                "label": 'Story ID',
                "modifiable": 0,
                "description": 'The ID of the story.',
                "section": 'general',
                "type": "input_field",
                "order": 0
            },
            {
                "value": 'estimation_method',
                "label": 'Estimation method',
                "modifiable": 0,
                "description": 'The method used to estimate the effort for the story or task.',
                "section": 'estimation',
                "type": "hidden"
            },
        ]
        self.helper.post_to_collection("story_fields", story_fields)
        print("populated story_fields")

    def populate_epic_fields(self):
        epic_fields = [
            {
                "value": 'title',
                "label": 'Title',
                "modifiable": 0,
                "description": 'The title of the epic.',
                "section": 'general',
                "type": "input_field",
                "order": 1
            },
            {
                "value": 'description',
                "label": 'Description',
                "modifiable": 0,
                "description": 'A detailed description of the epic.',
                "section": 'general',
                "type": "text_area",
                "order": 2
            },
            {
                "value": 'creator',
                "label": 'Creator',
                "modifiable": 0,
                "description": 'The person who created the story or task.',
                "section": "users",
                "type": "user"
            },
            # {
            #     "value": 'assigned_to',
            #     "label": 'Assigned To',
            #     "modifiable": 0,
            #     "description": 'The person responsible for completing the story or task.',
            #     "section": 'users',
            #     "type": "dropdown"
            # },
            {
                "value": 'priority',
                "label": 'Priority',
                "modifiable": 1,
                "description": 'The importance level of the epic.',
                "section": 'general',
                "type": "select"
            },
            {
                "value": 'epic_color',
                "label": 'Color',
                "modifiable": 1,
                "description": 'The color associated to the epic.',
                "section": 'general',
                "type": "select"
            },
        ]
        self.helper.post_to_collection("epic_fields", epic_fields)
        print("populated epic_fields")

    def populate_permissions(self):
        permissions = [{
            'options': [{
                "role": Role.PRODUCT_OWNER.value,
                "actions": [
                    {
                        "value": "edit_story",
                        "label": "Edit story"
                    },
                    {
                        'value': 'delete_story',
                        'label': 'Delete story'
                    },
                    {
                        'value': 'add_team_members',
                        'label': 'Add team members'
                    },
                    {
                        'value': 'join_standup',
                        'label': 'Join standup'
                    },
                    {
                        'value': 'all_time_metrics',
                        'label': 'Access to all time metrics'
                    }
                ]
            }, {
                "role": Role.DEV.value,
                "actions": [
                    {
                        "value": "create_story",
                        'label': 'Create story'
                    },
                    {
                        "value": "edit_story",
                        'label': 'Edit story'
                    },
                    {
                        "value": "delete_story",
                        'label': 'Delete story'
                    },
                    {
                        'value': 'modify_sprint_schedule',
                        'label': 'Modify sprint schedule'
                    }
                ]}
            ] 
        }]
        self.helper.post_to_collection("permissions", permissions)
        print("populated permissions")
    
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
    
    def populate_estimation_methods(self):
        estimation_methods = [
            {
                "label": "Fibonacci",
                "key": "fibonacci",
                "options": [1, 2, 3, 5, 8, 13, 21, 34]
            },
            {
                "label": "Days",
                "key": "days",
            },
            {
                "label": "Sizes",
                "key": "sizes",
                "options": ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']
            },
        ]
        self.helper.post_to_collection("estimation_methods", estimation_methods)
        print("populated estimation_methods")

