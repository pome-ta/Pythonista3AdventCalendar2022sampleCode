import editor
import clipboard
from objc_util import ObjCClass


def get_feedback_generator(style=4):
  """
  todo: style 0-4
  call feedback ex:
  `UIImpactFeedbackGenerator.impactOccurred()`
  """
  UIImpactFeedbackGenerator = ObjCClass('UIImpactFeedbackGenerator').new()
  UIImpactFeedbackGenerator.prepare()
  UIImpactFeedbackGenerator.initWithStyle_(style)
  return UIImpactFeedbackGenerator


def main():
  feedback = get_feedback_generator(4)
  path = editor.get_path()
  clipboard.set(str(path))
  feedback.impactOccurred()


if __name__ == '__main__':
  main()
