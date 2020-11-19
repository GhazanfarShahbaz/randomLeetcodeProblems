difficulties = ("Easy", "Medium", "Hard")
tags = {'Arrays' ,'Hash_Table' ,'Linked_Lists' ,'Math' ,'Two_Pointers' ,'String' ,'Binary_Search' ,'Divide_and_Conquer' ,'Dynamic_Programming' ,'Backtracking' ,'Stack' ,'Heap' ,'Greedy' ,'Sort' ,'Bit_Manipulation' ,'Tree' ,'Depth_First_Search' ,'Breadth_First_Search' ,'Union_Find' ,'Graph' ,'Design' ,'Topological_Sort' ,'Trie' ,'Binary_Indexed_Tree' ,'Segment_Tree' ,'Binary_Search_Tree' ,'Recursion' ,'Brain_Teaser' ,'Memoization' ,'Queue' ,'Minimax' ,'Reservoir_Sampling' ,'Ordered_Map' ,'Geometry' ,'Random' ,'Rejection_Sampling' ,'Sliding_Window' ,'Line_Sweep' ,'Rolling_Hash' ,'Suffix_Array'}


def allowedDifficulties(userPickedDifficulty: str) -> bool:
    return userPickedDifficulty.title() in difficulties


def allowedTags(userPickedTag: str) -> bool:
    return userPickedTag.title() in tags
