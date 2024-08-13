class Ceremony:
    def __init__(self, type, title, date, duration, status):
        self.type = type
        self.title = title
        self.date = date
        self.duration = duration
        self.status = status
        self.attendees = []  # Listado de asistentes

    def add_attendee(self, user_id, justification=""):
        self.attendees.append({
            "user_id": user_id,
            "justification": justification
        })