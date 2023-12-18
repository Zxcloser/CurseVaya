from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtGui import QCursor
import sqlite3


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Вход в приложение "Отдел кадров"')


        # Установка окна посередине
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        self.setObjectName("LoginWindow")
        self.setFixedHeight(300)
        self.setFixedWidth(300)
        self.centralwidget = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setEnabled(True)
        self.frame.setGeometry(QtCore.QRect(0, 0, 901, 601))
        self.frame.setStyleSheet("border: 4px solid \'#FFFFFF\';\n"
                                 "border-radius: 15px;\n"
                                 "margin: 10px;\n"
                                 "background: #FFFFFF")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 861, 71))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.username_label = QtWidgets.QLabel('Логин:')
        self.username_input = QtWidgets.QLineEdit()
        self.password_label = QtWidgets.QLabel('Пароль:')
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_button = QtWidgets.QPushButton('Войти')
        self.login_button.clicked.connect(self.login)

        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.username_label)
        hbox1.addWidget(self.username_input)
        vbox.addLayout(hbox1)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.password_label)
        hbox2.addWidget(self.password_input)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.login_button)

        self.setLayout(vbox)

        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        self.cursor.execute("SELECT * FROM users WHERE login = ? AND password = ?", (username, password))
        user = self.cursor.fetchone()
        if user:
            self.mainWindow = MainWindow()
            self.mainWindow.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка входа', 'Неправильное имя пользователя или пароль')

class Dialog(QtWidgets.QDialog):
    def __init__(self, main, parent=None):
        super(Dialog, self).__init__(parent)
        self.main = main
        self.btn_add = QtWidgets.QPushButton("Добавить")
        self.btn_add.clicked.connect(self.add_rows)
        layout = QtWidgets.QGridLayout(self)
        self.line_edits = []  # Список для хранения экземпляров QLineEdit
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('hum_res.db')
        if not db.open():
            print("Не удалось установить соединение с базой данных.")
        else:
            # Получение названий столбцов из базы данных
            table = status.tableName()
            query = QSqlQuery(f"PRAGMA table_info({table})")
            i = 1
            while query.next():
                if query.value(1) != "номер":
                    label = QtWidgets.QLabel(f'Введите {query.value(1)}:')
                    line = QtWidgets.QLineEdit()
                    layout.addWidget(label, i, 1, 1, 1)
                    layout.addWidget(line, i, 2, 1, 1)
                    self.line_edits.append(line)  # Добавляем экземпляр QLineEdit в список
                    i += 1
            layout.addWidget(self.btn_add, i, 2, 1, 1)

    def add_rows(self):
        values = [line.text() for line in self.line_edits]  # Получаем значения из QLineEdit
        self.main.add_r(values)
        self.close()
class ChangeDialog(QtWidgets.QDialog):
    def __init__(self, main, parent=None):
        super(ChangeDialog, self).__init__(parent)
        self.main = main
        self.btn_change = QtWidgets.QPushButton("Подтвердить")
        self.btn_change.clicked.connect(self.change_row)
        layout = QtWidgets.QGridLayout(self)
        self.label = QtWidgets.QLabel("Изменить на")
        self.line = QtWidgets.QLineEdit()
        layout.addWidget(self.label, 1, 1, 1, 1)
        layout.addWidget(self.line, 1, 2, 1, 1)
        layout.addWidget(self.btn_change, 2, 2, 1, 1)
    def change_row(self):
        changed = self.line.text()
        self.main.changeRow(changed)
        self.close()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global status
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedHeight(600)
        MainWindow.setFixedWidth(900)
        MainWindow.setStyleSheet("background:rgb(109, 20, 184)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setEnabled(True)
        self.frame.setGeometry(QtCore.QRect(0, 0, 901, 601))
        self.frame.setStyleSheet("border: 4px solid \'#FFFFFF\';\n"
                                 "border-radius: 15px;\n"
                                 "margin: 10px;\n"
                                 "background: #FFFFFF")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 861, 71))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setMouseTracking(True)
        self.pushButton_3.setStyleSheet(
            "border: 0;\n"
            "border-radius: 15px;\n"
            "background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(245, 172, 235), stop:1 rgba(109, 20, 184));\n"
            "color: #FFFFFF;\n"
            "padding: 8px 16px;\n"
            "font-size: 16px;\n"
            "")
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(
            "border: 0;\n"
            "border-radius: 15px;\n"
            "background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(245, 172, 235), stop:1 rgba(109, 20, 184));\n"
            "color: #FFFFFF;\n"
            "padding: 8px 16px;\n"
            "font-size: 16px;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_5 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet(
            "border: 0;\n"
            "border-radius: 15px;\n"
            "background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(245, 172, 235), stop:1 rgba(109, 20, 184));\n"
            "color: #FFFFFF;\n"
            "padding: 8px 16px;\n"
            "font-size: 16px;")
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.pushButton_4 = QtWidgets.QComboBox(self.horizontalLayoutWidget)

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("hum_res.db")
        if not db.open():
            print("Unable to open database")
            sys.exit(1)
        tables_check = []
        tables = db.tables()
        for t in tables:
            if t != "sqlite_sequence":
                tables_check.append(t)
        self.pushButton_4.clear()
        self.pushButton_4.addItems(tables_check)


        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet(
            "border: 0;\n"
            "border-radius: 15px;\n"
            "background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(245, 172, 235), stop:1 rgba(109, 20, 184));\n"
            "color: #FFFFFF;\n"
            "padding: 8px 16px;\n"
            "font-size: 16px;\n"
            "")
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(
            "border: 0;\n"
            "border-radius: 15px;\n"
            "background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(245, 172, 235), stop:1 rgba(109, 20, 184));\n"
            "color: #FFFFFF;\n"
            "padding: 8px 16px;\n"
            "font-size: 16px;")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.tableWidget = QtWidgets.QTableView(self.frame)
        status = QSqlTableModel()
        status.setTable(self.pushButton_4.currentText())
        status.select()
        self.tableWidget.setModel(status)

        self.tableWidget.setGeometry(QtCore.QRect(40, 220, 830, 351))
        self.tableWidget.setMinimumSize(QtCore.QSize(830, 351))
        self.tableWidget.setMaximumSize(QtCore.QSize(811, 351))
        self.tableWidget.setStyleSheet("border: 4px solid \'#2DACEB\';\n"
                                       "border-radius: 15px;\n"
                                       "margin: 10px;\n"
                                       "background: #FFFFFF")
        self.tableWidget.setObjectName("tableWidget")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Отдел кадров"))
        self.pushButton_3.setText(_translate("MainWindow", "Добавить запись"))
        self.pushButton_5.setText(_translate("MainWindow", "Изменить запись"))
        self.pushButton_2.setText(_translate("MainWindow", "Удалить запись"))
        self.pushButton.setText(_translate("MainWindow", "Выход"))
        self.pushButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_5.setCursor(QCursor(QtCore.Qt.PointingHandCursor))



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.add_row)
        self.pushButton_4.currentTextChanged.connect(self.updateTable)
        self.pushButton_2.clicked.connect(self.deleteTable)
        self.pushButton_5.clicked.connect(self.change_D_row)

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('hum_res.db')
        db.open()

    def add_row(self):
        self.dialog = Dialog(self)
        self.dialog.exec_()
    def add_r(self, lst):
        r = status.record()
        table = status.tableName()
        query = QSqlQuery(f"PRAGMA table_info({table})")
        name = []
        while query.next():
            name.append(query.value(1))
        for i in range(len(lst)):
            r.setValue(name[i+1],lst[i])
        status.insertRecord(-1, r)
        status.select()

    def updateTable(self):
        global status
        table_name = self.pushButton_4.currentText()
        status = QSqlTableModel()
        status.setTable(table_name)
        status.select()
        self.tableWidget.setModel(status)
    def deleteTable(self):
        sel = self.on_sel()[0]
        if sel is not None:
            status.removeRow(sel)
            status.submitAll()
            status.select()
            self.tableWidget.setModel(status)
            self.tableWidget.reset()
    def change_D_row(self):
        self.changedialog = ChangeDialog(self)
        self.changedialog.exec_()
    def changeRow(self, new_value):
        sel = self.on_sel()
        if sel is not None:
            row = sel[0]
            column = sel[1]
            status.setData(status.index(row, column), new_value)
            status.submitAll()
            status.select()
    def on_sel(self):
        selected_indexes = self.tableWidget.selectedIndexes()
        if selected_indexes:
            row = selected_indexes[0].row()
            item = status.record(row).value(2)
            column = selected_indexes[0].column()
            return row, column
        else:
            return None

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    l = LoginWindow()
    l.show()
    sys.exit(app.exec_())