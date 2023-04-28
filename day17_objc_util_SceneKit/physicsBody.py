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
'''
Static = 0
Dynamic = 1
Kinematic = 2
'''
SCNPhysicsBody = ObjCClass('SCNPhysicsBody')
SCNPhysicsShape = ObjCClass('SCNPhysicsShape')

SCNSphere = ObjCClass('SCNSphere')
SCNFloor = ObjCClass('SCNFloor')


class GameScene:

  def __init__(self):
    self.scene: SCNScene
    self.setUpScene()

  def setUpScene(self):
    scene = SCNScene.scene()
    # 呼び出しが面倒なので、変数化
    scene_rootNode_addChildNode_ = scene.rootNode().addChildNode_

    # --- SCNFloor
    floor = SCNFloor.floor()
    floorNode = SCNNode.nodeWithGeometry_(floor)
    floorNode.position = (0.0, -4.0, 0.0)
    floorNode.eulerAngles = (-0.001, 0.0, 0.0)
    floorNode.physicsBody = SCNPhysicsBody.bodyWithType_shape_(0, None)
    scene_rootNode_addChildNode_(floorNode)

    # --- SCNSphere
    ball = SCNSphere.sphereWithRadius_(0.5)
    ballNode = SCNNode.nodeWithGeometry_(ball)
    ballNode.position.y = 2

    physicsBall = SCNPhysicsShape.shapeWithGeometry_options_(ball, None)
    #physicsBall = SCNPhysicsShape.shapeWithNode_options_(ballNode, None)

    ballNode.physicsBody = SCNPhysicsBody.bodyWithType_shape_(1, physicsBall)
    scene_rootNode_addChildNode_(ballNode)

    # --- SCNLight
    lightNode = SCNNode.node()
    lightNode.light = SCNLight.light()

    lightNode.position = (0.0, 10.0, 10.0)
    scene_rootNode_addChildNode_(lightNode)

    # --- SCNCamera
    cameraNode = SCNNode.node()
    cameraNode.camera = SCNCamera.camera()
    cameraNode.position = (0.0, 0.0, 10.0)
    scene_rootNode_addChildNode_(cameraNode)

    self.scene = scene
    self.scene_rootNode_addChildNode_ = scene_rootNode_addChildNode_
    self.ballNode = ballNode


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
    '''
    OptionNone = 0
    ShowPhysicsShapes = (1 << 0)
    ShowBoundingBoxes = (1 << 1)
    ShowLightInfluences = (1 << 2)
    ShowLightExtents = (1 << 3)
    ShowPhysicsFields = (1 << 4)
    ShowWireframe = (1 << 5)
    RenderAsWireframe = (1 << 6)
    ShowSkeletons = (1 << 7)
    ShowCreases = (1 << 8)
    ShowConstraints = (1 << 9)
    ShowCameras = (1 << 10)
    '''
    _debugOptions = ((1 << 0) | (1 << 1) | (1 << 4) | (1 << 10))
    scnView.debugOptions = _debugOptions

    scnView.autorelease()

    scnView.scene = scene.scene
    self.scene = scene
    self.scnView = scnView

  def touch_began(self, touch):
    ballNode = self.scene.ballNode.clone()
    self.scene.scene_rootNode_addChildNode_(ballNode)


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

