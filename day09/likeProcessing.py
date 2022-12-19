import scene
import ui


def create_button(icon_name):
  button_icon = ui.Image.named(icon_name)
  button = ui.ButtonItem(image=button_icon)
  return button


class mainview(ui.View):
  def __init__(self, canvas):
    self.bg_color = tint_color
    self.tint_color = title_color
    self.name = title
    self.height_ratio = 0.96  # todo: safe area

    self.canvas = canvas
    self.scene_view = None

    self.setup_navigationbuttons()
    self.setup_scene()
    self.show_scene()

  def draw(self):
    # todo: init background color
    w = self.width
    h = self.height * self.height_ratio
    wrap = ui.Path.rect(0, 0, w, h)
    ui.set_color(bg_color)
    wrap.fill()

  def layout(self):
    self.scene_view.width = self.width
    self.scene_view.height = self.height * self.height_ratio
    self.scene_view.x = self.width / 2 - self.scene_view.width / 2

  def setup_scene(self):
    scene_view = scene.SceneView()
    scene_view.frame_interval = 2
    scene_view.shows_fps = True
    scene_view.alpha = 0
    scene_view.scene = self.canvas
    self.add_subview(scene_view)
    self.scene_view = scene_view

  @ui.in_background
  def show_scene(self):
    def dissolve():
      self.scene_view.alpha = 1

    ui.animate(dissolve, duration=.3)

  def setup_navigationbuttons(self):
    show_console_icon = 'iob:ios7_download_outline_32'
    show_console_button = create_button(show_console_icon)
    show_console_button.action = self.show_console

    self.right_button_items = [show_console_button]

  @ui.in_background
  def show_console(self, sender):
    raw_image = self.canvas.view._debug_quicklook_()
    image = ui.image.from_data(raw_image, 2.0)
    image.show()


class canvas(scene.Scene):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.background_color = bg_color

  @ui.in_background
  def setup(self):
    self.set_line(128)

  def set_line(self, dire):
    w2, h2 = self.size / 2
    path = ui.Path()
    path.move_to(w2 - dire, h2 - dire)
    path.line_to(w2 + dire, h2 + dire)
    line = scene.ShapeNode(parent=self)
    line.path = path
    line.stroke_color = 'red'
    line.position = self.size / 2

  @ui.in_background
  def update(self):
    #print(f'{self.t}')  # 画面左下にlog として表示される
    pass


if __name__ == '__main__':
  title = 'プログラミングでお絵描き'

  bg_color = 0.872
  tint_color = 0.128
  title_color = 0.872
  af_color = tint_color

  canvas = canvas()

  view = mainview(canvas)
  view.present(
    style='fullscreen',
    orientations='portrait',
    title_bar_color=tint_color,
    title_color=title_color)
