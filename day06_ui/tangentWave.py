from math import sin, pi, tan
import ui

wire = ui.Path()
wire.line_width = 0.5


class MainView(ui.View):
  def __init__(self):
    self.name = 'sin -> tan'
    self.bg_color = 0.2

    self.update_interval = 1 / 60
    self.counter = 0

    self.line_stroke_color = (0.8, 0.8, 0.8, 0.8)
    self.segment = 8

  def draw(self):
    amp = self.height / 6
    for i in range(self.segment):
      x = i / (self.segment - 1) * self.width

      radian = (i / self.segment * pi) + (self.counter / 32)
      y = (amp * tan(radian)) + (self.height / 2)
      if i: wire.line_to(x, y)
      else: wire.move_to(x, y)

    ui.set_color(self.line_stroke_color)
    wire.stroke()

  def update(self):
    self.counter += 1
    self.set_needs_display()


if __name__ == '__main__':
  main_view = MainView()
  main_view.present(style='fullscreen', orientations=['portrait'])
