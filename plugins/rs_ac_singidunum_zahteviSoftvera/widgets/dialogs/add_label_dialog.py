from PySide2 import QtWidgets, QtGui, QtCore
from ...label.label import Label
import sqlite3 

class AddLabelDialog(QtWidgets.QDialog):
    """ 
    Dijalog za kreiranje labele.
    """
    def __init__(self, label_service, user_id, parent=None):
        """ 
        Inicijalizator dijaloga za dodavanje nove labele.

        :param label_service: servis za manipulisanje labelama
        :type label_service: LabelService
        :param user_id: id korisnika koji kreira labelu - autora
        :type user_id: int
        :param parent: roditeljski widget.
        :type parent: QWidget
        """
        super().__init__(parent)

        self.user_id = user_id

        self.label_service = label_service

        self.setWindowTitle("Kreiraj labelu")
        self.setWindowIcon(QtGui.QIcon("resources/icons/application-plus.png")) 

        self.resize(350, 150)
        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setGeometry(QtCore.QRect(140, 120, 140, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)

        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setText("Naziv labele")
        self.label_name.setGeometry(QtCore.QRect(10, 20, 110, 20))
        self.label_name_input = QtWidgets.QLineEdit(self)        
        self.label_name_input.setGeometry(QtCore.QRect(140, 20, 180, 20))       

        self.label_color = QtWidgets.QLabel(self)
        self.label_color.setGeometry(QtCore.QRect(10, 60, 110, 20))
        self.label_color.setText("Boja labele")
        self.label_color_input = QtWidgets.QLineEdit(self)
        self.label_color_input.setGeometry(QtCore.QRect(140, 60, 120, 20))

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.new_label = None

    def _on_accept(self):
        """
        Metoda koja se poziva kada se pritisne na dugme ok.
        Prvo proverava popunjenost forme. 
        """
        if self.label_name_input.text() == "": 
            QtWidgets.QMessageBox.warning(self, 
            "Provera naziva labele", "Naziv labele mora biti unet!", QtWidgets.QMessageBox.Ok)
            return
        if self.label_color_input.text() == "": 
            QtWidgets.QMessageBox.warning(self, 
            "Provera boje labele", "Mora se uneti boja labele!", QtWidgets.QMessageBox.Ok)
            return

        self.new_label = self.get_label()
        provera = self.label_service.create(self.new_label)
        if provera == False:
            QtWidgets.QMessageBox.warning(self, 
            "Provera naziva labele", "Labela sa tim nazivom vec postoji!", QtWidgets.QMessageBox.Ok)
            return

        self.accept()   
 
    def get_label(self):
        """
        Dobavlja podatke iz forme.
        :return: Label - nova labela.
        """   
        return Label(self.label_name_input.text(), self.label_color_input.text(), self.user_id)



