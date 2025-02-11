#Stefanos Fotopoulos 4829
import csv

def merge_join(R_csv, S_csv, output):
    with open(R_csv, newline='') as R, open(S_csv, newline='') as S, open(output, 'w', newline='') as output_csv:
        #Dimiourgia readers/writer gia na mporesw na diatreksw to arxeio kai na grapsw ta apotelesmata sto output
        reader_R = csv.reader(R)
        reader_S = csv.reader(S)
        writer = csv.writer(output_csv)

        for row_R in reader_R:
            S.seek(0) #Epanaferw ton file pointer stin arxi tou S
            for row_S in reader_S:
                if row_R[0] == row_S[1]: #R(ABC) S(DAE) elegxw tin prwth stili tou R me tin mesaia tou S
                    writer.writerow(row_R + row_S[:1] + row_S[2:]) #Krataw mono ABC apo R kai DE apo S

if __name__ == "__main__":
    merge_join('R.csv', 'S.csv', 'O2.csv')
