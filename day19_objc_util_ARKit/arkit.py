from objc_util import load_framework, ObjCClass
from objc_util import UIColor
import ui

#import pdbg

load_framework('ARKit')

ARSCNView = ObjCClass('ARSCNView')
ARWorldTrackingConfiguration = ObjCClass('ARWorldTrackingConfiguration')

SCNScene = ObjCClass('SCNScene')
SCNNode = ObjCClass('SCNNode')

SCNAction = ObjCClass('SCNAction')

SCNBox = ObjCClass('SCNBox')


class GameScene:
  def __init__(self):
    self.scene: SCNScene
    self.setUpScene()

  def setUpScene(self):
    scene = SCNScene.scene()
    scene_rootNode_addChildNode_ = scene.rootNode().addChildNode_

    box = SCNBox.boxWithWidth_height_length_chamferRadius_(0.5, 0.5, 0.5, 0.08)
    box.firstMaterial().diffuse().contents = UIColor.blueColor()

    geometryNode = SCNNode.nodeWithGeometry_(box)
    geometryNode.position = (0, -1.0, -1.0)

    geometryNode.runAction_(
      SCNAction.repeatActionForever_(
        SCNAction.rotateByX_y_z_duration_(0.0, 0.2, 0.1, 0.3)))

    scene_rootNode_addChildNode_(geometryNode)

    self.scene = scene


class ViewController:
  def __init__(self):
    self.sceneView: ARSCNView
    self.scene: GameScene
    self.viewDidLoad()
    self.viewWillAppear()

  def viewDidLoad(self):
    scene = GameScene()

    _frame = ((0, 0), (100, 100))
    sceneView = ARSCNView.alloc().initWithFrame_(_frame)
    sceneView.autoresizingMask = (1 << 1) | (1 << 4)
    sceneView.autoenablesDefaultLighting = True
    sceneView.showsStatistics = True
    ''' debugOptions
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
    ARSCNDebugOptionShowFeaturePoints = (1 << 30)
    ARSCNDebugOptionShowWorldOrigin = (1 << 32)
    '''

    _debugOptions = (1 << 1) | (1 << 30) | (1 << 32)
    sceneView.debugOptions = _debugOptions

    sceneView.scene = scene.scene
    sceneView.autorelease()

    self.scene = scene
    self.sceneView = sceneView

  def viewWillAppear(self):
    self.resetTracking()

  def viewWillDisappear(self):
    self.sceneView.session().pause()

  def resetTracking(self):
    configuration = ARWorldTrackingConfiguration.new()
    self.sceneView.session().runWithConfiguration_(configuration)


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.vc = ViewController()
    self.objc_instance.addSubview_(self.vc.sceneView)

  def will_close(self):
    self.vc.viewWillDisappear()


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])
