import sqlite3
from datetime import date
import os, shutil

con = sqlite3.connect('ChicagoCTA-7000.db')
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
# UpdateDatabase.UploadDB.ppi("Test", "INI", False)

# UpdateDatabase.UploadDB.ppi("Test", "PFP", "Test PFP EXR COT EXR20111111JK-1")

# UpdateDatabase.UploadDB.ppiWithExr_OpenExr_INSP("Test", "COT", "EXR20111111JK-1")

# a = UpdateDatabase.UploadDB.ppiWithExr_OpenExr_EXR("Test", "PFP", "PSI", "EXR20111111JK-1")
# print(a)


# UpdateDatabase.UploadDB.CloseErExr("Test", "COT", "EXR20111111JK-1")
# cur.execute(f"""Update EXR set EXR_Status = "OPEN" where id = '0' """)

cur.execute(f"""UPDATE CarInsp set RRN = ?, EXR = ?, ER = ? WHERE Car_INSP_Point = 'TestINI'""", ("rrn-1,rrn-2,rrn-3", "EXR-1,Exr-2,Exr-3", "er-2"))
cur.execute(f"""Select * from CarInsp""")
ls = cur.fetchall()
for i in ls:
    print(i)

con.commit()
#
# cur.execute(f"""Select * from EXR""")
# ls = cur.fetchall()
# for i in ls:
#     print(i)
# a = UpdateDatabase.UploadDB.CloseErExr("Test", "COT", "EXR20111111JK-1")
# print(a)