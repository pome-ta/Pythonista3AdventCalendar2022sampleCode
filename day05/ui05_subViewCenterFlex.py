import ui


class MainView(ui.View):
  def __init__(self):
    self.name = '上下左右中心: flex'
    self.bg_color = 0.5  # todo: 灰色
    self.sub = ui.View()
    self.sub.flex = 'TBLR'
    self.sub.bg_color = 'red'
    self.add_subview(self.sub)



if __name__ == '__main__':
  main_view = MainView()
  main_view.present(style='fullscreen', orientations=['portrait'])
