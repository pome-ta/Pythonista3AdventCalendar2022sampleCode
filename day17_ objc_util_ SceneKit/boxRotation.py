from objc_util import load_framework, ObjCClass, on_main_thread
from objc_util import UIColor
import ui

#import pdbg

load_framework('SceneKit')

SCNScene = ObjCClass('SCNScene')
SCNView = ObjCClass('SCNView')
SCNNode = ObjCClass('SCNNode')

SCNLight = ObjCClass('SCNLight')
SCNCamera = ObjCClass('SCNCamera')

SCNAction = ObjCClass('SCNAction')

SCNBox = ObjCClass('SCNBox')


class GameScene:
  def __init__(self):
    self.scene: SCNScene
    self.setUpScene()

  def setUpScene(self):
    scene = SCNScene.scene()
    # 呼び出しが面倒なので、変数化
    scene_rootNode_addChildNode_ = scene.rootNode().addChildNode_

    box = SCNBox.boxWithWidth_height_length_chamferRadius_(2, 2, 2, 0.2)
    #box.firstMaterial().diffuse().contents = UIColor.blueColor()
    geometryNode = SCNNode.nodeWithGeometry_(box)
    geometryNode.runAction_(
      SCNAction.repeatActionForever_(
        SCNAction.rotateByX_y_z_duration_(0.0, 0.2, 0.1, 0.3)))
    scene_rootNode_addChildNode_(geometryNode)

    # --- SCNLight
    lightNode = SCNNode.node()
    lightNode.light = SCNLight.light()
    lightNode.position = (0.0, 10.0, 10.0)
    scene_rootNode_addChildNode_(lightNode)

    ambientLightNode = SCNNode.node()
    ambientLightNode.light = SCNLight.light()
    ambientLightNode.light().type = 'ambient'
    ambientLightNode.light().color = UIColor.redColor()
    #ambientLightNode.light().color = UIColor.darkGrayColor()
    scene_rootNode_addChildNode_(ambientLightNode)

    # --- SCNCamera
    cameraNode = SCNNode.node()
    cameraNode.camera = SCNCamera.camera()
    cameraNode.position = (0.0, 0.0, 10.0)
    scene_rootNode_addChildNode_(cameraNode)

    self.scene = scene


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.name = ''
    self.bg_color = 'maroon'

    self.scene: GameScene
    self.scnView: SCNView

    self.viewDidLoad()
    self.objc_instance.addSubview_(self.scnView)

  #@on_main_thread
  def viewDidLoad(self):
    scene = GameScene()

    # --- SCNView
    _frame = ((0, 0), (100, 100))
    scnView = SCNView.alloc().initWithFrame_(_frame)
    # ui.View.flex = 'WH' と同じ
    scnView.setAutoresizingMask_((1 << 1) | (1 << 4))
    scnView.backgroundColor = UIColor.blackColor()

    scnView.allowsCameraControl = True
    scnView.showsStatistics = True
    scnView.autorelease()

    scnView.scene = scene.scene
    self.scene = scene
    self.scnView = scnView

  def touch_began(self, touch):
    pass


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])
