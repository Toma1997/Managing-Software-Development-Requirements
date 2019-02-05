class Label:
    """
    Ova klasa predstavlja osnovu za svaku konkretnu labelu.
    """
    def __init__(self, name, color, author_id):
        """
        Inicijalizator.

        :param name: ime labele
        :type name: str
        :param color: boja labele
        :type color: str
        :param author_id: strani kljuc autora labele
        :type author_id: int
        """
        self._name = name
        self._color = color
        self._author_id = author_id
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, value):
        self._author_id = value

    def get_db_data(self): 
        """
        Metoda koja daje vrednosti za dobavljanje podataka iz baze.
        """
        return (self.name, self.color, self.author_id)