from PySide2 import QtWidgets, QtGui, QtCore
from ...label.label import Label
import sqlite3 

class EditLabelDialog(QtWidgets.QDialog):
    """ 
    Dijalog za izmenu labele.
    """
    def __init__(self, label_service, user_id, parent=None):
        """ 
        Inicijalizator dijaloga za izmenu boje odabrane labele.

        :param label_service: servis za manipulisanje labelama
        :type label_service: LabelService
        :param user_id: id korisnika koji menja labelu - autora
        :type user_id: int
        :param parent: roditeljski widget.
        :type parent: QWidget
        """
        super().__init__(parent)

        self.user_id = user_id

        self.label_service = label_service

        self.setWindowTitle("Izmeni labelu")
        self.setWindowIcon(QtGui.QIcon("resources/icons/edit.png")) 

        self.resize(350, 150)
        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setGeometry(QtCore.QRect(140, 120, 140, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)

        self.label_name_color = QtWidgets.QLabel(self)
        self.label_name_color.setGeometry(QtCore.QRect(10, 20, 125, 20))
        self.label_name_color.setText("Naziv labele - boja labele:")
        self.label_name_color_selection = QtWidgets.QComboBox(self)
        self.label_name_color_selection.setGeometry(QtCore.QRect(140, 20, 200, 20))
        self._get_all_labels()

        self.new_label_color = QtWidgets.QLabel(self)
        self.new_label_color.setGeometry(QtCore.QRect(10, 60, 110, 20))
        self.new_label_color.setText("Nova boja labele:")
        self.new_label_color_input = QtWidgets.QLineEdit(self)
        self.new_label_color_input.setGeometry(QtCore.QRect(140, 60, 120, 20))       

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.new_label = None

    def _on_accept(self):
        """
        Metoda koja se poziva kada se pritisne na dugme ok.
        Prvo proverava popunjenost forme.
        """
        if self.new_label_color_input.text() == "": 
            QtWidgets.QMessageBox.warning(self, "Provera boje labele", "Mora se uneti nova boja labele!", QtWidgets.QMessageBox.Ok)
            return

        self.new_label = self.get_label()
        provera = self.label_service.edit(self.new_label, self.user_id)
        if provera == False:
            QtWidgets.QMessageBox.warning(self, "Provera izmene boje labele", "Samo autor moze menjati boju ove labele!", QtWidgets.QMessageBox.Ok)
            return

        self.accept()  
    
    def _get_all_labels(self):
        """
        Metoda koja dodaje u meni sve labele sa bojama.
        """
        for lab in  self.label_service.labels:
            labelNameColor = lab.name + " - " + lab.color
            self.label_name_color_selection.addItem(labelNameColor)
 
    def get_label(self):
        """
        Dobavlja podatke iz forme.
        :return: Label - nova labela.
        """ 
        labelNameColor = self.label_name_color_selection.itemText(self.label_name_color_selection.currentIndex()).split(" - ")
        return Label(labelNameColor[0], self.new_label_color_input.text(), self.user_id)



