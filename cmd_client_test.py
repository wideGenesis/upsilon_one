import json
import requests
import datetime
from quotes.sql_queries import *
from time import sleep


def send_command(host, port, action, value, id, msg):
    print("send_command")
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
            print(parsed_json)


if __name__ == '__main__':
    print(f'Argv len: {len(sys.argv)}')
    if len(sys.argv) < 4:
        print("usage:", sys.argv[0], "<host> <port> <action> <value>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    if host == '':
        host = '127.0.0.1'
    if port == '':
        port = 8445
    print(f'H:{host} P:{port}')
    action, value = sys.argv[3], sys.argv[4]
    print(f'A:{action} V:{value}')
    msg = None
    id = None
    if len(sys.argv) == 6:
        id = sys.argv[5]
    if len(sys.argv) == 7:
        msg = sys.argv[6]
    print("Client start")
    send_command(host, port, action, value, id, msg)
