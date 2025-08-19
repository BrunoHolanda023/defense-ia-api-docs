import sys
import json
import time
import hashlib
import requests
import urllib3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# CONFIG
SERVER_IP = '10.200.19.75'
USERNAME = 'system'
PASSWORD = '@Bruno9090'
API_HOST = f"https://{SERVER_IP}:443"
CLIENT_TYPE = 'WINPC_V2'


class DefenseClient:
    def __init__(self, host, username, password, client_type="WINPC"):
        self.host = host
        self.username = username
        self.password = password
        self.client_type = client_type
        self.token = None
        self.tempSig = None
        self.signature = None

    def _md5(self, value):
        return hashlib.md5(value.encode('utf-8')).hexdigest()

    def login(self):
        # First request
        url1 = f"{self.host}/brms/api/v1.0/accounts/authorize"
        payload1 = {
            "userName": self.username,
            "ipAddress": "",
            "clientType": self.client_type
        }

        r1 = requests.post(url1, json=payload1, verify=False)
        r1.raise_for_status()
        resp1 = r1.json()

        realm = resp1.get("realm") or resp1.get("digestRealm")
        randomKey = resp1["randomKey"]

        # 5 etapas de assinatura
        step1 = self._md5(self.password)
        step2 = self.username + step1
        step3 = self._md5(step2)
        step4 = self._md5(f"{self.username}:{realm}:{step3}")
        step5 = self._md5(f"{step4}:{randomKey}")
        self.tempSig = step4
        self.signature = step5

        # Second request
        payload2 = {
            "userName": self.username,
            "randomKey": randomKey,
            "encryptType": "MD5",
            "ipAddress": "",
            "signature": step5,
            "clientType": self.client_type
        }

        r2 = requests.post(url1, json=payload2, verify=False)
        r2.raise_for_status()
        resp2 = r2.json()
        self.token = resp2["token"]

    def get_persons(self):
        url = f"{self.host}/obms/api/v1.1/acs/person"
        headers = {
            "X-Subject-Token": self.token,
            "Accept-Language": "pt-BR",
            "Content-Type": "application/json"
        }

        r = requests.get(url, headers=headers, verify=False)
        r.raise_for_status()
        return r.json()["data"]


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teste - Listar Pessoas")
        self.setMinimumSize(500, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.button = QPushButton("Listar Pessoas")
        self.button.clicked.connect(self.carregar_pessoas)
        layout.addWidget(self.button)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(2)
        self.tabela.setHorizontalHeaderLabels(["Nome", "Documento"])
        layout.addWidget(self.tabela)

    def carregar_pessoas(self):
        try:
            client = DefenseClient(API_HOST, USERNAME, PASSWORD)
            client.login()
            pessoas = client.get_persons()

            self.tabela.setRowCount(len(pessoas))
            for i, p in enumerate(pessoas):
                nome = p.get("name", "")
                doc = p.get("document", "")
                self.tabela.setItem(i, 0, QTableWidgetItem(nome))
                self.tabela.setItem(i, 1, QTableWidgetItem(doc))

        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
