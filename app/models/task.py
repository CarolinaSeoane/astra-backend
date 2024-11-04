from app.models.configurations import Status


NOT_STARTED = Status.NOT_STARTED.value
DOING = Status.DOING.value
BLOCKED = Status.BLOCKED.value
DONE = Status.DONE.value


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

        i = 0
        while tasks:
            title_key = f"task_{i}_title"
            description_key = f"task_{i}_description"
            status_key = f"task_{i}_status"
            keys = [title_key, description_key, status_key]

            title = tasks.get(title_key, '')
            description = tasks.get(description_key, '')
            status = tasks.get(status_key, '')

            formatted_task = {}
            if title:
                formatted_task['title'] = title
            if description:
                formatted_task['description'] = description
            if status:
                formatted_task['status'] = status
            else:
                formatted_task['status'] = NOT_STARTED
            if not title and not description:
                i += 1
                continue
            formatted_tasks.append(formatted_task)

            for key in keys:
                try:
                    del tasks[key]
                except KeyError:
                    pass
            i += 1

        return formatted_tasks

    @staticmethod
    def get_story_status(tasks):
        for task in tasks:
            if task['status'] == BLOCKED:
                return BLOCKED
        for task in tasks:
            if task['status'] == DOING:
                return DOING
        if all(task['status'] == DONE for task in tasks):
            return DONE
        return NOT_STARTED

    @staticmethod
    def get_statuses():
        return [NOT_STARTED, DOING, BLOCKED, DONE]

    @staticmethod
    def have_tasks_changed(old_tasks, new_tasks):
        if len(old_tasks) != len(new_tasks):
            return True
        for index, old_task in enumerate(old_tasks):
            if (
                old_task["title"] != new_tasks[index]["title"]
                or old_task["description"] != new_tasks[index]["description"]
            ):
                return True
        return False
