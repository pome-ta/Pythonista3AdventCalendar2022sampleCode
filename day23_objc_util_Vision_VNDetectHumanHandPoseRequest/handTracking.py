from math import pi
import ctypes

from objc_util import c, ObjCClass, ObjCInstance, create_objc_class, on_main_thread
from objc_util import UIBezierPath, UIColor, CGRect
import ui

#import pdbg

VNDetectHumanHandPoseRequest = ObjCClass('VNDetectHumanHandPoseRequest')
VNSequenceRequestHandler = ObjCClass('VNSequenceRequestHandler')

AVCaptureVideoPreviewLayer = ObjCClass('AVCaptureVideoPreviewLayer')
AVCaptureSession = ObjCClass('AVCaptureSession')
AVCaptureDevice = ObjCClass('AVCaptureDevice')
AVCaptureDeviceInput = ObjCClass('AVCaptureDeviceInput')
AVCaptureVideoDataOutput = ObjCClass('AVCaptureVideoDataOutput')

CAShapeLayer = ObjCClass('CAShapeLayer')


def dispatch_queue_create(_name, parent):
  _func = c.dispatch_queue_create
  _func.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
  _func.restype = ctypes.c_void_p
  name = _name.encode('ascii')
  return ObjCInstance(_func(name, parent))


def parseCGRect(cg_rect: CGRect) -> tuple:
  origin, size = [cg_rect.origin, cg_rect.size]
  return (origin.x, origin.y, size.width, size.height)


class CameraView(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'green'
    self.flex = 'WH'
    self.log_area = ui.TextView()
    self.log_area.editable = False
    self.log_area.flex = 'WH'
    self.log_area.font = ('Inconsolata', 10)
    self.log_area.bg_color = (0.0, 0.0, 0.0, 0.0)
    self.layer = self.objc_instance.layer()

    self.previewLayer: AVCaptureVideoPreviewLayer
    self.overlayLayer: CAShapeLayer
    self.init()

    self.log_area.text = ''
    # layer を重ねた後でないと、隠れてしまう
    self.add_subview(self.log_area)

  def layout(self):
    self.previewLayer.frame = self.objc_instance.bounds()
    self.overlayLayer.frame = self.objc_instance.bounds()

  def update_log_area(self, text):
    self.log_area.text = f'{text}'

  def init(self):
    previewLayer = AVCaptureVideoPreviewLayer.new()
    overlayLayer = CAShapeLayer.new()

    self.layer.addSublayer_(previewLayer)
    self.previewLayer = previewLayer
    self.overlayLayer = overlayLayer
    self.setupOverlay()

  def setupOverlay(self):
    self.previewLayer.addSublayer_(self.overlayLayer)
    self.setCAShapeLayer()

  def setCAShapeLayer(self):
    _blueColor = UIColor.blueColor().cgColor()
    _cyanColor = UIColor.cyanColor().cgColor()

    self.overlayLayer.setLineWidth_(2.0)
    self.overlayLayer.setStrokeColor_(_blueColor)
    self.overlayLayer.setFillColor_(_cyanColor)
    self.previewLayer.addSublayer_(self.overlayLayer)

  @on_main_thread
  def showPoints(self, _x, _y):
    _, _, _width, _height = parseCGRect(self.overlayLayer.frame())
    x = _width - (_width * (1 - _x))
    y = _height - (_height * _y)

    radius = 8.0
    startAngle = 0.0
    endAngle = pi * 2.0

    arc = UIBezierPath.new()
    arc.addArcWithCenter_radius_startAngle_endAngle_clockwise_(
      (x, y), radius, startAngle, endAngle, True)

    self.overlayLayer.setPath_(arc.CGPath())


class CameraViewController:
  def __init__(self):
    self.cameraView = CameraView()
    _name = 'CameraFeedDataOutput'
    self.videoDataOutputQueue = dispatch_queue_create(_name, None)
    self.delegate = self.create_sampleBufferDelegate()

    self.cameraFeedSession: AVCaptureSession
    self.handPoseRequest: VNDetectHumanHandPoseRequest
    self.viewDidLoad()
    self.viewDidAppear()

  def viewDidLoad(self):
    handPoseRequest = VNDetectHumanHandPoseRequest.new()
    handPoseRequest.maximumHandCount = 1

    self.handPoseRequest = handPoseRequest

  def viewDidAppear(self):
    _resizeAspectFill = 'AVLayerVideoGravityResizeAspectFill'

    self.cameraView.previewLayer.videoGravity = _resizeAspectFill
    self.setupAVSession()
    self.cameraView.previewLayer.session = self.cameraFeedSession

    self.cameraFeedSession.startRunning()

  def viewWillDisappear(self):
    self.cameraFeedSession.stopRunning()

  def setupAVSession(self):
    _builtInWideAngleCamera = 'AVCaptureDeviceTypeBuiltInWideAngleCamera'
    _video = 'vide'
    _front = 2
    _back = 1

    videoDevice = AVCaptureDevice.defaultDeviceWithDeviceType_mediaType_position_(
      _builtInWideAngleCamera, _video, _back)

    deviceInput = AVCaptureDeviceInput.deviceInputWithDevice_error_(
      videoDevice, None)

    session = AVCaptureSession.new()
    session.beginConfiguration()
    _Preset_high = 'AVCaptureSessionPresetHigh'
    session.setSessionPreset_(_Preset_high)

    if session.canAddInput_(deviceInput):
      session.addInput_(deviceInput)
    else:
      raise

    dataOutput = AVCaptureVideoDataOutput.new()
    if session.canAddOutput_(dataOutput):
      session.addOutput_(dataOutput)
      dataOutput.alwaysDiscardsLateVideoFrames = True
      dataOutput.setSampleBufferDelegate_queue_(self.delegate,
                                                self.videoDataOutputQueue)
    else:
      raise
    session.commitConfiguration()
    self.cameraFeedSession = session

  def detectedHandPose_request(self, request_list):
    _all = 'VNIPOAll'  # VNHumanHandPoseObservationJointsGroupNameAll
    _point = 'VNHLKITIP'  # 人差し指先端
    for result in request_list:
      handParts = result.recognizedPointsForJointsGroupName_error_(_all, None)

      self.cameraView.update_log_area(f'{handParts}')

      recognizedPoint = handParts[_point]
      x_point = recognizedPoint.x()
      y_point = recognizedPoint.y()
      self.cameraView.showPoints(x_point, y_point)

  def create_sampleBufferDelegate(self):
    sequenceHandler = VNSequenceRequestHandler.new()
    _right = 6  # kCGImagePropertyOrientationRight

    # --- /delegate
    def captureOutput_didOutputSampleBuffer_fromConnection_(
        _self, _cmd, _output, _sampleBuffer, _connection):
      sampleBuffer = ObjCInstance(_sampleBuffer)
      sequenceHandler.performRequests_onCMSampleBuffer_orientation_error_(
        [self.handPoseRequest], sampleBuffer, _right, None)

      observation_array = self.handPoseRequest.results()
      if observation_array:
        self.detectedHandPose_request(observation_array)

    def captureOutput_didDropSampleBuffer_fromConnection_(
        _felf, _cmd, _output, _sampleBuffer, _connection):
      ObjCInstance(_sampleBuffer)  # todo: 呼ぶだけ

    # --- delegate/

    _methods = [
      captureOutput_didOutputSampleBuffer_fromConnection_,
      captureOutput_didDropSampleBuffer_fromConnection_,
    ]

    _protocols = ['AVCaptureVideoDataOutputSampleBufferDelegate']

    sampleBufferDelegate = create_objc_class(
      'sampleBufferDelegate', methods=_methods, protocols=_protocols)
    return sampleBufferDelegate.new()


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.cvc = CameraViewController()
    self.add_subview(self.cvc.cameraView)

  def will_close(self):
    self.cvc.viewWillDisappear()


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])
