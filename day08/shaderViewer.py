import scene
import editor

shader_code = editor.get_text()


class MyScene(scene.Scene):
  def setup(self):
    self.div = scene.Node()
    self.add_child(self.div)

    self.shdr = scene.SpriteNode(parent=self.div)
    self.shdr.shader = scene.Shader(f'{shader_code}')

    self.set_shader_area()

  def did_change_size(self):
    self.set_shader_area()

  def set_shader_area(self):
    self.div.position = self.size / 2
    _size = min(self.size.x, self.size.y) * .957
    self.shdr.size = (_size, _size)


if __name__ == '__main__':
  main = MyScene()
  scene.run(main, show_fps=True, frame_interval=2)
