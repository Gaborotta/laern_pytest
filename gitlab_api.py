import urllib.parse
import requests
import json
import os
from pprint import pp, pprint

os.getcwd()

# API KEY読み込み
with open('SETTING/SETTING.json') as f:
    setting_df = json.load(f)
headers = {'PRIVATE-TOKEN': setting_df['API_KEY']}
pid = setting_df["PROJECT_ID"]

# issue 一覧
res = requests.get(
    f'https://gitlab.com/api/v4/projects/{pid}/issues', headers=headers)

pprint(res.json())

# issue 作成
issue_param = {
    'title': 'API_ISSUE_TEST',
    "description": """
これはテストです
あばばばば
    あばばば

- aaaaaa
    - aaaaa
    - aaaaa
- bbbb
    """,
    "labels": "TEST1,TEST2,XXXX,YYYYY,adsasd,dsfsbfgrt,"
}
res = requests.post(
    f'https://gitlab.com/api/v4/projects/{pid}/issues',
    headers=headers,
    params=issue_param
)
pprint(res.json())

# wiki 取得
res = requests.get(
    f'https://gitlab.com/api/v4/projects/{pid}/wikis', headers=headers)

pprint(res.json())

slag = "Home/asdasdas"
encoded = urllib.parse.quote(slag, safe='')
res = requests.get(
    f'https://gitlab.com/api/v4/projects/{pid}/wikis/{encoded}', headers=headers)
pprint(res.json())

# wiki 作成
slag = "Home/test"
wiki_param = {
    'title': slag,  # タイトルとslagは一緒みたい
    "content": """
これはテストです
あばばばば
    あばばば

- aaaaaa
    - aaaaa
    - aaaaa
- bbbb
    """,
}


res = requests.post(
    f'https://gitlab.com/api/v4/projects/{pid}/wikis/', headers=headers, params=wiki_param)
pprint(res.json())
