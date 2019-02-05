import sqlite3

class Task:
    """
    Ova klasa predstavlja osnovu za svaki konkretni zadatak.
    """
    def __init__(self, name, description, label_id, author_id, createdAt, acceptedAt, userAccepted_id, status):
        """
        Inicijalizator.

        :param name: ime zadatka
        :type name: str
        :param description: kratak opis zadatka
        :type description: str
        :param label_id: id labele kojom je naznacen zadatak
        :type label_id: int
        :param author_id: id autora zadatka
        :type author_id: int
        :param createdAt: datum i vreme kreiranja zadatka
        :type createdAt: str
        :param acceptedAt: datum i vreme prihvatanja zadatka
        :type acceptedAt: str
        :param userAccepted_id: id korisnika koji je prihvatio zadatak
        :type userAccepted_id: int
        :param status: status zadatka 
        :type status: str
        """
        self._name = name
        self._description = description
        self._label_id = label_id
        self._author_id = author_id
        self._name = name
        self._createdAt = createdAt
        self._acceptedAt = acceptedAt
        self._userAccepted_id = userAccepted_id
        self._status = status
        self._labelNameColor = [] # lista gde ce se naknadno pribaviti naziv i boja labele na osnovu id
        self._authorFullName = "" # puno ime i prezime autora u jednom stringu
        self._userAcceptedFullName = "" # puno ime i prezime korisnika koji je prihvatio zadatak
 
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value
    
    @property
    def label_id(self):
        return self._label_id

    @label_id.setter
    def label_id(self, value):
        self._label_id = value

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, value):
        self._author_id = value
    
    @property
    def createdAt(self):
        return self._createdAt

    @createdAt.setter
    def createdAt(self, value):
        self._createdAt = value
    
    @property
    def acceptedAt(self):
        return self._acceptedAt

    @acceptedAt.setter
    def acceptedAt(self, value):
        self._acceptedAt = value
    
    @property
    def userAccepted_id(self):
        return self._userAccepted_id

    @userAccepted_id.setter
    def userAccepted_id(self, value):
        self._userAccepted_id = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def labelNameColor(self):
        """
        Metoda koja dobavlja iz baze naziv i boju labele kojom je naznacen zadatak.
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_zahteviSoftvera\\baza\\zahteviSoftvera.db')
        c = conn.cursor()
        for name, color in c.execute('SELECT name, color FROM labels WHERE label_id = ?', (self.label_id,)):
            self._labelNameColor = [name, color]
        conn.close()
        return self._labelNameColor
    
    @property
    def authorFullName(self):
        """
        Metoda koja dobavlja iz baze puno ime korisnika koji je kreirao zadatak.
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_zahteviSoftvera\\baza\\zahteviSoftvera.db')
        c = conn.cursor()
        for first_name, last_name in c.execute('SELECT first_name, last_name FROM users WHERE user_id = ?', (self.author_id,)):
            self._authorFullName = first_name + " " + last_name
        conn.close()
        return self._authorFullName
    
    @property
    def userAcceptedFullName(self):
        """
        Metoda koja dobavlja iz baze puno ime korisnika koji je prihvatio zadatak.
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_zahteviSoftvera\\baza\\zahteviSoftvera.db')
        c = conn.cursor()
        for first_name, last_name in c.execute('SELECT first_name, last_name FROM users WHERE user_id = ?', (self.userAccepted_id,)):
            self._userAcceptedFullName = first_name + " " + last_name
        conn.close()
        return self._userAcceptedFullName

    def get_db_data(self):
        """
        Metoda koja daje vrednosti za dobavljanje podataka iz baze.
        """
        return (self.name, self.description, self.label_id, self.author_id, self.createdAt, self.acceptedAt, self.userAccepted_id, self.status)