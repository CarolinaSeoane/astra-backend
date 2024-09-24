from enum import Enum


class CeremonyType(Enum):
    PLANNING = "Planning"
    STANDUP = "Standup"
    RETRO = "Retrospective"

class Ceremony:

    def __init__(self, _id, name, organization, team_settings, member_status, members):
        pass
