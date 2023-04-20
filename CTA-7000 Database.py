import sqlite3
import os
from datetime import datetime

con = sqlite3.connect('ChicagoCTA-7000.db')
cur = con.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cur.fetchall())

cur.execute("""Create Table if not exists Main(
            carNum text PRIMARY KEY,
            Car_Start_Date int,
            Car_End_Date int,
            Status text not null
            )""")

cur.execute("""Create Table if not exists CarInsp(
            Car_INSP_Point text PRIMARY KEY,
            INSP_Start_Date int,
            INSP_End_Date int,
            EXR text,
            ER text,
            RRN text,
            PPI text,
            TN text,
            NNP text,
            Status text not null
            )""")

cur.execute("""Create Table if not exists EXR(
            id integer not null,
            EXR_Num PRIMARY KEY,
            EXR_Start_Date int,
            EXR_End_Date int,
            StartP text not null,
            EndP text not null,
            EXR_Status text not null
            )""")

cur.execute("""Create Table if not exists ER(
            id integer not null,
            ER_Num PRIMARY KEY,
            ER_Start_Date int,
            ER_End_Date int,
            EndP text not null,
            ER_Status text not null
            )""")



con.commit()
con.close()

