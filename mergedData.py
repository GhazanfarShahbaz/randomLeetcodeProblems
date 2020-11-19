import pandas as pd 

leetcodeData =  pd.read_csv("leetcodeData.csv")
tagData = pd.read_csv("tagDataExpanded.csv")

newData = leetcodeData.merge(tagData, how = 'inner', on = "number")

newData.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y'], inplace = True, axis = 1)
newData.to_csv("mergedLeetcodeData.csv")