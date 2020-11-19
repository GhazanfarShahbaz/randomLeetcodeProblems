import pandas as pd 

file = pd.read_csv("tagData.csv")

tagDataExpanded = []

for x, y in file.iterrows():
    currentData = {"number": f"{y[0]}", 'Arrays': 'No', 'Hash Table': 'No', 'Linked Lists': 'No', 'Math': 'No', 'Two Pointers': 'No', 'String': 'No', 'Binary Search': 'No', 'Divide and Conquer': 'No', 'Dynamic Programming': 'No', 'Backtracking': 'No', 'Stack': 'No', 'Heap': 'No', 'Greedy': 'No', 'Sort': 'No', 'Bit Manipulation': 'No', 'Tree': 'No', 'Depth First Search': 'No', 'Breadth First Search': 'No', 'Union Find': 'No', 'Graph': 'No', 'Design': 'No', 'Topological Sort': 'No', 'Trie': 'No', 'Binary Indexed Tree': 'No', 'Segment Tree': 'No', 'Binary Search Tree': 'No', 'Recursion': 'No', 'Brain Teaser': 'No', 'Memoization': 'No', 'Queue': 'No', 'Minimax': 'No', 'Reservoir Sampling': 'No', 'Ordered Map': 'No', 'Geometry': 'No', 'Random': 'No', 'Rejection Sampling': 'No', 'Sliding Window': 'No', 'Line Sweep': 'No', 'Rolling Hash': 'No', 'Suffix Array': 'No'}
    for z in range(1,5):
        if pd.isna(y[z]):
            break
        currentData[y[z]] = 'Yes'
    tagDataExpanded.append(currentData)


df = pd.DataFrame.from_dict(tagDataExpanded)
df.to_csv("tagDataExpanded.csv")