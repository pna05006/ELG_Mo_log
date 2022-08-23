#!/usr/bin/env python3
from log_merge_pds import DF_pds
import pandas as pd
import argparse
import sys, os

def main(args):
    try:
        print("데이터 추출 중...")
        DF = DF_pds(args.folder)
        print("데이터 추출 완료!")
        buf_table = []

        print("데이터 매칭 중...")
        for df in DF.dataframe_set:
            t = pd.merge(df[2], df[3], how='outer')
            t = pd.merge(df[4], t, how='left')
            t = t.rename(columns={'Op. State': 'FRU Op. State', 'Adm State': 'FRU Adm State', 'Proxy': 'FRU Proxy'})
            t = pd.merge(t, df[1], how='left', on = 'FDD')
            t = t.rename(columns={'Op. State': 'Cell Op. State', 'Adm State': 'Cell Adm State', 'Proxy': 'Cell Proxy'})
            buf_table.append(t)

        total_df = buf_table[0]
        for df in buf_table[1:]:
            total_df = pd.concat([total_df, df])
        print("데이터 매칭 완료!")

        DF.Save_by_sheet(total_df, str(os.getcwd()) + '/' + str(args.save_file_name))
        print("데이타 저장 완료!")
        print("프로그램을 종료합니다.")
        sys.exit()

    except KeyboardInterrupt:
        print("프로그램을 종료합니다.")
        sys.exit()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="분석하려는 로그 폴더")
    parser.add_argument("save_file_name", help="저장할 xlsx 파일 이름")
    args = parser.parse_args()
    main(args)