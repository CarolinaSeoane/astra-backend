from enum import Enum


class Estimation(Enum):
    FIBONACCI = "fibonacci"
    SIZES = "sizes"
    PLANNING_POKER = "planning poker"
    HOURS = "hours"
    DAYS = "days"


class Settings:

    def __init__(self, sprint_duration, sprint_begins_on, estimation_method, mandatory_fields):
        self.sprint_duration = sprint_duration
        self.sprint_begins_on = sprint_begins_on
        self.estimation_method = estimation_method
        self.mandatory_fields = mandatory_fields
