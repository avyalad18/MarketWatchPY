import json
from re import S
import time
from websocket import create_connection
import threading 
import gc
import datetime
from LiveExcel import LiveExcel


class BinanceFeed(LiveExcel):
     
    def __init__(self): 
        super().__init__()
        self.DStreamSock = 'open'
        self.SStreamSock = 'open'
        self.FStreamSock = 'open'
        self.RefreshSym = 'open'
        self.DSYM = 'btcusd_perp@bookTicker'
        self.FSYM = 'btcusdt@bookTicker'
        self.SSYM = 'btcusdt@bookTicker' 
        self._LTP_DATA = [{'symbol':'BTCUSDT','bid':0,'bidqty':0,'ask':0,'askqty':0,'prevbidqty':0,'prevaskqty':0},
                    {'symbol':'BTCUSD_PERP','bid':0,'bidqty':0,'ask':0,'askqty':0,'prevbidqty':0,'prevaskqty':0}]
        # print(self.__OrderObjdict) 
        # self.startThreads()    
        # time.sleep(10)
        # self.stopThreads()       

    #RECIEVING DATA FROM BINANCE DSTRREAM===== (DELIVERABLES)
    def DStreamSocket(self): 
        try:       
            dws = create_connection('wss://dstream.binance.com/stream?streams='+self.DSYM)                   
            while (self.DStreamSock=='open'):
                response = dws.recv() 
                DstreamData = json.loads(response) 
                # print(DstreamData)
                self.updateSYMBOLS(DstreamData['data'])               
                     
            else:
                dws.close()   
        except Exception as e:
            print("[Error] in (self,DStreamSocket) msg: ",str(e))   
            time.sleep(0.3) 
            self.DStreamSocket()

    # def unix_to_dt(self,dt):
    #     if len(dt)>10:
    #         dt = dt[:-3]+'.'+dt[-3:]
    #     ts = float(str(dt))
    #     dt = datetime.utcfromtimestamp(ts)
    #     return (dt)

    #RECIEVING DATA FROM BINANCE FSTRREAM======(FUTURE)  
    def FStreamSocket(self):  
        try:
            fws =  create_connection('wss://fstream.binance.com/stream?streams='+self.FSYM)                 
            while (self.FStreamSock=='open'):
                response = fws.recv()     
                FstreamData = json.loads(response) 
                # print(FstreamData['data'])
                self.updateSYMBOLS(FstreamData['data'])              
             
            else:
                fws.close()
        except Exception as e:
            print("[Error] in (SocketData,FStreamSocket) msg: ",str(e))   
            time.sleep(0.3)           
            self.FStreamSocket()

    #RECIEVING DATA FROM BINANCE SSTRREAM ====(SPOT)
    def SStreamSocket(self):
        try : 
            sws = create_connection('wss://stream.binance.com:9443/stream?streams='+self.SSYM)         
            while (self.SStreamSock=='open'):
                response = sws.recv()  
                SstreamData = json.loads(response)                 
                self.updateSYMBOLS(SstreamData['data']) 
            else:
                sws.close() 

        except Exception as e:
            print("[Error] in (SocketData,SStreamSocket) msg: ",str(e))   
            time.sleep(0.3)           
            self.SStreamSocket()
            

# ============ Setter to close/open socket ======= #   

    def setSStreamSock(self,val):
        print("CALLED++++++")
        self.SStreamSock = val

    def setDStreamSocket(self,value):
        self.DStreamSock = value 

    def setFStreamSocket(self,value):
        self.FStreamSock = value    

    def setRefreshSym(self,value):
        self.RefreshSym = value
   
# ======================================================================================   

    def startThreads(self):
        global spotThread,futureThread,delThread,refreshSymbols

        
        spotThread = threading.Thread(target=self.SStreamSocket)
        futureThread = threading.Thread(target=self.FStreamSocket)
        delThread = threading.Thread(target=self.DStreamSocket)
        refreshSymbols = threading.Thread(target=self.updateSocket) 

        self.setSStreamSock('open') 
        self.setDStreamSocket('open')
        self.setFStreamSocket('open')
        self.setRefreshSym('open')     
      
        try :  
            spotThread.start()
            futureThread.start()
            delThread.start()   
            # refreshSymbols.start()
                   
            print('CONNECTION STARTED : =================>')

        except Exception as e :           
            print("[Error] in (SocketData,startThreads) msg: ",str(e))   
        print('AllThreadStarted')  

    
    def stopThreads(self):      
        try:
            global spotThread,futureThread,delThread,refreshSymbols  
            self.setSStreamSock('close') 
            self.setDStreamSocket('close')
            self.setFStreamSocket('close')
            self.setRefreshSym('close') 
          
            if(self.SStreamSock=='close'):
                try :
                    spotThread._stop()
                    spotThread._delete()
                    print('SSTREAM socket closed!!!')
                except Exception as e :
                    print(e) 

            if(self.DStreamSock=='close'):
                try:
                    delThread._stop()
                    delThread._delete()
                    print('DSTREAM socket closed!!!')
                except Exception as e:
                    print(e)    
            if(self.FStreamSock=='close'):
                try :
                    futureThread._stop()
                    futureThread._delete() 
                    print('FSTREAM socket closed!!!')
                except Exception as e:
                    print(e)    
            try:    
                refreshSymbols._stop()  
                refreshSymbols._delete() 
            except Exception as e:
                pass
                # print(e)   
           
            gc.collect()
        except Exception as e :
            print("[Error] in (SocketData,stopThreads) msg: ",str(e))   



    # ===================>>>>>>>|| Updating Symbols ||<<<<<<<=====================
    def updateSocket(self):
        try:
            while (self.RefreshSym=='open'):
                        
                for i in self._LTP_DATA:                              
                    if i['InstrumentType']=='SPOT':                       
                        self.addSpotSymbol(i)
                    if i['InstrumentType']=='FUTURE':                  
                        self.addFutureSymbol(i)
                    if i['InstrumentType']=='COIN':
                        self.addFutureCoinSymbol(i)        
                time.sleep(1)
                # print('TOTAL SYMBOL PROCESSES : ',len(self.__Symbol_Process))
        except Exception as e :
            print("[Error] in (SocketData,updateSocket) msg: ",str(e))   

    # Add symbol for SPOT
    def addSpotSymbol(self,symbol):     
        if(self.SSYM.find(symbol['Symbol'].lower()+'@bookTicker')==-1):
            if len(self.SSYM)==0 :
                self.SSYM = symbol['Symbol'].lower()+'@bookTicker'
            else :
                self.SSYM = self.SSYM + '/'+symbol['Symbol'].lower()+'@bookTicker'
            self.SSYMUpdate = True
            print('New Spot Symbol ADDED :'+self.SSYM)     
    
    # ADD symbol for Future
    def addFutureSymbol(self,symbol):
        if(self.FSYM.find(symbol['Symbol'].lower()+'@bookTicker')==-1):
            if len(self.FSYM)==0:                
                self.FSYM = symbol['Symbol'].lower()+'@bookTicker'
            else :
                self.FSYM = self.FSYM + '/'+symbol['Symbol'].lower()+'@bookTicker'                
            self.FSYMUpdate = True
            print('FUTURE SYMBOL UPDATED : ',self.FSYM)
    
    #ADD Symbol for FutureCoin (Deliverables)   
    def addFutureCoinSymbol(self,symbol):
        if(self.DSYM.find(symbol['Symbol'].lower()+'@bookTicker')==-1):
            if len(self.DSYM)==0:
                self.DSYM = symbol['Symbol'].lower()+'@bookTicker'
            else :
                self.DSYM = self.DSYM + '/'+symbol['Symbol'].lower()+'@bookTicker'                
            self.DSYMUpdate = True
            print('FUTURE_COIN SYMBOL UPDATED : ',self.DSYM)  

    def updateSYMBOLS(self,sockdata):      
        try:
            if(len(sockdata)>0):
                for strg in self._LTP_DATA :                   
                    if(strg['symbol']==sockdata["s"]):                       
                        strg['bid'] = float(sockdata["b"])
                        strg['ask'] = float(sockdata["a"])
                        if(float(sockdata["B"])!= float(strg["prevbidqty"])):
                            strg['bidqty'] = sockdata['B'] 
                            strg["prevbidqty"] = sockdata['B']                       
                        if(float(sockdata["A"])!= float(strg["prevaskqty"])):
                            strg['askqty'] = sockdata["A"]
                            strg["prevaskqty"] = sockdata["A"]
                self.OpenExcel(self._LTP_DATA)        
        except Exception as e :
            print("[Error] in (SocketData,updateSYMBOLS) msg: ",str(e))   

