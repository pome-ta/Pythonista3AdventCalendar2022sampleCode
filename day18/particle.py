from objc_util import load_framework, ObjCClass, on_main_thread
from objc_util import UIColor, UIImage, NSData, nsurl
import ui

#import pdbg

load_framework('SceneKit')

SCNScene = ObjCClass('SCNScene')
SCNParticleSystem = ObjCClass('SCNParticleSystem')
SCNSphere = ObjCClass('SCNSphere')
SCNNode = ObjCClass('SCNNode')
SCNAction = ObjCClass('SCNAction')
SCNLight = ObjCClass('SCNLight')
SCNCamera = ObjCClass('SCNCamera')
SCNView = ObjCClass('SCNView')


class GameScene:
  def __init__(self):
    self.scene: SCNScene
    self.setUpScene()

  def setUpScene(self):

    # --- import
    bkSky_URL = NSData.dataWithContentsOfURL_(
      nsurl('./assets/textures/Background_sky.png'))
    tex_bks = UIImage.alloc().initWithData_(bkSky_URL)

    # --- SCNScene
    scene = SCNScene.scene()
    scene.background().contents = tex_bks
    scene.lightingEnvironment().contents = tex_bks
    scene.lightingEnvironment().intensity = 1.24

    scene_rootNode_addChildNode_ = scene.rootNode().addChildNode_

    emitterBall = SCNSphere.sphereWithRadius_(0.25)
    emitterBall.geodesic = True
    emitterBall.segmentCount = 32

    # SCNParticleSystem
    particleSys = SCNParticleSystem.particleSystem()
    particleSys.emitterShape = emitterBall
    particleSys.birthRate = 1024
    particleSys.birthRateVariation = 128
    particleSys.birthDirection = 2
    particleSys.particleColor = UIColor.blueColor()
    particleSys.particleColorVariation = (0.1, 0.4, 0.6, 0.5)
    particleSys.particleAngle = 0.1
    particleSys.particleAngleVariation = 8
    particleSys.particleVelocity = 0.1
    particleSys.particleVelocityVariation = 0.2
    particleSys.particleSize = 0.001
    particleSys.particleSizeVariation = 0.005
    particleSys.emissionDuration = 0.001
    particleSys.emissionDurationVariation = 0.1
    particleSys.particleLifeSpan = 1
    particleSys.particleLifeSpanVariation = 8
    particleSys.particleAngularVelocity = 0.01
    particleSys.particleAngularVelocityVariation = 8
    particleSys.idleDuration = 0.4
    particleSys.idleDurationVariation = 0.8
    particleSys.particleIntensity = 2
    particleSys.particleIntensityVariation = 4
    particleSys.isLightingEnabled = True

    particleNode = SCNNode.node()
    particleNode.addParticleSystem(particleSys)
    scene_rootNode_addChildNode_(particleNode)

    # --- SCNCamera
    camera = SCNCamera.camera()
    camera.wantsHDR = True
    camera.wantsExposureAdaptation = True
    camera.exposureAdaptationBrighteningSpeedFactor = 0.02
    camera.exposureAdaptationDarkeningSpeedFactor = 0.1
    camera.minimumExposure = -15
    camera.maximumExposure = 15
    camera.bloomIntensity = 2.0
    camera.bloomThreshold = 0.6
    camera.bloomBlurRadius = 18
    camera.colorFringeIntensity = 4.0
    camera.colorFringeStrength = 4.0
    camera.motionBlurIntensity = 6
    camera.xFov = 35.0
    camera.yFov = 35.0
    camera.zNear = 2
    camera.zFar = 100

    cameraNode = SCNNode.node()
    cameraNode.camera = camera
    cameraNode.position = (0.0, 1.0, 2.0)
    cameraNode.eulerAngles = (-0.5, 0, 0)

    dollyNode = SCNNode.node()
    dollyNode.addChildNode_(cameraNode)

    dollyNode.runAction_(
      SCNAction.repeatActionForever_(
        SCNAction.rotateByX_y_z_duration_(0.0, 2.0, 0.1, 8.0)))

    scene_rootNode_addChildNode_(dollyNode)

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
    _debugOptions = ((1 << 0) | (1 << 1) | (1 << 3) | (1 << 5) | (1 << 10))
    scnView.debugOptions = _debugOptions

    scnView.autorelease()

    scnView.scene = scene.scene
    self.scene = scene
    self.scnView = scnView

  def touch_began(self, touch):
    pass


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])
