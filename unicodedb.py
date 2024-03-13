import unicodedata as ud
import sqlite3
import meta
from pathlib import Path
import wx

HARD_LIMIT = -1

#define the highest unicode symbol to include in database
MAX_UNICODE_CODE = 0x1FBFF

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
        
        #count the number of valid code points. This method is inefficient, but works for now.
        numValidCodePoint = 0
        for i in range(0, MAX_UNICODE_CODE):
            u = chr(i)
            try:
                name = ud.name(u)
                numValidCodePoint = numValidCodePoint + 1
            except ValueError:
                pass
        
        if count >= numValidCodePoint: 
            # If the numbers match, we don't need to update the db.
            # If the number of entries in the db is larger, we might have a db from a future version.
            #   We don't want to loose the frequency entries, so we don't want to re-create the db automatically.
            return
        
        for i in range(0, MAX_UNICODE_CODE):
            u = chr(i)
            try:
                name = ud.name(u)
                conn.execute('insert into udata(id, name, freq) values (?, ?, ?) ON CONFLICT (id) DO NOTHING;',
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
    print(udb.get_count('infinity'))
    for row in udb.get_chars('infinity', 0, 10):
        print(row)
    print(udb.get_count('i'))
    udb.increment_frequency(row)
