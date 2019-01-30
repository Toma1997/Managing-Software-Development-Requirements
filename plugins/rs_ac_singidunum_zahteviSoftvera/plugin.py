from plugin_framework.plugin import Plugin
from .widgets.tasks_widget import TasksWidget

class Main(Plugin):
    """
    Klasa koja predstavlja konkretni plugin. Nasledjujemo "apstraktnu" klasu Plugin.
    Ova klasa predstavlja plugin za aplikaciju zahteva o razvoju softvera.
    """
    def __init__(self, spec):
        """
        Inicijalizator Razvoj Softvera plugina.

        :param spec: specifikacija metapodataka o pluginu.
        :type spec: dict
        """
        super().__init__(spec)

    def get_widget(self, parent=None):
        """
        Ova metoda vraca konkretni widget koji ce biti smesten u centralni deo aplikacije i njenog 
        glavnog prozora. Može da vrati toolbar, kao i meni, koji će biti smešten u samu aplikaciju.
        
        :param parent: bi trebao da bude widget u koji će se smestiti ovaj koji naš plugin omogućava.
        :returns: QWidget, QToolbar, QMenu
        """
        return TasksWidget(parent), None, None