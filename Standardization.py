import pandas as pd

class Standardization:
    def __init__(self, dataFile) -> None:
        self.dataFile = dataFile

    def sortByValues(self, key, reversed = False):
        data = pd.read_csv(self.dataFile)
        try: 
            data_sorted = data.sort_values(by=key, ascending=not reversed)
            data_sorted.to_csv(self.dataFile, index=False)
            return self.dataFile
        except KeyError:
            raise KeyError("Error! Maybe key not exactly!\n")

    def listGameByValues(self, key, value) -> list:
        data = pd.read_csv(self.dataFile)
        try: 
            listGame = data[data[key] == value]['Name'].to_list()
            listGame = list(set(listGame))
            return listGame
        except KeyError:
            raise KeyError("Error! Maybe key not exactly!\n")
