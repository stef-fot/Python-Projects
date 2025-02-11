# Stefanos Fotopoulos 4829
import sys
import heapq
import time
from collections import defaultdict

def read_and_filter_data(filename):
    data = defaultdict(list)
    with open(filename) as f:
        for line in f:
            fields = line.strip().split(',')
            age = int(fields[1])
            marital_status = fields[8]
            if age >= 18 and not marital_status.startswith(" Married"):
                filtered_record = (fields[0], int(fields[1]), float(fields[25]))
                data[age].append(filtered_record)
    return data

def top_k_join(original_males_data, original_females_data, k):
    min_heap = []

    males_data = read_and_filter_data(original_males_data)

    with open(original_females_data) as f:
        for line in f:
            fields = line.strip().split(',')
            age = int(fields[1])
            marital_status = fields[8]
            if age >= 18 and not marital_status.startswith(" Married"):
                female_id, female_age, female_score = fields[0], int(fields[1]), float(fields[25])

                if female_age in males_data:
                    for male_id, male_age, male_score in males_data[female_age]:
                        score = male_score + female_score
                        if len(min_heap) < k:
                            heapq.heappush(min_heap, (score, (male_id, female_id)))
                        else:
                            if score > min_heap[0][0]:
                                heapq.heappushpop(min_heap, (score, (male_id, female_id)))
    return heapq.nlargest(k, min_heap)
if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 2:
        print("Usage: python script_name.py k")
        sys.exit(1)

    k = int(sys.argv[1])

    top_k_results = top_k_join("males_sorted", "females_sorted", k)

    for i, result in enumerate(top_k_results, start=1):
        print(f"{i}. pair: {result[1]} score: {result[0]:.2f}")

    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")



