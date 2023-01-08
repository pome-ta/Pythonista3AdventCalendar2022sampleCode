from pathlib import Path
import requests


def get_accesstoken():
  _path = Path().home() / 'Documents' / 'qiitaAccessToken.txt'
  return _path.read_text().replace('\n', '') if _path.exists() else None


TOKEN = get_accesstoken()
HEADERS = {'Authorization': f'Bearer {TOKEN}'} if TOKEN else None
URL = 'https://qiita.com/api/v2/tags/'


def get_tag_items_count(tag_name):
  url = URL + tag_name
  r = requests.get(url, headers=HEADERS)
  text_json = r.json()
  return int(text_json['items_count'])  # int 追い掛け


def get_item_list(tag_name, items_count):
  item_list = []
  url = URL + tag_name + '/items'
  count = (items_count // 100) + 1  # 100記事以上あれば
  for c in range(count):
    params = {
      'page': f'{c + 1}',
      'per_page': '100',
    }
    r = requests.get(url, params=params, headers=HEADERS)
    items_json = r.json()
    for item in items_json:
      item_list.append([
        item['title'],
        item['url'],
        item['user']['id'],
        item['created_at'],
      ])
  return item_list


def get_qiita():
  pool_list = []
  tags = ['Pythonista3', 'Pythonista']
  for tag in tags:
    count = get_tag_items_count(tag)
    item_list = get_item_list(tag, count)
    pool_list.extend(item_list)
  return list(map(list, set(map(tuple, pool_list))))  # 重複しているものを削除


def out_md_format(tag_item_list):
  out_txt = ''
  for item in tag_item_list:
    # 力技
    out_txt += f'- [{item[0]}]({item[1]})\n  - {item[2]}\n  - {item[3]}\n\n'
  print(out_txt)
  print(f'\n{len(tag_item_list)} 記事')


if __name__ == '__main__':
  qiita_list = get_qiita()
  l = sorted(qiita_list, key=lambda x: x[3], reverse=True)  # 作成日でソート
  out_md_format(l)

