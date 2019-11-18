# arcgis-addin-tool-py-template-with-selection-input
ArcGIS python add-in tool that takes selected features as input

Initially created by the ArcGIS Desktop Python AddIn Wizard.

This repo was created to solve the "tkFileDialog.askopenfilename crashes ArcMap" issue.

On stackexchange: https://gis.stackexchange.com/q/342073/5834

On GeoNet: https://community.esri.com/thread/243845-tkfiledialogaskopenfilename-in-python-addin-crashes-arcmap

MANIFEST
========

README.md   : This file

makeaddin.py : A script that will create a .esriaddin file out of this 
               project, suitable for sharing or deployment

config.xml   : The AddIn configuration file

Images/*     : all UI images for the project (icons, images for buttons, 
               etc)

Install/*    : The Python project used for the implementation of the
               AddIn. The specific python script to be used as the root
               module is specified in config.xml.

Some info about addins:
https://desktop.arcgis.com/en/arcmap/latest/analyze/python-addins/what-is-a-python-add-in.htm

Git repo:
https://github.com/r-pankevicius/arcgis-addin-tool-py-template-with-selection-input