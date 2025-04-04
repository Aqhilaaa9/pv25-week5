from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QTextEdit, QComboBox, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import QEvent
import re
import sys

class FormValidationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Week5.ui", self)
        self.setWindowTitle("Form Validation App - PV25 Week 5")

        self.name_input = self.findChild(QLineEdit, "name_input")
        self.email_input = self.findChild(QLineEdit, "email_input")
        self.age_input = self.findChild(QLineEdit, "age_input")
        self.phone_input = self.findChild(QLineEdit, "phone_input")
        self.address_input = self.findChild(QTextEdit, "address_input") 
        self.gender_input = self.findChild(QComboBox, "gender_input")
        self.education_input = self.findChild(QComboBox, "education_input")
        self.pushButton_save = self.findChild(QPushButton, "pushButton_save") 
        
        if self.pushButton_save:
            self.pushButton_save.clicked.connect(self.validate_form)
        else:
            QMessageBox.critical(self, "Error", "pushButton_save tidak ditemukan! Periksa nama objek di UI.")


        if self.pushButton_clear:
            self.pushButton_clear.clicked.connect(self.clear_fields)  # Tambahkan koneksi tombol Clear
        else:
            QMessageBox.critical(self, "Error", "pushButton_clear tidak ditemukan! Periksa nama objek di UI.")

        # Pasang event filter untuk menangkap tombol 'Q'
        QApplication.instance().installEventFilter(self)

    def validate_form(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        age = self.age_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.toPlainText().strip() 
        gender = self.gender_input.currentText()
        education = self.education_input.currentText()

        errors = []

        # Validasi Nama (tidak boleh kosong)
        if not name:
            errors.append("All fields are required")

        # Validasi Email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("Please enter a valid email address")

        # Validasi Umur (harus angka)
        if not age.isdigit():
            errors.append("Please enter a valid age (integer value)")

        # Validasi Nomor Telepon (harus dimulai dengan +62 dan diikuti 10-13 digit angka)
        if not phone.startswith("+62") or not phone[3:].isdigit() or not (10 <= len(phone[3:]) <= 13):
            errors.append("Phone number must start with +62 and contain 10–13 digits after +62")
        
        # Validasi Alamat (tidak boleh kosong)
        if not address:
            errors.append("All fields are required")

        # Validasi Gender & Pendidikan (harus dipilih)
        if self.gender_input.currentIndex() == 0:
            errors.append("All fields are required")

        if self.education_input.currentIndex() == 0:
            errors.append("All fields are required")

        if errors:
            self.show_error(errors[0])
        else:
            self.show_message("Success", "Profile saved successfully")
            self.clear_fields()

    def show_error(self, message):
        QMessageBox.warning(self, "Validation Error", message)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def clear_fields(self):
        self.name_input.clear()
        self.email_input.clear()
        self.age_input.clear()
        self.phone_input.clear()
        self.address_input.setPlainText("")
        self.gender_input.setCurrentIndex(0)
        self.education_input.setCurrentIndex(0)


    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.text().upper() == 'Q':  # Tekan 'Q' untuk keluar
            self.close()
            return True
        return super().eventFilter(obj, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FormValidationApp()
    window.show()
    sys.exit(app.exec_())
