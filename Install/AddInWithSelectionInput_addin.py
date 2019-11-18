import arcpy
import pythonaddins
import os
import itertools
import collections
import Tkinter as tkinter
import tkFileDialog

"""
Instances in this module.
It allows coordination between extension and buttons, but more important
you get an interactive Python window to inspect addin behaviour.
In ArcMap select Geoprocessing | Python to open Python window, then:
>>> import AddInWithSelectionInput_addin as ext
>>> ext.extension
<AddInWithSelectionInput_addin.ExtensionAttachments object at 0x1197BCB0>
>>> ext.button
<AddInWithSelectionInput_addin.ButtonClickMe object at 0x1197BDD0>
>>>
If you have used IDLE, you know what it means.
"""

button = None
extension = None

# ======================================================================
#
# Properties: featureClass = data source string, objectIds : list of int-s
MySelection = collections.namedtuple('MySelection', ['featureClass', 'objectIds'])

# ======================================================================
class Helpers:
    
    @staticmethod
    def AreAnyFeaturesSelected():
        mxd = arcpy.mapping.MapDocument('CURRENT')
        layers = arcpy.mapping.ListLayers(mxd)
        for layer in layers:
            selection = layer.getSelectionSet()
            if (selection is not None) and (len(selection) > 0):
                return True
        return False

    @staticmethod
    def GetSelectedFeatures():
        """Returns OIDs of selected features ordered by feature classes (list of MySelection tuples)"""

        mxd = arcpy.mapping.MapDocument('CURRENT')
        if mxd.activeDataFrame is None:
            return []
        try:
            layers = arcpy.mapping.ListLayers(mxd)
        except TypeError: # May happen during mapsChanged event => 'NoneType' object is not iterable
            return []

        def layerHasSelectedFeatures(layer):
            if not layer.isBroken and layer.isFeatureLayer:
                selection = layer.getSelectionSet()
                if selection is not None and len(selection) > 0:
                    return True
            return False

        # Get a list of layers that have at least one selected feature
        layersWithSelection = filter(lambda l: layerHasSelectedFeatures(l), layers)

        # Group layers by data source (for example, if we have layers
        # with query definitions, then underlying feature classes will be the same)
        grouped = itertools.groupby(layersWithSelection, key = lambda layer : layer.dataSource)

        # Now for each data source select object IDs of selected features
        result = []

        for key, group in grouped:
            objectIds = []
            for layer in group:
                objectIds.extend(layer.getSelectionSet())
            result.append(MySelection(featureClass = key, objectIds = objectIds))

        return result

    @staticmethod
    def CanEnableMe(needsEditMode):
        """Tells if button can be enabled.
        
        Args:
            needsEditMode (bool): True if button can be enable in edit mode, False - otherwise.

        Returns:
            bool: True if some features are selected in active view and edit mode matches needsEditMode parameter.

        """
        if extension is None:
            return False
        if extension.inEditMode <> needsEditMode:
            return False
        return Helpers.AreAnyFeaturesSelected()

# ======================================================================
class ButtonClickMe(object):
    """Implementation for button"""

    def __init__(self):
        button = self
        self.checked = False
        self.pathToFile = ''
        self.changeEnabled()

    def onClick(self):
        self.pathToFile = ButtonClickMe.PickFileToAttach()
        if os.path.isfile(self.pathToFile):
            self.doTheAction()

    def changeEnabled(self):
        self.enabled = Helpers.CanEnableMe(False)

    def doTheAction(self):
        selected = Helpers.GetSelectedFeatures()

        for sel in selected:
            print('Invoked action with selected feature class ', sel.featureClass, ' and file ', self.pathToFile)
            print('Object IDs:', sel.objectIds)

    @staticmethod
    def PickFileToAttach():
        root = tkinter.Tk()
        root.withdraw()
        options = {
            'parent': root,
            'title': "Select a file to attach",
            'multiple': False,
            'filetypes': [('All files', '*')]
        }
        pathFile = tkFileDialog.askopenfilename(**options)
        root.destroy()
        return pathFile

# ======================================================================
class ExtensionAttachments(object):
    """Implementation for extension"""
    def __init__(self):
        # For performance considerations, please remove all unused methods in this class.
        self.enabled = True
        self.inEditMode = False
        extension = self
    # Extension methods
    def startup(self):
        self.setButtonsState()
        pass
    def activeViewChanged(self):
        print('extension.activeViewChanged')
        self.setButtonsState()
        pass
    def mapsChanged(self):
        self.setButtonsState() # this will fail with exception when another MXD is opened
        print('extension.mapsChanged')
        pass
    def newDocument(self):
        self.setButtonsState()
        pass
    def openDocument(self):
        self.setButtonsState()
        pass
    def beforeCloseDocument(self):
        print('extension.beforeCloseDocument')
        pass
    def closeDocument(self):
        print('extension.closeDocument')
        pass
    def beforePageIndexExtentChange(self, old_id):
        print('extension.beforePageIndexExtentChange')
        pass
    def pageIndexExtentChanged(self, new_id):
        print('extension.pageIndexExtentChanged')
        pass
    def contentsChanged(self):
        print('extension.contentsChanged')
        pass
    def spatialReferenceChanged(self):
        print('extension.spatialReferenceChanged')
        pass
    def itemAdded(self, new_item):
        print('extension.itemAdded', new_item)
        pass
    def itemDeleted(self, deleted_item):
        print('extension.itemDeleted')
        pass
    def itemReordered(self, reordered_item, new_index):
        print('extension.itemReordered')
        pass
    def onEditorSelectionChanged(self):
        self.setButtonsState()
        pass
    def onCurrentLayerChanged(self):
        print('extension.onCurrentLayerChanged')
        pass
    def onCurrentTaskChanged(self):
        print('extension.onCurrentTaskChanged')
        pass
    def onStartEditing(self):
        #print('extension.onStartEditing')
        self.inEditMode = True
        self.setButtonsState()
        pass
    def onStopEditing(self, save_changes):
        #print('extension.onStopEditing')
        self.inEditMode = False
        self.setButtonsState()
        pass
    def onStartOperation(self):
        print('extension.onStartOperation')
        pass
    def beforeStopOperation(self):
        print('extension.beforeStopOperation')
        pass
    def onStopOperation(self):
        print('extension.onStopOperation')
        pass
    def onSaveEdits(self):
        print('extension.onSaveEdits')
        pass
    def onChangeFeature(self):
        print('extension.onChangeFeature')
        pass
    def onCreateFeature(self):
        print('extension.onCreateFeature')
        pass
    def onDeleteFeature(self):
        print('extension.onDeleteFeature')
        pass
    def onUndo(self):
        print('extension.onUndo')
        pass
    def onRedo(self):
        print('extension.onRedo')
        pass

    # Own methods
    def setButtonsState(self):
        if button is not None:
            button.changeEnabled()
