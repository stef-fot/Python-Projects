#Stefanos Fotopoulos 4829
import csv

def composite_query(R_csv, S_csv, output):

    with open(R_csv, newline='') as R, open(S_csv, newline='') as S, open(output, 'w', newline='') as output_csv:
        # Dimiourgia readers/writer gia na mporesw na diatreksw to arxeio kai na grapsw ta apotelesmata sto output
        reader_S = csv.reader(S)
        reader_R = csv.reader(R)
        writer = csv.writer(output_csv)

        for row_R in reader_R:
            R_A = row_R[0]
            C = int(row_R[2])
            sum = 0

            if C == 7:
                S.seek(0)  # Epanaferw ton file pointer stin arxi tou S
                for row_S in reader_S:
                    S_A = row_S[1]
                    E = int(row_S[2])
                    if R_A == S_A:
                        sum += E
                if sum > 0: # Xwris auth thn synthiki krataei kai tis times pou exoun mono R.C = 7
                    writer.writerow([R_A, sum])


if __name__ == "__main__":
    composite_query('R.csv', 'S.csv', 'O3.csv')
