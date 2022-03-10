import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.cmds as cmds
import math

class rayProjection:
    
    def create_UI(self):
        self.name = "rayProjection"
        self.all_cam = cmds.listCameras( p=True )
        
        if cmds.window( self.name, exists=True ):
            cmds.deleteUI(self.name)
            
        self.win_width = 270
        window = cmds.window( self.name, sizeable=1, resizeToFitChildren=1, title=self.name , width=self.win_width)
        cmds.frameLayout( l="Ray to mesh", marginHeight=5, marginWidth=5 )
        cmds.columnLayout()
        cmds.optionMenuGrp( 'selcam', label='Camera:', w=self.win_width)
        for cam in self.all_cam:
            cmds.menuItem( label=cam )
        cmds.textFieldButtonGrp( 'get_mesh', label='Geo Target: ', cw3=(140, 100, 50), text='', buttonLabel='<<', buttonCommand="cmds.textFieldButtonGrp( 'get_mesh', edit=True, text=(cmds.ls( sl=True, o=True )[0]))" )
        cmds.textFieldButtonGrp( 'selJnt', label='Joint Target: ', cw3=(140, 100, 50), text='', buttonLabel='<<', buttonCommand="cmds.textFieldButtonGrp( 'selJnt', edit=True, text=(cmds.ls( sl=True, o=True )[0]))" )
        cmds.setParent( '..' )
    
        cmds.separator()
        cmds.text( l='Step1: select locator before run.' )
        cmds.rowLayout(numberOfColumns=2)
        cmds.checkBox( "oneframe_check", label='One frame', width=self.win_width*0.3, align='right', value=1)
        cmds.button( l="Ray to Mesh" , command=self.rayProjection ,width=self.win_width*0.7)
        cmds.setParent( '..' )
        
        cmds.showWindow( window )
        
        
    def rayProjection(self, *args):
        
        self.cam_select = self.all_cam[cmds.optionMenuGrp( 'selcam', q=True, select=True )-1] # optionmenu will return number only
        
        #get frmae start and frame end
        self.start_frame = int(cmds.playbackOptions(query=True, minTime=True))
        self.end_frame = int(cmds.playbackOptions(query=True, maxTime=True))

        #list locator
        self.selection = cmds.ls( sl=True )
        
        #mesh select
        self.mesh_select = cmds.textFieldButtonGrp( 'get_mesh', q=True, tx=True ) #merge_mmstage()

        #aim all locator to cam to get direction
        for loc in self.selection:
            
            self.test = cmds.aimConstraint( self.cam_select, loc, offset=(0,0,0), weight=1, aimVector=(0,0,1), upVector=(0,1,0), worldUpType="vector",worldUpVector=(0, 1, 0) )
            
            self.check_oneframe = cmds.checkBox( "oneframe_check", query=True, value=True)
            
            if self.check_oneframe:
                self.raycal(loc, self.mesh_select)
                cmds.select(clear=True)
            else:
                for f in range(self.start_frame,self.end_frame+1):
                    cmds.currentTime(f)
                    self.raycal(loc, self.mesh_select)
                    cmds.select(clear=True)
                    

            cmds.setAttr( loc+".rotateX" ,0 )
            cmds.setAttr( loc+".rotateY" ,0 )
            cmds.setAttr( loc+".rotateZ" ,0 )

    
    def raycal(self, loc, mesh):
        pos = cmds.xform(loc, query=True, worldSpace=True, translation=True) # get locator position in world space
                
        world_mat = cmds.xform(loc, q=True, matrix=True, worldSpace=True)[8:11] #get loc world 
        forward = [i * -1 for i in world_mat] #get camera direction
        
        locMPointTmp = om.MPoint(pos[0],pos[1],pos[2])
        
        selectionList = om.MSelectionList()
        selectionList.add(mesh)
        
        dagPath = selectionList.getDagPath(0)
        
        fnMesh = om.MFnMesh(dagPath)
    
        intersection = fnMesh.closestIntersection(
                        om.MFloatPoint(locMPointTmp),
                        om.MFloatVector(forward),
                        om.MSpace.kWorld, 999999, False)
                        
        
        hitPoint, hitRayParam, hitFace, hitTriangle, hitBary1, hitBary2 = intersection
        
        x,y,z,_ = hitPoint
        if x == 0.0:
            print("not found mesh")
            pass
            
        else:
            try:
                cmds.setAttr( loc+"_rpLoc.translateX" ,x )
                cmds.setAttr( loc+"_rpLoc.translateY" ,y )
                cmds.setAttr( loc+"_rpLoc.translateZ" ,z )
                cmds.setKeyframe( loc+"_rpLoc.tx" )
                cmds.setKeyframe( loc+"_rpLoc.ty" )
                cmds.setKeyframe( loc+"_rpLoc.tz" )

            except RuntimeError:
                loc_cast = cmds.spaceLocator( name=loc+"_rpLoc", relative=True )
                cmds.setAttr( loc+"_rpLoc.translateX" ,x )
                cmds.setAttr( loc+"_rpLoc.translateY" ,y )
                cmds.setAttr( loc+"_rpLoc.translateZ" ,z )
                cmds.setKeyframe( loc+"_rpLoc.tx" )
                cmds.setKeyframe( loc+"_rpLoc.ty" )
                cmds.setKeyframe( loc+"_rpLoc.tz" )

                print("Placed locator at "+ str(x),str(y),str(z))
            

if __name__ == '__main__':
    print("This module for ray projecting to mesh.")
    rp = rayProjection()
    rp.create_UI()

else:
    pass