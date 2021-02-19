# -*- coding: utf-8 -*-
import json
import requests
import datetime
from quotes.sql_queries import *
from time import sleep
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QMainWindow



def send_command(rhost, rport, raction, rvalue, ruser_id, rmsg):
    print("send_command")
    with requests.Session() as session:
        url = f'http://{rhost}:{rport}/{COMMAND_TOKEN}/'
        data = {}
        if ruser_id is None and rmsg is None:
            data = {'action': raction, 'value': rvalue}
        else:
            data = {'action': raction, 'value': rvalue, 'id': ruser_id, 'msg': rmsg}

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


class MainWin(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.window = QWidget()
        self.window.setWindowTitle('PyQt5 App')
        self.layout = QGridLayout()

        self.hostLabel = QLabel("Host:")
        self.host = QComboBox()
        self.host.addItem("")
        self.host.addItem("127.0.0.1")
        self.host.addItem("104.154.228.185")
        self.host.setCurrentIndex(0)
        self.host.setPlaceholderText("Select host")
        self.host.currentIndexChanged.connect(self._host_combobox_changed)

        self.portLabel = QLabel("Port:")
        self.port = QComboBox()
        self.port.addItem("")
        self.port.addItem("8445")
        self.port.addItem("8443")
        self.port.setCurrentIndex(0)
        self.port.setPlaceholderText("Select port")
        self.port.currentIndexChanged.connect(self._port_combobox_changed)

        self.actionLabel = QLabel("Action:")
        self.action = QComboBox()
        self.action.addItem("")
        self.action.setCurrentIndex(0)
        self.action.setPlaceholderText("Select action")
        self.action.currentIndexChanged.connect(self._action_combobox_changed)

        self.useridLabel = QLabel("UserId:")
        self.user_id = QLineEdit()
        self.action.setPlaceholderText("Enter user_id")

        self.layout.addWidget(self.hostLabel, 0, 1)
        self.layout.addWidget(self.host, 0, 2)
        self.layout.addWidget(self.portLabel, 1, 1)
        self.layout.addWidget(self.port, 1, 2)
        self.layout.addWidget(self.actionLabel, 2, 1)
        self.layout.addWidget(self.action, 2, 2)
        self.layout.addWidget(self.useridLabel, 3, 1)
        self.layout.addWidget(self.user_id, 3, 2)
        self.window.setLayout(self.layout)
        self.window.show()

    def _host_combobox_changed(self, indx):
        debug(f"Index: {indx}")
        if indx == 0:
            self.hostLabel.setText("Host:")
        if indx == 1:
            self.hostLabel.setText("Local host:")
        if indx == 2:
            self.hostLabel.setText("Instance:")

    def _port_combobox_changed(self, indx):
        debug(f"Index: {indx}")
        if indx == 0:
            self.portLabel.setText("Port:")
        if indx == 1:
            self.portLabel.setText("Upsilon bot:")
        if indx == 2:
            self.portLabel.setText("Getekeeper:")

    def _action_combobox_changed(self, indx):
        debug(f"Index: {indx}")


def main():
    app = QApplication(sys.argv)
    mainWin = MainWin()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

    # print(f'Argv len: {len(sys.argv)}')
    # if len(sys.argv) < 4:
    #     print("usage:", sys.argv[0], "<host> <port> <action> <value>")
    #     sys.exit(1)
    #
    # host, port = sys.argv[1], int(sys.argv[2])
    # if host == '':
    #     host = '127.0.0.1'
    # if port == '':
    #     port = 8445
    # print(f'H:{host} P:{port}')
    # action, value = sys.argv[3], sys.argv[4]
    # print(f'A:{action} V:{value}')
    # msg = None
    # user_id = None
    # if len(sys.argv) == 7:
    #     user_id = sys.argv[5]
    #     msg = sys.argv[6]
    # print("Client start")
    # send_command(host, port, action, value, user_id, msg)
