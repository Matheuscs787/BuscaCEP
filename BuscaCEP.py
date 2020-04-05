from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit, 
                            QGroupBox, QVBoxLayout, QFormLayout, QMessageBox)
import sys
import requests

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__()
        self.settings()
        self.create_widgets()
        self.create_layout()

    def settings(self):
        self.resize(300, 150)
        self.setWindowTitle('Consulta CEP')

    def create_widgets(self):
        self.ed_cep = QLineEdit(self)
        self.ed_cep.setMaxLength(8)
        self.ed_cep.setFixedWidth(60)
        self.ed_cep.returnPressed.connect(self.buscaCEP)
        self.ed_logradouro = QLineEdit()
        self.ed_logradouro.setReadOnly(True)
        self.ed_bairro = QLineEdit()
        self.ed_bairro.setReadOnly(True)
        self.ed_cidade = QLineEdit()
        self.ed_cidade.setReadOnly(True)
        self.ed_uf = QLineEdit()
        self.ed_uf.setReadOnly(True)
        self.ed_uf.setFixedWidth(20)
        
        self.button = QPushButton('Buscar')
        self.button.clicked.connect(self.buscaCEP)

    def create_layout(self):
        self.layout = QFormLayout()
        self.layout.addRow('            CEP: ', self.ed_cep)
        self.layout.addRow('Logradouro: ', self.ed_logradouro)
        self.layout.addRow('         Bairro: ', self.ed_bairro)
        self.layout.addRow('       Cidade: ', self.ed_cidade)
        self.layout.addRow('             UF: ', self.ed_uf)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def buscaCEP(self):
        if self.ed_cep.text().isdigit():
            cep_input = self.ed_cep.text()

            if len(cep_input) != 8:
                self.ed_logradouro.setText('')
                self.ed_bairro.setText('')
                self.ed_cidade.setText('')
                self.ed_uf.setText('')
                self.messsage_box = QMessageBox.information(self,"ALERTA", 'CEP precisa ter 8 dígitos!')
            else:
                request = requests.get('https://viacep.com.br/ws/{}/json/'.format(cep_input))

                address_data = request.json()

                if 'erro' not in address_data:
                    self.ed_logradouro.setText(format(address_data['logradouro']))
                    self.ed_bairro.setText(format(address_data['bairro']))
                    self.ed_cidade.setText(format(address_data['localidade']))
                    self.ed_uf.setText(format(address_data['uf']))
                else:
                    self.ed_logradouro.setText('')
                    self.ed_bairro.setText('')
                    self.ed_cidade.setText('')
                    self.ed_uf.setText('')
                    self.messsage_box = QMessageBox.information(self,"ALERTA", 'CEP não encontrado!')
        else:
            self.ed_logradouro.setText('')
            self.ed_bairro.setText('')
            self.ed_cidade.setText('')
            self.ed_uf.setText('')
            self.messsage_box = QMessageBox.information(self,"ALERTA", 'Digite somente números!')

root = QApplication([])
app = Window()
app.show()
sys.exit(root.exec_())
