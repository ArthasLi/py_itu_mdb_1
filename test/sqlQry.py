import pypyodbc
def sqlQry(qry,mdb_idx):
    mdb_str = []
    mdb_str.append('Driver={Microsoft Access Driver (*.mdb)};DBQ=G:/ITU_mdb/srs2888_part2of2.mdb')
    mdb_str.append('Driver={Microsoft Access Driver (*.mdb)};DBQ=G:/ITU_mdb/30B_2891.mdb')
    mdb_str.append('Driver={Microsoft Access Driver (*.mdb)};DBQ=G:/ITU_mdb/SPS_ALL_IFIC2891.mdb')
    conn = pypyodbc.win_connect_mdb(mdb_str[mdb_idx])
    cur = conn.cursor()
    cur.execute(qry)
 #   for row in cur.fetchall():
  #      print(row)
    data = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return data

