import sqlite3
from ..label.label import Label

class LabelService:
    """
    Klasa koja manipulise nad labelama.
    """
    def __init__(self):
        """
        Inicijalizator servisne klase za labele.
        """
        self._labels = list()
        

    def create(self, label):
        """
        Kreira labelu, ako vec ne postoji ista sa takvim nazivom.
        :param label: instanca label koju dodajemo.
        :type label: label
        :returns: bool -- podatak da li je kreirana labela.
        """
        for lab in self._labels:
            if label.name == lab.name:
                return False

        self._labels.append(label)
        return True

    def delete(self, label, author_id):
        """
        Brise labelu. Labelu moze obrisati samo autor.

        :param label: instanca label koju brisemo.
        :type label: label
        :param author_id: autor labele.
        :type author_id: int
        :returns: bool -- podatak o uspesnosti brisanja.
        """
        for lab in self._labels:
            if label.name == lab.name and label.color == lab.color and lab.author_id == author_id:
                self._labels.remove(lab)
                return True
        return False

    def edit(self, label, author_id):
        """
        Menja boju labele.

        :param label: instanca label koju menjamo.
        :type label: label
        :param author_id: autor labele.
        :type author_id: int
        :param color: boja labele.
        :type color: str
        """
        for lab in self._labels:
            if label.name == lab.name and author_id == lab.author_id:
                lab.color = label.color
                return True
        return False

        
    @property
    def labels(self):
        """
        Property za dobavljanje liste labela.
        """
        return self._labels 

    def load_labels(self):
        """
        Očitava sve podatke iz sqlite baze. 
        Pravi instance labela koje se dodaju u listu labela.
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_zahteviSoftvera\\baza\\zahteviSoftvera.db')
        c = conn.cursor()
        for name, color, author_id in c.execute('SELECT name, color, author_id FROM labels'):
            lab = Label(name, color, author_id)
            self.create(lab)   
        conn.close()

    def add_label(self, label):
        """
        Dodaje labelu u sqlite baze.
        :param label: instanca label koju kreiramo.
        :type label: label
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_zahteviSoftvera\\baza\\zahteviSoftvera.db')
        c = conn.cursor()
        c.execute('INSERT INTO labels (name, color, author_id) VALUES (?,?,?)', label.get_db_data())
        conn.commit()
        conn.close()
    
    def delete_label(self, label, user_id):
        """
        Briše labelu iz sqlite baze.
        :param label: instanca label koju brisemo.
        :type label: label
        :param user_id: autor labele.
        :type user_id: int
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_zahteviSoftvera\\baza\\zahteviSoftvera.db')
        c = conn.cursor()

        # posto sqlite baza nece da obrise strani kljuc cak i kad je ON DELETE = SET NULL
        label_id = 0
        for lid, in c.execute('SELECT label_id FROM labels WHERE name = ? AND author_id = ?', (label.name, user_id)):
            label_id = int(lid)

        c.execute('DELETE FROM labels WHERE name = ? and author_id = ?', (label.name, user_id)) 
        conn.commit()
        c.execute('UPDATE tasks SET label_id = NULL WHERE label_id = ?', (label_id,))  
        conn.commit()
        conn.close()

    def edit_label(self, label, user_id):
        """
        Menja boju labela u sqlite bazi.  
        :param label: instanca label koju menjamo.
        :type label: label
        :param color: boja labele.
        :type color: str
        :param user_id: autor labele.
        :type user_id: int
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_zahteviSoftvera\\baza\\zahteviSoftvera.db')
        c = conn.cursor()
        c.execute('UPDATE labels SET color = ? WHERE name = ? and author_id = ?', (label.color, label.name, user_id)) 
        conn.commit()
        conn.close()

    