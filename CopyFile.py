import shutil
from tkinter import messagebox, filedialog
class CopyFile:
    def CopyPPI(carNum:str, INSPP:str, CopyPath:str):
        Destination = rf"M:\QA 11122019\06 Scanned PPI-PQCF document STORAGE\Production cars\{carNum}"
        shutil.copy(CopyPath, Destination)
        print("From Copy File CopyPPI function PPI Copied")

    def CopyRRN(carNum:str, INSPP:str, CopyPath:str):
        Destination = rf"M:\QA 11122019\04 RRN(Repair Rework Notice)\Production\{carNum}"
        shutil.copy(CopyPath, Destination)
        print("From Copy File CopyPPI function RRN Copied")

    def CopyEXR(carNum:str, EXRNum:str, CopyPath:str):
        Destination = r"M:\QA 11122019\05 EMERGENCY-EXCEPTION STORAGE\Exception release storage"
        shutil.copy(CopyPath, Destination)
        print("From Copy File CopyPPI function EXR Copied")

    def CopyER(carNum:str, ERNum:str, CopyPath:str):
        Destination = r"M:\QA 11122019\05 EMERGENCY-EXCEPTION STORAGE\Emergency release storage\Production car"
        shutil.copy(CopyPath, Destination)
        print("From Copy File CopyPPI function EXR Copied")



# def CopyPPI(carNum:str, Sinsp: str):
#     PPIPath = filedialog.askopenfilename(title="PPI File Input", initialdir="/", filetypes=[("PPI", ".pdf")])
#     print(f"path of PPI is {PPIPath}")
#
#     Docment = PPIPath.split("/")[-1].split(".")[0]
#     Suffex = PPIPath.split("/")[-1].split(".")[1]
#     bogienum = Docment.split(" ")[0].upper()
#     insp = Docment.split(" ")[1].upper()
#
#     print(PPIPath, bogienum, insp)
#     if carNum.upper() != bogienum:
#         messagebox.showerror(message=f"Bogie Number not the same you have: {bogienum}, assigning for {carNum}")
#         exit()
#     if Sinsp.upper() != insp:
#         messagebox.showerror(message=f"Bogie Inspection not the same you have: {insp}, but assigning for {Sinsp}")
#         exit()
#
#     PPI_CopyPath = rf"M:\\QA 11122019\\21 Bogie Document\PPI\\{Docment}.{Suffex}"
#
#
#     '''store in database update PPI'''
#     UpdateDatabase.PPI.PPI(carNum.upper(), insp.upper())
#
#     '''copy folder'''
#     shutil.copy(PPIPath, PPI_CopyPath)
#     # shutil.copy(PPIEXRPath, PPI_EXR_CopyPath2)
#     #
#     messagebox.showinfo(message=f"PPI for car {carNum} {Sinsp} uploaded")
