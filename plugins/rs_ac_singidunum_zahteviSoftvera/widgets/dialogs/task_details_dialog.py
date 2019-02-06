from PySide2 import QtWidgets, QtGui, QtCore
from ...task.task_service import TaskService
from ...task.task import Task
import sqlite3

class TaskDetailsDialog(QtWidgets.QDialog):
    """ 
    Klasa koja predstavlja dialog u kojoj se prikazuje lista informacija o odabranom zadatku
    """
    def __init__(self, task, task_service, parent=None):
        """
        Inicijalizator dijaloga za podesavanje i prikaz licnih zadataka.

        :param task: zadatak koji se selektovan za detaljni pregled
        :type task: Task
        :param task_service: servis za manipulisanje zadacima
        :type task_service: TaskService
        :param user_id: id korisnika ciji su prihvaceni zadaci
        :type user_id: int
        :param parent: roditeljski widget dijaloga.
        :type parent: QWidget
        """
        # podesavanje dijaloga
        super().__init__(parent)
        self.setWindowTitle("Detalji odabranog zadatka")
        # prosiriv ekran velicina
        self.resize(1200, 700)
        # postavljanje ikonice prozora
        self.setWindowIcon(QtGui.QIcon("resources/icons/application-detail.png")) 

        self.selected_task = task
        self.task_service = task_service
        self.task_details = self.task_service.task_details(self.selected_task)

        self.personal_tasks_dialog_layout = QtWidgets.QVBoxLayout()

        self.tasks_table = QtWidgets.QTableWidget(self)
        self.tasks_table.verticalHeader().setVisible(True)
        self.tasks_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tasks_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tasks_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        #self.tasks_table.setGridStyle(QtCore.Qt.SolidLine)

        self._populate_table()

        self.tasks_table.verticalHeader().setStretchLastSection(True)
        self.personal_tasks_dialog_layout.addWidget(self.tasks_table)
        self.setLayout(self.personal_tasks_dialog_layout)
        
    def _populate_table(self):
        """
        Popunjava tabelu sa podacima za licne zadatke.
        """
        self.tasks_table.clear()
        self.tasks_table.setColumnCount(1)
        self.tasks_table.setVerticalHeaderLabels(
               ["Broj", "Naziv zadatka", "Ceo opis", "Labela", "Autor zadatka", "Datum kreiranja", "Datum prihvatanja", "Prihvatio korisnik", "Status"])
        self.tasks_table.setColumnWidth(0, 1160)
        
        self.tasks_table.setRowCount(len(self.task_details))

        for i, detail in enumerate(self.task_details):
            detailItem = QtWidgets.QTableWidgetItem(detail)
            self.tasks_table.setItem(i, 0, detailItem)
    