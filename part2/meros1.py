# Stefanos Fotopoulos 4829
import math
import sys


def read_data(filename):
    with open(filename) as f:
        num_points = int(f.readline())
        print("Total Coordinates: ", num_points, "\n")
        points = []
        for i, line in enumerate(f.readlines(), start=1):
            point = [i] + list(map(float, line.strip().split()))
            points.append(point)
    return points, num_points


def sort_points_by_x(points):
    sorted_points = sorted(points, key=lambda p: p[1])  #sort by x
    return sorted_points


def sort_points_by_y(points,num_points):
    num_per_node = math.floor(1024 / 20)#51 stoixeia tha xei to kathe fyllo
    num_nodes = math.ceil(num_points / num_per_node)#Synolika 1020 fylla
    square_root = math.ceil(math.sqrt(num_nodes))
    vertical_2d_lines = square_root * num_per_node
    sorted_points = []

    #Xwrizw ton pinaka se 1632 tmimata kai ta taksinomw kata y
    for i in range(0, len(points), vertical_2d_lines):
        segment = points[i:i + vertical_2d_lines]
        sorted_segment = sorted(segment, key=lambda p: p[2])  #sort by y
        sorted_points.extend(sorted_segment)

    return sorted_points


def minimum_bounding_rectangle(data, flag):
    mbr = []
    if flag == 0:
        flattened_data = data

        flattened_data = [item for sublist in flattened_data for item in sublist]
    else:
        flattened_data = data
    for i in range(0, len(flattened_data)):
        min_X = min(item[1] for item in flattened_data[i])
        max_X = max(item[1] for item in flattened_data[i])
        min_Y = min(item[2] for item in flattened_data[i])
        max_Y = max(item[2] for item in flattened_data[i])
        mbr.append([min_X, min_Y, max_X, max_Y])
    return mbr


def find_best_mbr(data,total_areas):
    areas_list = []
    flattened_data = data
    counter = 0
    flattened_data = [item for sublist in flattened_data for item in sublist]
    index_list = []
    mbr_list = []
    for i in range(0, len(flattened_data)):
        counter = 0
        for item in flattened_data[i][0]:
            min_X = item[0]
            min_Y = item[1]
            max_X = item[2]
            max_Y = item[3]
            width = max_X - min_X
            height = max_Y - min_Y
            temp_area = width * height
            total_areas.append(temp_area)
            if counter == 0:
                areas_list.append(temp_area)
                index_list.append(counter)
            if temp_area > areas_list[i]:
                areas_list.pop(i)
                index_list.pop(i)
                areas_list.append(temp_area)
                index_list.append(counter)
            counter += 1

    for i in range(0, len(index_list)):
        index = index_list[i]
        mbr_list.append(flattened_data[i][0][index])
    return mbr_list


def average_mbr_area(nodes,num_nodes,num_of_last_nodes):
    total_area  = 0
    for i in range(0, len(nodes)):
        total_area += nodes[i]
    total_nodes = (num_nodes-1) * 28 + num_of_last_nodes
    result = total_area / total_nodes
    return result


def build_leaf(coordinates, num_points,level):
    num_per_node = math.floor(1024 / 20)
    num_nodes = math.ceil(num_points / num_per_node)
    leafs = []
    id = 0
    def sort_tile_recursive(coords, node_id):
        nonlocal id
        if not coords:
            return []
        leafs_for_node = []
        while coords:
            tile = coords[:num_per_node]
            sorted_coords_y = sorted(tile, key=lambda x: x[2])

            leaf_bytes = 0
            temp_leaf = []
            for coord in sorted_coords_y:
                if leaf_bytes + 20 > 1024:
                    leafs_for_node.append(temp_leaf)
                    leaf_bytes = 0
                    temp_leaf = []
                temp_leaf.append(coord)
                leaf_bytes += 20

            if temp_leaf:
                leafs_for_node.append(temp_leaf)
                temp_leaf = []
            coords = coords[num_per_node:]
        id = node_id + 1
        return leafs_for_node
    leafs = sort_tile_recursive(coordinates, id)
    level += 1
    return leafs


def build_rtree(leafs_list,R_tree,total_areas,temp_mbr,average_list,flag,num_points):
    total_bytes = 1024
    num_per_node = math.floor(total_bytes / 20)  # ta shmeia poy xwraei kathe fyllo (51)
    num_nodes = math.ceil(num_points / num_per_node)  # synolika fylla (1020)
    leafs_per_node = math.floor(total_bytes / 36)  # fylla ana komvo (28)
    total_nodes = math.ceil(num_nodes / leafs_per_node)  # synolo komvwn (37)
    mbr_bytes = 32 + 4
    original_list = leafs_list
    first_len = len(leafs_list)
    average_list.append(first_len)
    leafs = leafs_list
    mbr = []
    counter_leaf = 0
    counter_node = 0
    node_id = 0
    last_mbr = 1


    if len(leafs) == num_nodes:
        flag = 0
        for i in range(1, len(leafs)+1):
            if i % leafs_per_node == 0 or i == num_nodes:
                mbr = []

                if counter_node + mbr_bytes > total_bytes:
                    node_coords = []
                    node_coords.append(original_list[counter_node:first_len])
                    mbr.append(minimum_bounding_rectangle(node_coords, flag))
                    node_id += 1
                    leafs.append(mbr)
                    R_tree.append(mbr)
                    temp_mbr.append(len(node_coords[0]))
                    counter_node += leafs_per_node
                else:
                    node_coords = []
                    node_coords.append(leafs[counter_node:counter_node + leafs_per_node])
                    mbr.append(minimum_bounding_rectangle(node_coords, flag))
                    last_mbr += 1
                    node_id += 1
                    leafs.append(mbr)
                    R_tree.append(mbr)

                    counter_node += leafs_per_node
                counter_leaf += num_per_node
    else:
        flag = 1
        for i in range(1,len(leafs_list)+1):
            if i % leafs_per_node == 0 or i == first_len:
                mbr = []
                if i == first_len:
                    node_coords = []
                    node_coords.append(original_list[counter_node:first_len])
                    mbr_list = find_best_mbr(node_coords,total_areas)
                    mbr.append(mbr_list)
                    last_mbr += 1
                    node_id += 1
                    leafs.append(mbr)
                    if first_len!=1:
                        R_tree.append(mbr)
                    temp_mbr.append(len(node_coords[0]))
                    counter_node += leafs_per_node
                else:
                    node_coords = []
                    node_coords.append(original_list[counter_node:counter_node + leafs_per_node])
                    mbr_list = find_best_mbr(node_coords,total_areas)
                    mbr.append(mbr_list)
                    last_mbr += 1
                    node_id += 1
                    leafs.append(mbr)
                    R_tree.append(mbr)
                    counter_node += leafs_per_node
                counter_leaf += num_per_node
    if flag == 1:
        num_of_last_nodes = temp_mbr[0]
        avg_mbr = average_mbr_area(total_areas, first_len, num_of_last_nodes)
        temp_mbr.pop(0)
        average_list.append(avg_mbr)
        total_areas = []
    if first_len == 1:
        return R_tree

    last_level_list = leafs[first_len:]

    if first_len != 1:
        build_rtree(last_level_list,R_tree,total_areas,temp_mbr,average_list,flag,num_points)



def print_tree_statistics(R_tree, avg_list, Tree_Stats, level):
    Stats = ""
    Tree_Stats += "Root id is: " + str(len(R_tree)-1) + "\n"
    Tree_Stats += "                      ——————— Leaf Node ———————\n"
    indices_to_move = [0, 1, 3, 5]
    num_of_nodes = [avg_list.pop(i) for i in reversed(indices_to_move)]
    for i in range(0,num_of_nodes[-1]):
        Stats = str(i) + ", " + str(len(R_tree[i])) + ", " + str(0)
        coords = ""
        for j in range(0,len(R_tree[i])):
            coords += ", "  + "(" + str(R_tree[i][j][0]) + ", " + "(" + str(R_tree[i][j][1]) + ", " + str(R_tree[i][j][2]) + ")" + ")"
        Tree_Stats += Stats + coords + "\n"

    print("Total number of leafs: ",num_of_nodes[-1]," found in level",level)
    print("Average MBR for level ", level, "is: 0.0")
    first_len_of_avg_list = len(avg_list)
    last_num = num_of_nodes[-1]
    num_of_nodes.pop(-1)
    level += 1
    record_id = 0
    while len(num_of_nodes) != 0:
        Tree_Stats += "                      ——————— Inner Node at Level " + str(level) + " ———————\n"
        for i in range(last_num, last_num + num_of_nodes[-1]):

            Stats = str(i) + ", " + str(len(R_tree[i][0])) + ", " + str(1)
            coords = ""
            for j in range(0, len(R_tree[i][0])):
                coords += ", " + "(" + str(record_id) + ", " + "(" + str(R_tree[i][0][j][0]) + ", " + str(R_tree[i][0][j][1]) + ", " + str(R_tree[i][0][j][2]) + ", " + str(R_tree[i][0][j][3]) + ")" + ")"
                record_id += 1
            Tree_Stats += Stats + coords + "\n"
        print("Total number of internal nodes: ", num_of_nodes[-1], " found in level", level)
        print("Average MBR for level ", level, "is: ",avg_list[0])
        avg_list.pop(0)
        level += 1
        last_num += num_of_nodes[-1]
        num_of_nodes.pop(-1)
    print("Height of R_Tree is: ",first_len_of_avg_list + 1)

    return Tree_Stats


def main(output_filename):
    input_filename = "Beijing_restuarants.txt"
    R_tree = []
    total_areas = []
    temp_mbr = []
    average_list = []
    Tree_Stats = ""
    level = 0
    flag = 0
    coordinates, num_points = read_data(input_filename)
    sorted_coords_x = sort_points_by_x(coordinates)
    sorted_coords = sort_points_by_y(sorted_coords_x,num_points)
    root = build_leaf(sorted_coords, num_points, level)

    R_tree += root
    nodes = build_rtree(root, R_tree, total_areas, temp_mbr, average_list, flag,num_points)
    Tree_Stats = print_tree_statistics(R_tree, average_list, Tree_Stats, level)


    with open(output_filename, "w") as file:
        file.write(Tree_Stats)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py output_filename")
        sys.exit(1)

    output_filename = sys.argv[1]
    main(output_filename)
