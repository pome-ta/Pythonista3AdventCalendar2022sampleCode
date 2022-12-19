import ui


class MainView(ui.View):
  def __init__(self):
    self.name = 'sub の縦横を半分に'
    self.bg_color = 0.5  # todo: 灰色
    self.sub = ui.View()
    self.sub.bg_color = 'red'
    self.add_subview(self.sub)

  def layout(self):
    _, _, w, h = self.frame
    self.sub.width = w / 2
    self.sub.height = h / 2


if __name__ == '__main__':
  main_view = MainView()
  main_view.present(style='fullscreen', orientations=['portrait'])
