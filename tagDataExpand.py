import pandas as pd 

file = pd.read_csv("tagData.csv")

tagDataExpanded = []

for x, y in file.iterrows():
    currentData = {"number": f"{y[0]}",'Arrays' : False,'Hash Table' : False,'Linked Lists' : False,'Math' : False,'Two Pointers' : False,'String' : False,'Binary Search' : False,'Divide and Conquer' : False,'Dynamic Programming' : False,'Backtracking' : False,'Stack' : False,'Heap' : False,'Greedy' : False,'Sort' : False,'Bit Manipulation' : False,'Tree' : False,'Depth First Search' : False,'Breadth First Search' : False,'Union Find' : False,'Graph' : False,'Design' : False,'Topological Sort' : False,'Trie' : False,'Binary Indexed Tree' : False,'Segment Tree' : False,'Binary Search Tree' : False,'Recursion' : False,'Brain Teaser' : False,'Memoization' : False,'Queue' : False,'Minimax' : False,'Reservoir Sampling' : False,'Ordered Map' : False,'Geometry' : False,'Random' : False,'Rejection Sampling' : False,'Sliding Window' : False,'Line Sweep' : False,'Rolling Hash' : False,'Suffix Array' : False}
    for z in range(1,5):
        if pd.isna(y[z]):
            break
        currentData[y[z]] = True
    tagDataExpanded.append(currentData)


df = pd.DataFrame.from_dict(tagDataExpanded)
df.to_csv("tagDataExpanded.csv")
# currentData = {"number": "NA", 'Arrays': 'No', 'Hash Table': 'No', 'Linked Lists': 'No', 'Math': 'No', 'Two Pointers': 'No', 'String': 'No', 'Binary Search': 'No', 'Divide and Conquer': 'No', 'Dynamic Programming': 'No', 'Backtracking': 'No', 'Stack': 'No', 'Heap': 'No', 'Greedy': 'No', 'Sort': 'No', 'Bit Manipulation': 'No', 'Tree': 'No', 'Depth First Search': 'No', 'Breadth First Search': 'No', 'Union Find': 'No', 'Graph': 'No', 'Design': 'No', 'Topological Sort': 'No', 'Trie': 'No', 'Binary Indexed Tree': 'No', 'Segment Tree': 'No', 'Binary Search Tree': 'No', 'Recursion': 'No', 'Brain Teaser': 'No', 'Memoization': 'No', 'Queue': 'No', 'Minimax': 'No', 'Reservoir Sampling': 'No', 'Ordered Map': 'No', 'Geometry': 'No', 'Random': 'No', 'Rejection Sampling': 'No', 'Sliding Window': 'No', 'Line Sweep': 'No', 'Rolling Hash': 'No', 'Suffix Array': 'No'}

# for x in currentData.keys():
#     t = ""
#     for y in x:
#         t += y if y != " " else "_"
#     print(t, ",", end="")

# for x in currentData.keys():
#     print(f"\'{x}\'", ":", "False,", end="")