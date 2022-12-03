# [Google翻訳APIを無料で作る方法 - Qiita](https://qiita.com/satto_sann/items/be4177360a0bc3691fdf)

import requests

from objc_util import ObjCClass
import editor
import clipboard

URL = '自分で作ったウェブアプリケーションのURL'


def get_params(text):
  _params = {'text': f'{text}', 'source': 'en', 'target': 'ja'}
  return _params


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

  all_text = editor.get_text()
  selection_start_end = editor.get_selection()
  [s, e] = selection_start_end if selection_start_end else [0, 0]
  select_text = all_text[s:e]

  if select_text:
    params = get_params(select_text)
    r = requests.get(URL, params=params)
    text_json = r.json()
    out_text = text_json['text']

    clipboard.set(f'{out_text}')

  feedback.impactOccurred()


if __name__ == '__main__':
  main()
