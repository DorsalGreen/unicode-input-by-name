import unicodedata as ud
import sqlite3
import meta
from path import path as Path
import wx

HARD_LIMIT = -1

class UnicodeDatabase(object):
    
    def __init__(self):
        wx.GetApp().SetAppName(meta.APPNAME_SHORT)
        data_dir = Path(wx.StandardPaths.Get().GetUserDataDir())
        try:
            data_dir.mkdir()
        except:
            pass
        db_file = data_dir / 'unicodedata.db'
        
        if meta.MEMORY:
            self.conn = sqlite3.connect(':memory:')
        else:    
            self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self._create_db(self.conn)
    
    @staticmethod
    def _create_db(conn):
        sql_query = 'CREATE TABLE IF NOT EXISTS udata ( id integer primary key, name text, freq integer )'
        conn.execute(sql_query)
        sql_query = "SELECT count(id) FROM udata"
        count = conn.execute(sql_query).fetchone()[0]
        
        if count != 0:
            return
        
        for i in xrange(0, 0xFFFF):
            u = unichr(i)
            try:
                name = ud.name(u)
                conn.execute('insert into udata values (?, ?, ?)',
                             (i, name, 0))
            except ValueError:
                pass
        conn.commit()
                    
    def get_count(self, query):
        query = '%' + query + '%'
        sql_query = "select count(id) from udata where name like ?"
        count = self.conn.execute(sql_query, (query,)).fetchone()[0]
        if HARD_LIMIT > 0:
            return min(count, HARD_LIMIT)
        return count
        
    def get_chars(self, query, start, count):
        query = '%' + query + '%'
        sql_query = "select id, name from udata where name like ? order by freq desc, id asc limit ? offset ?"
        return self.conn.execute(sql_query, (query, count, start))
    
    def increment_frequency(self, char):
        sql_query = "select freq from udata where id = ?"
        count = self.conn.execute(sql_query, (char['id'],)).fetchone()[0]
        sql_query = "update udata set freq = ? where id = ?"
        self.conn.execute(sql_query, (count + 1, char['id']))
        self.conn.commit()


if __name__ == '__main__':
    udb = UnicodeDatabase()
    print udb.get_count('infinity')
    for row in udb.get_chars('infinity', 0, 10):
        print row
    print udb.get_count('i')
    udb.increment_frequency(row)



