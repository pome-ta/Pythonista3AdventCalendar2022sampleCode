from pathlib import Path

path = Path()
abs_path = path.resolve()

print(abs_path)
for f in abs_path.glob('*'):
  print(f'\t- {f.name}')
