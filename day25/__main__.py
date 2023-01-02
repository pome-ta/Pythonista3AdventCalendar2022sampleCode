import sys
from pathlib import Path

import ui

sys.path.append(str(Path.cwd()))
from wkwebview import WKWebView

js_func = '''function getShaderCode() {
  const area = document.querySelector('#textArea');
  return `${area.value}`;
}
'''


class View(ui.View):
  def __init__(self, root, save_path, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.save_path = save_path

    self.wv = WKWebView()
    self.wv.flex = 'WH'
    self.add_subview(self.wv)

    self.wv.load_url(str(root))
    self.wv.add_script(js_func)
    self.wv.clear_cache()
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
    self.get_shader_code()
    self.wv.reload()

  def get_shader_code(self):
    js_code = 'getShaderCode()'
    self.wv.eval_js_async(js_code, lambda v: overwrite_code(v, self.save_path))


def overwrite_code(value, save_path):
  shader_path = Path(f'{save_path}')
  shader_path.write_text(value, encoding='utf-8')


if __name__ == '__main__':
  entry_point = Path('./docs/index.html')
  save_uri = Path('./docs/shaders/fragment/fragmentMain.js')

  view = View(entry_point, save_uri)
  view.present(style='fullscreen', orientations=['portrait'])

