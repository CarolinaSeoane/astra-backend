from enum import Enum

from app.services.mongoHelper import MongoHelper


class Estimation(Enum):
    FIBONACCI = "Fibonacci"
    SIZES = "Sizes"
    PLANNING_POKER = "Planning poker"
    HOURS = "Hours"
    DAYS = "Days"

class Settings:

    def __init__(self, sprint_duration, sprint_begins_on, estimation_method,
                 mandatory_story_fields, permits):
        self.sprint_duration = sprint_duration
        self.sprint_begins_on = sprint_begins_on
        self.estimation_method = estimation_method
        self.mandatory_story_fields = mandatory_story_fields
        self.permits = permits

    @staticmethod
    def get_estimation_method_options(estimation_method):
        '''
        returns None if estimation_method is not found and dict if found
        '''
        return MongoHelper().get_document_by('estimation_methods', {'key': estimation_method})
    
    @staticmethod
    def get_default_settings():
        return MongoHelper().get_document_by('default_settings', {})

