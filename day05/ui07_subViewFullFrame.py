import ui


class MainView(ui.View):
  def __init__(self):
    self.name = '全画面: frame'
    self.bg_color = 0.5  # todo: 灰色
    self.sub = ui.View()
    self.sub.bg_color = 'red'
    self.add_subview(self.sub)

  def layout(self):
    _, _, main_width, main_height = self.frame
    self.sub.frame = (0.0, 0.0, main_width, main_height)


if __name__ == '__main__':
  main_view = MainView()
  main_view.present(style='fullscreen', orientations=['portrait'])
