from objc_util import load_framework, ObjCClass, ObjCInstance, create_objc_class
from objc_util import UIColor
import ui

#import pdbg

load_framework('ARKit')

ARSCNView = ObjCClass('ARSCNView')
ARFaceTrackingConfiguration = ObjCClass('ARFaceTrackingConfiguration')
ARSCNFaceGeometry = ObjCClass('ARSCNFaceGeometry')

SCNNode = ObjCClass('SCNNode')
SCNSphere = ObjCClass('SCNSphere')


class ViewController:
  def __init__(self):
    self.sceneView: ARSCNView
    self.viewDidLoad()
    self.viewWillAppear()

  def viewDidLoad(self):
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
    _debugOptions = (1 << 1) | (1 << 5) | (1 << 30) | (1 << 32)
    sceneView.debugOptions = _debugOptions

    sceneView.autorelease()
    sceneView.scene().background().contents = UIColor.blackColor()
    self.sceneView = sceneView

  def viewWillAppear(self):
    self.resetTracking()

  def viewWillDisappear(self):
    self.sceneView.session().pause()

  def resetTracking(self):
    _configuration = ARFaceTrackingConfiguration.new()
    _configuration.isLightEstimationEnabled = True
    '''ARSessionRunOptions
    ARSessionRunOptionResetTracking = (1 << 0)
    ARSessionRunOptionRemoveExistingAnchors = (1 << 1)
    '''
    _options = (1 << 0) | (1 << 1)
    self.sceneView.session().runWithConfiguration_options_(
      _configuration, _options)

  def create_delegate(self):
    # --- /delegate
    def renderer_didAddNode_forAnchor_(_self, _cmd, _renderer, _node, _anchor):
      renderer = ObjCInstance(_renderer)
      node = ObjCInstance(_node)

      faceGeometry = ARSCNFaceGeometry.faceGeometryWithDevice_(
        renderer.device())
      #faceGeometry.firstMaterial().fillMode = 1
      faceGeometry.firstMaterial().diffuse().contents = UIColor.blueColor()
      faceGeometry.material(
      ).lightingModelName = 'SCNLightingModelPhysicallyBased'

      ball = SCNSphere.sphereWithRadius_(0.03)
      ball.segmentCount = 8
      ball.geodesic = True

      ball.firstMaterial().diffuse().contents = UIColor.redColor()

      ball.material().lightingModelName = 'SCNLightingModelPhysicallyBased'

      ballNode = SCNNode.nodeWithGeometry_(ball)
      ballNode.position = (0.0, 0.0, 0.08)
      node.addChildNode_(ballNode)

      node.geometry = faceGeometry

    def renderer_didUpdateNode_forAnchor_(_self, _cmd, _renderer, _node,
                                          _anchor):
      node = ObjCInstance(_node)
      faceAnchor = ObjCInstance(_anchor)

      faceGeometry = node.geometry()
      faceGeometry.updateFromFaceGeometry_(faceAnchor.geometry())

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
