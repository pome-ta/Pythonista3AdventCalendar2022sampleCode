from objc_util import load_framework, ObjCClass, on_main_thread
from objc_util import UIColor
import ui

load_framework('SceneKit')

SCNScene = ObjCClass('SCNScene')
SCNView = ObjCClass('SCNView')


class GameScene:
  def __init__(self):
    self.scene: SCNScene
    self.setUpScene()

  def setUpScene(self):
    scene = SCNScene.scene()
    # ---
    # ここに処理を書いていく
    # ---
    self.scene = scene


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.name = '土台作り'
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
