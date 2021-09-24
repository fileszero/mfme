
import os
import MySQLdb
import settings

_sql_cache_ = {}

def get_sql(name:str)->str:
    if name in _sql_cache_:
        return _sql_cache_[name]

    filename=os.path.join(*[os.path.abspath(os.path.dirname(__file__)),'sql',f"{name}.sql"] )
    with open(filename, 'r') as f:
        SQL=f.read()
        _sql_cache_[name]=SQL

    return SQL

def create_connection(dbname:str='kabuka')->MySQLdb.Connect:
    # 接続とカーソル取得
    con = MySQLdb.connect(
        user=settings.mysql['user'],
        passwd=settings.mysql['passwd'],
        host=settings.mysql['host'],
        db=dbname,
        charset='utf8',
        use_unicode=True)
    return con

if __name__ == "__main__":
    print( get_sql('basic_filter') )
    print( get_sql('basic_filter') )