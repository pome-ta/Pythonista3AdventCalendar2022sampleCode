from pathlib import Path

import arrow

from objc_util import ObjCClass
import editor
import console

# todo: set code templates
blank_value = ''

copy_value = str(editor.get_text() if editor.get_text() else blank_value)

ui_value = '''\
import ui


class View(ui.View):
  def __init__(self):
    self.bg_color = 1

  def did_load(self):
    pass

  def will_close(self):
    pass

  def draw(self):
    pass

  def layout(self):
    pass

  def touch_began(self, touch):
    pass

  def touch_moved(self, touch):
    pass

  def touch_ended(self, touch):
    pass

  def keyboard_frame_will_change(self, frame):
    pass

  def keyboard_frame_did_change(self, frame):
    pass


if __name__ == '__main__':
  view = View()
  view.present()
  #view.present(hide_title_bar=True)
  #view.present(style='fullscreen', orientations=['portrait'])

'''

shader_value = '''\
precision highp float;

uniform float u_time;
uniform vec2 u_sprite_size;
uniform float u_scale;
uniform sampler2D u_texture;
uniform vec4 u_tint_color;
uniform vec4 u_fill_color;
varying vec2 v_tex_coord;


void main(){
  float t = u_time;
  vec2 uv = v_tex_coord;
  vec2 p = (uv- vec2(0.5)) *2.0;
  
  
  uv = uv / 2.0 + vec2(0.5);
  if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0)discard;
  gl_FragColor = vec4(uv.x, uv.y, 0.0, 1.0);
  //gl_FragColor = texture2D(u_texture,uv.xy);
  
}

'''


def get_feedback_generator():
  """
  call feedback ex:
  `UIImpactFeedbackGenerator.impactOccurred()`
  """
  style = 4  # 0-4 
  UIImpactFeedbackGenerator = ObjCClass('UIImpactFeedbackGenerator').new()
  UIImpactFeedbackGenerator.prepare()
  UIImpactFeedbackGenerator.initWithStyle_(style)
  return UIImpactFeedbackGenerator


class TemplateItem:
  def __init__(self, prompt, code, extension='.py'):
    self.prompt = prompt
    self.code = code
    self.extension = extension


def get_prompt(templates):
  prompt = ''
  for n, template in enumerate(templates):
    prompt += f'{n} => {template.prompt},\n'
  prompt += 'select a num, create a template file.\n'
  return prompt


def get_dirpath():
  fliepath = editor.get_path()
  if fliepath:
    dir_path = Path(f'{fliepath}').parent
  else:
    _home = Path('/').home()
    dir_path = _home / 'Documents'
  return dir_path


def get_nowtime():
  utc = arrow.utcnow().to('JST')
  now_str = utc.format('YYMMDD_HHmm')
  return now_str


def create_flie(templates):
  prompt = get_prompt(templates)
  feedback = get_feedback_generator()
  try:
    choose_num = int(input(prompt))
  except:
    print('Select the number(int) displayed. ')
    feedback.impactOccurred()
    return
  if choose_num == None:
    print('I can\'t find the number I chose.')
    feedback.impactOccurred()
    return

  choose_template = templates[choose_num]
  now_time = get_nowtime()

  root_dir = get_dirpath()
  new_file = Path(root_dir, f'{now_time}{choose_template.extension}')
  new_file.write_text(choose_template.code, encoding='utf-8')

  console.clear()
  editor.open_file(str(new_file), new_tab=True)
  console.hide_output()
  feedback.impactOccurred()


def main():
  blank = TemplateItem('blank', blank_value)
  copy = TemplateItem('copy', copy_value)
  ui = TemplateItem('ui', ui_value)
  shader = TemplateItem('shader', shader_value, '.js')

  template_list = [blank, copy, ui, shader]
  create_flie(template_list)


if __name__ == '__main__':
  main()