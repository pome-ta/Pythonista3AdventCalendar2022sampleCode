import ui


class MainView(ui.View):
  def __init__(self):
    self.name = 'ただView をadd しただけ'
    self.bg_color = 0.5  # todo: 灰色
    self.sub = ui.View()
    self.sub.bg_color = 'red'
    self.add_subview(self.sub)
    print(f'__init__: {self.frame}')

  def layout(self):
    print(f'layout: {self.frame}')


if __name__ == '__main__':
  main_view = MainView()
  main_view.present(style='fullscreen', orientations=['portrait'])
