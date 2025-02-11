# Stefanos Fotopoulos 4829
import heapq
import sys
import time
from collections import defaultdict


def read_and_filter_data(file):
    end_of_file = False
    for line in file:
        fields = line.strip().split(',')
        age = int(fields[1])
        marital_status = fields[8]
        if age >= 18 and not marital_status.startswith(" Married"):
            filtered_record = [fields[0], age, float(fields[25])]
            return filtered_record, end_of_file
    end_of_file = True
    return None, end_of_file


def top_k_join(original_males_data, original_females_data, k):
    max_heap = []
    males_data = defaultdict(list)
    females_data = defaultdict(list)
    p1_max = 0
    p2_max = 0
    counter = 0
    valid_lines = 0
    with open(original_males_data) as males_file, open(original_females_data) as females_file:
        while True:
            filtered_record, end_of_male_file = read_and_filter_data(males_file)
            if not end_of_male_file:
                valid_lines += 1
                males_data[filtered_record[1]].append(filtered_record)
                male_id, male_age, p1_cur = filtered_record
                p1_max = max(p1_max, p1_cur)
                for female_id, _, p2_cur in females_data[male_age]:
                    pair = (male_id, female_id)
                    score = p1_cur + p2_cur
                    heapq.heappush(max_heap, (-score, pair))
                    threshold = max(p1_max + p2_cur, p1_cur + p2_max)
                    if threshold <= -max_heap[0][0]:
                        heap_score, heap_pair = heapq.heappop(max_heap)
                        counter += 1
                        yield f"{counter}. pair: {heap_pair} score: {-heap_score:.2f}"
                        if counter == k:
                            print("Valid lines:", valid_lines)
                            return

            filtered_record, end_of_female_file = read_and_filter_data(females_file)
            if not end_of_female_file:
                valid_lines += 1
                females_data[filtered_record[1]].append(filtered_record)
                female_id, female_age, p2_cur = filtered_record
                p2_max = max(p2_max, p2_cur)
                for male_id, _, p1_cur in males_data[female_age]:
                    pair = (male_id, female_id)
                    score = p1_cur + p2_cur
                    heapq.heappush(max_heap, (-score, pair))
                    threshold = max(p1_max + p2_cur, p1_cur + p2_max)
                    if threshold <= -max_heap[0][0]:
                        heap_score, heap_pair = heapq.heappop(max_heap)
                        counter += 1
                        yield f"{counter}. pair: {heap_pair} score: {-heap_score:.2f}"
                        if counter == k:
                            print("Valid lines:", valid_lines)
                            return

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 2:
        print("Usage: python script_name.py k")
        sys.exit(1)

    k = int(sys.argv[1])

    generator = top_k_join("males_sorted", "females_sorted", k)
    for result in generator:
        print(result)

    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")
