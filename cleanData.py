import pandas as pd

def cleanData(dataFile, value, outputPath = "cleanData.csv"):
    data = pd.read_csv(dataFile, header=0, index_col= 0)

    cleanData = data[
                    (data[value] != 0)   # Loại bỏ các giá trị = 0 (kiểu số)
                    ]
    
    cleanData = cleanData.map(lambda x: x.strip() if isinstance(x, str) else x) # Loại bỏ khoảng trắng dư thừa

    cleanData.to_csv(outputPath)

def ChangeType(dataFile, value, type, outputPath = "cleanData.csv"):
    data = pd.read_csv(dataFile, header=0, index_col= 0)
    data[value] = data[value].astype(type)
    data.to_csv(outputPath)

cleanData("data.csv", "Global_Sales")
cleanData("cleanData.csv", "Year", "cleanData1.csv")
ChangeType("cleanData.csv", "Year", int)
