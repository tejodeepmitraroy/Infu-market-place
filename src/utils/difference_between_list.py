def difference_between_list(list1,list2):
    # Convert lists to sets
    set1 = set(list1)
    set2 = set(list2)

    # Find the difference
    difference1 = list(set1 - set2)  # Elements in list1 but not in list2

    # Display the results
    print("Elements in list1 but not in list2:", difference1)

    return difference1
