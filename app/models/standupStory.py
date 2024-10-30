from app.utils import kanban_format
from app.services.mongoHelper import MongoHelper
class StandupStory:
    @staticmethod
    def get_standup_stories_by_ceremony_id_and_team_id(ceremony_id, team_id, **kwargs):
        # Definir proyección específica para el formato `kanban`
        projection = {
            '_id', 
            'story_id', 
            'title', 
            'assigned_to', 
            'estimation', 
            'tasksDoing', 
            'tasksDone', 
            'tasksNotStarted', 
            'tasksBlocked'
        }

        # Filtro inicial con `ceremony_id` y `team_id`
        filter = {
            "ceremony_id": ceremony_id,
            "team_id": team_id
        }
        print(f"Filtro: {filter}")
        print(f"Proyección: {projection}")
        # Añadir filtros opcionales según los valores en kwargs
        if 'assigned_to' in kwargs and kwargs['assigned_to']:
            filter["assigned_to.username"] = kwargs['assigned_to']
        # Agrega más filtros opcionales aquí si es necesario

        # Consultar la base de datos en `stories_standboard` y aplicar proyección
        stories = MongoHelper().get_documents_by('stories_standboard', filter=filter, projection=projection)
        
        print(f"Historias encontradas: {stories}")

        # Formatear en kanban y retornar
        return kanban_format(stories)

