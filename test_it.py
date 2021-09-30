# Класс для работы с TestIT API
import json
import requests
import log

# Блок настроек для подключения к TestIT
TESTIT_URL = "http://192.168.103.201"
PRIVATE_KEY = "NFhETnVHenVqMkJlREV2a1Ju"

class TestIT:
    url = None
    token = None
    headers = None

    def __init__(self):
        self.url = TESTIT_URL
        self.token = PRIVATE_KEY
        self.headers = {'Content-type': 'application/json;charset=UTF-8', 'Authorization': 'PrivateToken ' + PRIVATE_KEY}

    # Метод для создания проекта
    def create_project(self, name, description):
        project = Project()
        data = json.dumps({"description": description,"name": name})
        r = requests.post(self.url + "/api/v2/projects", data=data.encode("utf-8"), headers=self.headers)
        j_data = self.r_log(r).json()
        project.id = j_data["id"]
        return project

    # Метод для добавления attachment
    def add_attachment(self, file, type):
        headers = {'Authorization': 'PrivateToken ' + self.token}
        r = requests.post(self.url + "/api/Attachments", files = {'file': (file.name, file, type)}, headers=headers)
        j_data = self.r_log(r).json()
        return j_data["id"]

    def r_log(self, response):
        if response.status_code != 200 and response.status_code != 201:
            log.write_log("<TestIT> Ошибка выполнения " + response.request.method + " запроса к TestIt: " + response.request.path_url + ". Код ошибки: " + str(response.status_code))
            log.write_log("<TestIT> Текст ошибки: " + response.text)
        return response


class Project(TestIT):
    id = None

    def create_attrib(self, name, type, values, enabled = True, required = False, isGlobal = False):
        data = json.dumps({
              "options": values,
              "type": type,
              "name": name,
              "enabled": enabled,
              "required": required,
              "isGlobal": isGlobal
            })
        r = requests.post(self.url + "/api/v2/projects/" + self.id + "/attributes", data=data.encode("utf-8"), headers=self.headers)
        j_data = self.r_log(r).json()

    def get_parent_section(self):
        return self.get_sections()[0]

    def get_sections(self):
        sArr = []
        r = requests.get(self.url + "/api/v2/projects/" + self.id + "/sections", headers=self.headers)
        j_data = self.r_log(r).json()
        for item in j_data:
            section = Section()
            section.section_id = item["id"]
            section.id = self.id
            sArr.append(section)

        return sArr

class Section(Project):
    section_id = None

    def create_subsection(self, name, description):
        subsection = Section()

        complete = False
        max_count = 10   # Количество попыток создания секций (при наличии одинаковых названий)
        count = 1
        postfix = ""
        j_data = None
        while not complete and count < max_count:
            data = json.dumps({
                "name": name + postfix,
                "projectId": self.id,
                "parentId": self.section_id
            })
            r = requests.post(self.url + "/api/v2/sections", data=data.encode("utf-8"), headers=self.headers)
            j_data = self.r_log(r).json()
            if r.status_code == 200 or r.status_code == 201: complete = True
            postfix = " " + str(count)
            count += 1

        subsection.section_id = j_data["id"]
        subsection.id = self.id
        return subsection

    def add_work_item(self, work_item):
        work_item.section_id = self.section_id
        work_item.project_id = self.id
        data = work_item.get_data()
        r = requests.post(self.url + "/api/v2/workItems", data=data.encode("utf-8"), headers=self.headers)
        j_data = self.r_log(r).json()

class WorkItem():
    name = "Basic template"
    project_id = ""
    section_id = ""
    duration = 1        # Длительность всегда должна быть больше 0
    attributes =  {
    }
    description = ""
    attachments = ""
    priority = "Medium"
    state = "Ready"
    preconditionSteps = []
    postconditionSteps = []
    steps = [
    {
      "action": "User press the button",
      "expected": "System makes a beeeep sound",
      "testData": "Some variables values",
      "comments": "Comment on what to look for",
    }
  ]
    tags = []
    links = []

    def get_data(self):
        data = json.dumps({
                          "entityTypeName": "TestCases",
                          "description": self.description,
                          "state": self.state,
                          "priority": self.priority,
                          "steps": self.steps,
                          "preconditionSteps": self.preconditionSteps,
                          "postconditionSteps": self.postconditionSteps,
                          "duration": self.duration,
                          "attributes": self.attributes,
                          "tags": self.tags,
                          "attachments": self.attachments,
                          "links": self.links,
                          "name": self.name,
                          "projectId": self.project_id,
                          "sectionId": self.section_id
                        })

        return data