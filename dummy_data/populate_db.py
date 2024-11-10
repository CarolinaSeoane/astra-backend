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
    org4_id = ObjectId()

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

    email1 = "carolina.b.seoane@gmail.com"
    email2 = "seoane.m.b@gmail.com"
    email3 = "msaenz@gmail.com"
    email4 = "juan.pol@gmail.com"
    email5 = "melisa_leon@gmail.com"
    email6 = "pepilombardo@gmail.com"
    email7 = "nic.justo@gmail.com"
    email8 = "matmass03@gmail.com"
    email9 = "guderianfront2000@gmail.com"

    pfp1 = "10"
    pfp2 = "3"
    pfp3 = "2"
    pfp4 = "5"
    pfp5 = "11"
    pfp6 = "7"
    pfp7 = "8"
    pfp8 = "16"
    pfp9 = "9"

    team1_id = ObjectId("66f37a50e315dc85955a32a3")
    team2_id = ObjectId()
    team3_id = ObjectId("672fb0f43e5191f98c4fc6c9")

    epic1_id = ObjectId()
    epic2_id = ObjectId()
    epic3_id = ObjectId()
    epic4_id = ObjectId()
    epic5_id = ObjectId()
    epic6_id = ObjectId()

    epic1_title = "Mejoras del buscador"
    epic2_title = "Migracion de ordernes a base NoSql"
    epic3_title = "Definición de la problemática"
    epic4_title = "Gestión"
    epic5_title = "Desarrollo"
    epic6_title = "Cierre de proyecto"

    epic1_color = Color.LIME.value
    epic2_color = Color.GREEN.value
    epic3_color = Color.ORANGE.value
    epic4_color = Color.BLUE.value
    epic5_color = Color.RED.value
    epic6_color = Color.PURPLE.value

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

    sprint1_q4_team1 = ObjectId()
    sprint2_q4_team1 = ObjectId()
    sprint3_q4_team1 = ObjectId()
    sprint4_q4_team1 = ObjectId()
    sprint5_q4_team1 = ObjectId()
    sprint6_q4_team1 = ObjectId()

    backlog_team2 = ObjectId()
    
    backlog_team3 = ObjectId()
    sprint1_q2_team3 = ObjectId()
    sprint2_q2_team3 = ObjectId()
    sprint3_q2_team3 = ObjectId()
    sprint4_q2_team3 = ObjectId()
    sprint5_q2_team3 = ObjectId()
    sprint6_q2_team3 = ObjectId()

    sprint1_q3_team3 = ObjectId()
    sprint2_q3_team3 = ObjectId()
    sprint3_q3_team3 = ObjectId()
    sprint4_q3_team3 = ObjectId()
    
    sprint1_q4_team3 = ObjectId()
    sprint2_q4_team3 = ObjectId()
    sprint3_q4_team3 = ObjectId()
    sprint4_q4_team3 = ObjectId()
    sprint5_q4_team3 = ObjectId()

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
                "email": self.email1,
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
                    {
                        "_id": self.team3_id,
                        "name": "Proyecto final",
                        "member_status": MemberStatus.ACTIVE.value,
                    },
                ],
            },
            {
                "_id": self.user2_id,
                "name": "Belen",
                "surname": "Seoane",
                "username": self.username2,
                "email": self.email2,
                "profile_picture": self.pfp2,
                "access_token": "ya29.a0AcM612zC8pqJaxmqD9fiQt4r-o_7HzPLS3pbnmn1iEf0LkXsSozG_y7S7SlCQD8gp78CyZKQ7mdRC5rejew98T4zvoNdEYADNS8w2Hbu5oxoQc1U-oSSPEHUqhRZ0E2ZWsrNAWB6TNoMnTw5DF1pvZErqpDfu3y3WCxkwP3PaCgYKAW4SARASFQHGX2MiGDhouJyj2Izbn-23dfOWAw0175",
                "refresh_token": "1//0h94vTaXx9580CgYIARAAGBESNwF-L9Ir_LcwUS7ax9LZ2uxVnGwOeHZlzDO3WptQViFivjgmFTOcf9-A5dRyObFcizTN44YaCJU",
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
                    {
                        "_id": self.team3_id,
                        "name": "Proyecto final",
                        "member_status": MemberStatus.ACTIVE.value,
                    },
                ],
            },
            {
                "_id": self.user3_id,
                "name": "Maria José",
                "surname": "Saenz",
                "username": self.username3,
                "email": self.email3,
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
                "email": self.email4,
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
                "email": self.email5,
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
                "email": self.email6,
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
                "email": self.email7,
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
                "email": self.email8,
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
                    {
                        "_id": self.team3_id,
                        "name": "Proyecto final",
                        "member_status": MemberStatus.ACTIVE.value,
                    },
                ],
            },
            {
                "_id": self.user9_id,
                "name": "Federico",
                "surname": "Sepulveda",
                "username": self.username9,
                "email": self.email9,
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
                    {
                        "_id": self.team3_id,
                        "name": "Proyecto final",
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
                        "starts": "10:00",  # "HH:MM,
                        "ends": "12:00",
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
                        "starts": "09:30",  # "HH:MM
                        "ends": "09:45",
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
                        "starts": "10:00",  # "HH:MM
                        "ends": "11:00",
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
                "estimation_method": ["fibonacci"],
                "sprint_set_up": {
                    "sprint_duration": 2,  # weeks
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
                    {
                        "role": Role.DEV.value,
                        "options": ["create_story", "edit_story"]
                    },
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
                        "starts": "10:00",  # "HH:MM
                        "ends": "12:00",
                        "google_meet_config": {},
                    },
                    "standup": {
                        "days": ["mon", "wed", "thu"],
                        "starts": "09:30",  # "HH:MM
                        "ends": "10:00",
                        "google_meet_config": {},
                    },
                    "retrospective": {
                        "when": CeremonyStartOptions.END.value,
                        "starts": "10:00",  # "HH:MM
                        "ends": "12:00",
                        "google_meet_config": {},
                    },
                },
                "estimation_method": ["fibonacci"],
                "sprint_set_up": {
                    "sprint_duration": 3,  # weeks
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
                        "email": self.email1,
                        "profile_picture": self.pfp1,
                        "role": Role.SCRUM_MASTER.value,
                        "member_status": MemberStatus.ACTIVE.value,
                        # "date": self.user1_id.generation_time
                    },
                    {
                        "_id": self.user2_id,
                        "username": self.username2,
                        "email": self.email2,
                        "profile_picture": self.pfp2,
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
            {
                "_id": self.team3_id,
                "name": "Proyecto final",
                "organization": self.org4_id,
                "ceremonies": {
                    "planning": {
                        "when": CeremonyStartOptions.BEGINNING.value,
                        "starts": "10:00",  # "HH:MM,
                        "ends": "12:00",
                        "google_meet_config": { # COMPLETAR
                            "name": "",
                            "meetingUri": "",
                            "meetingCode": "",
                            "config": {
                                "accessType": "TRUSTED",
                                "entryPointAccess": "ALL",
                            },
                        },
                    },
                    "standup": {
                        "days": ["mon", "wed", "thu"],
                        "starts": "09:30",  # "HH:MM
                        "ends": "09:45",
                        "google_meet_config": { # COMPLETAR
                            "name": "",
                            "meetingUri": "",
                            "meetingCode": "",
                            "config": {
                                "accessType": "TRUSTED",
                                "entryPointAccess": "ALL",
                            },
                        },
                    },
                    "retrospective": {
                        "when": CeremonyStartOptions.END.value,
                        "starts": "10:00",  # "HH:MM
                        "ends": "11:00",
                        "google_meet_config": { # COMPLETAR
                            "name": "",
                            "meetingUri": "",
                            "meetingCode": "",
                            "config": {
                                "accessType": "TRUSTED",
                                "entryPointAccess": "ALL",
                            },
                        },
                    },
                },
                "estimation_method": ["fibonacci"],
                "sprint_set_up": {
                    "sprint_duration": 3,  # weeks
                    "sprint_begins_on": "tue",
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
                    {
                        "role": Role.DEV.value,
                        "options": ["create_story", "edit_story"]
                    },
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
                        "role": Role.PRODUCT_OWNER.value,
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
                "epic_color": self.epic1_color,
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
                "epic_color": self.epic2_color,
                "acceptance_criteria": "100% del schema migrado exitosamente.",
                "business_value": "MongoDB permitirá reducir el tiempo de las consultas, haciendo la aplicación más rápida, lo que generará una mejor experiencia de los usuarios.",
                "team": self.team2_id,
                "organization": self.org3_id,
                "status": Status.DOING.value,
            },
            {
                "_id": self.epic3_id,
                "title": self.epic3_title,
                "description": "Etapa inicial del proyecto.",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                },
                "priority": Priority.HIGH.value,
                "epic_color": self.epic3_color,
                "acceptance_criteria": "El 100% de los documentos deben estar entregados.",
                "business_value": "Comprender el alcance y factibilidad de nuestro proyecto nos permite sentar las bases para las etapas posteriores.",
                "team": self.team3_id,
                "organization": self.org4_id,
                "status": Status.DOING.value,
            },
            {
                "_id": self.epic4_id,
                "title": self.epic4_title,
                "description": "Etapa de elaboración de los documentos centrales del proyecto.",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                },
                "priority": Priority.HIGH.value,
                "epic_color": self.epic4_color,
                "acceptance_criteria": "El 100% de los documentos deben estar entregados.",
                "business_value": "La etapa de gestión nos permitirá elaborar los documentos principales para llevar a cabo la realización del proyecto.",
                "team": self.team3_id,
                "organization": self.org4_id,
                "status": Status.DOING.value,
            },
            {
                "_id": self.epic5_id,
                "title": self.epic5_title,
                "description": "Etapa de desarrollo de la solución.",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                },
                "priority": Priority.HIGH.value,
                "epic_color": self.epic5_color,
                "acceptance_criteria": "Aplicación deployada y funcionando correctamente, con más del 90% de los casos de prueba positivos.",
                "business_value": "El desarrollo de la aplicación.",
                "team": self.team3_id,
                "organization": self.org4_id,
                "status": Status.DOING.value,
            },
            {
                "_id": self.epic6_id,
                "title": self.epic6_title,
                "description": "Etapa de cierre y elaboración de documentos finales.",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                },
                "priority": Priority.HIGH.value,
                "epic_color": self.epic6_color,
                "acceptance_criteria": "El 100% de los documentos deben estar entregados.",
                "business_value": "Presentación final del proyecto.",
                "team": self.team3_id,
                "organization": self.org4_id,
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
                    "email": self.email1
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                    "epic_color": self.epic1_color,
                },
                "sprint": {"_id": self.sprint4_q3_team1, "name": "S4-Q3-2024"},
                "estimation": 5,
                "tags": ["Buscador"],
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DOING.value,
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
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                    "epic_color": self.epic1_color,
                },
                "sprint": {"_id": self.sprint4_q3_team1, "name": "S4-Q3-2024"},
                "estimation": 1,
                "tags": ["UX", "Accesibilidad"],
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.NOT_STARTED.value,
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
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                    "epic_color": self.epic1_color,
                },
                "sprint": {"_id": self.sprint1_q1_team1, "name": "S1-Q1-2024"},
                "estimation": 3,
                "tags": ["QA", "Performance"],
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
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
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic2_id,
                    "title": self.epic2_title,
                    "epic_color": self.epic2_color,
                },
                "sprint": {"_id": self.sprint1_q1_team1, "name": "S1-Q1-2024"},
                "estimation": 5,
                "tags": ["Stakeholder"],
                "priority": Priority.MEDIUM.value,
                "story_type": Type.DISCOVERY.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
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
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                    "epic_color": self.epic1_color,
                },
                "sprint": {"_id": self.sprint5_q3_team1, "name": "S5-Q3-2024"},
                "estimation": 1,
                "tags": ["Frontend"],
                "priority": Priority.LOW.value,
                "story_type": Type.BUGFIX.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DOING.value,
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
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                    "epic_color": self.epic1_color,
                },
                "sprint": {"_id": self.sprint1_q1_team1, "name": "S1-Q1-2024"},
                "estimation": 8,
                "tags": ["Backend", "Performance"],
                "priority": Priority.HIGH.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DOING.value,
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
                    "email": self.email1
                },
                "assigned_to": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                    "epic_color": self.epic1_color,
                },
                "sprint": {"_id": self.sprint1_q1_team1, "name": "S1-Q1-2024"},
                "estimation": 2,
                "tags": ["Frontend", "Validations"],
                "priority": Priority.MEDIUM.value,
                "story_type": Type.BUGFIX.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DOING.value,
                "creation_date": datetime.datetime(2023, 12, 27),
                "added_to_sprint": datetime.datetime(2024, 1, 4),
                "start_date": datetime.datetime(2024, 1, 5),
                "end_date": datetime.datetime(2024, 1, 7),
                "tasks": [
                    {
                        "title": "Añadir validación de campos vacíos",
                        "description": "Verificar que todos los campos requeridos estén completados",
                        "status": Status.DOING.value,
                    },
                    {
                        "title": "ESTE ES EL TITULO 2",
                        "description": "ESTA ES LA DESCRIPCION 2",
                        "status": Status.BLOCKED.value,
                    },
                    {
                        "title": "ESTE ES EL TITULO 3",
                        "description": "ESTA ES LA DESCRIPCION 3",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "ESTE ES EL TITULO 4",
                        "description": "ESTA ES LA DESCRIPCION 4",
                        "status": Status.NOT_STARTED.value,
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
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "epic": {
                    "_id": self.epic2_id,
                    "title": self.epic2_title,
                    "epic_color": self.epic2_color,
                },
                "sprint": {"_id": self.sprint1_q1_team1, "name": "S1-Q1-2024"},
                "estimation": 5,
                "tags": ["Frontend", "UI/UX"],
                "priority": Priority.LOW.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DOING.value,
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
                    "email": self.email1
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic1_id,
                    "title": self.epic1_title,
                    "epic_color": self.epic1_color,
                },
                "sprint": {"_id": self.sprint1_q1_team1, "name": "S1-Q1-2024"},
                "estimation": 4,
                "tags": ["Frontend", "Bugfix"],
                "priority": Priority.MEDIUM.value,
                "story_type": Type.BUGFIX.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DOING.value,
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
            {
                "story_id": "PROYECTO_FINAL-000001",
                "title": "Presentación de propuestas",
                "description": "Elaborar 3 propuestas y armar el documento de propuestas siguiendo los lineamientos de la cátedra.",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic3_id,
                    "title": self.epic3_title,
                    "epic_color": self.epic3_color,
                },
                "sprint": {"_id": self.sprint1_q2_team3, "name": "S1-Q2-2024"},
                "estimation": 5,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Elaborar propuesta 1",
                        "description": "Hacer el canvas y completar el documento de propuestas",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Elaborar propuesta 2",
                        "description": "Hacer el canvas y completar el documento de propuestas",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Elaborar propuesta 3",
                        "description": "Hacer el canvas y completar el documento de propuestas",
                        "status": Status.DONE.value,
                    }
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000002",
                "title": "Investigación y análisis de la problemática",
                "description": "Una vez aprobada una de las propuestas, investigar en profundidad la problemática a resolver.",
                "creator": {
                    "_id": self.user9_id,
                    "username": self.username9,
                    "profile_picture": self.pfp9,
                    "email": self.email9
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic3_id,
                    "title": self.epic3_title,
                    "epic_color": self.epic3_color,
                },
                "sprint": {"_id": self.sprint1_q2_team3, "name": "S1-Q2-2024"},
                "estimation": 3,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Investigar problemática",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Conseguir sponsor",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Elaborar documento con la información encontrada",
                        "status": Status.DONE.value,
                    }
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000003",
                "title": "Estudio de factibilidad",
                "description": "Realizar el estudio de factibilidad de la propuesta seleccionada para determinar si el proyecto es factible.",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "assigned_to": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "epic": {
                    "_id": self.epic3_id,
                    "title": self.epic3_title,
                    "epic_color": self.epic3_color,
                },
                "sprint": {"_id": self.sprint2_q2_team3, "name": "S2-Q2-2024"},
                "estimation": 8,
                "priority": Priority.CRITIC.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Completar sección Factibilidad Técnica y Operativa",
                        "description": "Revisar qué ofrece la versión free de MongoDB",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Completar sección Factibilidad de Calendario",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Completar sección Factibilidad Legal",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Completar sección Factibilidad de Mercado",
                        "status": Status.DONE.value,
                    }
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000004",
                "title": "Business Canvas Model",
                "description": "Realizar el Canvas para la propuesta seleccionada.",
                "creator": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "assigned_to": {
                    "_id": self.user9_id,
                    "username": self.username9,
                    "profile_picture": self.pfp9,
                    "email": self.email9
                },
                "epic": {
                    "_id": self.epic3_id,
                    "title": self.epic3_title,
                    "epic_color": self.epic3_color,
                },
                "sprint": {"_id": self.sprint2_q2_team3, "name": "S2-Q2-2024"},
                "estimation": 2,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Hacer CANVAS en Mural",
                        "description": "Usar template de Mural",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000005",
                "title": "Acta de proyecto",
                "description": "Elaborar documento de acta de proyecto",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "assigned_to": {
                    "_id": self.user9_id,
                    "username": self.username9,
                    "profile_picture": self.pfp9,
                    "email": self.email9
                },
                "epic": {
                    "_id": self.epic4_id,
                    "title": self.epic4_title,
                    "epic_color": self.epic4_color,
                },
                "sprint": {"_id": self.sprint2_q2_team3, "name": "S2-Q2-2024"},
                "estimation": 8,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Elaborar plan de alto nivel",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Definir funcionalidades de la aplicación separadas por roles",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000006",
                "title": "WBS",
                "description": "Elaborar diagrama de WBS",
                "creator": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "assigned_to": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "epic": {
                    "_id": self.epic4_id,
                    "title": self.epic4_title,
                    "epic_color": self.epic4_color,
                },
                "sprint": {"_id": self.sprint3_q2_team3, "name": "S3-Q2-2024"},
                "estimation": 5,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Definir tareas que se incluirán en el WBS",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Elaborar diagrama en Mural",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000007",
                "title": "Matriz de roles y responsabilidades",
                "description": "Elaborar matriz de roles y responsabilidades",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic4_id,
                    "title": self.epic4_title,
                    "epic_color": self.epic4_color,
                },
                "sprint": {"_id": self.sprint3_q2_team3, "name": "S3-Q2-2024"},
                "estimation": 5,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Definir roles",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Definir responsabilidades",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000008",
                "title": "Matriz de gestión de riesgos",
                "description": "Elaborar matriz de riesgos del proyecto en base a los riesgos identificados",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user9_id,
                    "username": self.username9,
                    "profile_picture": self.pfp9,
                    "email": self.email9
                },
                "epic": {
                    "_id": self.epic4_id,
                    "title": self.epic4_title,
                    "epic_color": self.epic4_color,
                },
                "sprint": {"_id": self.sprint3_q2_team3, "name": "S3-Q2-2024"},
                "estimation": 3,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Completar matriz de riesgos",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000009",
                "title": "Matriz de habilidades y competencias",
                "description": "Elaborar matriz de habilidades de los distintos roles",
                "creator": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "assigned_to": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "epic": {
                    "_id": self.epic4_id,
                    "title": self.epic4_title,
                    "epic_color": self.epic4_color,
                },
                "sprint": {"_id": self.sprint3_q2_team3, "name": "S3-Q2-2024"},
                "estimation": 3,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Completar matriz",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000010",
                "title": "Matriz de comunicaciones",
                "description": "Elaborar matriz de comunicaciones",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "epic": {
                    "_id": self.epic4_id,
                    "title": self.epic4_title,
                    "epic_color": self.epic4_color,
                },
                "sprint": {"_id": self.sprint4_q2_team3, "name": "S4-Q2-2024"},
                "estimation": 2,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Completar matriz",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000011",
                "title": "Estimación de costos",
                "description": "Completar planilla de Excel con los costos del proyecto",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "assigned_to": {
                    "_id": self.user9_id,
                    "username": self.username9,
                    "profile_picture": self.pfp9,
                    "email": self.email9
                },
                "epic": {
                    "_id": self.epic4_id,
                    "title": self.epic4_title,
                    "epic_color": self.epic4_color,
                },
                "sprint": {"_id": self.sprint4_q2_team3, "name": "S4-Q2-2024"},
                "estimation": 3,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Completar planilla de Excel con los costos del proyecto",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000012",
                "title": "Diagrama de Gantt",
                "description": "En base a las tareas definidas en el WBS y sus dependencias, construir el Gantt del proyecto",
                "creator": {
                    "_id": self.user9_id,
                    "username": self.username9,
                    "profile_picture": self.pfp9,
                    "email": self.email9
                },
                "assigned_to": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "epic": {
                    "_id": self.epic4_id,
                    "title": self.epic4_title,
                    "epic_color": self.epic4_color,
                },
                "sprint": {"_id": self.sprint4_q2_team3, "name": "S4-Q2-2024"},
                "estimation": 3,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Establecer dependencias entre tareas",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Utilizar Gantter para construir el Gantt del proyecto",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000013",
                "title": "Release plan",
                "description": "Establecer el plan de releases de las funcionalidades",
                "creator": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic4_id,
                    "title": self.epic4_title,
                    "epic_color": self.epic4_color,
                },
                "sprint": {"_id": self.sprint4_q2_team3, "name": "S4-Q2-2024"},
                "estimation": 5,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Separar funcionalidades de la aplicación en releases",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Definir fechas para cada release",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Armar release plan",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000014",
                "title": "Tablero de control I",
                "description": "Completar y enviar el primer tablero de control a la cátedra",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "assigned_to": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "epic": {
                    "_id": self.epic4_id,
                    "title": self.epic4_title,
                    "epic_color": self.epic4_color,
                },
                "sprint": {"_id": self.sprint5_q2_team3, "name": "S5-Q2-2024"},
                "estimation": 2,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Completar tablero",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000015",
                "title": "Tablero de control II",
                "description": "Completar y enviar el segundo tablero de control a la cátedra",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic4_id,
                    "title": self.epic4_title,
                    "epic_color": self.epic4_color,
                },
                "sprint": {"_id": self.sprint1_q3_team3, "name": "S1-Q3-2024"},
                "estimation": 2,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Completar tablero",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000016",
                "title": "Tablero de control III",
                "description": "Completar y enviar el tercer tablero de control a la cátedra",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "assigned_to": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "epic": {
                    "_id": self.epic4_id,
                    "title": self.epic4_title,
                    "epic_color": self.epic4_color,
                },
                "sprint": {"_id": self.sprint3_q3_team3, "name": "S3-Q3-2024"},
                "estimation": 2,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Completar tablero",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000017",
                "title": "Tablero de control IV",
                "description": "Completar y enviar el cuarto tablero de control a la cátedra",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user9_id,
                    "username": self.username9,
                    "profile_picture": self.pfp9,
                    "email": self.email9
                },
                "epic": {
                    "_id": self.epic4_id,
                    "title": self.epic4_title,
                    "epic_color": self.epic4_color,
                },
                "sprint": {"_id": self.sprint1_q4_team3, "name": "S1-Q4-2024"},
                "estimation": 2,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Completar tablero",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000018",
                "title": "Story mapping",
                "description": "Elaborar el story mapping en base al release plan",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "assigned_to": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint5_q2_team3, "name": "S5-Q2-2024"},
                "estimation": 3,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Elaborar story mapping",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000019",
                "title": "Plan de pruebas",
                "description": "Elaborar el plan de pruebas",
                "creator": {
                    "_id": self.user9_id,
                    "username": self.username9,
                    "profile_picture": self.pfp9,
                    "email": self.email9
                },
                "assigned_to": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint5_q2_team3, "name": "S5-Q2-2024"},
                "estimation": 5,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Elaborar casos a probar en el plan de pruebas",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Elaborar documento de plan de pruebas",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000020",
                "title": "Casos de prueba",
                "description": "Elaborar los casos de prueba",
                "creator": {
                    "_id": self.user9_id,
                    "username": self.username9,
                    "profile_picture": self.pfp9,
                    "email": self.email9
                },
                "assigned_to": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint5_q2_team3, "name": "S5-Q2-2024"},
                "estimation": 8,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Describir escenario esperado para cada caso de prueba",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Elaborar documento de casos de prueba",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000021",
                "title": "Documento de arquitectura",
                "description": "Elaborar el documento de arquitectura",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "assigned_to": {
                    "_id": self.user9_id,
                    "username": self.username9,
                    "profile_picture": self.pfp9,
                    "email": self.email9
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint5_q2_team3, "name": "S5-Q2-2024"},
                "estimation": 3,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Diagramar la arquitectura del sistema",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000022",
                "title": "Diagrama de clases",
                "description": "Elaborar el diagrama de clases",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint6_q2_team3, "name": "S6-Q2-2024"},
                "estimation": 2,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Confeccionar el diagrama de clases del backend",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000023",
                "title": "Ejecución de los casos de prueba",
                "description": "Ejecutar los casos de pruebas confeccionados",
                "creator": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "assigned_to": {
                    "_id": self.user9_id,
                    "username": self.username9,
                    "profile_picture": self.pfp9,
                    "email": self.email9
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint6_q2_team3, "name": "S6-Q2-2024"},
                "estimation": 13,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Ejecutar los diferentes casos de prueba",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Documentar el resultado de los tests",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Confeccionar un documento de fallas detectadas",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000024",
                "title": "Login",
                "description": "Como usuario quiero loguearme en la aplicación para administrar mis proyectos.",
                "creator": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint6_q2_team3, "name": "S6-Q2-2024"},
                "estimation": 8,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Usar un SSO para validar la identidad del usuario.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Guardar email y alias del usuario en la base..",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Integrar pantalla de login en el frontend.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Permitir a un usuario crear una cuenta..",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Manejo de sesión con jwt (json web token).",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000025",
                "title": "Conexión con base de datos",
                "description": "Como administrador quiero realizar la conexión del backend con la base de datos para poder realizar acciones CRUD desde el backend.",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint6_q2_team3, "name": "S6-Q2-2024"},
                "estimation": 1,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Utilizar biblioteca pymongo para hacer la conexión.",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000026",
                "title": "Crear pantallas iniciales del frontend",
                "description": "Como usuario quiero acceder a las secciones principales de la aplicación para interactuar con las funcionalidades del sistema.",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint1_q3_team3, "name": "S1-Q3-2024"},
                "estimation": 5,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Acceder a página principal de Home",
                        "description": "Como usuario quiero acceder a la sección Home para interactuar con las funcionalidades de la misma.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Acceder a página principal de Mi Perfil",
                        "description": "Como usuario quiero acceder a la sección Mi Perfil para interactuar con las funcionalidades de la misma.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Acceder a página principal de Notificaciones",
                        "description": "Como usuario quiero acceder a la sección Notificaciones para interactuar con las funcionalidades de la misma.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Acceder a página principal de Ceremonias",
                        "description": "Como usuario quiero acceder a la sección Ceremonias para interactuar con las funcionalidades de la misma.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Acceder a página principal de Métricas",
                        "description": "Como usuario quiero acceder a la sección Métricas para interactuar con las funcionalidades de la misma.",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000027",
                "title": "Filtrar stories",
                "description": "Como usuario quiero filtrar mis stories para encontrarlas más fácilmente.",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint1_q3_team3, "name": "S1-Q3-2024"},
                "estimation": 5,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Filtros backend",
                        "description": "Desarrollo de la lógica necesaria para cumplir con los filtros establecidos.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Filtros frontend",
                        "description": "Creación de componentes clickeables para el filtro",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000028",
                "title": "Editar stories",
                "description": "Como usuario quiero editar mis stories para agregar o modificar su contenido.",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint1_q3_team3, "name": "S1-Q3-2024"},
                "estimation": 5,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Generar endpoint PUT /story",
                        "description": "Se reescribe el registro de la story con los nuevos datos editados. No se contempla historial de versiones.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Creación de vista de una story",
                        "description": "Lógica para permitir editar story en base al rol del usuario. Considerar campos editables y no editables (como el ID).",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000029",
                "title": "Formatos lista, kanban y gantt",
                "description": "Como usuario quiero poder contar con diferentes modos de visualización de mis sprints para ver mis datos de la forma más conveniente.",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint1_q3_team3, "name": "S1-Q3-2024"},
                "estimation": 8,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Formato List",
                        "description": "Generar vista List donde se muestran los datos en formato tabla scrolleable en el eje x. Evaluar qué campos mostrar o si mostrar todos.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Formato Kanban",
                        "description": "Generar vista Kanban. Separar las stories según su estado. Vista en formato de tarjetas en las columnas de Kanban.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Formato Gantt",
                        "description": "Generar vista Gantt. Ubicar las stories en un gantt de acuerdo a sus fechas de inicio (cuando la tarjeta pasó a In-Progress) y finalización.",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000030",
                "title": "Ver banner con aviso de próxima ceremonia Scrum ",
                "description": "Como usuario quiero ver un banner que indique la próxima ceremonia de mi equipo.",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint2_q3_team3, "name": "S2-Q3-2024"},
                "estimation": 13,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "(Backend) Generar endpoint que devuelva la próxima ceremonia.",
                        "description": "Generar endpoint que devuelva la próxima ceremonia.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "(Frontend) Generar componente banner",
                        "description": "Generar componente banner que indique la próxima ceremonia Scrum. Ejecutar llamado en cada reload de la página o cuando el contador llega a 0.",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000031",
                "title": "Crear nueva story/épica/task",
                "description": "Como usuario quiero crear una nueva story/épica/task para administrar mis elementos Scrum.",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint2_q3_team3, "name": "S2-Q3-2024"},
                "estimation": 8,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "(Backend) POST /story",
                        "description": "Generar endpoint (POST /story) para persistir los elementos Scrum en la base de datos.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "(Frontend) Generar pantalla de creación",
                        "description": "Generar vista para crear story (reutilizar componente de Edición de story).",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000032",
                "title": "Configuraciones del scrum master",
                "description": "Como scrum master quiero administrar la configuración del board de mi equipo.",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint2_q3_team3, "name": "S2-Q3-2024"},
                "estimation": 21,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Agregar o eliminar usuarios del equipo",
                        "description": "Como scrum master quiero administrar los integrantes de mi equipo para gestionar los accesos.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Definir periodicidad de las ceremonias",
                        "description": "Como scrum master quiero definir la periodicidad de las ceremonias scrum para organizar el sprint.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Definir duración del sprint",
                        "description": "Como scrum master quiero definir la duración del sprint para organizar el desarrollo de tareas.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Definir campos obligatorios de las stories",
                        "description": "Como scrum master quiero definir los campos obligatorios de las stories para que se adapten a las necesidades de mi equipo.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Definir permisos y roles",
                        "description": "Como scrum master quiero definir los permisos y roles de mi equipo para mantener la seguridad de los datos.",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000033",
                "title": "Conexión Google Meet API",
                "description": "Como administrador quiero establecer una conexión con Meet para obtener los datos de las ceremonias de los usuarios.",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint2_q3_team3, "name": "S2-Q3-2024"},
                "estimation": 13,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Crear meeting space",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "List conference records",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "GET data de conference records",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000034",
                "title": "Pantalla de ceremonias",
                "description": "Como usuario quiero ver todas las ceremonias del sprint para tener visibilidad del calendario de próximas ceremonias.",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint3_q3_team3, "name": "S3-Q3-2024"},
                "estimation": 3,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Ver todas las ceremonias del sprint actual, pasados y futuros",
                        "description": "En la sección ceremonias, generar un desplegable en cada ceremonia que muestre datos adicionales. Dentro de ellos, los datos de la ceremonia.",
                        "status": Status.DONE.value,
                    }
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000035",
                "title": "Pantalla de métricas",
                "description": "Como usuario quiero ver las métricas del sprint actual para extraer datos relevantes sobre la performance del equipo.",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint3_q3_team3, "name": "S3-Q3-2024"},
                "estimation": 8,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Gráfico de torta",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Burn down chart",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Velocity",
                        "status": Status.DONE.value,
                    }
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000036",
                "title": "Retro board",
                "description": "Como usuario quiero cargar un post it durante la retro para expresar qué salió bien, mal, etc.",
                "creator": {
                    "_id": self.user9_id,
                    "username": self.username9,
                    "profile_picture": self.pfp9,
                    "email": self.email9
                },
                "assigned_to": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint3_q3_team3, "name": "S3-Q3-2024"},
                "estimation": 5,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Carga de post-its",
                        "description": "Permitir a los usuarios cargar tarjetas en formato post it dentro del board de la retro.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Crear story a partir de una tarjeta",
                        "description": "Como scrum master quiero crear una story en base a un post it de la retro para poder tomar acción sobre un punto expresado en la retro.",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000037",
                "title": "Mi perfil",
                "description": "Como usuario quiero ver las stories en las que trabajé para poder sacar conclusiones de mi carga de trabajo.",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user9_id,
                    "username": self.username9,
                    "profile_picture": self.pfp9,
                    "email": self.email9
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint3_q3_team3, "name": "S3-Q3-2024"},
                "estimation": 2,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Ver stories trabajadas por un usuario",
                        "description": "Filtrar stories en base al usuario. Hacer un GET /stories/user_id",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Velocidad del usuario",
                        "description": "Como usuario quiero conocer mi propia velocidad de trabajo para tener un registro de mi performance.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Porcentaje de stories completadas a tiempo",
                        "description": "Como usuario quiero ver el porcentaje de stories que completé a tiempo para saber si cumplo con lo estimado.",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000038",
                "title": "Notificaciones",
                "description": "Como usuario quiero ver las notificaciones de las historias relevantes en la sección de notificaciones.",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "assigned_to": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "epic": {
                    "_id": self.epic5_id,
                    "title": self.epic5_title,
                    "epic_color": self.epic5_color,
                },
                "sprint": {"_id": self.sprint3_q3_team3, "name": "S3-Q3-2024"},
                "estimation": 5,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Ver notificaciones de las cuales el usuario es el reporter",
                        "description": "Como usuario quiero recibir notificaciones de las historias de las cuales soy el reporter para hacerles un seguimiento.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Ver notificaciones referentes a productos de los que es dueño",
                        "description": "Como PO quiero recibir notificaciones referentes a productos de los cuales soy dueño para hacerles un seguimiento.",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Ver notificaciones de stories asignadas al usuario",
                        "description": "Como usuario quiero recibir notificaciones de las stories que tengo asignadas para estar al tanto de actualizaciones.",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000039",
                "title": "Presentación comercial",
                "description": "Preparar la presentacion comercial para exponer",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "epic": {
                    "_id": self.epic6_id,
                    "title": self.epic6_title,
                    "epic_color": self.epic6_color,
                },
                "sprint": {"_id": self.sprint2_q3_team3, "name": "S2-Q3-2024"},
                "estimation": 5,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Preparar la ppt",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Confeccionar el documento de presentación",
                        "status": Status.DONE.value,
                    }
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000040",
                "title": "Poster del proyecto",
                "description": "Elaborar el poster del proyecto para presentar a la cátedra",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "assigned_to": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "epic": {
                    "_id": self.epic6_id,
                    "title": self.epic6_title,
                    "epic_color": self.epic6_color,
                },
                "sprint": {"_id": self.sprint3_q3_team3, "name": "S3-Q3-2024"},
                "estimation": 3,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Elaborar el poster para profesores",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Elaborar el poster de presentación",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Imprimir los posters",
                        "status": Status.DONE.value,
                    }
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000041",
                "title": "Presentacion final",
                "description": "Elaborar una presentación final del proyecto para exponer frente a los profesores de la cátedra",
                "creator": {
                    "_id": self.user2_id,
                    "username": self.username2,
                    "profile_picture": self.pfp2,
                    "email": self.email2
                },
                "assigned_to": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "epic": {
                    "_id": self.epic6_id,
                    "title": self.epic6_title,
                    "epic_color": self.epic6_color,
                },
                "sprint": {"_id": self.sprint4_q3_team3, "name": "S4-Q3-2024"},
                "estimation": 5,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Preparar ppt",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Cargar datos en la base de datos para la presentación",
                        "status": Status.DONE.value,
                    },
                    {
                        "title": "Confeccionar un roadmap de presentación",
                        "status": Status.DONE.value,
                    }
                ],
                "team": self.team3_id,
            },
            {
                "story_id": "PROYECTO_FINAL-000042",
                "title": "Documento de lecciones aprendidas",
                "description": "Confeccionar el documento final de lecciones aprendidas como cierre del proyecto",
                "creator": {
                    "_id": self.user1_id,
                    "username": self.username1,
                    "profile_picture": self.pfp1,
                    "email": self.email1
                },
                "assigned_to": {
                    "_id": self.user8_id,
                    "username": self.username8,
                    "profile_picture": self.pfp8,
                    "email": self.email8
                },
                "epic": {
                    "_id": self.epic6_id,
                    "title": self.epic6_title,
                    "epic_color": self.epic6_color,
                },
                "sprint": {"_id": self.sprint1_q4_team3, "name": "S1-Q4-2024"},
                "estimation": 3,
                "priority": Priority.MEDIUM.value,
                "story_type": Type.FEATURE.value,
                "estimation_method": "Fibonacci",
                "story_status": Status.DONE.value,
                "creation_date": datetime.datetime(2024, 7, 20),
                "tasks": [
                    {
                        "title": "Confeccionar el documento",
                        "status": Status.DONE.value,
                    },
                ],
                "team": self.team3_id,
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
                            {
                                "value": "edit_story",
                                "label": "Edit story",
                                "description": "Modify the content and details of any story in the project."
                            },
                            {
                                "value": "delete_story",
                                "label": "Delete story",
                                "description": "Permanently remove a story from the project."
                            },
                            {
                                "value": "add_team_members",
                                "label": "Add team members",
                                "description": "Invite new members to join the project team."
                            },
                            {
                                "value": "join_standup",
                                "label": "Join standup",
                                "description": "Participate in daily stand-up meetings."
                            },
                            {
                                "value": "all_time_metrics",
                                "label": "Access to all time metrics",
                                "description": "View metrics across all time periods for performance tracking."
                            },
                        ],
                    },
                    {
                        "role": Role.DEV.value,
                        "actions": [
                            {
                                "value": "create_story",
                                "label": "Create story",
                                "description": "Add a new story to the project backlog."
                            },
                            {
                                "value": "edit_story",
                                "label": "Edit story",
                                "description": "Modify the content and details of any story in the project."
                            },
                            {
                                "value": "delete_story",
                                "label": "Delete story",
                                "description": "Permanently remove a story from the project."
                            }
                        ],
                    },
                    {
                        "role": Role.SCRUM_MASTER.value,
                        "actions": [
                            {
                                "value": "create_story",
                                "label": "Create story",
                                "description": "Add a new story to the project backlog."
                            },
                            {
                                "value": "edit_story",
                                "label": "Edit story",
                                "description": "Modify the content and details of any story in the project."
                            },
                            {
                                "value": "delete_story",
                                "label": "Delete story",
                                "description": "Permanently remove a story from the project."
                            },

                            {
                                "value": "add_team_members",
                                "label": "Add team members",
                                "description": "Invite new members to join the project team."
                            },
                            {
                                "value": "join_standup",
                                "label": "Join standup",
                                "description": "Participate in daily stand-up meetings."
                            },
                            {
                                "value": "all_time_metrics",
                                "label": "Access to all time metrics",
                                "description": "View metrics across all time periods for performance tracking."
                            },
                        ],
                    }
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
                "sprint_number": 1,
                "quarter": 1,
                "year": 2024,
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
                "sprint_number": 2,
                "quarter": 1,
                "year": 2024,
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
                "sprint_number": 3,
                "quarter": 1,
                "year": 2024,
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
                "sprint_number": 4,
                "quarter": 1,
                "year": 2024,
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
                "sprint_number": 5,
                "quarter": 1,
                "year": 2024,
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
                "sprint_number": 6,
                "quarter": 1,
                "year": 2024,
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
                "sprint_number": 1,
                "quarter": 2,
                "year": 2024,
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
                "sprint_number": 2,
                "quarter": 2,
                "year": 2024,
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
                "sprint_number": 3,
                "quarter": 2,
                "year": 2024,
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
                "sprint_number": 4,
                "quarter": 2,
                "year": 2024,
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
                "sprint_number": 5,
                "quarter": 2,
                "year": 2024,
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
                "sprint_number": 6,
                "quarter": 2,
                "year": 2024,
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
                "sprint_number": 1,
                "quarter": 3,
                "year": 2024,
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
                "sprint_number": 2,
                "quarter": 3,
                "year": 2024,
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
                "sprint_number": 3,
                "quarter": 3,
                "year": 2024,
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
                "sprint_number": 4,
                "quarter": 3,
                "year": 2024,
                "start_date": datetime.datetime(2024, 8, 5),
                "end_date": datetime.datetime(2024, 8, 18),
                "status": SprintStatus.FINISHED.value,
                "target": 85,
                "completed": 80,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint5_q3_team1,
                "name": "S5-Q3-2024",
                "sprint_number": 5,
                "quarter": 3,
                "year": 2024,
                "start_date": datetime.datetime(2024, 8, 19),
                "end_date": datetime.datetime(2024, 9, 1),
                "status": SprintStatus.FINISHED.value,
                "target": 97,
                "completed": 74,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint6_q3_team1,
                "name": "S6-Q3-2024",
                "sprint_number": 6,
                "quarter": 3,
                "year": 2024,
                "start_date": datetime.datetime(2024, 9, 2),
                "end_date": datetime.datetime(2024, 9, 15),
                "status": SprintStatus.FINISHED.value,
                "target": 115,
                "completed": 115,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint1_q4_team1,
                "name": "S1-Q4-2024",
                "sprint_number": 1,
                "quarter": 4,
                "year": 2024,
                "start_date": datetime.datetime(2024, 9, 16),
                "end_date": datetime.datetime(2024, 9, 29),
                "status": SprintStatus.CURRENT.value,
                "target": 120,
                "completed": 74,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint2_q4_team1,
                "name": "S2-Q4-2024",
                "sprint_number": 2,
                "quarter": 4,
                "year": 2024,
                "start_date": datetime.datetime(2024, 9, 30),
                "end_date": datetime.datetime(2024, 10, 13),
                "status": SprintStatus.FUTURE.value,
                "next": True,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint3_q4_team1,
                "name": "S3-Q4-2024",
                "sprint_number": 3,
                "quarter": 4,
                "year": 2024,
                "start_date": datetime.datetime(2024, 10, 14),
                "end_date": datetime.datetime(2024, 10, 27),
                "status": SprintStatus.FUTURE.value,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint4_q4_team1,
                "name": "S4-Q4-2024",
                "sprint_number": 4,
                "quarter": 4,
                "year": 2024,
                "start_date": datetime.datetime(2024, 10, 28),
                "end_date": datetime.datetime(2024, 11, 10),
                "status": SprintStatus.FUTURE.value,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint5_q4_team1,
                "name": "S5-Q4-2024",
                "sprint_number": 5,
                "quarter": 4,
                "year": 2024,
                "start_date": datetime.datetime(2024, 11, 11),
                "end_date": datetime.datetime(2024, 11, 24),
                "status": SprintStatus.FUTURE.value,
                "team": self.team1_id,
            },
            {
                "_id": self.sprint6_q4_team1,
                "name": "S6-Q4-2024",
                "sprint_number": 6,
                "quarter": 4,
                "year": 2024,
                "start_date": datetime.datetime(2024, 11, 25),
                "end_date": datetime.datetime(2024, 12, 8),
                "status": SprintStatus.FUTURE.value,
                "team": self.team1_id,
            },
            {
                "_id": self.backlog_team2,
                "name": "Backlog",
                "status": SprintStatus.ACTIVE.value,
                "team": self.team2_id,
            },
            {
                "_id": self.backlog_team3,
                "name": "Backlog",
                "status": SprintStatus.ACTIVE.value,
                "team": self.team3_id,
            },
            {
                "_id": self.sprint1_q2_team3,
                "name": "S1-Q2-2024",
                "sprint_number": 1,
                "quarter": 2,
                "year": 2024,
                "start_date": datetime.datetime(2024, 4, 9),
                "end_date": datetime.datetime(2024, 4, 22),
                "target": 8,
                "completed": 8,
                "status": SprintStatus.FINISHED.value,
                "team": self.team3_id
            },
            {
                "_id": self.sprint2_q2_team3,
                "name": "S2-Q2-2024",
                "sprint_number": 2,
                "quarter": 2,
                "year": 2024,
                "start_date": datetime.datetime(2024, 4, 23),
                "end_date": datetime.datetime(2024, 5, 6),
                "target": 18,
                "completed": 18,
                "status": SprintStatus.FINISHED.value,
                "team": self.team3_id
            },
            {
                "_id": self.sprint3_q2_team3,
                "name": "S3-Q2-2024",
                "sprint_number": 3,
                "quarter": 2,
                "year": 2024,
                "start_date": datetime.datetime(2024, 5, 7),
                "end_date": datetime.datetime(2024, 5, 20),
                "target": 16,
                "completed": 16,
                "status": SprintStatus.FINISHED.value,
                "team": self.team3_id
            },
            {
                "_id": self.sprint4_q2_team3,
                "name": "S4-Q2-2024",
                "sprint_number": 4,
                "quarter": 2,
                "year": 2024,
                "start_date": datetime.datetime(2024, 5, 21),
                "end_date": datetime.datetime(2024, 6, 3),
                "target": 13,
                "completed": 13,
                "status": SprintStatus.FINISHED.value,
                "team": self.team3_id
            },
            {
                "_id": self.sprint5_q2_team3,
                "name": "S5-Q2-2024",
                "sprint_number": 5,
                "quarter": 2,
                "year": 2024,
                "start_date": datetime.datetime(2024, 6, 4),
                "end_date": datetime.datetime(2024, 6, 24),
                "target": 21,
                "completed": 21,
                "status": SprintStatus.FINISHED.value,
                "team": self.team3_id
            },
            {
                "_id": self.sprint6_q2_team3,
                "name": "S6-Q2-2024",
                "sprint_number": 6,
                "quarter": 2,
                "year": 2024,
                "start_date": datetime.datetime(2024, 6, 25),
                "end_date": datetime.datetime(2024, 7, 15),
                "target": 24,
                "completed": 24,
                "status": SprintStatus.FINISHED.value,
                "team": self.team3_id
            },
            {
                "_id": self.sprint1_q3_team3,
                "name": "S1-Q3-2024",
                "sprint_number": 1,
                "quarter": 3,
                "year": 2024,
                "start_date": datetime.datetime(2024, 7, 16),
                "end_date": datetime.datetime(2024, 8, 5),
                "target": 25,
                "completed": 25,
                "status": SprintStatus.FINISHED.value,
                "team": self.team3_id
            },
            {
                "_id": self.sprint2_q3_team3,
                "name": "S2-Q3-2024",
                "sprint_number": 2,
                "quarter": 3,
                "year": 2024,
                "start_date": datetime.datetime(2024, 8, 6),
                "end_date": datetime.datetime(2024, 8, 26),
                "target": 60,
                "completed": 60,
                "status": SprintStatus.FINISHED.value,
                "team": self.team3_id
            },
            {
                "_id": self.sprint3_q3_team3,
                "name": "S3-Q3-2024",
                "sprint_number": 3,
                "quarter": 3,
                "year": 2024,
                "start_date": datetime.datetime(2024, 8, 27),
                "end_date": datetime.datetime(2024, 9, 16),
                "target": 28,
                "completed": 28,
                "status": SprintStatus.FINISHED.value,
                "team": self.team3_id
            },
            {
                "_id": self.sprint4_q3_team3,
                "name": "S4-Q3-2024",
                "sprint_number": 4,
                "quarter": 3,
                "year": 2024,
                "start_date": datetime.datetime(2024, 9, 17),
                "end_date": datetime.datetime(2024, 10, 7),
                "target": 5,
                "completed": 5,
                "status": SprintStatus.FINISHED.value,
                "team": self.team3_id
            },
            {
                "_id": self.sprint1_q4_team3,
                "name": "S1-Q4-2024",
                "sprint_number": 1,
                "quarter": 4,
                "year": 2024,
                "start_date": datetime.datetime(2024, 10, 8),
                "end_date": datetime.datetime(2024, 10, 28),
                "target": 5,
                "completed": 5,
                "status": SprintStatus.FINISHED.value,
                "team": self.team3_id
            },
            {
                "_id": self.sprint2_q4_team3,
                "name": "S2-Q4-2024",
                "sprint_number": 2,
                "quarter": 4,
                "year": 2024,
                "start_date": datetime.datetime(2024, 10, 29),
                "end_date": datetime.datetime(2024, 11, 18),
                "target": 1,
                "completed": 1,
                "status": SprintStatus.FINISHED.value,
                "team": self.team3_id
            },
            {
                "_id": self.sprint3_q4_team3,
                "name": "S3-Q4-2024",
                "sprint_number": 3,
                "quarter": 4,
                "year": 2024,
                "start_date": datetime.datetime(2024, 11, 19),
                "end_date": datetime.datetime(2024, 12, 9),
                "target": 1,
                # "completed": 1,
                "status": SprintStatus.CURRENT.value,
                "team": self.team3_id
            },
            {
                "_id": self.sprint4_q4_team3,
                "name": "S4-Q4-2024",
                "sprint_number": 4,
                "quarter": 4,
                "year": 2024,
                "start_date": datetime.datetime(2024, 12, 10),
                "end_date": datetime.datetime(2024, 12, 30),
                "status": SprintStatus.FUTURE.value,
                "team": self.team3_id
            },
            {
                "_id": self.sprint5_q4_team3,
                "name": "S5-Q4-2024",
                "sprint_number": 5,
                "quarter": 4,
                "year": 2024,
                "start_date": datetime.datetime(2024, 12, 31),
                "end_date": datetime.datetime(2025, 1, 20),
                "status": SprintStatus.FUTURE.value,
                "team": self.team3_id
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
                        "starts": "10:00",  # "HH:MM
                        "ends": "12:00",
                        "google_meet_config": {},
                    },
                    "standup": {
                        "days": ["mon", "tue", "wed", "thu", "fri"],
                        "starts": "12:00",  # "HH:MM
                        "ends": "12:15",
                        "google_meet_config": {},
                    },
                    "retrospective": {
                        "when": CeremonyStartOptions.END.value,
                        "starts": "16:00",  # "HH:MM
                        "ends": "17:00",
                        "google_meet_config": {},
                    },
                },
            },
            {
                "key": "default_settings",
                "value": "estimation_method",
                "estimation_method": {
                    "estimation_method": ["fibonacci"]
                },
            },
            {
                "key": "default_settings",
                "value": "sprint_set_up",
                "sprint_set_up": {
                    "sprint_duration": 2,  # weeks
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
