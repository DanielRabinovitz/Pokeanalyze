def filter_unique_tuples(tuples_list):
    unique_tuples = []  # List to store unique tuples without any previously seen tuple completely contained

    for current_tuple in sorted(tuples_list, key=len):  # Sort by length to ensure smaller tuples are considered first
        # Check if the current tuple contains any of the previously added tuples as a subset
        if not any(set(sub_tuple).issubset(set(current_tuple)) for sub_tuple in unique_tuples if sub_tuple != current_tuple):
            unique_tuples.append(current_tuple)

    return unique_tuples

# Example usage
tuples_list = [('a', 'b'), ('a', 'b', 'c'), ('a', 'c', 'd'), ('b', 'c')]
filtered_tuples = filter_containing_previous_tuples(tuples_list)
print(filtered_tuples)