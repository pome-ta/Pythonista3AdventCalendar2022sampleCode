from pathlib import Path
import webbrowser

origin_path = Path()

url = 'pythonista3://' + str(origin_path)

webbrowser.open(url)
