import maya.cmds as cmds

def setHoldoutAll():
    
    targets = cmds.ls(type="mesh")
    GetA = cmds.getAttr(targets[0]+".holdOut")
    
    for target in targets:
    
        selPanel = cmds.getPanel( withFocus = True )
    
        if GetA == 0:
            cmds.setAttr(target+".holdOut", 1)
            cmds.modelEditor( selPanel, edit = True, wireframeOnShaded = True )
        else:
            cmds.setAttr(target+".holdOut", 0);
            cmds.modelEditor( selPanel, edit = True, wireframeOnShaded = False )
            
if __name__ == '__main__':
    print("This module for setting all holdout on")
    setHoldoutAll()
    
else:
    pass