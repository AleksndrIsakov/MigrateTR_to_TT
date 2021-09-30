# Журнал выполнения
import logging
import os
from datetime import datetime

FILENAME = 'migrate.log'
LOG_LEVEL = logging.INFO
ES_HOST = 'elasticsearch'
ES_PORT = 9200


try:
    from cmreslogging.handlers import CMRESHandler
except:
    print(
        "Can't find CMRESHandler package. Install it with: pip3 install CMRESHandler. " +
        "Or run gitlab_runners playbook")


def write_log(l_text, level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    es = CMRESHandler(hosts=[{'host': ES_HOST, 'port': ES_PORT}],
                        auth_type=CMRESHandler.AuthType.NO_AUTH,
                        es_index_name="python-index",
                        es_additional_fields={'facility': 'SkypeBot'},
                        default_timestamp_field_name="@timestamp")
    logger.addHandler(es)
    try:
        if os.path.exists('logs/' + FILENAME):
            f = open ('logs/' + FILENAME, 'a')
            f.write(str(datetime.today()) + ': ' + l_text + '\n')
            f.close()
        else:
            if os.path.exists('logs') == False:
                os.mkdir('logs/', mode=0o777)
            f = open ('logs/' + FILENAME, 'wt')
            f.write(str(datetime.today()) + ': ' + l_text + '\n')
            f.close()

    except Exception as e:
        print('Ошибка при записи в лог файл. Error: ' + str(e))