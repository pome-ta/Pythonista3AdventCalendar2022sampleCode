import ui


class MyView(ui.View):
  def __init__(self):
    print('__init__')

  def did_load(self):
    print('did_load')

  def will_close(self):
    print('will_close')

  def draw(self):
    path = ui.Path.oval(0, 0, self.width, self.height)
    ui.set_color('red')
    path.fill()
    img = ui.Image.named('ionicons-beaker-256')
    img.draw(0, 0, self.width, self.height)
    print('draw')

  def layout(self):
    print('layout')

  def touch_began(self, touch):
    print('touch_began')

  def touch_moved(self, touch):
    print('touch_moved')

  def touch_ended(self, touch):
    print('touch_ended')

  def keyboard_frame_will_change(self, frame):
    print('keyboard_frame_will_change')

  def keyboard_frame_did_change(self, frame):
    print('keyboard_frame_did_change')


v = MyView()
v.present('sheet')