from bson import ObjectId


class Sprint:

    def __init__(self, sprint_number, quarter, year, start_date, end_date, target, team, _id=ObjectId()):
        self._id = _id
        self.sprint_number: sprint_number
        self.quarter: quarter
        self.year: year
        self.start_date: start_date
        self.end_date: end_date
        self.target: target
        self.team: team