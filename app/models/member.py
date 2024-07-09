from enum import Enum


class Role(Enum):
    SCRUM_MASTER = "Scrum Master"
    PRODUCT_OWNER = "Product Owner"
    DEV = "Developer"


class Member:

    def __init__(self, user, team, role, date):
        self.user = user
        self.team = team
        self.role = role
        self.date = date
