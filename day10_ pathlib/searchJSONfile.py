from pathlib import Path

root_path = Path().home()

print('検索するディレクトリ:')
print(root_path)

for f in root_path.glob('*.json'):
  print('\n.json ファイル ---')
  print(f)
  print('--- /')
