from time import time
import traceback
import xlwings as xw
import pandas as pd
import time
import xlsxwriter
import pythoncom

# import DBConnection as DBCon


class LiveExcel :
    def __init__(self,filename='LiveExcel'):
        self.wb = xlsxwriter.Workbook(str(filename)+'.xlsx')
        xl=win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
        # self.sht2 = self.wb.add_worksheet('Data')
        # self.tb = self.wb.add_worksheet('Tradebook')
        # self.wb.close()
        self.wb = xw.Book(str(filename)+'.xlsx')
        self.sht2 = self.wb.sheets['Data']
        

    def OpenExcel(self,data):
        try:
            self.Live_Data = dict()
            for i in data:
                print(i)
                # print("Live_Data===",self.Live_Data)
                self.Live_Data[i["symbol"]] = {
                    "BID": float(i["bid"]),
                    "BIDQTY": float(i["bidqty"]),
                    "ASK": float(i["ask"]),
                    "ASKQTY": float(i["askqty"]),  
                    "PREVBIDQTY":float(i['prevbidqty']),
                    "PREVASKQTY":float(i['prevaskqty']),                 
                    }

                df2=pd.DataFrame(self.Live_Data).T
                # print(df2)
                self.sht2.range('A1').value = df2
                
        except Exception as e:            
            print("liveExcel error==",traceback.format_exc())


