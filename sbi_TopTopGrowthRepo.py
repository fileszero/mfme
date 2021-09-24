import os
import json
import datetime
from decimal import Decimal

import mylib
import sbi_client

# date, datetimeの変換関数
def json_serial(obj):
    # 日付型の場合には、文字列に変換します
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, object) and hasattr(obj, '__dict__'):
        return obj.__dict__
    # return str(obj)

    # 上記以外はサポート対象外.
    raise TypeError ("Type %s not serializable" % type(obj))

sbi_config = mylib.get_config("sbi.jsonc")

sbi = sbi_client.sbi_client(sbi_config["sbi"])

sbi.login()
# sbi.openStock('9984')
script_dir = os.path.dirname(os.path.abspath(__file__))
sbi_hash=sbi.GetHashCode()
growth=sbi.GetTopGrowth()
js_file = os.path.join(*[script_dir, "charts","top_growth_data.js"])
with open(js_file, 'w',encoding="UTF-8") as f:
    js=f'top_growth={json.dumps(growth,default=json_serial, indent=2, ensure_ascii=False)};\n'
    f.write(js)
    js=f'\n\nhash_code="{sbi_hash}";\n'
    f.write(js)
    js=f'\n\ntop_growth_updatetime="{datetime.datetime.now().isoformat()}";\n'
    f.write(js)
    abs_path=os.path.abspath(__file__).replace("\\","\\\\")
    js=f'\n\ntop_growth_update_command="python {abs_path}";\n'
    f.write(js)

