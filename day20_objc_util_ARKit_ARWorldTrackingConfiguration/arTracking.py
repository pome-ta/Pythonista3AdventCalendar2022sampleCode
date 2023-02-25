from math import pi

from objc_util import load_framework, ObjCClass, ObjCInstance, create_objc_class
from objc_util import UIColor
import ui

#import pdbg

load_framework('ARKit')

ARSCNView = ObjCClass('ARSCNView')
ARWorldTrackingConfiguration = ObjCClass('ARWorldTrackingConfiguration')

SCNScene = ObjCClass('SCNScene')
SCNNode = ObjCClass('SCNNode')
SCNPlane = ObjCClass('SCNPlane')


class GameScene:
  def __init__(self):
    self.scene: SCNScene
    self.setUpScene()

  def setUpScene(self):
    scene = SCNScene.scene()
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

    _delegate = self.create_delegate()
    sceneView.delegate = _delegate

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
    _configuration = ARWorldTrackingConfiguration.new()
    _configuration.planeDetection = (1 << 0)
    self.sceneView.session().runWithConfiguration_(_configuration)

  def create_delegate(self):
    # --- /delegate
    def renderer_didAddNode_forAnchor_(_self, _cmd, renderer, _node, _anchor):
      node = ObjCInstance(_node)
      planeAnchor = ObjCInstance(_anchor)
      _width = planeAnchor.planeExtent().width()
      _height = planeAnchor.planeExtent().height()
      geometry = SCNPlane.planeWithWidth_height_(_width, _height)
      geometry.firstMaterial().diffuse().contents = UIColor.color(
        red=1.0, green=0.0, blue=0.0, alpha=0.8)
      planeNode = SCNNode.nodeWithGeometry_(geometry)
      planeNode.eulerAngles = (-pi / 2.0, 0.0, 0.0)
      node.addChildNode_(planeNode)

    def renderer_didUpdateNode_forAnchor_(_self, _cmd, renderer, node, anchor):
      pass

    # --- delegate/

    _methods = [
      renderer_didAddNode_forAnchor_,
      renderer_didUpdateNode_forAnchor_,
    ]
    _protocols = ['ARSCNViewDelegate']

    renderer_delegate = create_objc_class(
      'renderer_delegate', methods=_methods, protocols=_protocols)
    return renderer_delegate.new()


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
