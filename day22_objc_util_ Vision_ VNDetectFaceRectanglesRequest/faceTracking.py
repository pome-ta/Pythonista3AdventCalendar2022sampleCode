from pathlib import Path
import ctypes

from objc_util import ObjCInstance, ObjCClass
from objc_util import UIImage, UIColor, UIBezierPath, NSData, nsurl, CGRect
import ui

#import pdbg

VNDetectFaceRectanglesRequest = ObjCClass('VNDetectFaceRectanglesRequest')
VNImageRequestHandler = ObjCClass('VNImageRequestHandler')

UIImageView = ObjCClass('UIImageView')
CAShapeLayer = ObjCClass('CAShapeLayer')


def get_image_absolutepath(path):
  _img_path = Path(path)
  if (_img_path.exists()):
    return str(_img_path.absolute())
  else:
    print('画像が見つかりません')
    raise


def get_UIImage(path: str) -> UIImage:
  _nsurl = nsurl(get_image_absolutepath(path))
  _data = NSData.dataWithContentsOfURL_(_nsurl)
  uiImage = UIImage.alloc().initWithData_(_data)
  return uiImage


def parseCGRect(cg_rect: CGRect) -> tuple:
  origin, size = [cg_rect.origin, cg_rect.size]
  return (origin.x, origin.y, size.width, size.height)


class RectangleShapeLayer:
  def __init__(self,
               bounds: CGRect,
               frame: CGRect,
               strokeColor=None,
               fillColor=None):

    _greenColor = UIColor.greenColor().cgColor()
    _clearColor = UIColor.clearColor().CGColor()

    self.strokeColor = strokeColor if strokeColor else _greenColor
    self.fillColor = fillColor if fillColor else _clearColor

    self.layer = CAShapeLayer.alloc().init()
    self.layer.frame = bounds
    self.rect = UIBezierPath.bezierPathWithRect_(frame)

    self.path_setup()

  def path_setup(self):
    self.layer.setLineWidth_(2.0)
    self.layer.setStrokeColor_(self.strokeColor)
    self.layer.setFillColor_(self.fillColor)
    self.layer.setPath_(self.rect.CGPath())


class ViewController:
  def __init__(self, _previewView, img_path):
    self.previewView = _previewView
    self.originalImage = get_UIImage(img_path)
    self.imageView = UIImageView.alloc().initWithImage_(self.originalImage)
    self.overlayLayer = CAShapeLayer.alloc().init()
    self.setupOverlay()
    self.faceDetection()

    self.previewView.addSubview_(self.imageView)

  def setupOverlay(self):
    self.overlayLayer.frame = self.imageView.bounds()
    self.imageView.layer().addSublayer_(self.overlayLayer)

  def faceDetection(self):
    cgImage = self.originalImage.CGImage()
    request = VNDetectFaceRectanglesRequest.alloc().init().autorelease()
    handler = VNImageRequestHandler.alloc().initWithCGImage_options_(
      cgImage, None).autorelease()

    handler.performRequests_error_([request], None)
    observation_array = request.results()
    self.drawFaceRectangle_observations_(observation_array)

  def drawFaceRectangle_observations_(self, observations):
    bounds = self.overlayLayer.frame()
    _, _, layerWidth, layerHeight = parseCGRect(bounds)

    for observation in observations:
      _x, _y, _width, _height = parseCGRect(observation.boundingBox())

      width = _width * layerWidth
      height = _height * layerHeight
      x = _x * layerWidth
      # todo: 左下原点から、左上原点へ
      y = (layerHeight - height) - (_y * layerHeight)
      frame = ((x, y), (width, height))

      rect = RectangleShapeLayer(bounds, frame)
      self.overlayLayer.addSublayer_(rect.layer)


class View(ui.View):
  def __init__(self, img_path, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.view_controller = ViewController(self.objc_instance, img_path)


if __name__ == '__main__':
  img_file_path = './img/multi-face.png'

  view = View(img_file_path)
  view.present(style='fullscreen', orientations=['portrait'])
