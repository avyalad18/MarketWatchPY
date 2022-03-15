import time
from BinanceFeed import BinanceFeed

class Main(BinanceFeed) :

    def __init__(self):
        super().__init__()
        self.Symbols = ['BTCUSDT','BTCUSD_PERP']
        self.__getInput()

    def __getSymbols(self):
        symbol = ''
        for i in range(len(self.Symbols)) : 
            symbol = symbol + f'\n\t\t | {i+1}. ' + self.Symbols[i]
            # print(symbol)
        return symbol

    def __getInput(self):    
        try :
            value  = int(input(f""" 
                ===================|| Binance ||==================\n
                |   1. Symbols (1) 
                |   2. Live Feed (2)
                |   0. Exit(0)
                ===================================================
            """))
        except Exception as e :
            print("symbol"," please Select appropriate value !!" )    
        
        if value==1:
            try :
                value = int(input(f"""  
                =================|| Symbols ||======================\n
                    {
                        self.__getSymbols()
                    }
                 | 8.Back
                 | 0.Exit
                ===================================================
                """))
                if value==8 :
                    self.__getInput()
                if value==0:
                    pass
            except Exception as e:
                print(" please Select appropriate value !!" )
        
        if value==2:
            try :
                self.startThreads()
                time.sleep(3)
                self.stopThreads()
                print(" open LiveExcel.xlsx to See live Feed! ")
                pass
            except Exception as e:
                print(" please Select appropriate value !!" )

        elif value==0:
            pass
        else:
            print(" please Select Appropriate option!")
            self.__getInput()


Main()        