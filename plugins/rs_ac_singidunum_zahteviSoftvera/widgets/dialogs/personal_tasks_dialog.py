from PySide2 import QtWidgets, QtGui, QtCore
from .task_details_dialog import TaskDetailsDialog
from ...task.task_service import TaskService
from ...task.task import Task
import sqlite3

class PersonalTasksDialog(QtWidgets.QDialog):
    """ 
    Klasa koja predstavlja dialog u kojoj se prikazuje lista prihvacenih zadataka trenutnog korisnika
    """
    def __init__(self, task_service, user_id, parent=None):
        """
        Inicijalizator dijaloga za podesavanje i prikaz licnih zadataka.

        :param task_service: servis za manipulisanje zadacima
        :type task_service: TaskService
        :param user_id: id korisnika ciji su prihvaceni zadaci
        :type user_id: int
        :param parent: roditeljski widget dijaloga.
        :type parent: QWidget
        """
        # podesavanje dijaloga
        super().__init__(parent)
        self.setWindowTitle("Moji zadaci")
        # prosiriv ekran velicina
        self.resize(1400, 700)
        # postavljanje ikonice prozora
        self.setWindowIcon(QtGui.QIcon("resources/icons/category-item.png")) 

        self.user_id = user_id
        self.task_service = task_service
        self.task_service.load_personal_tasks(self.user_id)
        
        self.personal_tasks_dialog_layout = QtWidgets.QVBoxLayout()

        self.tasks_table = QtWidgets.QTableWidget(self)
        self.tasks_table.verticalHeader().setVisible(False)
        self.tasks_table.horizontalHeader().setVisible(True)
        self.tasks_table.horizontalHeader().setSortIndicatorShown(True)
        self.tasks_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tasks_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tasks_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tasks_table.setGridStyle(QtCore.Qt.SolidLine)
        self.tasks_table.setAlternatingRowColors(True)

        # popunjavamo toolbar
        self._set_toolbar()

        self._populate_table()

        self.tasks_table.horizontalHeader().setStretchLastSection(True)
        
        self.personal_tasks_dialog_layout.addLayout(self.personal_tasks_options_layout)
        self.personal_tasks_dialog_layout.addWidget(self.tasks_table)
        
        
        self.setLayout(self.personal_tasks_dialog_layout)

        self._bind_actions()
        self.tasks_table.setSortingEnabled(True)

    def _set_toolbar(self):
        """
        Populise toolbar sa korisnim funkcijama.
        """
        self.personal_tasks_options_layout = QtWidgets.QHBoxLayout()
        
        self.finish_task = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/tick.png"), "Razresi zadatak", self)
        self.task_details = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/application-detail.png"), "Detaljan pregled zadatka", self)

        self.personal_tasks_options_layout.addWidget(self.finish_task)
        self.personal_tasks_options_layout.addWidget(self.task_details)
        
    def _populate_table(self):
        """
        Popunjava tabelu sa podacima za licne zadatke.
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
        self.tasks_table.setRowCount(len(self.task_service.personal_tasks))

        for i, task in enumerate(self.task_service.personal_tasks):
            
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
        Uvezuje akcije sa funkcijama koje se izvrsavaju na njihovo okidanje.
        """
        self.finish_task.clicked.connect(self._on_finish)
        self.task_details.clicked.connect(self._on_task_details)

    def _on_finish(self):
        """
        Metoda koja menja status zadatka u prihvacen i dodaje datum i korisnika koji je prihvatio zadatak koji je selektovan.
        """
        self.tasks_table.setSortingEnabled(False)
        selected_task = self.tasks_table.selectedItems()
        if len(selected_task) == 0:
            return QtWidgets.QMessageBox.warning(self, "Obaveštenje", "Odaberite zadatak", QtWidgets.QMessageBox.Ok)
        task = self.get_task(selected_task)
        provera = self.task_service.edit(task, "razresen")
        if provera:
            self._populate_table()
            self.task_service.edit_task(task, "razresen")
            QtWidgets.QMessageBox.information(self, "Obaveštenje", "Zadatak uspesno razresen", QtWidgets.QMessageBox.Ok)
        self.tasks_table.setSortingEnabled(True)

    def _on_task_details(self):
        """
        Metoda koja otvara novi prozor sa svim detaljima odabranog zadatka.
        """
        self.tasks_table.setSortingEnabled(False)
        selected_task = self.tasks_table.selectedItems()
        if len(selected_task) == 0:
            return QtWidgets.QMessageBox.warning(self, "Obaveštenje", "Odaberite zadatak", QtWidgets.QMessageBox.Ok)
        task = self.get_task(selected_task)
        dialog = TaskDetailsDialog(task, self.task_service)
        dialog.exec_()
        
    def get_task(self, task):
        """
        Dobavlja podatke iz tabele.
        
        :param task: selektovan zadatak
        :type task: QItem
        :returns: Task -- inicializuje zadatak.
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
        imePrezimePrihvatio = task[8].text().split(" ")
        for uaid, in c.execute('SELECT user_id FROM users WHERE first_name = ? and last_name = ?', (imePrezimePrihvatio[0], imePrezimePrihvatio[1])):
            userAccepted_id = int(uaid)
        conn.close()
        return Task(task[1].text(), task[2].text(), label_id, author_id, task[6].text(), task[7].text(), userAccepted_id, task[9].text())
    