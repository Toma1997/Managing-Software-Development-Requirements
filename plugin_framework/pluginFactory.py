from plugin_service import PluginService

class PluginFactory:

    def __init__(self, plugins : dict):
        self.plugins = plugins

    def createPlugin(self, symbolic_name):
        
        modul_spec = self.plugins.get(symbolic_name, None)
        plugin = modul_spec[0].Main(modul_spec[1])
        
        return plugin