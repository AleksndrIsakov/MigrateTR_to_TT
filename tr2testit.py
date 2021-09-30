# Миграция данных с TestRail на TestIt ver 1.0
from test_it import *
from test_rail import *

# Настройки подключения к TestIT в test_it.py
testit = TestIT()

# Настройки подключения к TestRail в test_rail.py
testrail = TestRail()

# Здесь можно перечислить исключаемые проекты
EXCLUDED_PROJECTS = []

# Соответствие приоритетов в TestRail и TestIT
PRIORITY_MAP = {1:"Lowest", 2:"Low", 3:"Medium", 4:"High", 5:"Highest"}


# Получим все проекты в TR и выполним последовательный перенос
tr_projects = testrail.get_projects()
for project in tr_projects:

    # Исключим завершенные и отдельные проекты
    if project.name in EXCLUDED_PROJECTS or project.is_completed: continue

    tt_project = testit.create_project(project.name, project.announcement)
    tt_parent_section = tt_project.get_parent_section()


    suits = testrail.get_suites(project)


    for suit in suits:
        tt_suit = tt_parent_section.create_subsection(suit.name, suit.description)
        cases = testrail.get_cases(project, suit)

        # Создадим все секции сьюта
        sections = testrail.get_sections(suit)
        section_max_depth = testrail.get_max_section_depth(sections)
        tt_sections = {}

        for depth in range(0, section_max_depth + 1):
            for section in sections:
                if section.depth == depth:
                    if section.depth > 0 and section.parent.id in tt_sections:
                        tt_sections[section.id] = tt_sections[section.parent.id].create_subsection(
                            section.name, section.description)
                    else:
                        tt_sections[section.id] = tt_suit.create_subsection(section.name,
                                                                                 section.description)

        for case in cases:
            tt_case = WorkItem()
            raw = case.raw_data()

            # Заполним данными WorkItem - имя теста, описание и предусловия
            tt_case.name = raw['title']
            tt_case.description = raw['custom_desctpn']
            if raw['custom_preconds'] != None:
                tt_case.preconditionSteps = [{"action":raw['custom_preconds']}]

            tt_case.priority = PRIORITY_MAP[case.priority.level]

            # Заполним шаги
            tt_case.steps = []
            if raw['custom_steps_separated'] != None:
                for step in raw['custom_steps_separated']:
                    tt_case.steps.append({"action":step['content'], "expected":step['expected']})

            #TODO: Сделать заполнение времени и результата
            #TODO: Добавить вложения
            #TODO: Импортировать оформление (выделять код (SQL))
            #TODO: Сделать эрканирование спецсимволов (В JSON часть символов является служебными)

            # Добавим кейс в секцию
            tt_sections[case.section.id].add_work_item(tt_case)