
import sys

import PySide
from PySide import QtGui
from PySide import QtCore

from base_gateway import BaseGateway

from selectiveDelete_GUI_Handler import selectiveDelete_GUI_Handler
from selectiveDelete_GUI import selectiveDelete_GUI

# Script settings
scriptRootVersion = "1.0"         # Please don't change the script root version
scriptVersion = "1.0"             # Use this variable for your versioning.
currentTraceLevel = 1             # 0: No Traces, 1: Normal, ..., 6 Exhaustive


class selectiveDelete_Gateway( BaseGateway ):

    def __init__( self, **kwargs ):

        super(selectiveDelete_Gateway, self).__init__()

        self.trace_buffer = ''
        self.trace_level = currentTraceLevel
        self._trace( "__init__", 6 )

        # GUI_Handler
        self.GUI_Handler = selectiveDelete_GUI_Handler( **kwargs )
        self.GUI_Handler.Gateway = self

        self.db_mode = self.GUI_Handler.db_mode
        self.clicast_mode = self.GUI_Handler.clicast_mode
        self.repository_path = self.GUI_Handler.repository_path

        
    def _trace(self, msg, lvl):
        if lvl <= self.trace_level:
            # Record trace data to be shown to the user.
            self.trace_buffer += msg
            self.trace_buffer += '\n'


    def _set_error_trace( self, msg ):
        self._trace( msg, 1 )
        self._set_error( msg )


    def read_trace_log( self ):
        # Return the trace data.
        return_trace = self.trace_buffer
        self.trace_buffer = ""
        return ( True, return_trace )


    def launch_dialog( self ):

        self.dbFile = self.repository_path + "/requirements.db"

        self.GUI = selectiveDelete_GUI( self.dbFile )
        self.GUI.set_handler( self.GUI_Handler )
        
        self.GUI_Handler.GUI = self.GUI

        # Display the selective delete dialog.
        self.GUI.exec_()


def create_instance( **kwargs ):

    # print( "create_instance" )

    return selectiveDelete_Gateway( **kwargs )


def run( repository_path ):

    app_q = QtGui.QApplication( sys.argv )

    kwargs = {}

    # kwargs["db_mode"] = "xml"
    kwargs["db_mode"] = "sql"
    # kwargs["clicast_mode"] = "1"
    kwargs["repository_path"] = repository_path

    selectiveDelete_Gateway = create_instance( **kwargs )

    selectiveDelete_Gateway.launch_dialog()


if __name__ == "__main__":

    numParameters = len( sys.argv ) - 1

    if numParameters != 1:
        print( "Exactly one parameter needs to be provided!" )
        print( "The parameter must indicate the path (directory) to the db file which needs to be altered." )
        sys.exit()

    repository_path = sys.argv[1]

    run( repository_path )
