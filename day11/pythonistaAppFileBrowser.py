from pathlib import Path
import webbrowser


def parent_level(level_int):
  return '../' * level_int


# todo: 今回行きたいディレクトリパスを取得する処理
wbb_file_path = webbrowser.__file__  # webbrowser モジュールのファイルパス
wbb_path_list = wbb_file_path.split('/')  # インデックスでアクセスできるように、ファイルパスをlist化
app_index = wbb_path_list.index(
  'Pythonista3.app')  # webbrowser 格納先の手前のPythonista3.app のインデックスを取得
app_path_list = wbb_path_list[:app_index + 1]  # Pythonista3.app 以降の情報を排除
app_file_path = '.' + '/'.join(app_path_list)  # Pythonista3.app までのディレクトリパスを作成

# todo: ここから、いつもの処理
origin_path = Path()
level = 9

hub_path = origin_path / parent_level(level)

target_path = hub_path / app_file_path

webbrowser.open(f'pythonista3:/{target_path}')

resolve_origin_path = origin_path.resolve()
resolve_target_path = target_path.resolve()
