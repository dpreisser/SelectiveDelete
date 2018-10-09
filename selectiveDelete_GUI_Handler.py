
import sys

class selectiveDelete_GUI_Handler:

    def __init__( self, **kwargs ):

        self.settings = kwargs

        self.db_mode = self.settings["db_mode"]
        if "clicast_mode" in self.settings.keys():
            self.clicast_mode = True
        else:
            self.clicast_mode = False

        self.repository_path = self.settings["repository_path"]
