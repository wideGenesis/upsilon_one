# -*- coding: utf-8 -*-
import json
import requests
import datetime
import sys
from quotes.sql_queries import *
from time import sleep
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog


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


class MainWin(QDialog):

    def __init__(self):
        super().__init__()  # Call the inherited classes __init__ method
        uic.loadUi('cmd_client.ui', self)  # Load the .ui file
        self.initUI()
        self.show()

    def initUI(self):
        self.hostComboBox.currentIndexChanged.connect(self._host_combobox_changed)
        self.portComboBox.currentIndexChanged.connect(self._port_combobox_changed)
        self.actionComboBox.currentIndexChanged.connect(self._action_combobox_changed)
        self.actionDetailComboBox.currentIndexChanged.connect(self._actiondetail_combobox_changed)

        # self.chanelLineEdit.textChanged.connect(self._chanelTextChanged)
        # self.userIDLineEdit.textChanged.connect(self._userIdTextChanged)
        # self.messageTextEdit.textChanged.connect(self._messageTextChanged)

        self.sendCMADPushButton.clicked.connect(self._sendCMDButtonClicked)
        self.sendCMADPushButton.setEnabled(True)
        self.chanelLabel.hide()
        self.chanelLineEdit.hide()

    def _host_combobox_changed(self, indx):
        debug(f"Index: {indx}")
        if indx == 0:
            self.hostLabel.setText("Local host")
        if indx == 1:
            self.hostLabel.setText("Instance")

    def _port_combobox_changed(self, indx):
        debug(f"_port_combobox_changed Index: {indx} len={len(self.portComboBox)}")
        if indx == 0:
            self.portLabel.setText("UpsilonBot")
            self.actionComboBox.setItemText(0, "send_to")
            self.userIDLabel.show()
            self.userIDLineEdit.show()
            self.chanelLabel.hide()
            self.chanelLineEdit.hide()
            self.chanelLineEdit.clear()
            self.messageLabel.show()
            self.messageTextEdit.show()
            while len(self.actionComboBox) > 1:
                self.actionComboBox.removeItem(1)
            self.actionDetailLabel.show()
            self.actionDetailComboBox.show()
            self.actionDetailComboBox.setItemText(0, "message")
            while len(self.actionDetailComboBox) > 1:
                self.actionDetailComboBox.removeItem(1)
            self.actionDetailComboBox.addItem("broadcast_message")
            self.actionDetailComboBox.addItem("broadcast_poll")
            self.actionDetailComboBox.addItem("sac_pies")

        if indx == 1:
            self.portLabel.setText("Gatekeeper")
            self.actionComboBox.setItemText(0, "join_to")
            self.userIDLabel.hide()
            self.userIDLineEdit.hide()
            self.userIDLineEdit.clear()
            self.chanelLabel.show()
            self.chanelLineEdit.show()
            self.messageLabel.hide()
            self.messageTextEdit.hide()
            self.messageTextEdit.clear()
            self.actionDetailLabel.show()
            self.actionDetailComboBox.show()
            while len(self.actionComboBox) > 1:
                self.actionComboBox.removeItem(1)
            self.actionComboBox.addItem("leave_channel")
            self.actionDetailComboBox.setItemText(0, "simple_chat")
            while len(self.actionDetailComboBox) > 1:
                self.actionDetailComboBox.removeItem(1)
            self.actionDetailComboBox.addItem("private_chat")

    def _action_combobox_changed(self, indx):
        debug(f"_action_combobox_changed Index: {indx} len={len(self.actionComboBox)}")
        action_text = self.actionComboBox.itemText(indx)
        if action_text == "send_to":
            self.userIDLabel.show()
            self.userIDLineEdit.show()
            self.chanelLabel.hide()
            self.chanelLineEdit.hide()
            self.messageLabel.show()
            self.messageTextEdit.show()
            self.actionDetailLabel.show()
            self.actionDetailComboBox.show()
            self.actionDetailComboBox.setItemText(0, "message")
            while len(self.actionDetailComboBox) > 1:
                self.actionDetailComboBox.removeItem(1)
            self.actionDetailComboBox.addItem("broadcast_message")
            self.actionDetailComboBox.addItem("broadcast_poll")
            self.actionDetailComboBox.addItem("sac_pies")
        if action_text == "join_to":
            self.userIDLabel.hide()
            self.userIDLineEdit.hide()
            self.chanelLabel.show()
            self.chanelLineEdit.show()
            self.messageLabel.hide()
            self.messageTextEdit.hide()
            self.actionDetailLabel.show()
            self.actionDetailComboBox.show()
            self.actionDetailComboBox.setItemText(0, "simple_chat")
            while len(self.actionDetailComboBox) > 1:
                self.actionDetailComboBox.removeItem(1)
            self.actionDetailComboBox.addItem("private_chat")
        if action_text == "leave_channel":
            self.userIDLabel.hide()
            self.userIDLineEdit.hide()
            self.chanelLabel.show()
            self.chanelLineEdit.show()
            self.messageLabel.hide()
            self.messageTextEdit.hide()
            self.actionDetailLabel.hide()
            self.actionDetailComboBox.hide()
            self.actionDetailComboBox.setItemText(0, "")
            while len(self.actionDetailComboBox) > 1:
                self.actionDetailComboBox.removeItem(1)

    def _actiondetail_combobox_changed(self, indx):
        debug(f"_actiondetail_combobox_changed Index: {indx} len={len(self.actionDetailComboBox)}")
        actiondetail_text = self.actionDetailComboBox.itemText(indx)
        if actiondetail_text == "broadcast_message":
            self.userIDLabel.hide()
            self.userIDLineEdit.hide()
            self.chanelLabel.hide()
            self.chanelLineEdit.hide()
            self.messageLabel.show()
            self.messageTextEdit.show()
            self.actionDetailLabel.show()
            self.actionDetailComboBox.show()
        elif actiondetail_text == "broadcast_poll":
            self.userIDLabel.hide()
            self.userIDLineEdit.hide()
            self.chanelLabel.hide()
            self.chanelLineEdit.hide()
            self.messageLabel.hide()
            self.messageTextEdit.hide()
            self.actionDetailLabel.show()
            self.actionDetailComboBox.show()
        else:
            self.userIDLabel.show()
            self.userIDLineEdit.show()
            self.chanelLabel.hide()
            self.chanelLineEdit.hide()
            self.messageLabel.show()
            self.messageTextEdit.show()
            self.actionDetailLabel.show()
            self.actionDetailComboBox.show()

    # def _chanelTextChanged(self, txt):
    #     action_text = self.actionComboBox.itemText(self.actionComboBox.currentIndex())
    #     if len(txt) != 0 and (action_text == "join_to" or action_text == "leave_channel"):
    #         self.sendCMADPushButton.setEnabled(True)
    #     else:
    #         self.sendCMADPushButton.setEnabled(False)
    #
    # def _userIdTextChanged(self, txt):
    #     action_text = self.actionComboBox.itemText(self.actionComboBox.currentIndex())
    #     message_text = self.messageTextEdit.toPlainText()
    #     if len(txt) != 0 and len(message_text) != 0 and action_text == "send_to":
    #         self.sendCMADPushButton.setEnabled(True)
    #     else:
    #         self.sendCMADPushButton.setEnabled(False)
    #
    # def _messageTextChanged(self):
    #     action_text = self.actionComboBox.itemText(self.actionComboBox.currentIndex())
    #     actiondetail_text = self.actionDetailComboBox.itemText(self.actionDetailComboBox.currentIndex())
    #     userid_text = self.userIDLineEdit.text()
    #     message_text = self.messageTextEdit.toPlainText()
    #     if (len(message_text) != 0 and  action_text == "send_to" and ( actiondetail_text == "broadcast_message" or
    #                                                                   len(userid_text) != 0 :
    #         self.sendCMADPushButton.setEnabled(True)
    #     else:
    #         self.sendCMADPushButton.setEnabled(False)

    def _sendCMDButtonClicked(self):
        print("send_command")
        with requests.Session() as session:
            rhost = self.hostComboBox.itemText(self.hostComboBox.currentIndex())
            rport = self.portComboBox.itemText(self.portComboBox.currentIndex())
            raction = self.actionComboBox.itemText(self.actionComboBox.currentIndex())
            ruser_id = self.userIDLineEdit.text()
            chanel = self.chanelLineEdit.text()
            rmsg = self.messageTextEdit.toPlainText()
            url = f'http://{rhost}:{rport}/{COMMAND_TOKEN}/'
            raction_detail = self.actionDetailComboBox.itemText(self.actionDetailComboBox.currentIndex())
            data = {}
            if raction == 'send_to':
                if raction_detail == 'message':
                    data = {'action': raction, 'value': raction_detail, 'id': ruser_id, 'msg': rmsg}
                elif raction_detail == 'sac_pies':
                    data = {'action': raction, 'value': raction_detail, 'id': ruser_id, 'msg': ""}
                elif raction_detail == 'broadcast_message':
                    data = {'action': raction, 'value': raction_detail, 'id': "", 'msg': rmsg}
                elif raction_detail == 'broadcast_poll':
                    data = {'action': raction, 'value': raction_detail, 'id': "", 'msg': ""}
            if raction == 'join_to':
                data = {'action': raction, 'value': raction_detail, 'id': chanel}
            if raction == 'leave_channel':
                data = {'action': raction, 'value': chanel}

            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            try:
                request_result = session.post(url, data=json.dumps(data), headers=headers)
            except Exception as e:
                debug(e, ERROR)
            if request_result.status_code == requests.codes.ok:
                parsed_json = json.loads(request_result.text)
                print(parsed_json)


def main():
    app = QApplication(sys.argv)
    mainWin = MainWin()
    sys.exit(app.exec_())


if __name__ == '__main__':
    debug(f'Argv len: {len(sys.argv)}')
    if len(sys.argv) == 1 or len(sys.argv) == 0:
        main()
    if 1 < len(sys.argv) < 4:
        debug(f"usage: {sys.argv[0]} <host> <port> <action> <value> [<id> <msg>]")
        sys.exit(1)
    if len(sys.argv) > 4:
        host, port = sys.argv[1], int(sys.argv[2])
        if host == '':
            host = '127.0.0.1'
        if port == '':
            port = 8445
        print(f'H:{host} P:{port}')
        action, value = sys.argv[3], sys.argv[4]
        print(f'A:{action} V:{value}')
        msg = None
        user_id = None
        if len(sys.argv) == 7:
            user_id = sys.argv[5]
            msg = sys.argv[6]
        print("Client start")
        send_command(host, port, action, value, user_id, msg)
