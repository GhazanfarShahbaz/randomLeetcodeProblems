difficulties = ("Easy", "Medium", "Hard")
tags = {'arrays', 'backtracking', 'binary_indexed_tree', 'binary_search', 'binary_search_tree', 'bit_manipulation', 'brain_teaser', 'breadth_first_search', 'depth_first_search', 'design', 'divide_and_conquer', 'dynamic_programming', 'geometry', 'graph', 'greedy', 'hash_table', 'heap', 'line_sweep', 'linked_lists', 'math', 'memoization', 'minimax', 'ordered_map', 'queue', 'random', 'recursion', 'rejection_sampling', 'reservoir_sampling', 'rolling_hash', 'segment_tree', 'sliding_window', 'sort', 'stack', 'string', 'suffix_array', 'topological_sort', 'tree', 'trie', 'two_pointers', 'union_find'}


def allowedDifficulties(userPickedDifficulty: str) -> bool:
    return userPickedDifficulty.title() in difficulties


def allowedTags(userPickedTag: str) -> bool:
    return userPickedTag in tags
