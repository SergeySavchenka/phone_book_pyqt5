from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
import re
import os


class MainWindow(QMainWindow):
    def __init__(self):
        # инициализатор родительского класса
        super().__init__()

        # создается окно и ему присваивается заголовок
        self.setWindowTitle("Телефонная книга")

        # создания центрального виджета и его размещение в основном окне
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # создание grid панели, закрепленной на центральном виджете, на которой будут размещаться все остальные элементы
        self.grid_layout = QGridLayout(self)
        central_widget.setLayout(self.grid_layout)

        # считывается количество не пустых строчек в файле с данными
        with open("database.txt") as database:
            self.lines = len([i for i in database if i.strip()])

        # создание таблицы с 2 столбцами и self.line столбцами, в которую будет выводиться инфомрация из файла
        self.base_table = QTableWidget(self)
        self.base_table.setColumnCount(2)
        self.base_table.setRowCount(self.lines)
        # заголовки столбцов
        self.base_table.setHorizontalHeaderLabels(["ФИО", "Номер"])
        # выравнивание заголовков по центру ячейки
        self.base_table.horizontalHeaderItem(0).setTextAlignment(4)
        self.base_table.horizontalHeaderItem(1).setTextAlignment(4)
        self.base_table.horizontalHeader().setFont(QFont('Times New Roman', 14))
        self.base_table.verticalHeader().setFont(QFont('Times New Roman', 14))

        # авторастяжение таблицы по всей свободной области
        self.base_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.base_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # заполнение таблицы данными
        self.fill_in_table()
        # размещение таблицы "table" на grid панели "grid_layout в 4 ряду и 0 столбце"
        self.grid_layout.addWidget(self.base_table, 3, 0)

        # кнопка для показа таблицы "table"
        self.base_bth = QPushButton('Показать базу данных')
        self.base_bth.setFont(QFont('Times New Roman', 14))
        self.base_bth.clicked.connect(self.show_base)
        self.grid_layout.addWidget(self.base_bth, 0, 0)

        # кнопка для добавления нового номера
        self.new_number_btn = QPushButton('Добавить новый телефон')
        self.new_number_btn.setFont(QFont('Times New Roman', 14))
        self.new_number_btn.clicked.connect(self.add_new_number)
        self.grid_layout.addWidget(self.new_number_btn, 1, 0)

        # кнопка для удаления номера
        self.delete_number_btn = QPushButton('Удалить телефон')
        self.delete_number_btn.setFont(QFont('Times New Roman', 14))
        self.delete_number_btn.clicked.connect(self.delete_number)
        self.grid_layout.addWidget(self.delete_number_btn, 2, 0)

        # создание формы для добавления нового номера
        self.table_for_new_num = QTableWidget(self)
        self.table_for_new_num.setColumnCount(2)
        self.table_for_new_num.setRowCount(4)
        self.table_for_new_num.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_for_new_num.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # заголовки отключаются
        self.table_for_new_num.horizontalHeader().setVisible(False)
        self.table_for_new_num.verticalHeader().setVisible(False)
        # объединение ячеек и размещение формы на "self.grid_layout"
        self.table_for_new_num.setSpan(0, 0, 1, 2)
        self.grid_layout.addWidget(self.table_for_new_num, 3, 0)

        # создание текста для объединенной ячейки
        self.head_add = QTableWidgetItem("Введите ФИО и номер")
        self.head_add.setFont(QFont('Times New Roman', 14))
        self.head_add.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)
        self.table_for_new_num.setItem(0, 0, self.head_add)

        # Пометка, куда вводить ФИО
        self.table_for_num_fio = QLabel('ФИО:')
        self.table_for_num_fio.setFont(QFont('Times New Roman', 13))
        self.table_for_num_fio.setAlignment(QtCore.Qt.AlignCenter)
        self.table_for_new_num.setCellWidget(1, 0, self.table_for_num_fio)

        # поле для ввода ФИО
        self.fio_input = QTableWidgetItem()
        self.fio_input.setFont(QFont('Calibri', 15))
        self.table_for_new_num.setItem(1, 1, self.fio_input)

        # пометка, куда вводить номер
        self.table_for_num_num = QLabel('Номер:')
        self.table_for_num_num.setFont(QFont('Times New Roman', 13))
        self.table_for_num_num.setAlignment(QtCore.Qt.AlignCenter)
        self.table_for_new_num.setCellWidget(2, 0, self.table_for_num_num)

        # поле для ввода номера
        self.num_input = QTableWidgetItem()
        self.num_input.setFont(QFont('Calibri', 15))
        self.table_for_new_num.setItem(2, 1, self.num_input)

        # подтверждение добавления контакта
        self.num_table_add = QPushButton("Добавить")
        self.num_table_add.setFont(QFont('Times New Roman', 13))
        self.num_table_add.clicked.connect(self.add)
        self.table_for_new_num.setCellWidget(3, 1, self.num_table_add)

        # кнопка возврата к базе данных
        self.add_num_table_cancel = QPushButton("Назад")
        self.add_num_table_cancel.setFont(QFont('Times New Roman', 13))
        self.add_num_table_cancel.clicked.connect(self.show_base)
        self.table_for_new_num.setCellWidget(3, 0, self.add_num_table_cancel)

        # создание формы для удаления номера
        self.table_delete_num = QTableWidget(self)
        self.table_delete_num.setColumnCount(2)
        self.table_delete_num.setRowCount(3)
        self.table_delete_num.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_delete_num.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # заголовки отключаются
        self.table_delete_num.horizontalHeader().setVisible(False)
        self.table_delete_num.verticalHeader().setVisible(False)
        # объединение ячеек
        self.table_delete_num.setSpan(0, 0, 1, 2)
        # объединение ячеек и размещение формы на "self.grid_layout"
        self.grid_layout.addWidget(self.table_delete_num, 3, 0)

        # создание текста для объединенной ячейки
        self.head_del = QTableWidgetItem("Введите номер для удаления контакта")
        self.head_del.setFont(QFont('Times New Roman', 14))
        self.head_del.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)
        self.table_delete_num.setItem(0, 0, self.head_del)

        # пометка, куда вводить номер
        self.table_for_del_num = QLabel('Номер:')
        self.table_for_del_num.setFont(QFont('Times New Roman', 13))
        self.table_for_del_num.setAlignment(QtCore.Qt.AlignCenter)
        self.table_delete_num.setCellWidget(1, 0, self.table_for_del_num)

        # поле для ввода номера
        self.num_del = QTableWidgetItem()
        self.num_del.setFont(QFont('Calibri', 15))
        self.table_delete_num.setItem(1, 1, self.num_del)

        # подтверждение удаления контакта
        self.num_table_del = QPushButton("Удалить")
        self.num_table_del.setFont(QFont('Times New Roman', 13))
        self.num_table_del.clicked.connect(self.del_number)
        self.table_delete_num.setCellWidget(2, 1, self.num_table_del)

        # кнопка возврата к базе данных
        self.del_num_table_cancel = QPushButton("Назад")
        self.del_num_table_cancel.setFont(QFont('Times New Roman', 13))
        self.del_num_table_cancel.clicked.connect(self.show_base)
        self.table_delete_num.setCellWidget(2, 0, self.del_num_table_cancel)

        # отключение форм для удаления и добавления номера
        self.table_for_new_num.setVisible(False)
        self.table_delete_num.setVisible(False)

    def show_base(self):
        """Метод для показа базы данных, в котором только форме 'base_table' свойство setVisible устанавливается True"""
        self.base_table.setVisible(True)
        self.table_for_new_num.setVisible(False)
        self.table_delete_num.setVisible(False)

    def add_new_number(self):
        """Метод для показа формы для добавления номера, в котором только форме 'table_for_new_num' свойство setVisible устанавливается True"""
        self.base_table.setVisible(False)
        self.table_for_new_num.setVisible(True)
        self.table_delete_num.setVisible(False)

    def delete_number(self):
        """Метод для показа формы для удаления номера, в котором только форме 'table_delete_num' свойство setVisible устанавливается True"""
        self.base_table.setVisible(False)
        self.table_for_new_num.setVisible(False)
        self.table_delete_num.setVisible(True)

    def check_format(self):
        """Метод для проверки, правильный ли формат у введенного номера для его последующего добавления в базу данных"""
        if ((self.table_for_new_num.item(2, 1).text()[0] == '8' and len(self.table_for_new_num.item(2, 1).text()) == 11)
                or (self.table_for_new_num.item(2, 1).text()[0] == '+' and len(self.table_for_new_num.item(2, 1).text()) == 12)):
            return True
        else:
            return False

    def add(self):
        """Метод для добавления нового контакта в базу"""
        self.base_table.setVisible(True)
        self.table_for_new_num.setVisible(False)

        # если формат введённого номера правильный, то он добавляется в базу, иначе выскакивает сообщение о неправильном формате фио или номера
        if self.table_for_new_num.item(1, 1).text() != '' \
                and self.table_for_new_num.item(2, 1).text() != '' \
                and len(self.table_for_new_num.item(1, 1).text().split()) == 3 \
                and self.check_format():

            with open('database.txt', 'a') as database:
                # в конце файла указатель переходит на новую строку и на нее добавляется новый контакт
                database.write('\n')
                database.write(self.table_for_new_num.item(1, 1).text() + ' ' + self.table_for_new_num.item(2, 1).text())

            self.base_table.setRowCount(0)
            # подсчёт количества рядов
            with open("database.txt") as database:
                self.lines = len([i for i in database if i.strip()])
            self.base_table.setRowCount(self.lines)

            # заполнение таблицы обновленными данными

            self.fill_in_table()

            # поля для ввода фио и номера очищаются
            self.table_for_new_num.item(1, 1).setText('')
            self.table_for_new_num.item(2, 1).setText('')
        else:
            # сообщение о неправильном формате введенного номера или фио
            QMessageBox.about(self, "Ошибка", "Неверный формат данных")

    def del_number(self):
        """Метод для удаления контакта из базы"""
        self.table_delete_num.setVisible(False)
        self.base_table.setVisible(True)

        # данные из файла 'database.txt' перезаписываются в файл 'database1.txt'
        with open("database.txt") as r, open('database1.txt', 'w') as o:
            for line in r:
                if self.table_delete_num.item(1, 1).text() not in line and line.strip():
                    o.write(line)

        # с помощью модуля os файла с 'database.txt' с неактуальными данными удаляется
        os.remove('database.txt')
        # файл 'database1.txt' с актуальными данными переименовывается в 'database.txt'
        os.rename('database1.txt', 'database.txt')

        self.base_table.setRowCount(0)
        # подсчёт количества рядов
        with open("database.txt") as database:
            self.lines = len(database.readlines())
        self.base_table.setRowCount(self.lines)

        # заполнение таблицы обновленными данными
        self.fill_in_table()

        # поле для ввода номера очищается
        self.table_delete_num.item(1, 1).setText('')

    def fill_in_table(self):
        """Метод для считывания данных о контактах из файла и вывода этих контактов в таблицу"""
        # открытие файла в режиме чтения
        with open("database.txt") as database:
            # счётчик рядов
            row = 0
            # чтение файла
            for i in database:
                if len(i.split()) == 4:
                    *name, number = i.split()
                    number = re.sub(r"\+?[78](\d{3})(\d{3})(\d\d)(\d\d)", r'+7(\1)\2-\3-\4', number)

                    # создание виджета для ФИО
                    person = QTableWidgetItem()
                    person.setText(name[0] + " " + name[1] + " " + name[2])
                    person.setFont(QFont('Calibri', 13))
                    person.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)

                    # создание виджета для номера
                    num = QTableWidgetItem()
                    num.setText(number)
                    num.setFont(QFont('Calibri', 13))
                    num.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)

                    # размещение виджетов в таблице
                    self.base_table.setItem(row, 0, QTableWidgetItem(person))
                    self.base_table.setItem(row, 1, QTableWidgetItem(num))

                    row += 1

        # установка размера окна исходя из количества контактов и минимального размера окна
        self.resize(500, 232 + self.lines * 30)
        self.setMinimumSize(400, 300)


# запуск программы
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
