from PySide2 import QtWidgets, QtGui, QtCore
from .dialogs.add_task_dialog import AddTaskDialog
from .dialogs.add_label_dialog import AddLabelDialog
from .dialogs.edit_label_dialog import EditLabelDialog
from .dialogs.delete_label_dialog import DeleteLabelDialog
from .dialogs.personal_tasks_dialog import PersonalTasksDialog
from .dialogs.task_details_dialog import TaskDetailsDialog
from ..task.task import Task
import datetime
import sqlite3

class TasksTool(QtWidgets.QMainWindow):
    """
    Klasa koja predstavlja glavni prozor plugin-a

    """
    def __init__(self, tasks, labels, parent: QtWidgets.QWidget=None):
        """
        Inicijalizator za prozor.

        :param tasks: task servis koji nam obezbedjuje operacije nad zadacima.
        :type tasks: TaskService
        :param labels: label servis koji nam obezbedjuje operacije nad labelama.
        :type labels: LabelService
        :param parent: roditelj glavnog prozora (default: None).
        :type parent: QWidget
        """
        # pozivanje super inicijalizatora
        super().__init__(parent) 
        
        # cuvanje atributa za task servise
        self.task_service = tasks

        # cuvanje atributa za label servise
        self.label_service = labels

        # korisnik koji koristi , TREBA NAPRAVITI DIJALOG ZA PRIJAVU NA POCETKU POKRETANJA PLUGINA
        self.user_id = 1

        # centralni widget je mesto deo glavnog prozora u koji treba da se smesti glavni widget aplikacije
        self.centralwidget = QtWidgets.QWidget(self)

        # layout kako bi namestili table        
        self.tasks_dialog_layout = QtWidgets.QGridLayout(self.centralwidget)
        # table widget
        self.tasks_table = QtWidgets.QTableWidget(self.centralwidget)
        self.tasks_table.verticalHeader().setVisible(False)
        self.tasks_table.horizontalHeader().setVisible(True)
        self.tasks_table.horizontalHeader().setSortIndicatorShown(True)
        self.tasks_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tasks_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tasks_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tasks_table.setGridStyle(QtCore.Qt.SolidLine)
        self.tasks_table.setAlternatingRowColors(True)

        # popunjavamo tabelu sa podacima
        self._populate_table()
        self.tasks_table.horizontalHeader().setStretchLastSection(True)

        self.setCentralWidget(self.centralwidget)

        self.tasks_table.setSortingEnabled(True)

        # popunjavamo toolbar
        self._set_toolbar()
        
        # pozivanje sopstvenih privatnih metoda
        self._bind_actions()

        self.tasks_dialog_layout.addLayout(self.hbox_layout, 0, 0, 1, 1)
        self.tasks_dialog_layout.addWidget(self.tasks_table, 1, 0, 2, 2)
        self.setLayout(self.tasks_dialog_layout)
        self.tasks_table.setFocusPolicy(QtCore.Qt.ClickFocus)

    def _set_toolbar(self):
        """
        Popunjava toolbar sa korisnim funkcijama.
        """

        self.hbox_layout = QtWidgets.QHBoxLayout()

        self.add_task = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/plus.png"), "Kreiraj zadatak", self)
        self.delete_task = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/minus.png"), "Obrisi zadatak", self)
        self.task_details = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/application-detail.png"), "Detaljan pregled zadatka")
        self.accept_task = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/application-plus-red.png"), "Prihvati zadatak", self)
        self.personal_tasks = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/category-item.png"), "Otvori svoje zadatke", self)
        self.add_label = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/application-plus.png"), "Kreiraj labelu", self)
        self.edit_label = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/edit.png"), "Izmeni labelu", self)
        self.delete_label = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/minus-circle.png"), "Obrisi labelu", self)
        
        self.hbox_layout.addWidget(self.add_task)
        self.hbox_layout.addWidget(self.delete_task)
        self.hbox_layout.addWidget(self.task_details)
        self.hbox_layout.addWidget(self.accept_task)
        self.hbox_layout.addWidget(self.personal_tasks)
        self.hbox_layout.addWidget(self.add_label)
        self.hbox_layout.addWidget(self.edit_label)
        self.hbox_layout.addWidget(self.delete_label)

    def _populate_table(self):
        """
        Popunjava tabelu sa podacima za zadatke.
        """
        self.tasks_table.clear()
        self.tasks_table.setColumnCount(10)
        self.tasks_table.setHorizontalHeaderLabels(
               ["Broj", "Naziv zadatka", "Kratak opis", "Naziv labela", "Boja lebele", "Autor zadatka", "Datum kreiranja", "Datum prihvatanja", "Prihvatio korisnik", "Status"])
        self.tasks_table.setColumnWidth(0, 50)       
        self.tasks_table.setColumnWidth(1, 200)
        self.tasks_table.setColumnWidth(2, 350)
        self.tasks_table.setColumnWidth(3, 100)
        self.tasks_table.setColumnWidth(4, 70)
        self.tasks_table.setColumnWidth(5, 150)
        self.tasks_table.setColumnWidth(6, 100)
        self.tasks_table.setColumnWidth(7, 110)
        self.tasks_table.setColumnWidth(8, 150)
        self.tasks_table.setColumnWidth(9, 80)
        self.tasks_table.setRowCount(len(self.task_service.tasks))

        for i, task in enumerate(self.task_service.tasks):
            
            number = QtWidgets.QTableWidgetItem(str(i+1))
            name = QtWidgets.QTableWidgetItem(task.name)

            desc = ""
            if len(task.description) > 100: # kratak opis - do 100 karaktera
                desc = task.description[:100] + "..."
            else: 
                desc = task.description

            description = QtWidgets.QTableWidgetItem(desc)

            #ako se obrise labela
            labelName = QtWidgets.QTableWidgetItem("")
            labelColor = QtWidgets.QTableWidgetItem("")
            if len(task.labelNameColor) == 2:
                labelName = QtWidgets.QTableWidgetItem(task.labelNameColor[0])
                labelColor =  QtWidgets.QTableWidgetItem(task.labelNameColor[1])

            authorFullName = QtWidgets.QTableWidgetItem(task.authorFullName)
            createdAt = QtWidgets.QTableWidgetItem(task.createdAt)
            acceptedAt = QtWidgets.QTableWidgetItem(task.acceptedAt)
            userAcceptedFullName = QtWidgets.QTableWidgetItem(task.userAcceptedFullName)
            status = QtWidgets.QTableWidgetItem(task.status)

            self.tasks_table.setItem(i, 0, number)
            self.tasks_table.setItem(i, 1, name)
            self.tasks_table.setItem(i, 2, description)
            self.tasks_table.setItem(i, 3, labelName)
            self.tasks_table.setItem(i, 4, labelColor)
            self.tasks_table.setItem(i, 5, authorFullName)
            self.tasks_table.setItem(i, 6, createdAt)
            self.tasks_table.setItem(i, 7, acceptedAt)
            self.tasks_table.setItem(i, 8, userAcceptedFullName)
            self.tasks_table.setItem(i, 9, status)

    def _bind_actions(self):
        """
        Uvezuje akcije sa funkcijama koje se izvršavaju na njihovo pokretanje.
        """
        self.add_task.clicked.connect(self._on_add_task)
        self.delete_task.clicked.connect(self._on_delete_task)
        self.task_details.clicked.connect(self._on_task_details)
        self.accept_task.clicked.connect(self._on_accept_task)
        self.personal_tasks.clicked.connect(self._personal_tasks)
        self.add_label.clicked.connect(self._on_add_label)
        self.edit_label.clicked.connect(self._on_edit_label)
        self.delete_label.clicked.connect(self._on_delete_label)
    
    def _on_add_task(self):
        """
        Metoda koja dodaje zadatak.
        """
        self.tasks_table.setSortingEnabled(False)
        dialog = AddTaskDialog(self.task_service, self.label_service, self.user_id)
        odgovor = dialog.exec_()
        if odgovor != 0:
            self._populate_table()
            self.task_service.add_task(dialog.new_task)
            QtWidgets.QMessageBox.information(self, "Obaveštenje", "Zadatak uspesno kreiran", QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.warning(self, "Obaveštenje", "Zadatak nije kreiran", QtWidgets.QMessageBox.Ok)            
        self.tasks_table.setSortingEnabled(True)    
    
    def _on_delete_task(self):
        """
        Metoda koja brise zadatak koji je selektovan.
        """
        self.tasks_table.setSortingEnabled(False)
        selected_task = self.tasks_table.selectedItems()
        if len(selected_task) == 0:
            return QtWidgets.QMessageBox.warning(self, "Obaveštenje", "Odaberite zadatak", QtWidgets.QMessageBox.Ok)
        task = self.get_task(selected_task)
        provera = self.task_service.delete(task, self.user_id)
        if provera:
            self._populate_table()
            self.task_service.delete_task(task)
            QtWidgets.QMessageBox.information(self, "Obaveštenje", "Zadatak uspešno obrisan", QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.warning(self, "Obaveštenje", "Morate biti autor i zadatak ne sme biti prihvacen", QtWidgets.QMessageBox.Ok)
        self.tasks_table.setSortingEnabled(True)
    
    def _on_task_details(self):
        """
        Metoda koja otvara novi prozor sa detaljima selektovanog zadatka.
        """
        self.tasks_table.setSortingEnabled(False)
        selected_task = self.tasks_table.selectedItems()
        if len(selected_task) == 0:
            return QtWidgets.QMessageBox.warning(self, "Obaveštenje", "Odaberite zadatak", QtWidgets.QMessageBox.Ok)
        task = self.get_task(selected_task)
        dialog = TaskDetailsDialog(task, self.task_service)
        dialog.exec_()

    def _on_accept_task(self):
        """
        Metoda koja menja status zadatka u prihvacen i dodaje datum i korisnika koji je prihvatio zadatak koji je selektovan.
        """
        self.tasks_table.setSortingEnabled(False)
        selected_task = self.tasks_table.selectedItems()
        if len(selected_task) == 0:
            return QtWidgets.QMessageBox.warning(self, "Obaveštenje", "Odaberite zadatak", QtWidgets.QMessageBox.Ok)
        task = self.get_task(selected_task)
        now = datetime.datetime.now()
        datumVreme = str(now.day) + "." + str(now.month) + "." + str(now.year) + " " + str(now.hour) + ":" + str(now.minute)
        provera = self.task_service.edit(task, "prihvacen", datumVreme, self.user_id)
        if provera:
            self._populate_table()
            self.task_service.edit_task(task, "prihvacen", datumVreme, self.user_id)
            QtWidgets.QMessageBox.information(self, "Obaveštenje", "Zadatak uspešno prihvacen", QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.information(self, "Obaveštenje", "Zadatak je ili vec prihvacen ili razresen!", QtWidgets.QMessageBox.Ok)
        self.tasks_table.setSortingEnabled(True)

    def _personal_tasks(self):
        """
        Metoda koja poziva odgovarajucu listu licnih zadataka.
        """
        dialog = PersonalTasksDialog(self.task_service, self.user_id)
        dialog.exec_()
        self._populate_table()

    def _on_add_label(self):
        """
        Metoda koja dodaje labelu.
        """
        self.tasks_table.setSortingEnabled(False)
        dialog = AddLabelDialog(self.label_service, self.user_id)
        odgovor = dialog.exec_()
        if odgovor != 0:
            self.label_service.add_label(dialog.new_label)
            QtWidgets.QMessageBox.information(self, "Obaveštenje", "Labela uspesno kreirana", QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.warning(self, "Obaveštenje", "Labela nije kreirana", QtWidgets.QMessageBox.Ok)            
        self.tasks_table.setSortingEnabled(True)

    def _on_edit_label(self):
        """
        Metoda koja menja boju za odabranu labelu.
        """
        self.tasks_table.setSortingEnabled(False)
        dialog = EditLabelDialog(self.label_service, self.user_id)
        odgovor = dialog.exec_()
        if odgovor != 0:
            self.label_service.edit_label(dialog.new_label, self.user_id)
            self._populate_table()
            QtWidgets.QMessageBox.information(self, "Obaveštenje", "Boja Labele uspesno promenjena", QtWidgets.QMessageBox.Ok)
        self.tasks_table.setSortingEnabled(True)     
        
    def _on_delete_label(self):
        """
        Metoda koja brise odabranu labelu.
        """
        self.tasks_table.setSortingEnabled(False)
        dialog = DeleteLabelDialog(self.label_service, self.user_id)
        odgovor = dialog.exec_()
        if odgovor != 0:
            self.label_service.delete_label(dialog.new_label, self.user_id)
            self.task_service.clearList() # redefinisemo novu listu kako bi izvukli zadatke sa praznim label_id
            self.task_service.load_tasks()
            self._populate_table()
            QtWidgets.QMessageBox.information(self, "Obaveštenje", "Labela uspesno obrisana", QtWidgets.QMessageBox.Ok)
        self.tasks_table.setSortingEnabled(True)  

    def get_task(self, task):
        """
        Metoda koja dobavlja podatke iz tabele.

        :returns: task - inicijalizuje zadatak.
        """ 

        conn = sqlite3.connect('plugins\\rs_ac_singidunum_zahteviSoftvera\\baza\\zahteviSoftvera.db')
        c = conn.cursor()

        label_id = 0
        if task[3].text() == "" and task[4].text() == "":
            label_id = None
        else:
            for lid, in c.execute('SELECT label_id FROM labels WHERE name = ? and color = ?', (task[3].text(), task[4].text())):
                label_id = int(lid)
        
        author_id = 0
        imePrezime = task[5].text().split(" ")
        for aid, in c.execute('SELECT user_id FROM users WHERE first_name = ? and last_name = ?', (imePrezime[0], imePrezime[1])):
            author_id = int(aid)

        userAccepted_id = 0
        if task[8].text() != "":
            imePrezimePrihvatio = task[8].text().split(" ")
            for uaid, in c.execute('SELECT user_id FROM users WHERE first_name = ? and last_name = ?', (imePrezimePrihvatio[0], imePrezimePrihvatio[1])):
                userAccepted_id = int(uaid)
        else:
            userAccepted_id = None

        conn.close()
        return Task(task[1].text(), task[2].text(), label_id, author_id, task[6].text(), task[7].text(), userAccepted_id, task[9].text())
