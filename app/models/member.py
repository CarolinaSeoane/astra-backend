from enum import Enum


class Role(Enum):
    SCRUM_MASTER = "Scrum Master"
    PRODUCT_OWNER = "Product Owner"
    DEV = "Developer"


class Member:

    def __init__(self, user, role, date):
        self.user = user
        self.role = role
        self.date = date
