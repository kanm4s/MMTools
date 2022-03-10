import maya.cmds as cmds

def window_check():
    
    if cmds.window( "transformOffset_v2", exists=True ):
        cmds.deleteUI("transformOffset_v2")
    win_width = 270
    window = cmds.window( "transformOffset_v2", sizeable=1, resizeToFitChildren=1, title="transformOffset_v2" , width=win_width)

    cmds.frameLayout( l="Camera Offset", marginHeight=5, marginWidth=5 )
    cmds.columnLayout()
    cmds.optionMenuGrp( 'oldcam', label='Old Camera:', w=win_width)
    for cam in all_cam:
        cmds.menuItem( label=cam )
    cmds.optionMenuGrp( 'newcam', label='New Camera:', w=win_width)
    for cam in all_cam:
        cmds.menuItem( label=cam )
    cmds.textFieldButtonGrp( 'locator_tmp', label='Locator Tmp: ', cw3=(140, 100, 50), text='', buttonLabel='<<', buttonCommand="cmds.textFieldButtonGrp( 'locator_tmp', edit=True, text=(select_without_unicode()))" )
    cmds.setParent( '..' )
    
    cmds.separator()
    cmds.optionMenuGrp( 'offsetMode', label='Offset Mode:', w=win_width)
    cmds.menuItem( label='Offset' )
    cmds.menuItem( label='Animate' )

    cmds.text( l='**Save the file before running script!**' )
    cmds.button( l="Moveit!" , command=camera_offset )

    cmds.showWindow( window )

def select_without_unicode():
    list = cmds.ls( sl=True, o=True )
    prefix = list[0]
    return prefix

def camera_offset(self):
    oldcam = all_cam[cmds.optionMenuGrp( 'oldcam', q=True, select=True )-1]
    newcam = all_cam[cmds.optionMenuGrp( 'newcam', q=True, select=True )-1]
    loctmp = cmds.textFieldButtonGrp( 'locator_tmp', q=True, tx=True )
    
    #unparent cam
    cmds.parent( oldcam, world=True )
    cmds.parent( newcam, world=True )
    
    #check mode
    off_mode = cmds.optionMenuGrp( 'offsetMode', q=True, select=True ) # return 1=Offset, 2=animate
    
    if off_mode == 1:
        # create node for offset cam
        node_offset_cam = cmds.createNode( 'transform' , n=oldcam+"_offset")
        cmds.parentConstraint( oldcam, node_offset_cam, n=node_offset_cam[0]+"_parentConstraint1" )
        cmds.delete( node_offset_cam[0]+"_parentConstraint1" )
        cmds.parent( loctmp, node_offset_cam )
        cmds.parentConstraint( newcam, node_offset_cam )
        
    else:
        loc_for_con = cmds.spaceLocator( n=loctmp+"_for_constraint" )
        cmds.setKeyframe( loctmp+"_for_constraint.t" )
        cmds.setKeyframe( loctmp+"_for_constraint.r" )
        
        frame_start = cmds.playbackOptions( q=True, min=True )
        frame_end = cmds.playbackOptions( q=True, max=True )
        for frame in range(int(frame_start), int(frame_end)+1):
            cmds.currentTime( frame, edit=True)
    
            loc_dummy = cmds.spaceLocator( n=loctmp+"_dummy" )
            cmds.parentConstraint( loctmp, loc_dummy, n=loc_dummy[0]+"_parentConstraint1" )
            cmds.delete( loc_dummy[0]+"_parentConstraint1" )
            
            node_offset_cam = cmds.createNode( 'transform' , n=oldcam+"_offset")
            cmds.parentConstraint( oldcam, node_offset_cam, n=node_offset_cam[0]+"_parentConstraint1" )
            cmds.delete( node_offset_cam[0]+"_parentConstraint1" )
            cmds.parent( loc_dummy, node_offset_cam )
            cmds.parentConstraint( newcam, node_offset_cam )
            cmds.parent( loc_dummy, world=True )
            
            #get translate and rotate from dummy
            get_T = cmds.xform( loc_dummy, query=True, translation=True )
            get_R = cmds.xform( loc_dummy, query=True, rotation=True )
            cmds.xform( loc_for_con, absolute=True, translation=(get_T[0], get_T[1], get_T[2]) )
            cmds.xform( loc_for_con, absolute=True, rotation=(get_R[0], get_R[1], get_R[2]) )
            cmds.setKeyframe( loctmp+"_for_constraint.t" )
            cmds.setKeyframe( loctmp+"_for_constraint.r" )
            cmds.delete( node_offset_cam, loc_dummy )


if __name__ == '__main__':
    all_cam = cmds.listCameras( p=True )
    window_check()
