#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

try:
    import scribus
except ImportError,err:
    print "This Python script is written for the Scribus scripting interface."
    print "It can only be run from within Scribus."
    sys.exit(1)



#############################################################



layout_text = """
Select Page Mirror Type:

v = vertical mirror
h = horizontal mirror

"""



def main(argv):
    unit = scribus.getUnit()
    units = ['pts','mm','inches','picas','cm','ciceros']
    unitlabel = units[unit]
    
# get page size
    pagesize = scribus.getPageSize()

    
# ask for layout style
    layout_style = scribus.valueDialog("Select Mirror", layout_text, "v")
    if layout_style == "":
        sys.exit()

        

# v = vertical mirror
    if layout_style == "v":            
        # warn and exit if no selection
        if scribus.selectionCount() == 0:
            scribus.messageBox("Error", "Select an object first!", icon=scribus.ICON_WARNING)
            sys.exit()
        
        #create mirror guides
        scribus.setVGuides(scribus.getHGuides() + [pagesize[0]/2])
        
        #get selected object
        selection_name = scribus.getSelectedObject(0)
        objectpos = scribus.getPosition(selection_name)
        objectsize = scribus.getSize(selection_name)
        
        #duplicate object
        scribus.duplicateObject(selection_name)
        
        #move object
        newobjectpos = (pagesize[0] - (objectpos[0] + objectsize[0]) , objectpos[1])
        scribus.moveObjectAbs(newobjectpos[0], objectpos[1], selection_name)
        
        #flip object
        scribus.flipObject(1,0,selection_name)

        

# h = horizontal mirror
    if layout_style == "h":            
        # warn and exit if no selection
        if scribus.selectionCount() == 0:
            scribus.messageBox("Error", "Select an object first!", icon=scribus.ICON_WARNING)
            sys.exit()
        
        #create mirror guides
        scribus.setHGuides(scribus.getHGuides() + [pagesize[1]/2])
        
        #get selected object
        selection_name = scribus.getSelectedObject(0)
        objectpos = scribus.getPosition(selection_name)
        objectsize = scribus.getSize(selection_name)
        
        #duplicate object
        scribus.duplicateObject(selection_name)
        
        #move object
        newobjectpos = (objectpos[0] , pagesize[1] - (objectpos[1] + objectsize[1]))
        scribus.moveObjectAbs(objectpos[0], newobjectpos[1], selection_name)
        
        #flip object
        scribus.flipObject(0,1,selection_name)
        
       
        
        
        


#############################################################


def main_wrapper(argv):
    try:
        scribus.statusMessage("Running script...")
        scribus.progressReset()
        main(argv)
    finally:
        # Exit neatly even if the script terminated with an exception,
        # so we leave the progress bar and status bar blank and make sure
        # drawing is enabled.
        if scribus.haveDoc():
            scribus.setRedraw(True)
        scribus.statusMessage("")
        scribus.progressReset()


# This code detects if the script is being run as a script, or imported as a module.
# It only runs main() if being run as a script. This permits you to import your script
# and control it manually for debugging.
if __name__ == '__main__':
    main_wrapper(sys.argv)


