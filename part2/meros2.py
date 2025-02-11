# Stefanos Fotopoulos 4829
import math



def read_tree_from_file(file_path):
    result_list = []

    with open(file_path, 'r') as file:
        for line in file:
            if not (line.startswith("Root id") or "——————— Inner Node at Level 3 ———————" in line or "——————— Leaf Node ———————" in line or "——————— Inner Node at Level 1 ———————" in line or "——————— Inner Node at Level 2 ———————" in line):
                result_list.append(line.strip())


    return result_list


def mindist(point, mbr):
    total = 0
    for i in range(len(point)):
        if point[i] < mbr[i]:
            total += (mbr[i] - point[i]) ** 2
        elif point[i] > mbr[i + len(point)]:
            total += (point[i] - mbr[i + len(point)]) ** 2
    return math.sqrt(total)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python script_name.py rtree_file x,y k")
        sys.exit(1)
    tree_file = sys.argv[1]
    q_coordinates = tuple(map(float, sys.argv[2].split(',')))
    k = int(sys.argv[3])

    tree = read_tree_from_file(tree_file)




