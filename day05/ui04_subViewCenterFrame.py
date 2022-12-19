import ui


class MainView(ui.View):
  def __init__(self):
    self.name = '上下左右中心: frame'
    self.bg_color = 0.5  # todo: 灰色
    self.sub = ui.View()
    self.sub.bg_color = 'red'
    self.add_subview(self.sub)

  def layout(self):
    _, _, main_width, main_height = self.frame
    _, _, sub_width, sub_height = self.sub.frame
    sub_x = main_width / 2 - sub_width / 2
    sub_y = main_height / 2 - sub_height / 2

    self.sub.x = sub_x
    self.sub.y = sub_y


if __name__ == '__main__':
  main_view = MainView()
  main_view.present(style='fullscreen', orientations=['portrait'])

