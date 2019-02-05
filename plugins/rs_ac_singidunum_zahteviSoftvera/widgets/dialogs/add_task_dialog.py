from PySide2 import QtWidgets, QtGui, QtCore
from .add_label_dialog import AddLabelDialog
from ...task.task import Task
import sqlite3
import datetime

class AddTaskDialog(QtWidgets.QDialog):
    """ 
    Dijalog za kreiranje novog zadatka.
    """
    def __init__(self, task_service, label_service, user_id, parent=None):
        """ 
        Inicijalizator dijaloga za dodavanje novog zadatka.

        :param task_service: servis za maniplusanje nad zadacima
        :type task_service: TaskService
        :param label_service: servis za maniplusanje nad labelama
        :type label_service: LabelService
        :param user_id: id korisnika koji kreira zadatak
        :type user_id: int
        :param parent: roditeljski widget.
        :type parent: QWidget
        """
        super().__init__(parent)
        
        self.label_service = label_service
        self.task_service = task_service
        self.user_id = user_id

        self.setWindowTitle("Kreiraj zadatak")
        self.setWindowIcon(QtGui.QIcon("resources/icons/plus.png")) 

        self.resize(900, 250)
        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setGeometry(QtCore.QRect(500, 200, 200, 50))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)

        self.task_name = QtWidgets.QLabel(self)
        self.task_name.setText("Naziv zadatka:")
        self.task_name.setGeometry(QtCore.QRect(10, 20, 115, 20))
        self.task_name_input = QtWidgets.QLineEdit(self)        
        self.task_name_input.setGeometry(QtCore.QRect(140, 20, 300, 20))       

        self.task_description = QtWidgets.QLabel(self)
        self.task_description.setGeometry(QtCore.QRect(10, 65, 115, 20))
        self.task_description.setText("Opis zadatka:")
        self.task_description_input = QtWidgets.QLineEdit(self)
        self.task_description_input.setGeometry(QtCore.QRect(140, 65, 700, 20))

        self.label_name_color = QtWidgets.QLabel(self)
        self.label_name_color.setGeometry(QtCore.QRect(10, 105, 125, 20))
        self.label_name_color.setText("Naziv labele - boja labele:")
        self.label_name_color_selection = QtWidgets.QComboBox(self)
        self.label_name_color_selection.setGeometry(QtCore.QRect(140, 105, 250, 20))
        self._get_all_labels()

        self.add_label = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/application-plus.png"), "Kreiraj labelu", self)
        self.add_label.clicked.connect(self._on_add_label)
        self.add_label.setGeometry(QtCore.QRect(430, 105, 140, 30))

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.new_task = None

    def _on_add_label(self):
        """
        Metoda koja dodaje labelu.
        """
        dialog = AddLabelDialog(self.label_service, self.user_id)
        odgovor = dialog.exec_()
        if odgovor != 0:
            self.label_service.add_label(dialog.new_label)
            self.label_name_color_selection.addItem(dialog.new_label.name + " - " + dialog.new_label.color)
            QtWidgets.QMessageBox.information(self, "Obaveštenje", "Labela uspesno kreirana", QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.warning(self, "Obaveštenje", "Labela nije kreirana", QtWidgets.QMessageBox.Ok)          

    def _on_accept(self):
        """
        Metoda koja se poziva kada se pritisne na dugme ok.
        Prvo proverava popunjenost forme. 
        Ukoliko neko polje nije popunjeno korisniku se prikazuje upozorenje.
        """
        if self.task_name_input.text() == "": 
            QtWidgets.QMessageBox.warning(self, "Provera naziva zadatka", "Naziv zadatka mora biti unet!", QtWidgets.QMessageBox.Ok)
            return

        if self.task_description_input.text() == "": 
            QtWidgets.QMessageBox.warning(self, "Provera boje labele", "Mora se uneti opis zadatka!", QtWidgets.QMessageBox.Ok)
            return

        # kreira se novi zadatak i dodaje u listu ako je prethodno sve u redu
        self.new_task = self.get_task()
        provera = self.task_service.create(self.new_task)
        if provera == False:
            QtWidgets.QMessageBox.warning(self, "Provera kreiranja zadatka", "Zadatak sa tim nazivom i opisom vec postoji!", QtWidgets.QMessageBox.Ok)
            return
        
        self.accept()   

    def _get_all_labels(self):
        """
        Metoda koja dodaje u meni sve labele sa bojama.
        """
        for lab in  self.label_service.labels:
            labelNameColor = lab.name + " - " + lab.color
            self.label_name_color_selection.addItem(labelNameColor)
    
    def get_task(self):
        """
        Dobavlja podatke iz forme.
        :returns: Task - novi zadatak.
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_zahteviSoftvera\\baza\\zahteviSoftvera.db')
        c = conn.cursor()

        label_id = 0
        labelNameColor = self.label_name_color_selection.itemText(self.label_name_color_selection.currentIndex()).split(" - ")
        for lid, in c.execute('SELECT label_id FROM labels WHERE name = ? and color = ?', (labelNameColor[0], labelNameColor[1])):
            label_id = int(lid)
        conn.close()

        now = datetime.datetime.now()
        datumVreme = str(now.day) + "." + str(now.month) + "." + str(now.year) + " " + str(now.hour) + ":" + str(now.minute)

        return Task(self.task_name_input.text(), self.task_description_input.text(), label_id, self.user_id, datumVreme, "", None, "neprihvacen")
    