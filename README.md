# Query Evaluation on Complex Data(Part1)

This project focuses on evaluating queries on complex data, implementing operations such as grouping with aggregate functions, natural join, and composite queries. The implementation reads two CSV files (`R.csv` and `S.csv`) simultaneously, producing results efficiently without requiring a full read of the files.

## Features
- **Grouping with Aggregate Functions**: Computes grouped results with functions like SUM, AVG, COUNT, etc.
- **Natural Join**: Performs an efficient natural join between two datasets.
- **Composite Queries**: Executes multi-step queries with optimized processing.

## Requirements
- Python 3.x
- Pandas (for data manipulation)
- Any additional required libraries (specified in `requirements.txt`)


## Usage
1. Place your `R.csv` and `S.csv` files in the designated directory.
2. Run the main script:
   ```bash
   python meros1.py
   ```
3. The results will be displayed and saved accordingly.

## File Structure
- `meros1.py`: The main script executing query evaluations.
- `R.csv` / `S.csv`: Input data files.
- `requirements.txt`: Dependencies required for the project.
- `README.md`: Project documentation.

## License
This project is licensed under the MIT License.



