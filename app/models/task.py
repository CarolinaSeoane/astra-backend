from app.models.configurations import Status


class Task:

    def __init__(self, _id, title, description, status, app):
        self._id = _id
        self.title = title
        self.description = description
        self.status = status
        self.app = app

    @staticmethod
    def format(story):
        tasks = {key: value for key, value in story.items() if key.split('_')[0] == 'task'}
        formatted_tasks = []

        i = 1
        while tasks:
            title_key = f"task_{i}_title"
            description_key = f"task_{i}_description"
          
            title = tasks.get(title_key, '')
            description = tasks.get(description_key, '')
            
            formatted_task = {}
            if title: formatted_task['title'] = title
            if description: formatted_task['description'] = description
            if not title and not description: i += 1; continue
            formatted_task['status'] = Status.NOT_STARTED.value
            formatted_tasks.append(formatted_task) 
            
            try:
                del tasks[title_key]
                del story[title_key]
            except KeyError:
                pass

            try:
                del tasks[description_key]
                del story[description_key]
            except KeyError:
                pass
            i += 1

        return formatted_tasks
