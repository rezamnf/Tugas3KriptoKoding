from re import I
import sys
import time
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QFileDialog, QMessageBox
from RSA import *


class RSAScreen(QDialog):
    def __init__(self):
        super(RSAScreen, self).__init__()
        loadUi("UI/main.ui", self)

        self.pt_path = ''
        self.ct_path = ''
        self.RSA = RSA()

        self.generateKeyButton.clicked.connect(self.generate_key)
        self.saveKeyButton.clicked.connect(self.save_key)

        self.loadEKey.clicked.connect(self.load_public_key)
        self.loadDKey.clicked.connect(self.load_private_key)

        self.loadPlaintext.clicked.connect(self.load_pt)
        self.loadCiphertext.clicked.connect(self.load_ct)
        
        self.encryptButton.clicked.connect(self.encrypt)
        self.decryptButton.clicked.connect(self.decrypt)

    def readfile_bin(self, filename: str = "blue.png"):
    # Membaca file menjadi biner
        from pathlib import Path
        path = filename
        
        with open(path, 'rb') as file:
            temp = []
            byte = file.read(1)
            while byte:
                temp.append(int.from_bytes(byte, "big"))
                byte = file.read(1)
            
            temp = [bin(bits)[2:] for bits in temp]
            result = []
            for e in temp:
                if len(e) < 8:
                    e = (8 - len(e)) * "0" + e
                result.append(e)

            return "".join([chr(int(e, 2)) for e in result])

    def writefile_bin(self, filename: str="output.png", content: str=""):
    # Menulis biner ke dalam file
        from pathlib import Path

        path = filename
        
        with open(path, 'wb') as file:
            bytes = []
            for char in content:
                byte = int.to_bytes(ord(char), 1, "big")
                bytes.append(byte)
            file.write(b"".join(bytes))

    def generate_key(self):
        self.RSA.generate_key()
        self.nKey.setText(str(self.RSA.n))
        self.eKey.setText(str(self.RSA.e))
        self.dKey.setText(str(self.RSA.d))

    def save_key(self):
        try:
            n = int(self.nKey.toPlainText())
            e = int(self.eKey.toPlainText())
            d = int(self.dKey.toPlainText())
            name = QFileDialog.getSaveFileName(self, 'Save File', "Key/")
            self.RSA.save_key(name[0], e, n, d)
        except:
            self.warning_msg("Wrong Key!", "Key must be integer")

    def warning_msg(self,title, msg):
        temp = msg
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(str(title))
        msg.setInformativeText(temp)
        msg.exec_()
    
    def info_msg(self,title, msg):
        temp = msg
        msg = QMessageBox()
        # msg.setIcon(QMessageBox.Warning)
        msg.setText(str(title))
        msg.setInformativeText(temp)
        msg.exec_()

    def load_public_key(self):
        fname = QFileDialog().getOpenFileName(None, "Load Public Key", "Key/", "PublicKey (*.pub)")
        if(fname[0] == ''):
            self.warning_msg("Error","Pilih File Key")
        else:
            f = open(fname[0], "r")
            key = f.read().split(" ")
            f.close()
            self.nKey.setText(key[1])
            self.eKey.setText(key[0])

    def load_private_key(self):
        fname = QFileDialog().getOpenFileName(None, "Load Private Key", "Key/", "PrivateKey (*.pri)")
        if(fname[0] == ''):
            self.warning_msg("Error","Pilih File Key")
        else:
            f = open(fname[0], "r")
            key = f.read().split(" ")
            f.close()
            self.nKey.setText(key[1])
            self.dKey.setText(key[0])

    def load_pt(self):
        fname = QFileDialog().getOpenFileName(None, "Load Plaintext", "output_decrypt/", "Allfiles (*.*)")
        self.pt_path = (fname[0])
        self.refresh()

    def load_ct(self):
        fname = QFileDialog().getOpenFileName(None, "Load Ciphertext", "output_encrypt/", "Text (*.txt)")
        self.ct_path = (fname[0])
        self.refresh()
    
    def refresh(self):
        self.plaintextName.setText(self.pt_path)
        self.ciphertextName.setText(self.ct_path)

    def encrypt(self):
        s = time.time()
        
        if (self.nKey.toPlainText() == "" or self.eKey.toPlainText() == "" ):
            self.warning_msg("Wrong Key!", "Key must be filled!")
            return
        else:
            pt = self.readfile_bin(self.pt_path)
            ct = self.RSA.encrypt(pt, int(self.eKey.toPlainText()), int(self.nKey.toPlainText()))
            e = time.time()
            display = [hex(i) for i in ct]
            self.cipherResult.setPlainText(str(display))
            fname = QFileDialog.getSaveFileName(self, 'Save File',"output_encrypt/")
            if(fname[0] == ''):
                self.warning_msg("Error","Tulis Nama File")
            else:
                self.writefile_bin(fname[0],ct)
                self.pt_path = ""
                self.refresh()

        t = str(round(e-s, 10))
        pt_size = str(len(pt))
        ct_size = str(len(''.join(str(ct))))
        msg = "Time : " + t + " seconds\n" + "Plaintext : " + pt_size + " bytes\n" + "Ciphertext : " + ct_size + " bytes\n"
        self.info_msg("Encrypt Success!\n" + "Lihat File Hasil pada Folder Output!\n", msg)

    def decrypt(self):
        s = time.time()

        if (self.nKey.toPlainText() == "" or self.dKey.toPlainText() == "" ):
            self.warning_msg("Wrong Key!", "Key must be filled!")
            return
        else:
            ct = self.readfile_bin(self.ct_path)
            pt = self.RSA.decrypt(ct, int(self.dKey.toPlainText()), int(self.nKey.toPlainText()))
            e = time.time()
            self.plainResult.setPlainText(str(pt))
            fname = QFileDialog.getSaveFileName(self, 'Save File', "output_decrypt/")
            if(fname[0] == ''):
                self.warning_msg("Error","Tulis Nama File")
            else:
                self.writefile_bin(fname[0],pt)
                self.ct_path = ""
                self.refresh()

        t = str(round(e-s, 10))
        ct_size = str(len(ct))
        pt_size = str(len(pt))
        msg = "Time : " + t + " seconds\n" + "Ciphertext : " + ct_size + " bytes\n" + "Plaintext : " + pt_size + " bytes\n"
        self.info_msg("Decrypt Success!\n" + "Lihat File Hasil pada Folder Output!\n", msg)

app = QApplication(sys.argv)
widget = QStackedWidget()

main = RSAScreen()
main.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
