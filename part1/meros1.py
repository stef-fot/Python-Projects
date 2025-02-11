# Stefanos Fotopoulos 4829
import sys
import csv
from collections import defaultdict


def merge_sort(array, attribute_index):
    if len(array) <= 1:
        return array

    mid = len(array) // 2  # xwrizw ton pinika se 2 mikroterous
    first_half = merge_sort(array[:mid], attribute_index)#anadromiki klisi tis sinartisis mexri na exei mono 1 stoixeio kratontas mono to attribute pou mas endiaferei
    second_half = merge_sort(array[mid:], attribute_index)#anadromiki klisi tis sinartisis mexri na exei mono 1 stoixeio kratontas mono to attribute pou mas endiaferei
    sorted_array = []
    first_half_index = 0
    second_half_index = 0

    while first_half_index < len(first_half) and second_half_index < len(second_half):
        if int(first_half[first_half_index][attribute_index]) < int(second_half[second_half_index][attribute_index]): #elegxw poia timi einai megalyteri apo tis 2 gia na tin eisagw ston neo pinaka kai
            sorted_array.append(first_half[first_half_index])
            first_half_index += 1
        else:
            sorted_array.append(second_half[second_half_index])
            second_half_index += 1

    sorted_array.extend(first_half[first_half_index:])#edw eisagoume ta enapomeinanta stoixeia ta opoia den mpikan ston sorted array
    sorted_array.extend(second_half[second_half_index:])#edw eisagoume ta enapomeinanta stoixeia ta opoia den mpikan ston sorted array
    return sorted_array


def group_by_aggregation(sorted_data, group_by_attr, aggregation_attr, function):
    data = defaultdict(list)

    for row in sorted_data:#diatrexei kathe grammi tou sorted data pou phre apo tin merge_sort
        group_by = row[group_by_attr]
        aggregation_value = row[aggregation_attr]
        data[group_by].append(aggregation_value)#prosthetei tin aggregation_value sto leksiko analoga me to ekastote group by

    with open('O1.csv', 'w', newline='') as output:
        writer = csv.writer(output)
        for group_by, aggregation_values in data.items():#anatrexei gia to sygkekrimeno kleidi(group_by) stis times(aggregation_values) pou exei to leksiko
            if function == 'sum':
                result = sum(map(int, aggregation_values))#xreiazetai map gia na paroume ton akeraio
            elif function == 'min':
                result = min(map(int, aggregation_values))#xreiazetai map gia na paroume ton akeraio
            elif function == 'max':
                result = max(map(int, aggregation_values))#xreiazetai map gia na paroume ton akeraio
            writer.writerow([group_by, result])


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Warning follow the pattern: python program.py <filename> <group_by_attribute> <aggregation_attribute> <function>")
        sys.exit(1)

    filename = sys.argv[1]
    group_by_attribute = int(sys.argv[2])
    aggregation_attribute = int(sys.argv[3])
    aggregation_function = sys.argv[4]

    with open(filename, newline='') as file:
        reader = csv.reader(file)
        data = list(reader)

    sorted_data = merge_sort(data, group_by_attribute)

    group_by_aggregation(sorted_data, group_by_attribute, aggregation_attribute, aggregation_function)
