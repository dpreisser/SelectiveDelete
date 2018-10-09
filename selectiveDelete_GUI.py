
import sys

import PySide
from PySide import QtGui
from PySide import QtCore

def setWidthTextFields( theTextField, numCharsWidth, widthType ):

    sizeH = theTextField.sizeHint()
    sizeM = theTextField.minimumSizeHint()

    # font = theTextField.led_appName.font()
    # fm = QFontMetrics( font )
    fm = theTextField.fontMetrics()

    str = ''.join( ['X' for i in range(numCharsWidth)] )

    width = fm.width( str )

    if 0 == widthType:
      theTextField.setMinimumWidth( width )
    elif 1 == widthType:
      theTextField.setMaximumWidth( width )
    elif 2 == widthType:
      theTextField.setFixedWidth( width )

    return theTextField


class selectiveDelete_GUI( QtGui.QDialog ):
    
    def __init__(self, title, parent=None):
        
        super(selectiveDelete_GUI, self).__init__(parent)

        # Member vars
        self.gateway = None
        self.m_dicSettings = {}
        self.m_strCurrentSP = ""
        self.m_dicListData = {}
        self.m_blnCancel = False

        # Window title.
        self.setWindowTitle( title )
        
        # Force size
        self.setMinimumWidth( 900 )
        self.setMinimumHeight( 950 )

        # Groupbox containing seelection settings.
        l_grpSelection = QtGui.QGroupBox( "Selection" )
        l_grdSelection = QtGui.QGridLayout()
        l_intCurrRow = 0

        # Test Cases with linked requirements
        self.m_rdbSelectionTestCases = QtGui.QRadioButton( "Test Cases" )
        self.m_rdbSelectionRequirements = QtGui.QRadioButton( "Requirements" )

        l_grdSelection.addWidget( self.m_rdbSelectionTestCases, l_intCurrRow, 0 )
        l_grdSelection.addWidget( self.m_rdbSelectionRequirements, l_intCurrRow, 1 )
        l_intCurrRow += 1

        l_grpSelection.setLayout( l_grdSelection )

        l_grpSelectionFilter = QtGui.QGroupBox( "Selection Filter" )
        l_grdSelectionFilter = QtGui.QGridLayout()
        l_intCurrRow = 0

        self.m_rdbSelectionAll = QtGui.QRadioButton( "All" )
        self.m_rdbSelectionLinked = QtGui.QRadioButton( "Linked to Requirements/Test Cases" )
        l_intCurrRow += 1

        l_grdSelectionFilter.addWidget( self.m_rdbSelectionAll, l_intCurrRow, 0 )
        l_grdSelectionFilter.addWidget( self.m_rdbSelectionLinked, l_intCurrRow, 1 )
        l_intCurrRow += 1

        l_grpSelectionFilter.setLayout( l_grdSelectionFilter )

        # Groupbox containing selection treeview for folders and collections
        l_grpFolderSelection = QtGui.QGroupBox("Folder Selection")
        l_grdFolderSelection = QtGui.QGridLayout()

        l_intCurrRow = 0
        self.m_tvwFolder = QtGui.QTreeView()
        self.m_tvwFolder.setMinimumHeight( 200 )
        self.m_tvwFolder.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.m_tvwFolder.setUniformRowHeights( True )

        self.m_modFolder = QtGui.QStandardItemModel()
        self.m_modFolder.setHorizontalHeaderLabels( [ "Name", "ID", "Type" ] )
        self.m_tvwFolder.setModel( self.m_modFolder )

        header = self.m_tvwFolder.header()

        header.setResizeMode( 0, QtGui.QHeaderView.Stretch )
        header.setResizeMode( 1, QtGui.QHeaderView.Stretch )
        header.setResizeMode( 2, QtGui.QHeaderView.Stretch )

        l_grdFolderSelection.addWidget(self.m_tvwFolder, l_intCurrRow, 0, 2, 2)

        l_grpFolderSelection.setLayout(l_grdFolderSelection)

        # Groupbox containing selection of the collection
        l_grpCollectionSelection = QtGui.QGroupBox("Collection Selection")
        l_grdCollectionSelection = QtGui.QGridLayout()

        l_intCurrRow = 0

        l_lblCollection = QtGui.QLabel( "Selected Collection" )

        l_lblName = QtGui.QLabel( "Name" )
        l_lblID = QtGui.QLabel( "ID" )
        l_lblType = QtGui.QLabel( "Type" )

        l_grdCollectionSelection.addWidget(l_lblName, l_intCurrRow, 1)
        l_grdCollectionSelection.addWidget(l_lblID, l_intCurrRow, 2)
        l_grdCollectionSelection.addWidget(l_lblType, l_intCurrRow, 3)

        l_intCurrRow += 1

        l_grdCollectionSelection.addWidget(l_lblCollection, l_intCurrRow, 0)

        self.m_ledName = QtGui.QLineEdit()
        self.m_ledID = QtGui.QLineEdit()
        self.m_ledType = QtGui.QLineEdit()

        self.m_ledName.setReadOnly( True )
        self.m_ledID.setReadOnly( True )
        self.m_ledType.setReadOnly( True )

        l_grdCollectionSelection.addWidget(self.m_ledName, l_intCurrRow, 1)
        l_grdCollectionSelection.addWidget(self.m_ledID, l_intCurrRow, 2)
        l_grdCollectionSelection.addWidget(self.m_ledType, l_intCurrRow, 3)

        l_grpCollectionSelection.setLayout(l_grdCollectionSelection)

        # Groupbox containing selection of the types
        l_grpTypeSelection = QtGui.QGroupBox("Type Selection")
        l_vbxTypeSelection = QtGui.QVBoxLayout()

        self.m_tblType = QtGui.QTableWidget( 0, 3 )
        self.m_tblType.setMinimumHeight( 100 )
        self.m_tblType.setHorizontalHeaderLabels( [ "Name", "ID", "Type" ] )
        self.m_tblType.setSelectionBehavior( QtGui.QAbstractItemView.SelectRows )

        header = self.m_tblType.horizontalHeader()

        header.setResizeMode( 0, QtGui.QHeaderView.Stretch )
        header.setResizeMode( 1, QtGui.QHeaderView.Stretch )
        header.setResizeMode( 2, QtGui.QHeaderView.Stretch )

        l_vbxTypeSelection.addWidget( self.m_tblType )

        l_grpTypeSelection.setLayout( l_vbxTypeSelection )

        # Groupbox containing field selection dropdowns.
        l_grpFieldSelection = QtGui.QGroupBox("Field Selection")
        l_grdFieldSelection = QtGui.QGridLayout()

        l_lblKey = QtGui.QLabel("Key:")
        self.m_cbxKey = QtGui.QComboBox()
        self.m_cbxKey = setWidthTextFields( self.m_cbxKey, 35, 0 )

        l_lblKeyType = QtGui.QLabel("Associated Type(s):")
        self.m_ledKeyType = QtGui.QLineEdit()
        self.m_ledKeyType.setReadOnly( True )

        l_grdFieldSelection.addWidget(l_lblKey, l_intCurrRow, 0)
        l_grdFieldSelection.addWidget(self.m_cbxKey, l_intCurrRow, 1)

        l_grdFieldSelection.addWidget(l_lblKeyType, l_intCurrRow, 2)
        l_grdFieldSelection.addWidget(self.m_ledKeyType, l_intCurrRow, 3)
        l_intCurrRow += 1

        l_lblTitle = QtGui.QLabel("Title:")
        self.m_cbxTitle = QtGui.QComboBox()
        self.m_cbxTitle = setWidthTextFields( self.m_cbxTitle, 35, 0 )

        l_lblTitleType = QtGui.QLabel("Associated Type(s):")
        self.m_ledTitleType = QtGui.QLineEdit()
        self.m_ledTitleType.setReadOnly( True )

        l_grdFieldSelection.addWidget(l_lblTitle, l_intCurrRow, 0)
        l_grdFieldSelection.addWidget(self.m_cbxTitle, l_intCurrRow, 1)

        l_grdFieldSelection.addWidget(l_lblTitleType, l_intCurrRow, 2)
        l_grdFieldSelection.addWidget(self.m_ledTitleType, l_intCurrRow, 3)
        l_intCurrRow += 1

        l_lblDescription = QtGui.QLabel("Description:")
        self.m_cbxDescription = QtGui.QComboBox()
        self.m_cbxDescription = setWidthTextFields( self.m_cbxDescription, 35, 0 )

        l_lblDescriptionType = QtGui.QLabel("Associated Type(s):")
        self.m_ledDescriptionType = QtGui.QLineEdit()
        self.m_ledDescriptionType.setReadOnly( True )

        l_grdFieldSelection.addWidget(l_lblDescription, l_intCurrRow, 0)
        l_grdFieldSelection.addWidget(self.m_cbxDescription, l_intCurrRow, 1)

        l_grdFieldSelection.addWidget(l_lblDescriptionType, l_intCurrRow, 2)
        l_grdFieldSelection.addWidget(self.m_ledDescriptionType, l_intCurrRow, 3)
        l_intCurrRow += 1

        l_grpFieldSelection.setLayout(l_grdFieldSelection)

        # Groupbox containing trace output.
        l_grpOutput = QtGui.QGroupBox("Output")
        l_vbxOutput = QtGui.QVBoxLayout()
        self.m_tedOutput = QtGui.QTextEdit()
        self.m_tedOutput.setMinimumHeight( 200 )
        self.m_tedOutput.readOnly = True
        l_vbxOutput.addWidget( self.m_tedOutput )
        l_grpOutput.setLayout( l_vbxOutput )

        # Import Buttons
        l_hbxImportButtons = QtGui.QHBoxLayout()
        l_hbxImportButtons.setDirection(QtGui.QBoxLayout.RightToLeft)

        l_butClose = QtGui.QPushButton("Close")
        l_butClose.clicked.connect(self.close_clicked)
        l_hbxImportButtons.addWidget(l_butClose)

        l_butImport = QtGui.QPushButton("Import")
        l_butImport.clicked.connect(self.import_clicked)
        l_hbxImportButtons.addWidget(l_butImport)

        l_hbxImportButtons.addStretch(50)

        l_vbxMain = QtGui.QVBoxLayout()
        l_vbxMain.addWidget( l_grpSelection )
        l_vbxMain.addWidget( l_grpSelectionFilter )
        l_vbxMain.addWidget( l_grpFolderSelection )
        l_vbxMain.addWidget( l_grpCollectionSelection )
        l_vbxMain.addWidget( l_grpTypeSelection )
        l_vbxMain.addWidget( l_grpFieldSelection )
        l_vbxMain.addWidget( l_grpOutput )
        # Align button layout to bottom to allow resizing.
        l_vbxMain.addLayout( l_hbxImportButtons, alignment=QtCore.Qt.AlignBottom )

        l_mainWidget = QtGui.QWidget()
        l_mainWidget.setLayout( l_vbxMain )

        l_scroll = QtGui.QScrollArea()
        l_scroll.setVerticalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOn )
        l_scroll.setHorizontalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOff )
        l_scroll.setWidgetResizable( True )
        l_scroll.setWidget( l_mainWidget )

        l_mainLayout = QtGui.QVBoxLayout()
        l_mainLayout.addWidget( l_scroll )

        self.setLayout( l_mainLayout )


    def set_handler( self, GUI_Handler ):
        self.GUI_Handler = GUI_Handler
        self.Gateway = GUI_Handler.Gateway
        self.settings = GUI_Handler.settings
        # self._get_settings()
        self._activateGUI()
        self._append_output_log()


    def _get_settings( self ):

        self.rm_project_id = self.settings.get( "rm_project_id", "" )

        if self.rm_project_id in self.handler.serviceProviderInfo.keys():
            rm_project_title = self.handler.serviceProviderInfo[self.rm_project_id][0]
        else:
            rm_project_title = ""

        selectedIdx = build_combobox_fromList( self.m_cbxProject,
                                               self.handler.serviceProviderInfoAsList,
                                               where=0,
                                               selectedValue=rm_project_title )

        # This triggers the tree view to be populated with the root folder of the project.
        # This is regardless if the project could be found or not.
        self._project_selected()

        rm_collection_type = self.settings.get( "rm_collection_type", "" )
        rm_collection_title = self.settings.get( "rm_collection_title", "" )
        rm_collection_URL = self.settings.get( "rm_collection_URL", "" )
        rm_collection_id = self.settings.get( "rm_collection_id", "" )

        rm_type_ids = self.settings.get( "rm_type_ids", "" )
        if rm_type_ids:
            self.selectedInstanceShapeIDs = rm_type_ids.split( "," )
        else:
            self.selectedInstanceShapeIDs = []

        self.rm_attr_key = self.settings.get( "rm_attr_key", "" )
        self.rm_attr_title = self.settings.get( "rm_attr_title", "" )
        self.rm_attr_description = self.settings.get( "rm_attr_description", "" )

        if selectedIdx < 0:
            return

        if (not rm_collection_type) or (not rm_collection_title) or (not rm_collection_URL) or (not rm_collection_id):
            return

        self.selectedCollectionInfo = CollectionInfo( rm_collection_type,
                                                      rm_collection_title,
                                                      rm_collection_URL,
                                                      rm_collection_id )

        # This will provide the instance shape information of the collection.
        # And will set the content of the table associated with the types.
        self._populateCollections()

        if len( self.selectedInstanceShapeIDs ) > 0:
            self._populateAttributeFields( connected=False )


    def _set_settings(self):

        # Project
        self.settings["rm_project_id"] = self.rm_project_id

        # Folder

        # Collection
        self.settings["rm_collection_type"] = self.selectedCollectionInfo.colType
        self.settings["rm_collection_title"] = self.selectedCollectionInfo.title
        self.settings["rm_collection_URL"] = self.selectedCollectionInfo.URL
        self.settings["rm_collection_id"] = self.selectedCollectionInfo.ID

        # Type
        rm_type_ids = ",".join( self.selectedInstanceShapeIDs )
        self.settings["rm_type_ids"] = rm_type_ids

        # Attributes
        self.settings["rm_attr_key"] = self.rm_attr_key
        self.settings["rm_attr_title"] = self.rm_attr_title
        self.settings["rm_attr_description"] = self.rm_attr_description

        
    def _activateGUI( self ):

        self.m_tvwFolder.clicked.connect( self._folder_or_collection_selected )

        self.m_tblType.itemSelectionChanged.connect( self._on_typeSelectionChanged )

        self.m_cbxKey.currentIndexChanged.connect( self._populateAssociatedTypes )
        self.m_cbxTitle.currentIndexChanged.connect( self._populateAssociatedTypes )
        self.m_cbxDescription.currentIndexChanged.connect( self._populateAssociatedTypes )


    def _resetData_project( self ):

        self.rm_project_id = ""

        self._resetData_folders( resetHandlerData=True )


    def _resetData_folders( self, resetHandlerData=False ):

        self.selectedFolderInfo = FolderInfo( "", "", "" )

        if resetHandlerData:
            self.handler.folderInfo = {}

        self._resetData_collections( resetHandlerData )


    def _resetData_collections( self, resetHandlerData=False ):

        self.selectedCollectionInfo = CollectionInfo( "", "", "", "" )
        
        if resetHandlerData:
            self.handler.collectionInfo = {}

        self._resetData_types( resetHandlerData )

    
    def _resetData_types( self, resetHandlerData=False ):

        self.selectedInstanceShapeIDs = []
        self.handler.selectedInstanceShapeIDs = []

        if resetHandlerData:
            self.handler.instanceShapeInfo = {}

        self._resetData_attributes( resetHandlerData )


    def _resetData_attributes( self, resetHandlerData=False ):

        # self.rm_attr_key = ""
        # self.rm_attr_title = ""
        # self.rm_attr_description = ""

        if resetHandlerData:
            self.handler.titleToAttributes = {}


    def _resetGUI_folders( self ):

        self.foldersInTreeView = []
        self.collectionsInFolders = []
        self.collectionsInCollections = []

        self.m_modFolder.setRowCount( 0 )
        self.m_tvwFolder.setModel( self.m_modFolder )

        self._resetGUI_collections()


    def _resetGUI_collections( self ):
        self.m_ledName.setText( "" )
        self.m_ledID.setText( "" )
        self.m_ledType.setText( "" )

        self._resetGUI_types()

            
    def _resetGUI_types( self ):

        self.m_tblType.setRowCount( 0 )

        self._resetGUI_attributes()


    def _resetGUI_attributes( self ):

        build_combobox_fromList( self.m_cbxKey, [] )
        build_combobox_fromList( self.m_cbxTitle, [] )
        build_combobox_fromList( self.m_cbxDescription, [] )

        self.m_ledKeyType.setText( "" )
        self.m_ledTitleType.setText( "" )
        self.m_ledDescriptionType.setText( "" )


    def _append_output_log( self ):
        trace_log = self.Gateway.read_trace_log()
        self.m_tedOutput.append( trace_log[1] )
        self.m_tedOutput.verticalScrollBar().setValue( self.m_tedOutput.verticalScrollBar().maximum() )


    def _project_selected( self ):

        self._resetData_project()
        self._resetGUI_folders()

        currentIdx = self.m_cbxProject.currentIndex()

        # No projects or error in initialization means:
        # -1 == currentIdx

        if currentIdx > -1:

            serviceProviderInfo = self.handler.serviceProviderInfoAsList[currentIdx]
            rm_project_title = serviceProviderInfo[0]
            self.rm_project_id = serviceProviderInfo[2]

            self.handler.getServiceInfo( self.rm_project_id )

            # This should remain local: firstFolderInfo.
            # The real projectID can not be used as the projectID and the folderID of the root folder
            # might be the same depending on the version of the CLM.
            # So the hash (string) "projectID" is used instead.
            firstFolderInfo = FolderInfo( rm_project_title, None, "projectID" )
            folderIDs = self.handler.getFolderInfo( firstFolderInfo )

            self._populate_treeview( None, folderIDs, "Folder" )

        self._append_output_log()


    def _populate_treeview( self, i_modItem, i_IDs, i_dataType, isCollectionInFolders=True ):

        l_modItem = None

        if i_modItem is None:
            # Select the treeview root model.
            l_modItem = self.m_modFolder
        else:
            l_modItem = i_modItem

        isCollection = False

        if "Folder" == i_dataType:
            dataContainer = self.handler.folderInfo
            treeViewContainer = self.foldersInTreeView
            l_dataType = i_dataType
        elif "Collection" == i_dataType:            
            isCollection = True
            dataContainer = self.handler.collectionInfo
            if isCollectionInFolders:
                treeViewContainer = self.collectionsInFolders
            else:
                treeViewContainer = self.collectionsInCollections
        else:
            return
        
        for ID in i_IDs:

            if ID in treeViewContainer:
                continue
            else:
                treeViewContainer.append( ID )

            info = dataContainer[ID]
            title = info.title

            if isCollection:
                l_dataType = info.colType

            msg = "_populate_treeview: title: %s\n" % title
            msg += "_populate_treeview: ID: %s\n" % ID
            msg += "_populate_treeview: dataType: %s" % l_dataType
            self.gateway._trace( msg, 6 )

            itemTitle = QtGui.QStandardItem( title )
            itemID = QtGui.QStandardItem( ID )
            itemType = QtGui.QStandardItem( l_dataType )
            
            l_modItem.appendRow( [ itemTitle, itemID, itemType ] )


    def _folder_or_collection_selected( self, i_idxSelectedItem ):

        self._resetData_collections( resetHandlerData=False )
        self._resetGUI_collections()

        # Get the model of the parent item.
        l_modParent = i_idxSelectedItem.model()

        indexes = self.m_tvwFolder.selectedIndexes()
        for index in indexes:
            # We only care about column 0 to append children.
            if 0 == index.column():
                l_modItem = l_modParent.itemFromIndex(index)
                break;

        # Get the index of the name item.
        l_idxSelectedName = l_modParent.index(
            i_idxSelectedItem.row(),
            0,
            i_idxSelectedItem.parent() )
        # Get the value of the name item from the index.
        l_selectedName = l_idxSelectedName.data()

        # Get the index of the ID item.
        l_idxSelectedID = l_modParent.index(
            i_idxSelectedItem.row(),
            1,
            i_idxSelectedItem.parent() )
        # Get the value of the ID item from the index.
        l_selectedID = l_idxSelectedID.data()

        # Get the index of the data type item.
        l_idxSelectedDataType = l_modParent.index(
            i_idxSelectedItem.row(),
            2,
            i_idxSelectedItem.parent() )
        # Get the value of the data type item from the index.
        l_selectedDataType = l_idxSelectedDataType.data()

        if "Folder" == l_selectedDataType:

            self.selectedFolderInfo = self.handler.folderInfo[l_selectedID]
            folderIDs, collectionIDs = self._populateFoldersAndCollections()

            self._populate_treeview( l_modItem, folderIDs, "Folder" )
            self._populate_treeview( l_modItem, collectionIDs, "Collection" )

        else:

            self.selectedCollectionInfo = self.handler.collectionInfo[l_selectedID]
            collectionIDs = self._populateCollections()

            if collectionIDs is not None:
                self._populate_treeview( l_modItem, collectionIDs, "Collection", isCollectionInFolders=False )

        self._append_output_log()

            
    def _populateFoldersAndCollections( self ):
        # This function can also be used for initial population
        # when no GUI action has taken place yet!

        folderIDs = self.handler.getFolderInfo( self.selectedFolderInfo )
        collectionIDs = self.handler.getCollectionInfoFolders( self.selectedFolderInfo )

        return folderIDs, collectionIDs


    def _populateCollections( self ):

        self.m_ledName.setText( self.selectedCollectionInfo.title )
        self.m_ledID.setText( self.selectedCollectionInfo.ID )
        self.m_ledType.setText( self.selectedCollectionInfo.colType )

        collectionIDs, instanceShapeIDsToAdd = self.handler.getInstanceShapeInfo( self.selectedCollectionInfo )

        self._populateTypes( instanceShapeIDsToAdd )

        return collectionIDs

        
    def _populateTypes( self, instanceShapeIDsToAdd ):

        # This function can also be used for initial population
        # when no GUI action has taken place yet!

        numTypes = len( instanceShapeIDsToAdd )

        dataContainer = self.handler.instanceShapeInfo

        for idxType in range( numTypes ):

            self.m_tblType.insertRow( idxType )

            ID = instanceShapeIDsToAdd[idxType]
            info = dataContainer[ID]
            
            itemName = QtGui.QTableWidgetItem( info.title )
            itemName.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled )

            itemID = QtGui.QTableWidgetItem( info.ID )
            itemID.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled )

            itemType = QtGui.QTableWidgetItem( "Type" )
            itemType.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled )

            self.m_tblType.setItem( idxType, 0, itemName )
            self.m_tblType.setItem( idxType, 1, itemID )
            self.m_tblType.setItem( idxType, 2, itemType )


    def _on_typeSelectionChanged( self ):

        # This function is only to map user selection to self.selectedInstanceShapeIDs!

        selectedIdc = self.m_tblType.selectedIndexes()

        entireRows = []
    
        for qmIdx in selectedIdc:
            rowIdx = qmIdx.row()
            if not rowIdx in entireRows:
                entireRows.append( rowIdx )

        self.selectedInstanceShapeIDs = []

        for rowIdx in entireRows:
            instanceShapeID = self.m_tblType.item( rowIdx, 1 ).text()
            self.selectedInstanceShapeIDs.append( instanceShapeID  )

        self._populateAttributeFields()

        self._append_output_log()

            
    def _populateAttributeFields( self, connected=True ):

        # This function can also be used for initial population
        # when no GUI action has taken place yet!

        msg = "_populateAttributeFields: selectedInstanceShapeIDs: %s" % self.selectedInstanceShapeIDs
        self.gateway._trace( msg, 6 )

        attributeTitlesToAdd = self.handler.getAttributeInfo( self.selectedInstanceShapeIDs )

        if connected:
            self.m_cbxKey.currentIndexChanged.disconnect() 
            self.m_cbxTitle.currentIndexChanged.disconnect() 
            self.m_cbxDescription.currentIndexChanged.disconnect() 

        build_combobox_fromList( self.m_cbxKey,
                                 attributeTitlesToAdd,
                                 i_sorted=True,
                                 selectedValue=self.rm_attr_key )
        build_combobox_fromList( self.m_cbxTitle,
                                 attributeTitlesToAdd,
                                 i_sorted=True,
                                 selectedValue=self.rm_attr_title )
        build_combobox_fromList( self.m_cbxDescription,
                                 attributeTitlesToAdd,
                                 i_sorted=True,
                                 selectedValue=self.rm_attr_description )

        if connected:
            self.m_cbxKey.currentIndexChanged.connect( self._populateAssociatedTypes )
            self.m_cbxTitle.currentIndexChanged.connect( self._populateAssociatedTypes )
            self.m_cbxDescription.currentIndexChanged.connect( self._populateAssociatedTypes )

        self._populateAssociatedTypes()

        
    def _populateAssociatedTypes( self ):

        # Associated types to key attribute
        rm_attr_key = self.m_cbxKey.currentText()
        if rm_attr_key in self.handler.titleToAttributes.keys():
            associatedTypes = self.handler.titleToAttributes[rm_attr_key][2]
            assoctiatedTypesStr = ",".join( associatedTypes )
            self.rm_attr_key = rm_attr_key
        else:
            assoctiatedTypesStr = ""
        self.m_ledKeyType.setText( assoctiatedTypesStr ) 

        # Associated types to title attribute
        rm_attr_title = self.m_cbxTitle.currentText()
        if rm_attr_title in self.handler.titleToAttributes.keys():
            associatedTypes = self.handler.titleToAttributes[rm_attr_title][2]
            assoctiatedTypesStr = ",".join( associatedTypes )
            self.rm_attr_title = rm_attr_title
        else:
            assoctiatedTypesStr = ""
        self.m_ledTitleType.setText( assoctiatedTypesStr ) 

        # Associated types to description attribute
        rm_attr_description  = self.m_cbxDescription.currentText()
        if rm_attr_description in self.handler.titleToAttributes.keys():
            associatedTypes = self.handler.titleToAttributes[rm_attr_description][2]
            assoctiatedTypesStr = ",".join( associatedTypes )
            self.rm_attr_description = rm_attr_description
        else:
            assoctiatedTypesStr = ""
        self.m_ledDescriptionType.setText( assoctiatedTypesStr ) 


    def close_clicked(self):
        self.m_blnCancel = True
        self._set_settings()
        self.done(0)


    def import_clicked(self):
        self._set_settings()
        self.done(1)


def getKey( item ):

    global g_where

    if not None == g_where:
        return item[g_where]
    else:
        return item


def build_combobox( i_cbxCombo, i_dicLookup, i_strSelectedValue=None ):

    i_cbxCombo.clear()

    l_intSetIdx = -1
    l_intCurrIdx = -1

    for l_keyCurr, l_valCurr in i_dicLookup.items():

        l_intCurrIdx = l_intCurrIdx + 1

        i_cbxCombo.addItem( l_keyCurr )

        if i_strSelectedValue:
            if i_strSelectedValue == l_valCurr:
                l_intSetIdx = l_intCurrIdx 
            
    if l_intSetIdx > -1:
        i_cbxCombo.setCurrentIndex( l_intSetIdx )


def build_combobox_fromList( i_cbxCombo, i_listLookup, i_sorted=False, where=None, selectedValue=None ):

    global g_where
    g_where = where

    i_cbxCombo.clear()

    if i_sorted:
        listLookup = sorted( i_listLookup, key=getKey )
    else:
        listLookup = i_listLookup

    l_intSetIdx = -1
    l_intCurrIdx = -1

    for l_item in listLookup:

        l_intCurrIdx = l_intCurrIdx + 1

        if not None == where:
            l_valCurr = l_item[where]
        else:
            l_valCurr = l_item

        i_cbxCombo.addItem( l_valCurr )

        if not None == selectedValue:
            if selectedValue == l_valCurr:
                l_intSetIdx = l_intCurrIdx 
            
    if l_intSetIdx > -1:
        i_cbxCombo.setCurrentIndex( l_intSetIdx )

    return l_intSetIdx
