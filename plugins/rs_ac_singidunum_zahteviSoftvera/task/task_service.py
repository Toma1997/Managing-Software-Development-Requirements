import sqlite3
from ..task.task import Task

class TaskService:
    """
    Klasa koja manipulise nad zadacima (tasks) u prosirivom okviru. Sluzi kao service sloj.
    """
    def __init__(self):
        """
        Inicijalizator servisne klase za zadatke.
        """
        self._tasks = list()
        self._personal_tasks = list()

    def create(self, task):
        """
        Dodaje zadatak.
        
        :param task: instanca zadatka koju
        :type task: Task
        :returns: bool - podatak o uspesnosti dodavanja.
        """
        for tsk in self._tasks:
            if task.name == tsk.name and task.description == tsk.description:
                return False
        
        self._tasks.append(task)
        return True

    def createPersonal(self, task):
        """
        Dodaje zadatak trenutnom korisniku.
        
        :param task: instanca zadatka.
        :type task: Task
        :returns: bool - podatak o uspesnosti dodavanja.
        """
        for tsk in self._personal_tasks:
            if task.name == tsk.name and task.description == tsk.description:
                return False

        self._personal_tasks.append(task)
        return True

    def delete(self, task, user_id):
        """
        Briše zadatak.

        :param task: instanca zadatka.
        :type task: task
        :returns: bool - podatak o uspesnosti uklanjanja.
        """
        for tsk in self._tasks:
            if task.name == tsk.name and task.description == tsk.description:
                if task.status != "prihvacen" and user_id == task.author_id:
                    self._tasks.remove(tsk)
                    return True
        return False

    def edit(self, task, status, acceptedAt = None, userAccepted_id = None):
        """
        Dodaje zadatak u licne ili ga uklanja.
        
        :param task: instanca zadatka.
        :type task: Task
        :param status: status zadatka koji menjamo.
        :type status: str
        :param acceptedAt: datum i vreme prihvatanja zadatka ako je prihvacen.
        :type acceptedAt: str
        :param userAccepted_id: id korisnika koji je prihvatio zadatak.
        :type userAccepted_id: int
        :returns: bool - podatak o uspesnosti dodavanja.
        """
        
        if status == "prihvacen" and task.status == "neprihvacen":
            for tsk in self._tasks:
                if tsk.name == task.name and tsk.description == task.description:
                    tsk.status = status
                    tsk.acceptedAt = acceptedAt
                    tsk.userAccepted_id = userAccepted_id
                    self._personal_tasks.append(tsk)
                    return True

        elif status == "razresen":
            for tsk in self._tasks:
                if tsk.name == task.name and tsk.description == task.description:
                    tsk.status = status
                    break

            for tsk in self._personal_tasks:
                if tsk.name == task.name and tsk.description == task.description:
                    self._personal_tasks.remove(tsk)
                    return True
                    
        return False
        
    @property
    def tasks(self):
        return self._tasks

    @property
    def personal_tasks(self):
        return self._personal_tasks

    def clearList(self):
        """
        Pomocna metoda za praznjenje liste zbog brisanja labele
        """
        self._tasks = list()
             
    def load_tasks(self):
        """
        Očitava sve podatke iz sqlite baze. 
        Pravi instance zadataka koje se dodaju u listu zadataka.
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_zahteviSoftvera\\baza\\zahteviSoftvera.db')
        c = conn.cursor()
        for task_id, name, description, label_id, author_id, createdAt, acceptedAt, userAccepted_id, status in c.execute('SELECT * FROM tasks'):
            obj = Task(name, description, label_id, author_id, createdAt, acceptedAt, userAccepted_id, status)
            self.create(obj)  
        conn.close()
             
    def load_personal_tasks(self, user_id):
        """
        Očitava sve podatke iz sqlite baze. 
        Pravi instance licnih zadataka koje dodaje u listu licnih zadataka.
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_zahteviSoftvera\\baza\\zahteviSoftvera.db')
        c = conn.cursor()
        for task_id, name, description, label_id, author_id, createdAt, acceptedAt, userAccepted_id, status in c.execute('SELECT * FROM tasks WHERE user_id_accepted = ? AND status = "prihvacen"', (user_id,)):
            obj = Task(name, description, label_id, author_id, createdAt, acceptedAt, userAccepted_id, status)
            self.createPersonal(obj)  
        conn.close()

    def add_task(self, task):
        """
        Dodaje zadatak u sqlite bazu. 
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_zahteviSoftvera\\baza\\zahteviSoftvera.db')
        c = conn.cursor()
        c.execute('INSERT INTO tasks (name, description, label_id, user_id_author, created_at, accepted_at, user_id_accepted, status) VALUES (?,?,?,?,?,?,?,?)', task.get_db_data()) 
        conn.commit()
        conn.close()

    def delete_task(self, task):
        """
        Briše zadatak iz sqlite baze.
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_zahteviSoftvera\\baza\\zahteviSoftvera.db')
        c = conn.cursor()
        c.execute('DELETE FROM tasks WHERE name = ? AND description = ? AND created_at = ?', (task.name, task.description, task.createdAt))  
        conn.commit()
        conn.close()
        
    def edit_task(self, task, status, acceptedAt = None, userAccepted_id = None):
        """
        Menja status zadatka, i ako je status = prihvacen dodaje vreme prihvatanja, ili se razresava.  
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_zahteviSoftvera\\baza\\zahteviSoftvera.db')
        c = conn.cursor()
        if acceptedAt != None and userAccepted_id != None:
            c.execute('UPDATE tasks SET accepted_at = ?, user_id_accepted = ? WHERE name = ? AND description = ? AND created_at = ?', (acceptedAt, userAccepted_id, task.name, task.description, task.createdAt))
        
        c.execute('UPDATE tasks SET status = ? WHERE name = ? AND description = ? AND created_at = ?', (status, task.name, task.description, task.createdAt)) 
        conn.commit()
        conn.close()

    # DORADITI METODU
    def task_details(self, task):
        """
        Očitava detaljno sve podatke iz svih tabela sqlite baze. 
        Pravi listu sa detaljima i svim podacima za jedan zadatak.
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_zahteviSoftvera\\baza\\zahteviSoftvera.db')
        c = conn.cursor()

        for task_id, name, description, label_id, author_id, createdAt, acceptedAt, userAccepted_id, status in c.execute("SELECT * FROM tasks WHERE task_id = 1"):
            listaDetalja = [str(task_id), name, description, str(label_id), str(author_id), createdAt, acceptedAt, str(userAccepted_id), status]
        conn.close()

        return listaDetalja