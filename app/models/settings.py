from enum import Enum


class Estimation(Enum):
    FIBONACCI = "Fibonacci"
    SIZES = "Sizes"
    PLANNING_POKER = "Planning poker"
    HOURS = "Hours"
    DAYS = "Days"


class Settings:

    def __init__(self, sprint_duration, sprint_begins_on, estimation_method,
                 mandatory_fields, permits):
        self.sprint_duration = sprint_duration
        self.sprint_begins_on = sprint_begins_on
        self.estimation_method = estimation_method
        self.mandatory_fields = mandatory_fields
        self.permits = permits
