import json
import requests
import datetime
from project_shared import *
from quotes.sql_queries import *
from time import sleep


def send_command(host, port, action, value, id, msg):
    debug("send_command")
    with requests.Session() as session:
        url = f'http://{host}:{port}/{COMMAND_TOKEN}/'
        data = {}
        if id is None and msg is None:
            data = {'action': action, 'value': value }
        else:
            data = {'action': action, 'value': value, 'id': id, 'msg': msg}

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        try:
            request_result = session.post(url, data=json.dumps(data), headers=headers)
        except Exception as e:
            # print(e, 'Waiting 10 sec')
            sleep(10)
            request_result = session.post(url, data=json.dumps(data), headers=headers)
        if request_result.status_code == requests.codes.ok:
            parsed_json = json.loads(request_result.text)
            debug(parsed_json)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("usage:", sys.argv[0], "<host> <port> <action> <value>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    if host == '':
        host = '127.0.0.1'
    port = 8445
    action, value = sys.argv[3], sys.argv[4]
    msg = None
    id = None
    if len(sys.argv) > 5:
        id = sys.argv[5]
        msg = sys.argv[6]
    debug("Client start")
    send_command(host, port, action, value, id, msg)
