import sys
from pathlib import Path

import ui

sys.path.append(str(Path.cwd()))
from wkwebview import WKWebView


class View(ui.View):
  def __init__(self, url, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.wv = WKWebView()
    self.wv.load_url(str(url))
    self.wv.flex = 'WH'
    self.refresh_webview()
    self.add_subview(self.wv)
    self.set_reload_btn()

  def will_close(self):
    self.refresh_webview()

  def set_reload_btn(self):
    self.refresh_btn = self.create_btn('iob:ios7_refresh_outline_32')
    self.refresh_btn.action = (lambda sender: self.refresh_webview())
    self.right_button_items = [self.refresh_btn]

  def create_btn(self, icon):
    btn_icon = ui.Image.named(icon)
    return ui.ButtonItem(image=btn_icon)

  def refresh_webview(self):
    self.wv.clear_cache()
    self.wv.reload()


if __name__ == '__main__':
  uri_path = Path('./docs/index.html')
  view = View(uri_path)
  view.present(style='fullscreen', orientations=['portrait'])
