import keyboard
import ui
import clipboard

# You can modify or extend this list to change the characters that are shown in the keyboard extension:
characters = [
  '📝', '#', '-', '*', '/', '%', '`', '<', '>', '[', ']', '1', '2', '3', '4',
  '5', '6', '7', '8', '9', '0'
]


class CharsView(ui.View):
  def __init__(self, *args, **kwargs):
    super().__init__(self, *args, **kwargs)
    self.background_color = '#333'
    self.scroll_view = ui.ScrollView(frame=self.bounds, flex='WH')
    self.scroll_view.paging_enabled = True
    self.scroll_view.shows_horizontal_scroll_indicator = False
    self.add_subview(self.scroll_view)
    self.buttons = []
    for c in characters:
      button = ui.Button(title=c)
      button.font = ('<System>', 16)
      button.background_color = (1, 1, 1, 0.1)
      button.tint_color = 'white'
      button.corner_radius = 4
      button.action = self.button_action
      self.scroll_view.add_subview(button)
      self.buttons.append(button)

  def layout(self):
    rows = max(1, int(self.bounds.h / 36))
    bw = 32  # 44
    h = (self.bounds.h / rows) - 4
    x, y = 2.5, 2
    for button in self.buttons:
      button.frame = (x, y, bw, h)
      y += h + 4
      if y + h > self.bounds.h:
        y = 2
        x += bw + 4
    self.scroll_view.content_size = (
      (len(self.buttons) / rows + 1) * (bw + 4) + 40, 0)

  def button_action(self, sender):
    if sender.title == '📝':
      text = clipboard.get()
    else:
      text = sender.title

    if keyboard.is_keyboard():
      keyboard.play_input_click()
      keyboard.insert_text(text)
    else:
      print('Keyboard input:', text)


def main():
  v = CharsView(frame=(0, 0, 320, 40))
  if keyboard.is_keyboard():
    keyboard.set_view(v, 'current')
  else:
    # For debugging in the main app:
    v.name = 'Keyboard Preview'
    v.present('sheet')


if __name__ == '__main__':
  main()
