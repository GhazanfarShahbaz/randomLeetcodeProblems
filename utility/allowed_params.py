difficulties = ("any", "easy", "medium", "hard")
tags = {"any", 'arrays', 'backtracking', 'binary_indexed_tree', 'binary_search', 'binary_search_tree', 'bit_manipulation', 'brain_teaser', 'breadth_first_search', 'depth_first_search', 'design', 'divide_and_conquer', 'dynamic_programming', 'geometry', 'graph', 'greedy', 'hash_table', 'heap', 'line_sweep', 'linked_lists', 'math', 'memoization', 'minimax', 'ordered_map', 'queue', 'random', 'recursion', 'rejection_sampling', 'reservoir_sampling', 'rolling_hash', 'segment_tree', 'sliding_window', 'sort', 'stack', 'string', 'suffix_array', 'topological_sort', 'tree', 'trie', 'two_pointers', 'union_find'}
subscription = {"yes": "subscription" , "no": "not subscription", "any": "any"}

codechef_difficulty = {"beginner", "easy", "medium", "hard", "challenge"}

problem_types = {"euler": "Euler_Data", "leetcode": "Leetcode_Data", "codechef": "Codechef_Data"}


def allowedDifficulties(userPickedDifficulty: str) -> bool:
    """
    Returns True if the given difficulty is allowed, False otherwise.

    Args:
        userPickedDifficulty (str): The difficulty picked by the user.

    Returns:
        bool: True if the difficulty is allowed, False otherwise.
    """
    return userPickedDifficulty.lower() in difficulties


def allowedTags(userPickedTag: str) -> bool:
    """
    Returns True if the given tag is allowed, False otherwise.

    Args:
        userPickedTag (str): The tag picked by the user.

    Returns:
        bool: True if the tag is allowed, False otherwise.
    """
    return userPickedTag.lower() in tags


def allowedCodeChefDifficulty(userPickedDifficulty: str) -> bool:
    """
    Returns True if the given CodeChef difficulty is allowed, False otherwise.

    Args:
        userPickedDifficulty (str): The CodeChef difficulty picked by the user.

    Returns:
        bool: True if the CodeChef difficulty is allowed, False otherwise.
    """
    return userPickedDifficulty.lower() in codechef_difficulty


def allowedSubscription(userPickedSubscription: str) -> bool:
    """
    Returns True if the given subscription type is allowed, False otherwise.

    Args:
        userPickedSubscription (str): The subscription type picked by the user.

    Returns:
        bool: True if the subscription type is allowed, False otherwise.
    """
    return userPickedSubscription.lower() in subscription.keys()


def subscriptionQuery(userPickedSubscription: str) -> str:
    """
    Returns the query string for the given subscription type.

    Args:
        userPickedSubscription (str): The subscription type picked by the user.

    Returns:
        str: The query string for the subscription type.
    """
    return subscription[userPickedSubscription]


def worksheetName(userPickedType: str) -> str:
    """
    Returns the name of the worksheet for the given problem type, or an empty string if the type is not recognized.

    Args:
        userPickedType (str): The problem type picked by the user.

    Returns:
        str: The name of the worksheet for the problem type, or an empty string if the type is not recognized.
    """
    return problem_types[userPickedType] if userPickedType in problem_types.keys() else ""
