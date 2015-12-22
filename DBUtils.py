

DBFILE = "stock_fund.db"

def get_codes(dbconn):
    cursor = dbconn.cursor()
    cursor.execute("SELECT code FROM code")

    return [row[0] for row in cursor.fetchall()]