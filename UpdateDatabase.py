import sqlite3
import tkinter.messagebox
from tkinter import messagebox
from datetime import date
#
path = "./ChicagoCTA-7000.db"
today = date.today()
today = today.strftime("%Y%m%d")
class UploadDB:

    '''exr string or boolean: False '''
    def ppi(carNum:str, INSPP:str, ppiWithExr):
        PPIwithINSP = carNum.upper() + INSPP.upper()


        con = sqlite3.connect(path)
        cur = con.cursor()


        cur.execute(f"""Select Car_INSP_Point, Status, EXR, ER, INSP_End_Date from CarInsp where Car_INSP_Point = '{PPIwithINSP}'""")
        status = cur.fetchone()

        '''when PPI is the first document for this PPIwithINSP'''
        if status is None:
            if isinstance(ppiWithExr, str):
                cur.execute(f"""INSERT INTO CarInsp (Car_INSP_Point, INSP_Start_Date, INSP_END_Date, PPI , Status)
                Values(?, ?, ?,?,?)""", (PPIwithINSP, today, today, ppiWithExr, "Completed"))


            elif ppiWithExr is False:
                cur.execute(f"""INSERT INTO CarInsp (Car_INSP_Point, INSP_Start_Date, INSP_END_Date, PPI , Status) 
                Values (?,?,?,?,?)""", (PPIwithINSP, today, today, PPIwithINSP, "Completed"))

        elif status[1].upper() == "COMPLETED":
            messagebox.showinfo(message=f"PPI for {carNum} {INSPP} has already finished at {status[4]}")
            return "AlreadyClosed"
        elif status[1].upper() == "PENDING":
            cur.execute(f"""Update CarInsp set INSP_End_Date = ?, PPI = ?, Status = ?""", (today, PPIwithINSP, "Completed"))
        elif status[1].upper() == "STOP":
            exr = []
            er = []

            '''check for more than one exr'''
            try:
                for i in status[2].split(","):
                    exr.append(i)
            except AttributeError:
                print("Only one exr available")
            else:
                print("Exrs successfully extracted")

            """check for more than one er"""
            try:
                for i in status[3].split(","):
                    er.append(i)
            except AttributeError:
                print("Only one exr available")
            else:
                print("Exrs successfully extracted")

            exrStatus, erStatus, nonComplete = [], [], []
            for i in exr:
                cur.execute(f"""Select EXR_Status from EXR where EXR_NUM = '{i}'""")
                exrCheck = cur.fetchone()
                if exrCheck.upper() == "OPEN":
                    nonComplete.append(i)
                exrStatus.append(exrCheck)

            for i in er:
                cur.execute(f"""Select ER_Status from ER where ER_Num = '{i}'""")
                erCheck = cur.fetchone()
                if erCheck.upper() == "OPEN":
                    nonComplete.append(i)
                erStatus.append(erCheck)

            # return(exrStatus, erStatus, nonComplete)
            if nonComplete != []:
                message = f"Please close the following files: {', '.join(nonComplete)}"
                tkinter.messagebox.showerror("Error", message)
                return "ExrErFalse"
        con.commit()
        con.close()

    def ppiWithExr_OpenExr_INSP(carNum:str, INSPP:str, EXR:str):
        con = sqlite3.connect(path)
        cur = con.cursor()
        PPIwithINSP = carNum + INSPP
        print(f"PPIwith INSP is {PPIwithINSP}")
        cur.execute(f"""Select EXR from CarInsp where Car_INSP_Point = '{PPIwithINSP}'""")
        EXRCheck = cur.fetchone()
        if EXRCheck is None:
            cur.execute(f"""INSERT INTO CarInsp (Car_INSP_Point, EXR ,  Status) Values(?,?,?)""", (PPIwithINSP, EXR, "STOP"))
            con.commit()
        else:
            cur.execute(f"""Update CarInsp set EXR = ? WHERE Car_INSP_Point = ?""", (EXRCheck[0]+f",{EXR}",PPIwithINSP))
            # cur.execute(f"""Update INTO CarInsp (Car_INSP_Point, EXR , Status)
            #             Values(?,?,?)""", (PPIwithINSP, EXRCheck[0]+f",{EXR}", "STOP"))
            con.commit()
        con.close()


    '''update new EXR when PPI with EXR'''
    def ppiWithExr_OpenExr_EXR(carNum:str, INSPP:str, EndINSP:str, exr:str):
        con = sqlite3.connect(path)
        cur = con.cursor()

        '''Update EXR DB and Open New PPI with EndINSP point'''
        cur.execute("""Select id
                                        From EXR
                                        Order by id DESC
                                        Limit 1""")



        orinum = cur.fetchone()
        if orinum is None:
            num = 0
        else:
            num = orinum + 1
        # num = 0
        print(f"current EXR id number for Bogie is {num}")

        try:
            cur.execute("""INSERT INTO EXR (id, EXR_Num, StartP, EndP, EXR_Start_Date, EXR_Status) Values(?,?,?,?,?,?)""",
                        (num, exr, INSPP, EndINSP, today, "OPEN"))

            print(f"EXR uploaded for {exr}")
        except Exception as e:
            e = str(e)
            if "UNIQUE" in e:
                messagebox.showerror(title="EXR Database Update Failure", message=f"Can't update new EXR {exr} because this EXR number has already existed")
            else:
                messagebox.showerror(title="EXR Database Update Failure", message=f"Can't update new EXR {exr} due to {e}")
            return False
        con.commit()
        con.close()

    """extend exr in exr db"""
    def EXRWithExtension(carNum:str,  EndINSP:str, exr:str):
        con = sqlite3.connect(path)
        cur = con.cursor()
        cur.execute(f"""SELECT EXR_Num, Status from EXR where EXR_NUm = {exr}""")
        exrstatus = cur.fetchone()
        if exrstatus is None:
            tkinter.messagebox.showerror(message=f"{exr} is not opened yet")
            return "NoneExist"
        elif exrstatus[1].upper() == "CLOSED":
            tkinter.messagebox.showerror(message=f"{exr} is already closed")
            return "Closed"
        elif exrstatus[1].upper() == "OPEN":
            cur.execute(f"""UPDATE EXR set EndP = ? where EXR_Num = {exr}""", EndINSP)
            con.commit()
        '''session for change exr end point in CarINSP'''

    '''close exr er when updated corresponding documents'''
    def CloseErExr(carNum:str, INSPP:str, ErEXRNum:str):
        '''valiue for check the current status of CarINSP Point'''
        erCheck, exrCheck, rrnCheck = False, False, False
        ErEXRNum = ErEXRNum.upper()
        con = sqlite3.connect(path)
        cur = con.cursor()
        ''' change status in exr and er db '''
        if ErEXRNum.startswith("ER"):
            cur.execute(f"""Select ER_Status from ER where ER_Num = '{ErEXRNum}''""")
            check = cur.fetchone()
            if check[0] == "CLOSED":
                messagebox.showerror(title="ER Closed", message=f"""ER {ErEXRNum} is already been closed""")
                return "AlreadyClosed"
            cur.execute(f"""Update ER set ER_End_Date = ?, ER_Status = ? where ER_Num = ?""", (today, "CLOSED", ErEXRNum))
            con.commit()
        elif ErEXRNum.startswith("EXR"):
            cur.execute(f"""Select EXR_Status from EXR where EXR_Num = '{ErEXRNum}'""")
            check = cur.fetchone()
            if check[0] == "CLOSED":
                messagebox.showerror(title="EXR Closed", message=f"""EXR {ErEXRNum} is already been closed""")
                return "AlreadyClosed"
            cur.execute(f"""Update EXR set EXR_End_Date = ?, EXR_Status = ? where EXR_Num = ?""", (today, "CLOSED", ErEXRNum))
            con.commit()
        else:
            messagebox.showerror(message="Unidentified error in exr and er session")
            return False
        '''change status in carINSP db'''

        EINSP = carNum+INSPP
        exr, er, rrn = [], [], []
        cur.execute(f"""Select EXR, ER, RRN, Status from CarInsp where Car_INSP_Point = '{EINSP}'""")
        carStatus = cur.fetchone()
        if carStatus is None:
            messagebox.showerror(message=f"There is no data for {EINSP}")
            return "NoEndPData"
        else:
            if carStatus[3].upper() == "STOP":
                print("track")

                '''check if there are exr and their status'''
                if carStatus[0] is None:
                    print(f"no exr in {EINSP}")
                    exrCheck = False
                else:
                    try:
                        exr = carStatus[0].split(",")
                    except AttributeError:
                        exr = exr.append(carStatus[0])
                        print("Only one exr available")
                    else:
                        print("EXRs successfully extracted")

                    for i in exr:
                        cur.execute(f"""Select EXR_Status from EXR where EXR_Num = '{i}'""")
                        if cur.fetchone() == "OPEN":
                            exrCheck = True
                        else:
                            continue


                '''check if there are er and their status'''
                if carStatus[1] is None:
                    print(f"no er in {EINSP}")
                else:
                    try:
                        er = carStatus[1].split(",")
                    except AttributeError:
                        er = er.append(carStatus[1])
                        print("Only one er available")
                    else:
                        print("ERs successfully extracted")

                    for i in er:
                        cur.execute(f"""Select ER_Status from ER where ER_Num = {i}""")
                        if cur.fetchone() == "OPEN":
                            erCheck = True
                        else:
                            continue

                '''check if there are rrn and their status'''
                if carStatus[2] is None:
                   print(f"no rrn in {EINSP}")
                else:
                    try:
                        rrn = carStatus[2].split(",")
                    except AttributeError:
                        rrn = rrn.append(carStatus[2])
                        print("Only one exr available")
                    else:
                        print("EXRs successfully extracted")
                    for i in rrn:
                        cur.execute(f"""Select """)
                #This portion is saved for rrn change since rrn db is not created yet


                if exrCheck or erCheck:
                    cur.execute(f"""Update CarInsp set Status = ? WHERE Car_INSP_Point = {EINSP}""", ("STOP",))
                elif rrnCheck:
                    cur.execute(f"""Update CarInsp set Status = ? WHERE Car_INSP_Point = {EINSP}""", ("PENDING",))
                elif not exrCheck and not erCheck and not rrnCheck:
                    cur.execute(f"""Update CarInsp set Status = ? WHERE Car_INSP_Point = '{EINSP}'""", ("WORKED",))

                con.commit()
                #if one is them is True, then the inspection point can't be completed. abd we can ajust the inspection status
                # based on the exr, er, rrn checks.
                '''big session based on above three checks'''


            elif carStatus[3].upper() == "PENDING":
                messagebox.showerror(message=f"Trying to close {ErEXRNum} but the current status is Pending")
                return "FalsePending"

            elif carStatus[3].upper() == "COMPLETED":
                messagebox.showerror(message=f"Trying to close {ErEXRNum} but the current Car Inspection point is already Closed")
                return "FalseComplete"


    def OpenEr(carNum:str, INSPP:str, er:str):
        con = sqlite3.connect(path)
        cur = con.cursor()
        EINSP = carNum+INSPP
        '''grab the current number of er'''
        cur.execute("""Select id
                                                From ER
                                                Order by id DESC
                                                Limit 1""")

        num = cur.fetchone()[0] + 1
        print(f"current ER id number for Car is {num}")

        try:
            cur.execute("""INSERT INTO ER (id, ER_Num, Car_End_Insp, ER_Start_Date, ER_Status) Values(?,?,?,?,?)""",
                        (num, er, EINSP, today, "OPEN"))

            print(f"EXR uploaded for {er}")
        except Exception as e:
            e = str(e)
            if "UNIQUE" in e:
                messagebox.showerror(title="ER Database Update Failure",
                                     message=f"Can't update new ER {er} because this EXR number has already existed")
            else:
                messagebox.showerror(title="ER Database Update Failure",
                                     message=f"Can't update new EXR {er} due to {e}")
            return False
        con.commit()
        con.close()



    '''Upload RRN Session missing upload into RRN_DB '''
    ''' Have info for updating CarInsp while uploading RRN'''
    def RRN(carNum:str, INSPP:str, RRN:str, RRNInfoList:list):
        con = sqlite3.connect(path)
        cur = con.cursor()
        INSP = carNum + INSPP

        '''Update CarInsp status'''
        cur.execute(f"""Select Car_INSP_Point, Status, INSP_END_Date, RRN from CarInsp where Car_INSP_Point = {INSP})""")
        rrnStatus = cur.fetchone()

        if rrnStatus is None:
            cur.execute(f"""INSERT INTO CarInsp (Car_INSP_Point, INSP_Start_Date, RRN , Status)""",
                        (INSP, today, RRN, "Pending"))
        elif rrnStatus[1].upper() == "COMPLETED":
            messagebox.showinfo(message=f"{carNum} {INSPP} is finished at {rrnStatus[2]}, New RRN Updated")
            cur.execute(f"""UPDATE CarInsp set RRN = ? where Car_INSP_Point = {INSP}""", (rrnStatus[3] + f",{RRN}"))
            return "COMPLETED"

        elif rrnStatus[1].upper() == "Pending" or rrnStatus[1].upper() == "STOP":
            rrns = []
            try:
                rrns = rrnStatus[3].split(",")
            except AttributeError:
                print("Only one rrn available")
            else:
                print("RRNs successfully extracted")
            if RRN in rrns:
                tkinter.messagebox.showerror(message=f"{RRN} has already been allocated")

                '''stop the MainFunction loop'''
                return "DuplicateRRN"
            else:
                cur.execute(f"""UPDATE CarInsp set RRN = ? where Car_INSP_Point = {INSP}""", (rrnStatus[3] + f",{RRN}"))
        con.commit()
        con.close()

