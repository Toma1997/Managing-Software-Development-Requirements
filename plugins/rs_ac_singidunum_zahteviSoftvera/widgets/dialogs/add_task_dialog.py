from PySide2 import QtWidgets, QtCore, QtGui
import datetime

class AddTaskDialog(QtWidgets.QDialog):
    """
    Dijalog za dodavanje novog zahteva.
    """
    def __init__(self, parent=None):
        """
        Inicijalizator dijaloga za dodavanje novog zahteva.

        :param parent: roditeljski widget.
        :type parent: QWidget
        """
        super().__init__(parent)
        self.setWindowTitle("Dodaj zahtev")
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()

        self.name_input = QtWidgets.QLineEdit(self)
        self.description_input = QtWidgets.QLineEdit(self)
        self.label_input = QtWidgets.QLineEdit(self)

        # doraditi klasu za autora kao i za gore labelu
        #self.autor = Autor.getFullName()
        self.now = datetime.datetime.now()

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok 
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.form_layout.addRow("Naziv:", self.name_input)
        self.form_layout.addRow("Opis:", self.description_input)
        self.form_layout.addRow("Labela:", self.label_input)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def _on_accept(self):
        """
        Metoda koja se poziva kada se pritisne na dugme ok.
        Prvo proverava popunjenost forme. Ukoliko neko polje nije popunjeno korisniku se 
        prikazuje upozorenje.
        """
        if self.name_input.text() == "":
            QtWidgets.QMessageBox.warning(self, 
            "Provera naziva", "Naziv mora biti popunjen!", QtWidgets.QMessageBox.Ok)
            return
        if self.description_input.text() == "":
            QtWidgets.QMessageBox.warning(self, 
            "Provera opisa", "Opis mora biti popunjen!", QtWidgets.QMessageBox.Ok)
            return
        if not self.label_input.hasAcceptableInput():
            QtWidgets.QMessageBox.warning(self, 
            "Provera labele", "Labela mora biti popunjena!", QtWidgets.QMessageBox.Ok)
            return
        self.accept()

    def get_data(self):
        """
        Dobavlja podatke iz forme.

        :returns: dict -- recnik sa podacima iz forme.
        """
        return {
            "name": self.name_input.text(),
            "description": self.description_input.text(),
            "label": self.label_input.text(),
            #"author": self.autor,
            "created at": self.now.day + "." + self.now.month + "." + self.now.year + " " + self.now.hour + ":" + self.now.minute # trenutni datum
        }
    



