import testrail
import log

TESTRAIL_URL = 'http://testrail/'
EMAIL = "developer@mail.ru"
KEY = "developer"

class TestRail:

    client = None
    case_fields = None

    def __init__(self):
        log.write_log("<TestRail> Создаем подключение к TestRail (EMAIL: " + EMAIL + ", URL: " + TESTRAIL_URL + ")")
        self.client = testrail.TestRail(email=EMAIL, key=KEY, url=TESTRAIL_URL)
        self.case_fields = self.client.api._get("get_case_fields")

    # Получение всех проектов
    def get_projects(self):
        projects = self.client.projects()
        info_arr = []
        for project in projects:
            info_arr.append(project.name)
        log.write_log("<TestRail.get_projects> Список проектов: " + ", ".join(info_arr))
        return projects

    # Получение всех сьютов в проекте
    def get_suites(self, project):
        log.write_log("<TestRail.get_suites> Получим все сьюты проекта: " + project.name)
        self.client.set_project_id(project.id)
        return self.client.suites()

    def get_sections(self, suit):
        return self.client.sections(suit)

    def get_max_section_depth(self, sections):
        max_depth = 0
        for section in sections:
            if section.depth > max_depth:
                max_depth = section.depth

        return max_depth

    # Получение списка кейсов в сьюте
    def get_cases(self, project, suit):
        self.client.set_project_id(project.id)
        log.write_log("<TestRail.get_cases> Получим все кейсы в сьюте: " + suit.name)
        return self.client.cases(suit)