import sys
from PySide6 import QtWidgets
from Viste.Accedi import LoginWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())