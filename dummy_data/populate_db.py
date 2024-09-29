import datetime
from bson import ObjectId

from dummy_data.db_helper import DBHelper
from app.models.configurations import (
    Role,
    MemberStatus,
    Status,
    Type,
    Priority,
    SprintStatus,
    Color,
    CeremonyStartOptions,
    CollectionNames,
)


class Populate:
    org1_id = ObjectId()
    org2_id = ObjectId()
    org3_id = ObjectId()

    user1_id = ObjectId("66f21cea9883e33c91269f76")
    user2_id = ObjectId("66f37a50e315dc85955a329b")
    user3_id = ObjectId()
    user4_id = ObjectId()
    user5_id = ObjectId()
    user6_id = ObjectId()
    user7_id = ObjectId()
    user8_id = ObjectId()
    user9_id = ObjectId()

    username1 = "CarolinaSeoane"
    username2 = "BelenSeoane"
    username3 = "MariaJose"
    username4 = "JuanP"
    username5 = "Melisa"
    username6 = "Pedro07"
    username7 = "Nicolas"
    username8 = "MatiasMasseretti"
    username9 = "FedeUTN"

    pfp1 = "6"
    pfp2 = "4"
    pfp3 = "3"
    pfp4 = "5"
    pfp5 = "10"
    pfp6 = "8"
    pfp7 = "9"
    pfp8 = "16"
    pfp9 = "1"

    team1_id = ObjectId("66f37a50e315dc85955a32a3")
    team2_id = ObjectId()

    epic1_id = ObjectId()
    epic2_id = ObjectId()
    epic1_title = "Mejoras del buscador"
    epic2_title = "Migracion de ordernes a base NoSql"

    backlog_team1 = ObjectId()  # Backlog is handled as a sprint
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
        self.populate_permissions()
        self.populate_configurations()

    def populate_organizations(self):
        organizations = [
            {"_id": self.org1_id, "name": "Google"},
            {"_id": self.org2_id, "name": "IBM"},
            {"_id": self.org3_id, "name": "UTN"},
        ]
        self.helper.post_to_collection(
            CollectionNames.ORGANIZATIONS.value, organizations
        )
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
                "access_token": "ya29.a0AcM612yUpCKXBgIGJ3v-x9Y9Ld2u2E_7qbvZntH0GJJPqL8Cba3W0A-AcZHzehyQnjOLCyVjKT01lPI7WJWylZrzXyLywF8nlZQ6AnuvL2MzNDcJR45RrwTG0yfx9SePh_5x3DEeD0_KYEGEE-N38cyRVt6xgYW_gDsaCgYKASsSARASFQHGX2MiiGM7KNSCWXl35YdLXKVdUw0170",
                "refresh_token": "1//0ho11G9eYlzhOCgYIARAAGBESNwF-L9IrVFc5SwzPSm01IoILdYjCpH1Lr6hYBAAWYS1y45NUYenHBvXuRi6EJltNXxNQqiYU7yA",
                "teams": [
                    {
                        "_id": self.team1_id,
                        "name": "Argo",
                        "member_status": MemberStatus.ACTIVE.value,
                    },
                    {
                        "_id": self.team2_id,
                        "name": "Flyers",
                        "member_status": MemberStatus.ACTIVE.value,
                    },
                ],
            },
            {
                "_id": self.user2_id,
                "name": "Belen",
                "surname": "Seoane",
                "username": self.username2,
                "email": "seoane.m.b@gmail.com",
                "profile_picture": self.pfp2,
                "access_token": "ya29.a0AcM612zC8pqJaxmqD9fiQt4r-o_7HzPLS3pbnmn1iEf0LkXsSozG_y7S7SlCQD8gp78CyZKQ7mdRC5rejew98T4zvoNdEYADNS8w2Hbu5oxoQc1U-oSSPEHUqhRZ0E2ZWsrNAWB6TNoMnTw5DF1pvZErqpDfu3y3WCxkwP3PaCgYKAW4SARASFQHGX2MiGDhouJyj2Izbn-23dfOWAw0175",
                "refresh_token": "1//0h94vTaXx9580CgYIARAAGBESNwF-L9Ir_LcwUS7ax9LZ2uxVnGwOeHZlzDO3WptQViFivjgmFTOcf9-A5dRyObFcizTN44YaCJU",
                "teams": [
                    {
                        "_id": self.team1_id,
                        "name": "Argo",
                        "member_status": MemberStatus.ACTIVE.value,
                    },
                ],
            },
            {
                "_id": self.user3_id,
                "name": "Maria José",
                "surname": "Saenz",
                "username": self.username3,
                "email": "msaenz@gmail.com",
                "profile_picture": self.pfp3,
                "access_token": "COMPLETAR",
                "refresh_token": "",
                "teams": [
                    {
                        "_id": self.team1_id,
                        "name": "Argo",
                        "member_status": MemberStatus.ACTIVE.value,
                    }
                ],
            },
            {
                "_id": self.user4_id,
                "name": "Juan",
                "surname": "Politi",
                "username": self.username4,
                "email": "juan.pol@gmail.com",
                "profile_picture": self.pfp4,
                "access_token": "COMPLETAR",
                "refresh_token": "",
                "teams": [
                    {
                        "_id": self.team1_id,
                        "name": "Argo",
                        "member_status": MemberStatus.ACTIVE.value,
                    }
                ],
            },
            {
                "_id": self.user5_id,
                "name": "Melisa Camila",
                "surname": "León",
                "username": self.username5,
                "email": "melisa_leon@gmail.com",
                "profile_picture": self.pfp5,
                "access_token": "COMPLETAR",
                "refresh_token": "",
                "teams": [
                    {
                        "_id": self.team1_id,
                        "name": "Argo",
                        "member_status": MemberStatus.ACTIVE.value,
                    }
                ],
            },
            {
                "_id": self.user6_id,
                "name": "Pedro",
                "surname": "Lombardo",
                "username": self.username6,
                "email": "pepilombardo@gmail.com",
                "profile_picture": self.pfp6,
                "access_token": "COMPLETAR",
                "refresh_token": "",
                "teams": [
                    {
                        "_id": self.team1_id,
                        "name": "Argo",
                        "member_status": MemberStatus.ACTIVE.value,
                    }
                ],
            },
            {
                "_id": self.user7_id,
                "name": "Nicolás",
                "surname": "Justo",
                "username": self.username7,
                "email": "nic.justo@gmail.com",
                "profile_picture": self.pfp7,
                "access_token": "COMPLETAR",
                "refresh_token": "",
                "teams": [
                    {
                        "_id": self.team1_id,
                        "name": "Argo",
                        "member_status": MemberStatus.ACTIVE.value,
                    }
                ],
            },
            {
                "_id": self.user8_id,
                "name": "Matias",
                "surname": "Masseretti",
                "username": self.username8,
                "email": "matmass03@gmail.com",
                "profile_picture": self.pfp8,
                "access_token": "COMPLETAR",
                "refresh_token": "",
                "teams": [
                    {
                        "_id": self.team1_id,
                        "name": "Argo",
                        "member_status": MemberStatus.ACTIVE.value,
                    },
                    {
                        "_id": self.team2_id,
                        "name": "Flyers",
                        "member_status": MemberStatus.ACTIVE.value,
                    },
                ],
            },
            {
                "_id": self.user9_id,
                "name": "Federico",
                "surname": "Sepulveda",
                "username": self.username9,
                "email": "guderianfront2000@gmail.com",
                "profile_picture": self.pfp9,
                "access_token": "COMPLETAR",
                "refresh_token": "",
                "teams": [
                    {
                        "_id": self.team1_id,
                        "name": "Argo",
                        "member_status": MemberStatus.ACTIVE.value,
                    },
                    {
                        "_id": self.team2_id,
                        "name": "Flyers",
                        "member_status": MemberStatus.ACTIVE.value,
                    },
                ],
            },
        ]
        self.helper.post_to_collection(CollectionNames.USERS.value, users)
        print("populated users")

    def populate_teams(self):
        teams = [
            {
                "_id": self.team1_id,
                "name": "Argo",
                "organization": self.org3_id,
                "ceremonies": {
                    "planning": {
                        "when": CeremonyStartOptions.BEGINNING.value,
                        "time": "10:00",  # "HH:MM,
                        "google_meet_config": {
                            "name": "spaces/G3IVgQf5g1cB",
                            "meetingUri": "https://meet.google.com/dox-iazn-miy",
                            "meetingCode": "dox-iazn-miy",
                            "config": {
                                "accessType": "TRUSTED",
                                "entryPointAccess": "ALL",
                            },
                        },
                    },
                    "standup": {
                        "days": ["mon", "wed", "thu"],
                        "time": "09:30",  # "HH:MM
                        "google_meet_config": {
                            "name": "spaces/ATCX4-zHdhYB",
                            "meetingUri": "https://meet.google.com/dsr-aegc-hzc",
                            "meetingCode": "dsr-aegc-hzc",
                            "config": {
                                "accessType": "TRUSTED",
                                "entryPointAccess": "ALL",
                            },
                        },
                    },
                    "retrospective": {
                        "when": CeremonyStartOptions.END.value,
                        "time": "10:00",  # "HH:MM
                        "google_meet_config": {
                            "name": "spaces/wbnLUy_LK3QB",
                            "meetingUri": "https://meet.google.com/uis-ygog-rnn",
                            "meetingCode": "uis-ygog-rnn",
                            "config": {
                                "accessType": "TRUSTED",
                                "entryPointAccess": "ALL",
                            },
                        },
                    },
                },
                "sprint_set_up": {
                    "estimation_method": ["fibonacci"],
                    "sprint_duration": "2",  # weeks
                    "sprint_begins_on": "mon",
                },
                "mandatory_story_fields": [
                    "title",
                    "description",
                    "creator",
                    "assigned_to",
                    "epic",
                    "sprint",
                    "estimation",
                    "story_type",
                    "estimation_method",
                    "tasks",
                ],
                "permits": [
                    {
                        "role": Role.PRODUCT_OWNER.value,
                        "options": [
                            "edit_story",
                            "add_team_members",
                            "join_standup",
                            "all_time_metrics",
                        ],
                    },
                    {"role": Role.DEV.value, "options": ["create_story", "edit_story"]},
                ],
                "members": [
                    {
                        "_id": self.user1_id,
                        "username": self.username1,
                        "email": "carolina.b.seoane@gmail.com",
                        "profile_picture": self.pfp1,
                        "role": Role.SCRUM_MASTER.value,
                        "member_status": MemberStatus.ACTIVE.value,
                        # "date": self.user1_id.generation_time
                    },
                    {
                        "_id": self.user2_id,
                        "username": self.username2,
                        "email": "seoane.m.b@gmail.com",
                        "profile_picture": self.pfp2,
                        "role": Role.DEV.value,
                        "member_status": MemberStatus.ACTIVE.value,
                        # "date": self.user2_id.generation_time
                    },
                    {
                        "_id": self.user3_id,
                        "username": self.username3,
                        "email": "msaenz@gmail.com",
                        "profile_picture": self.pfp3,
                        "role": Role.DEV.value,
                        "member_status": MemberStatus.ACTIVE.value,
                        # "date": self.user2_id.generation_time
                    },
                    {
                        "_id": self.user4_id,
                        "username": self.username4,
                        "email": "juan.pol@gmail.com",
                        "profile_picture": self.pfp4,
                        "role": Role.DEV.value,
                        "member_status": MemberStatus.ACTIVE.value,
                        # "date": self.user2_id.generation_time
                    },
                    {
                        "_id": self.user5_id,
                        "username": self.username5,
                        "email": "melisa_leon@gmail.com",
                        "profile_picture": self.pfp5,
                        "role": Role.DEV.value,
                        "member_status": MemberStatus.ACTIVE.value,
                        # "date": self.user2_id.generation_time
                    },
                    {
                        "_id": self.user6_id,
                        "username": self.username6,
                        "email": "pepilombardo@gmail.com",
                        "profile_picture": self.pfp6,
                        "role": Role.DEV.value,
                        "member_status": MemberStatus.ACTIVE.value,
                        # "date": self.user2_id.generation_time
                    },
                    {
                        "_id": self.user7_id,
                        "username": self.username7,
                        "email": "nic.justo@gmail.com",
                        "profile_picture": self.pfp7,
                        "role": Role.DEV.value,
                        "member_status": MemberStatus.ACTIVE.value,
                        # "date": self.user2_id.generation_time
                    },
                    {
                        "_id": self.user8_id,
                        "username": self.username8,
                        "email": "matmass03@gmail.com",
                        "profile_picture": self.pfp8,
                        "role": Role.DEV.value,
                        "member_status": MemberStatus.ACTIVE.value,
                    },
                    {
                        "_id": self.user9_id,
                        "username": self.username9,
                        "email": "guderianfront2000@gmail.com",
                        "profile_picture": self.pfp9,
                        "role": Role.DEV.value,
                        "member_status": MemberStatus.ACTIVE.value,
                    },
                ],
            },
            {
                "_id": self.team2_id,
                "name": "Flyers",
                "organization": self.org3_id,
                "google_meet_config": {"meeting_code": "", "meeting_space": ""},
                "ceremonies": {
                    "planning": {
                        "when": CeremonyStartOptions.END.value,
                        "time": "10:00",  # "HH:MM
                        "google_meet_config": {},
                    },
                    "standup": {
                        "days": ["mon", "wed", "thu"],
                        "time": "09:30",  # "HH:MM
                        "google_meet_config": {},
                    },
                    "retrospective": {
                        "when": CeremonyStartOptions.END.value,
                        "time": "10:00",  # "HH:MM
                        "google_meet_config": {},
                    },
                },
                "sprint_set_up": {
                    "estimation_method": ["fibonacci"],
                    "sprint_duration": "3",  # weeks
                    "sprint_begins_on": "mon",
                },
                "mandatory_story_fields": [
                    "title",
                    "description",
                    "acceptance_criteria",
                    "creator",
                    "assigned_to",
                    "epic",
                    "sprint",
                    "estimation",
                    "tags",
                    "story_type",
                    "estimation_method",
                    "tasks",
                ],
                "permits": [
                    {
                        "role": Role.PRODUCT_OWNER.value,
                        "options": [
                            "edit_story",
                            "delete_story",
                            "join_standup",
                            "all_time_metrics",
                        ],
                    },
                    {"role": Role.DEV.value, "options": ["create_story", "edit_story"]},
                ],
                "members": [
                    {
                        "_id": self.user1_id,
                        "username": self.username1,
                        "email": "carolina.b.seoane@gmail.com",
                        "profile_picture": self.pfp1,
                        "role": Role.SCRUM_MASTER.value,
                        "member_status": MemberStatus.ACTIVE.value,
                        # "date": self.user1_id.generation_time
                    },
                    {
                        "_id": self.user8_id,
                        "username": self.username8,
                        "email": "matmass03@gmail.com",
                        "profile_picture": self.pfp8,
                        "role": "Developer",
                        "member_status": MemberStatus.ACTIVE.value,
                    },
                    {
                        "_id": self.user9_id,
                        "username": self.username9,
                        "email": "guderianfront2000@gmail.com",
                        "profile_picture": self.pfp9,
                        "role": "Developer",
                        "member_status": MemberStatus.ACTIVE.value,
                    },
                ],
            },
        ]
        self.helper.post_to_collection(CollectionNames.TEAMS.value, teams)
        print("populated teams")

    def populate_epics(self):
        epics = [
            {
                "_id": self.epic1_id,
                "title": self.epic1_title,
                "description": "Mejorar la precision del buscador para mejorar la experiencia de los usuarios.",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                },
                "priority": Priority.HIGH.value,
                "epic_color": Color.YELLOW.value,
                "acceptance_criteria": "El 90% de las pruebas son positivas.",
                "business_value": "Si el buscador es más preciso, los usuarios van a utilizarlo más.",
                "team": self.team1_id,
                "organization": self.org3_id,
                "status": Status.DOING.value,
            },
            {
                "_id": self.epic2_id,
                "title": self.epic2_title,
                "description": "Migrar el schema Ordenes a MongoDB",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                },
                "priority": Priority.HIGH.value,
                "epic_color": Color.GREEN.value,
                "acceptance_criteria": "100% del schema migrado exitosamente.",
                "business_value": "MongoDB permitirá reducir el tiempo de las consultas, haciendo la aplicación más rápida, lo que generará una mejor experiencia de los usuarios.",
                "team": self.team2_id,
                "organization": self.org3_id,
                "status": Status.DOING.value,
            },
        ]
        self.helper.post_to_collection(CollectionNames.EPICS.value, epics)
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
                    "profile_picture": self.pfp1,
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                },
                "sprint": {"_id": self.sprint4_q3_team1, "name": "S4-Q3-2024"},
                "estimation": 5,
                "tags": ["Buscador"],
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "creation_date": datetime.datetime(2024, 7, 20),
                "added_to_sprint": datetime.datetime(2024, 8, 4),
                "start_date": datetime.datetime(2024, 8, 5),
                "end_date": datetime.datetime(2024, 8, 9),
                "tasks": [
                    {
                        "title": "Revisar implementacion de libreria",
                        "description": "Ajustar parametros de la libreria de busqueda",
                        "app": "GOOGLE-SEARCH",
                        "status": Status.DOING.value,
                    },
                    {
                        "title": "Guardar busquedas recientes en cache",
                        "description": "Guardar las busquedas de las ultimas 24 horas en cache",
                        "app": "GOOGLE-SEARCH",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Agregar parametro de precision al endpoint /search",
                        "description": "Agregar parametro precision como entrada que tome un int",
                        "app": "GOOGLE-SEARCH",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team1_id,
            },
            {
                "story_id": "ARGO-000002",
                "title": "Cambiar color del botón de Buscar",
                "description": "Como usuario quiero que el color del boton del buscador cambie para que sea accesible",
                "acceptance_criteria": "El botón de Buscar se visualiza con el color #1D4ED8",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                },
                "assigned_to": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                },
                "sprint": {"_id": self.sprint4_q3_team1, "name": "S4-Q3-2024"},
                "estimation": 1,
                "tags": ["UX", "Accesibilidad"],
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "creation_date": datetime.datetime(2024, 7, 20),
                "added_to_sprint": datetime.datetime(2024, 8, 6),
                "start_date": datetime.datetime(2024, 8, 7),
                "end_date": datetime.datetime(2024, 8, 8),
                "tasks": [
                    {
                        "title": "Modificar valor de font-color",
                        "description": "En el archivo de configuración modificar el valor de la propiedad font-color",
                        "app": "GOOGLE-UI",
                        "status": Status.NOT_STARTED.value,
                    }
                ],
                "team": self.team1_id,
            },
            {
                "story_id": "ARGO-000003",
                "title": "Solicitar pruebas de performance del MS user",
                "description": "Como usuario quiero que el microservicio pase por pruebas de performance para asegurar su buen rendimiento",
                "acceptance_criteria": "Pruebas de performance pasan con resultado satisfactorio",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                },
                "sprint": {"_id": self.sprint1_q1_team1, "name": "S1-Q1-2024"},
                "estimation": 3,
                "tags": ["QA", "Performance"],
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "creation_date": datetime.datetime(2023, 12, 28),
                "added_to_sprint": datetime.datetime(2024, 1, 2),
                "start_date": datetime.datetime(2024, 1, 2),
                "end_date": datetime.datetime(2024, 1, 6),
                "tasks": [
                    {
                        "title": "Solicitar pruebas de performance para GET /user/id",
                        "description": "Crear ticket para pedir prueba de performance",
                        "app": "MS USER",
                        "status": Status.DONE.value,
                    }
                ],
                "team": self.team1_id,  # change to _id?
            },
            {
                "story_id": "ARGO-000004",
                "title": "Preparar ASL demo",
                "description": "Diseñar una demo de la aplicación para presentarla al cliente",
                "acceptance_criteria": "El cliente ",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                },
                "epic": {
                    "_id": self.epic2_id,
                    "title": self.epic2_title,
                },
                "sprint": {"_id": self.sprint1_q1_team1, "name": "S1-Q1-2024"},
                "estimation": 5,
                "tags": ["Stakeholder"],
                "priority": Priority.MEDIUM.value,
                "story_type": Type.DISCOVERY.value,
                "estimation_method": "Fibonacci",
                "creation_date": datetime.datetime(2023, 12, 21),
                "added_to_sprint": datetime.datetime(2024, 1, 2),
                "start_date": datetime.datetime(2024, 1, 3),
                "end_date": datetime.datetime(2024, 1, 6),
                "tasks": [
                    {
                        "title": "Preparar presentacion",
                        "description": "La PPT debe incluir todas las features que se estuvieron desarrollando en el ultimo semestre",
                        "app": "MS USER",
                        "status": Status.DONE.value,
                    }
                ],
                "team": self.team1_id,  # change to _id?
            },
            {
                "story_id": "ARGO-000005",
                "title": "Arreglar click en botón Buscar",
                "description": "Como usuario quiero que al hacer click en el botón buscar no aumente el tamaño del input field",
                "acceptance_criteria": "El tamaño del input field permanece constante",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                },
                "sprint": {"_id": self.sprint5_q3_team1, "name": "S5-Q3-2024"},
                "estimation": 1,
                "tags": ["Frontend"],
                "priority": Priority.LOW.value,
                "story_type": Type.BUGFIX.value,
                "estimation_method": "Fibonacci",
                "creation_date": datetime.datetime(2023, 8, 2),
                "added_to_sprint": datetime.datetime(2024, 8, 12),
                "start_date": datetime.datetime(2024, 8, 19),
                "end_date": datetime.datetime(2024, 8, 21),
                "tasks": [
                    {
                        "title": "Modificar componente buscador",
                        "description": "Eliminar propiedad de width en el componente buscador",
                        "status": Status.DOING.value,
                    }
                ],
                "team": self.team1_id,  # change to _id?
            },
            {
                "story_id": "ARGO-000006",
                "title": "Optimizar carga de imágenes en la galería",
                "description": "Como usuario quiero que las imágenes en la galería se carguen más rápido para mejorar la experiencia de navegación",
                "acceptance_criteria": "Las imágenes se cargan en menos de 2 segundos",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                },
                "sprint": {"_id": self.sprint1_q1_team1, "name": "S1-Q1-2024"},
                "estimation": 8,
                "tags": ["Backend", "Performance"],
                "priority": Priority.HIGH.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "creation_date": datetime.datetime(2023, 12, 27),
                "added_to_sprint": datetime.datetime(2023, 12, 30),
                "start_date": datetime.datetime(2024, 1, 3),
                "end_date": datetime.datetime(2024, 1, 7),
                "tasks": [
                    {
                        "title": "Optimizar función de carga de imágenes",
                        "description": "Refactorizar el método de carga para implementar lazy loading",
                        "status": Status.DOING.value,
                    }
                ],
                "team": self.team1_id,
            },
            {
                "story_id": "ARGO-000007",
                "title": "Añadir validación de formulario en la página de registro",
                "description": "Como usuario quiero recibir mensajes de error si los campos del formulario no son válidos para evitar errores en el registro",
                "acceptance_criteria": "El formulario muestra mensajes de error si se dejan campos en blanco o si los formatos son incorrectos",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                },
                "assigned_to": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                },
                "sprint": {"_id": self.sprint1_q1_team1, "name": "S1-Q1-2024"},
                "estimation": 2,
                "tags": ["Frontend", "Validations"],
                "priority": Priority.MEDIUM.value,
                "story_type": Type.BUGFIX.value,
                "estimation_method": "Fibonacci",
                "creation_date": datetime.datetime(2023, 12, 27),
                "added_to_sprint": datetime.datetime(2024, 1, 4),
                "start_date": datetime.datetime(2024, 1, 5),
                "end_date": datetime.datetime(2024, 1, 7),
                "tasks": [
                    {
                        "title": "Añadir validación de campos vacíos",
                        "description": "Verificar que todos los campos requeridos estén completados",
                        "status": Status.DOING.value,
                    }
                ],
                "team": self.team1_id,
            },
            {
                "story_id": "ARGO-000008",
                "title": "Actualizar estilos de la página de perfil",
                "description": "Como usuario quiero que el diseño de la página de perfil sea más moderno para mejorar la experiencia visual",
                "acceptance_criteria": "La página de perfil utiliza un nuevo tema con colores y fuentes actualizados",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                },
                "assigned_to": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                },
                "epic": {
                    "_id": self.epic2_id,
                    "title": self.epic2_title,
                },
                "sprint": {"_id": self.sprint1_q1_team1, "name": "S1-Q1-2024"},
                "estimation": 5,
                "tags": ["Frontend", "UI/UX"],
                "priority": Priority.LOW.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "creation_date": datetime.datetime(2023, 12, 15),
                "added_to_sprint": datetime.datetime(2024, 1, 2),
                "start_date": datetime.datetime(2024, 1, 2),
                "end_date": datetime.datetime(2024, 1, 7),
                "tasks": [
                    {
                        "title": "Cambiar esquema de colores",
                        "description": "Actualizar los colores y las fuentes en el CSS del perfil",
                        "status": Status.DOING.value,
                    }
                ],
                "team": self.team1_id,
            },
            {
                "story_id": "ARGO-000009",
                "title": "Corregir bug en el scroll infinito de la página principal",
                "description": "Como usuario quiero que la página principal cargue correctamente más contenido cuando hago scroll hacia abajo",
                "acceptance_criteria": "El scroll infinito carga contenido adicional sin errores",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                },
                "sprint": {"_id": self.sprint1_q1_team1, "name": "S1-Q1-2024"},
                "estimation": 4,
                "tags": ["Frontend", "Bugfix"],
                "priority": Priority.MEDIUM.value,
                "story_type": Type.BUGFIX.value,
                "estimation_method": "Fibonacci",
                "creation_date": datetime.datetime(2023, 12, 29),
                "added_to_sprint": datetime.datetime(2023, 12, 29),
                "start_date": datetime.datetime(2024, 1, 4),
                "end_date": datetime.datetime(2024, 1, 8),
                "tasks": [
                    {
                        "title": "Revisar lógica de paginación",
                        "description": "Verificar la implementación de scroll infinito para corregir errores de paginación",
                        "status": Status.DOING.value,
                    }
                ],
                "team": self.team1_id,
            },
        ]
        self.helper.post_to_collection(CollectionNames.STORIES.value, stories)
        print("populated stories")

    def populate_permissions(self):
        permissions = [
            {
                "options": [
                    {
                        "role": Role.PRODUCT_OWNER.value,
                        "actions": [
                            {"value": "edit_story", "label": "Edit story"},
                            {"value": "delete_story", "label": "Delete story"},
                            {"value": "add_team_members", "label": "Add team members"},
                            {"value": "join_standup", "label": "Join standup"},
                            {
                                "value": "all_time_metrics",
                                "label": "Access to all time metrics",
                            },
                        ],
                    },
                    {
                        "role": Role.DEV.value,
                        "actions": [
                            {"value": "create_story", "label": "Create story"},
                            {"value": "edit_story", "label": "Edit story"},
                            {"value": "delete_story", "label": "Delete story"},
                            {
                                "value": "modify_sprint_schedule",
                                "label": "Modify sprint schedule",
                            },
                        ],
                    },
                ]
            }
        ]
        self.helper.post_to_collection(CollectionNames.PERMISSIONS.value, permissions)
        print("populated permissions")

    def populate_sprints(self):
        sprints = [
            {
                "_id": self.backlog_team1,
                "name": "Backlog",
                "status": SprintStatus.ACTIVE.value,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint1_q1_team1,
                "name": "S1-Q1-2024",
                "sprint_number": "1",
                "quarter": "1",
                "year": "2024",
                "start_date": datetime.datetime(2024, 1, 1),
                "end_date": datetime.datetime(2024, 1, 14),
                "status": SprintStatus.FINISHED.value,
                "target": 12,
                "completed": 105,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint2_q1_team1,
                "name": "S2-Q1-2024",
                "sprint_number": "2",
                "quarter": "1",
                "year": "2024",
                "start_date": datetime.datetime(2024, 1, 15),
                "end_date": datetime.datetime(2024, 1, 28),
                "status": SprintStatus.FINISHED.value,
                "target": 103,
                "completed": 88,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint3_q1_team1,
                "name": "S3-Q1-2024",
                "sprint_number": "3",
                "quarter": "1",
                "year": "2024",
                "start_date": datetime.datetime(2024, 1, 29),
                "end_date": datetime.datetime(2024, 2, 11),
                "status": SprintStatus.FINISHED.value,
                "target": 102,
                "completed": 102,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint4_q1_team1,
                "name": "S4-Q1-2024",
                "sprint_number": "4",
                "quarter": "1",
                "year": "2024",
                "start_date": datetime.datetime(2024, 2, 12),
                "end_date": datetime.datetime(2024, 2, 25),
                "status": SprintStatus.FINISHED.value,
                "target": 95,
                "completed": 100,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint5_q1_team1,
                "name": "S5-Q1-2024",
                "sprint_number": "5",
                "quarter": "1",
                "year": "2024",
                "start_date": datetime.datetime(2024, 2, 26),
                "end_date": datetime.datetime(2024, 3, 10),
                "status": SprintStatus.FINISHED.value,
                "target": 90,
                "completed": 94,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint6_q1_team1,
                "name": "S6-Q1-2024",
                "sprint_number": "6",
                "quarter": "1",
                "year": "2024",
                "start_date": datetime.datetime(2024, 3, 11),
                "end_date": datetime.datetime(2024, 3, 24),
                "status": SprintStatus.FINISHED.value,
                "target": 110,
                "completed": 100,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint1_q2_team1,
                "name": "S1-Q2-2024",
                "sprint_number": "1",
                "quarter": "2",
                "year": "2024",
                "start_date": datetime.datetime(2024, 3, 25),
                "end_date": datetime.datetime(2024, 4, 7),
                "status": SprintStatus.FINISHED.value,
                "target": 97,
                "completed": 105,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint2_q2_team1,
                "name": "S2-Q2-2024",
                "sprint_number": "2",
                "quarter": "2",
                "year": "2024",
                "start_date": datetime.datetime(2024, 4, 15),
                "end_date": datetime.datetime(2024, 4, 28),
                "status": SprintStatus.FINISHED.value,
                "target": 107,
                "completed": 89,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint3_q2_team1,
                "name": "S3-Q2-2024",
                "sprint_number": "3",
                "quarter": "2",
                "year": "2024",
                "start_date": datetime.datetime(2024, 4, 29),
                "end_date": datetime.datetime(2024, 5, 12),
                "status": SprintStatus.FINISHED.value,
                "target": 98,
                "completed": 98,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint4_q2_team1,
                "name": "S4-Q2-2024",
                "sprint_number": "4",
                "quarter": "2",
                "year": "2024",
                "start_date": datetime.datetime(2024, 5, 13),
                "end_date": datetime.datetime(2024, 5, 26),
                "status": SprintStatus.FINISHED.value,
                "target": 93,
                "completed": 100,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint5_q2_team1,
                "name": "S5-Q2-2024",
                "sprint_number": "5",
                "quarter": "2",
                "year": "2024",
                "start_date": datetime.datetime(2024, 5, 27),
                "end_date": datetime.datetime(2024, 6, 9),
                "status": SprintStatus.FINISHED.value,
                "target": 95,
                "completed": 99,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint6_q2_team1,
                "name": "S6-Q2-2024",
                "sprint_number": "6",
                "quarter": "2",
                "year": "2024",
                "start_date": datetime.datetime(2024, 6, 10),
                "end_date": datetime.datetime(2024, 6, 23),
                "status": SprintStatus.FINISHED.value,
                "target": 103,
                "completed": 100,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint1_q3_team1,
                "name": "S1-Q3-2024",
                "sprint_number": "1",
                "quarter": "3",
                "year": "2024",
                "start_date": datetime.datetime(2024, 6, 24),
                "end_date": datetime.datetime(2024, 7, 7),
                "status": SprintStatus.FINISHED.value,
                "target": 97,
                "completed": 97,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint2_q3_team1,
                "name": "S2-Q3-2024",
                "sprint_number": "2",
                "quarter": "3",
                "year": "2024",
                "start_date": datetime.datetime(2024, 7, 8),
                "end_date": datetime.datetime(2024, 7, 21),
                "status": SprintStatus.FINISHED.value,
                "target": 100,
                "completed": 103,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint3_q3_team1,
                "name": "S3-Q3-2024",
                "sprint_number": "3",
                "quarter": "3",
                "year": "2024",
                "start_date": datetime.datetime(2024, 7, 22),
                "end_date": datetime.datetime(2024, 8, 4),
                "status": SprintStatus.FINISHED.value,
                "target": 94,
                "completed": 103,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint4_q3_team1,
                "name": "S4-Q3-2024",
                "sprint_number": "4",
                "quarter": "3",
                "year": "2024",
                "start_date": datetime.datetime(2024, 8, 5),
                "end_date": datetime.datetime(2024, 8, 18),
                "status": SprintStatus.CURRENT.value,
                "target": 85,
                "completed": 80,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint5_q3_team1,
                "name": "S5-Q3-2024",
                "sprint_number": "5",
                "quarter": "3",
                "year": "2024",
                "start_date": datetime.datetime(2024, 8, 19),
                "end_date": datetime.datetime(2024, 9, 1),
                "status": SprintStatus.FUTURE.value,
                "target": 97,
                "completed": 109,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint6_q3_team1,
                "name": "S6-Q3-2024",
                "sprint_number": "6",
                "quarter": "3",
                "year": "2024",
                "start_date": datetime.datetime(2024, 9, 2),
                "end_date": datetime.datetime(2024, 9, 15),
                "status": SprintStatus.FUTURE.value,
                "target": 115,
                "completed": 109,
                "team": self.team1_id,
            },
            {
                "_id": self.backlog_team2,
                "name": "Backlog",
                "status": SprintStatus.ACTIVE.value,
                "team": self.team2_id,
            },
        ]
        self.helper.post_to_collection(CollectionNames.SPRINTS.value, sprints)
        print("populated sprints")

    def populate_configurations(self):
        configurations = [
            {
                "key": "default_settings",
                "value": "ceremonies",
                "ceremonies": {
                    "planning": {
                        "when": CeremonyStartOptions.BEGINNING.value,
                        "time": "10:00",  # "HH:MM
                        "google_meet_config": {},
                    },
                    "standup": {
                        "days": ["mon", "tue", "wed", "thu", "fri"],
                        "time": "12:00",  # "HH:MM
                        "google_meet_config": {},
                    },
                    "retrospective": {
                        "when": CeremonyStartOptions.END.value,
                        "time": "16:00",  # "HH:MM
                        "google_meet_config": {},
                    },
                },
            },
            {
                "key": "default_settings",
                "value": "sprint_set_up",
                "sprint_set_up": {
                    "estimation_method": ["fibonacci"],
                    "sprint_duration": "2",  # weeks
                    "sprint_begins_on": "mon",
                },
            },
            {
                "key": "default_settings",
                "value": "mandatory_story_fields",
                "mandatory_story_fields": [
                    "title",
                    "description",
                    "acceptance_criteria",
                    "creator",
                    "assigned_to",
                    "epic",
                    "sprint",
                    "estimation",
                    "tags",
                    "story_type",
                    "estimation_method",
                    "tasks",
                ],
            },
            {
                "key": "default_settings",
                "value": "permits",
                "permits": [
                    {
                        "role": Role.PRODUCT_OWNER.value,
                        "options": [
                            "edit_story",
                            "delete_story",
                            "join_standup",
                            "all_time_metrics",
                        ],
                    },
                    {"role": Role.DEV.value, "options": ["create_story", "edit_story"]},
                ],
            },
            {
                "key": "estimation_methods",
                "value": "fibonacci",
                "fibonacci": {
                    "label": "Fibonacci",
                    "key": "fibonacci",
                    "options": [1, 2, 3, 5, 8, 13, 21, 34],
                },
            },
            {
                "key": "estimation_methods",
                "value": "days",
                "days": {
                    "label": "Days",
                    "key": "days",
                },
            },
            {
                "key": "estimation_methods",
                "value": "sizes",
                "sizes": {
                    "label": "Sizes",
                    "key": "sizes",
                    "options": ["XS", "S", "M", "L", "XL", "XXL", "XXXL"],
                },
            },
            {
                "key": "all_possible_fields",
                "value": "story_fields",
                "story_fields": [
                    {
                        "value": "story_id",
                        "label": "Story ID",
                        "modifiable": 0,
                        "description": "The ID of the story.",
                        "section": "general",
                        "type": "input_field",
                        "order": 0,
                    },
                    {
                        "value": "title",
                        "label": "Title",
                        "modifiable": 0,
                        "description": "The title of the story or task.",
                        "section": "general",
                        "type": "input_field",
                        "order": 1,
                    },
                    {
                        "value": "description",
                        "label": "Description",
                        "modifiable": 0,
                        "description": "A detailed description of the story or task.",
                        "section": "general",
                        "type": "text_area",
                        "order": 2,
                    },
                    {
                        "value": "acceptance_criteria",
                        "label": "Acceptance criteria",
                        "modifiable": 1,
                        "description": "The conditions that must be met for the story to be accepted.",
                        "section": "additional_information",
                        "type": "text_area",
                    },
                    {
                        "value": "creator",
                        "label": "Creator",
                        "modifiable": 0,
                        "description": "The person who created the story or task.",
                        "section": "users",
                        "type": "user",
                    },
                    {
                        "value": "assigned_to",
                        "label": "Assigned to",
                        "modifiable": 0,
                        "description": "The person responsible for completing the story or task.",
                        "section": "users",
                        "type": "dropdown",
                    },
                    {
                        "value": "epic",
                        "label": "Epic",
                        "modifiable": 1,
                        "description": "The larger body of work that this story or task belongs to.",
                        "section": "general",
                        "type": "dropdown",
                        "order": 4,
                    },
                    {
                        "value": "sprint",
                        "label": "Sprint",
                        "modifiable": 0,
                        "description": "The sprint in which the story or task is being worked on.",
                        "section": "general",
                        "type": "dropdown",
                        "order": 5,
                    },
                    {
                        "value": "estimation",
                        "label": "Estimation",
                        "modifiable": 0,
                        "description": "The estimated effort required to complete the story or task.",
                        "section": "estimation",
                        "type": "select",
                        "order": 1,
                    },
                    {
                        "value": "tags",
                        "label": "Tags",
                        "modifiable": 1,
                        "description": "Keywords associated with the story or task for categorization.",
                        "section": "additional_information",
                        "type": "hidden",
                    },
                    {
                        "value": "priority",
                        "label": "Priority",
                        "modifiable": 1,
                        "description": "The importance level of the story or task.",
                        "section": "additional_information",
                        "type": "select",
                    },
                    {
                        "value": "story_type",
                        "label": "Story type",
                        "modifiable": 1,
                        "description": "The classification of the story.",
                        "section": "general",
                        "type": "select",
                        "order": 3,
                    },
                    {
                        "value": "tasks",
                        "label": "Tasks",
                        "modifiable": 0,
                        "description": "The sub-tasks that need to be completed to finish the story.",
                        "section": "tasks",
                        "type": "task",
                        "components": [
                            {
                                "value": "task_0_title",
                                "label": "Task title",
                                "modifiable": 0,
                                "description": "The title of the task.",
                                "section": "task",
                                "type": "input_field",
                                "order": 1,
                            },
                            {
                                "value": "task_0_description",
                                "label": "Task description",
                                "modifiable": 0,
                                "description": "A detailed description of the task.",
                                "section": "task",
                                "type": "text_area",
                                "order": 2,
                            },
                        ],
                    },
                    {
                        "value": "estimation_method",
                        "label": "Estimation method",
                        "modifiable": 0,
                        "description": "The method used to estimate the effort for the story or task.",
                        "section": "estimation",
                        "type": "hidden",
                    },
                    # Add hidden values? team, status, etc?
                ],
            },
            {
                "key": "all_possible_fields",
                "value": "epic_fields",
                "epic_fields": [
                    {
                        "value": "title",
                        "label": "Title",
                        "modifiable": 0,
                        "description": "The title of the epic.",
                        "section": "general",
                        "type": "input_field",
                        "order": 1,
                    },
                    {
                        "value": "description",
                        "label": "Description",
                        "modifiable": 0,
                        "description": "A detailed description of the epic.",
                        "section": "general",
                        "type": "text_area",
                        "order": 2,
                    },
                    {
                        "value": "creator",
                        "label": "Creator",
                        "modifiable": 0,
                        "description": "The person who created the story or task.",
                        "section": "users",
                        "type": "user",
                    },
                    {
                        "value": "priority",
                        "label": "Priority",
                        "modifiable": 0,
                        "description": "The importance level of the epic.",
                        "section": "general",
                        "type": "select",
                        "order": 4,
                    },
                    {
                        "value": "epic_color",
                        "label": "Color",
                        "modifiable": 0,
                        "description": "The color associated to the epic.",
                        "section": "general",
                        "type": "select",
                        "order": 3,
                    },
                    {
                        "value": "acceptance_criteria",
                        "label": "Acceptance criteria",
                        "modifiable": 0,
                        "description": "The conditions that must be met for the epic to be accepted.",
                        "section": "additional_information",
                        "type": "text_area",
                    },
                    {
                        "value": "business_value",
                        "label": "Business value",
                        "modifiable": 0,
                        "description": "Benefit that this epic brings to the business.",
                        "section": "additional_information",
                        "type": "text_area",
                    },
                    # team, org, status
                ],
            },
        ]
        self.helper.post_to_collection(
            CollectionNames.CONFIGURATIONS.value, configurations
        )
        print("populated configurations")
