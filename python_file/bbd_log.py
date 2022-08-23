#!/usr/bin/env python3
from tqdm import tqdm
import pandas as pd
import numpy as np
import argparse
import os
import sys

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

class DF_pds():   
    def __init__(self, args):
        self.args = args
        self.UP_dic = {}
        with open(os.path.dirname(os.getcwd()) + '/' + args.file, "r") as log_txt:
            self.log_lines = log_txt.readlines()
        for line in self.log_lines:
            if ('[info]' in line): print(line, end='') 
            else: break

    def Get_UP_list(self):
        UP_set = set()
        for line in tqdm(self.log_lines, mininterval=0.5):
            if '<!' in line: UP_set.add(line.split("<!")[1].split(".")[0])
        return sorted([i for i in list(UP_set)])
        
    def Get_UP_code_list(self, UP_list):
        UP_dic = {}
        for UP_code in UP_list:
            ex_set = set()
            for line in self.log_lines:
                if UP_code in line: ex_set.add(line.split(UP_code + ".")[1].split("!")[0])
            UP_dic[str(UP_code)] = sorted([int(i) for i in list(ex_set)])
        return UP_dic
            
    def Get_UP_info(self):
        UP_list = self.Get_UP_list()
        self.UP_dic = self.Get_UP_code_list(UP_list)
        
    def UP_code_classification(self, code):
        for k in self.UP_dic:
            if code in self.UP_dic[k]: return k
        
    def Extract_tb(self, code):
        self.UPD_str = self.UP_code_classification(code)
        extract_data_a = []
        label_a = []
        extract_data_b = []
        label_b = []
        
        for line in tqdm(self.log_lines, mininterval=0.5):
            if (self.UPD_str + '.' + str(code)) in line:
                line_a, line_b = line.split(' <!' + self.UPD_str + '.' + str(code)+'!> ')
                #line a 처리
                line_a_split = line_a.replace("=", " ").split(" ")
                label_a=['date'                                      , 'code'                   , 'bfn'                  ,  'sfn'                 , 'sf'                   , 'bf'                   ,   'duId'           , 'EMCA3'        , 'LEVEL'        , 'c'             ]
                adj_a = [(line_a_split[0]+', '+line_a_split[1])[1:-1] , line_a_split[2]          , line_a_split[3][5:-1]  , line_a_split[4][4:-1]  , line_a_split[5][3:-1]  , line_a_split[6][3:-1]  , line_a_split[7][5:], line_a_split[8], line_a_split[9], line_a_split[10]]
                
                #line b 처리
                adj_b = []
                k_ex = ''
                v_ex = ''
                line_b_split = line_b.replace(",", "").replace(":", "").split(" ")
                if not label_b:#처음 데이타
                    for d in line_b_split:
                        if "=" in d:
                            if k_ex:
                                label_b.append(k_ex)
                                adj_b.append(v_ex[:-1])
                                k_ex = ''
                                v_ex = ''
                            k, v = d.split("=")
                            label_b.append(k)
                            adj_b.append(v)
                        else:
                            if "byte" in d:
                                if not k_ex:
                                    label_b[len(label_b)-1] = label_b[len(label_b)-1] + ' [' + d + ']'
                                    continue
                                if k_ex:
                                    k_ex = k_ex + ' [' + d + ']'
                                    continue
                            if not k_ex: k_ex = d
                            v_ex = v_ex + d + " "
                else:#데이타 추가
                    for d in line_b_split:
                        if "=" in d:
                            if k_ex:
                                adj_b.append(v_ex[:-1])
                                k_ex = ''
                                v_ex = ''
                            k, v = d.split("=")
                            adj_b.append(v)
                        else:
                            if "byte" in d: continue
                            if not k_ex: k_ex = d
                            v_ex = v_ex + d + " "
                extract_data_a.append(adj_a)
                extract_data_b.append(adj_b)
        extract_data_a = np.array(extract_data_a).transpose()
        extract_data_b = np.array(extract_data_b).transpose()
        dp_a = pd.DataFrame(dict(zip(label_a, extract_data_a)))
        dp_b = pd.DataFrame(dict(zip(label_b, extract_data_b)))
        self.Data_Table = pd.concat([dp_a, dp_b], axis = 1)
        
class Disp_tool():
    def __init__(self):
        self.prt_line = "---------------------------------------------"
    
    def UP_disp(self, UP_dic):
        print(self.prt_line)
        for u in UP_dic:
            print('[' +  str(u) + ' CODE in log]')
            for p in UP_dic[u]:
                print(str(p) + "\t", end="")
            print('\n')
        print(self.prt_line)
                
    def File_open_disp(self, file):
        print("Open log file : " + file + '\n' + self.prt_line)
        
    def input_TF(self, question):
        while "the answer is invalid":
            reply = str(input(question+' (y/n) >> ')).lower().strip()
            if reply[0] == 'y': return True
            if reply[0] == 'n': return False
            
    def input_num(question):
        while True:
            try: reply = float(input(question+' >> '))
            except Exception as e: print("the answer is invalid : ", e)
            else: break
        return reply
    
    def input_str_menu(self, question, list):
        while True:
            reply = str(input(question+' >> ')).strip()
            if reply in list: return reply
            else: print("목록에 없는 선택입니다.")
            
class Menu():
    def __init__(self):
        self.state = 0
        self.Disp = Disp_tool()
        
    def State1(self, DF, foldor):
        extract_list = [int(y) for x in list(DF.UP_dic.values()) for y in x]
        for i, code in enumerate(extract_list):
            DF.UPD_str = DF.UP_code_classification(code)
            print(DF.UPD_str + ' = ' + str(code) + ' 추출 중... (' + str(i+1) + '/' + str(len(extract_list)) + ')')
            DF.Extract_tb(code)
            DF.Data_Table.to_csv(foldor + '/' + args.file + DF.UPD_str + '=' + str(code) + ".csv")

    def State2(self, DF, mode, foldor):
        extract_list = DF.UP_dic[mode]
        for i, code in enumerate(extract_list):
            DF.UPD_str = DF.UP_code_classification(code)
            print(DF.UPD_str + ' = ' + str(code) + ' 추출 중... (' + str(i+1) + '/' + str(len(extract_list)) + ')')
            DF.Extract_tb(code)
            DF.Data_Table.to_csv(foldor + '/' + args.file + DF.UPD_str + '=' + str(code) + ".csv")
    
    def State3(self, DF, mode, foldor):
        DF.UPD_str = DF.UP_code_classification(mode)
        print(DF.UPD_str + ' = ' + str(mode) + ' 추출 중...')
        DF.Extract_tb(mode)
        DF.Data_Table.to_csv(foldor + '/' + args.file + DF.UPD_str + '=' + str(mode) + ".csv")
    
    def M_state(self, DF, mode, foldor):
        if self.state == 1: self.State1(DF, str(foldor))
        if self.state == 2: self.State2(DF, mode, str(foldor))
        if self.state == 3: self.State3(DF, int(mode), str(foldor))
        print("추출 완료\n" + self.Disp.prt_line)
        if self.Disp.input_TF("다른 코드도 추출하시겠습니까?"): self.state = 0
        else: 
            print("프로그램을 종료합니다.")
            self.state = 10
            
def main(args):
    try:
        foldor = str(os.path.dirname(os.getcwd())) + '/' + str(args.foldor)
        # print(foldor)
        createDirectory(os.path.dirname(os.getcwd()) + '/' + args.file)
    
        Disp = Disp_tool()
        Disp.File_open_disp(os.path.dirname(os.getcwd()) + '/' + args.file)
        
        DF = DF_pds(args)
        DF.Get_UP_info()
        M = Menu()
        Disp.UP_disp(DF.UP_dic)

        while M.state == 0:
            mode = Disp.input_str_menu('엑셀로 추출/변환하고자 하는 코드 (0 = 전체)', ['exit', '0'] + list(DF.UP_dic.keys()) + [str(y) for x in list(DF.UP_dic.values()) for y in x])
            if mode == 'exit': break
            M.state = 1 if mode == '0' else 2 if mode in list(DF.UP_dic.keys()) else 3
            M.M_state(DF, mode, foldor)

    except KeyboardInterrupt:
        print("프로그램을 종료합니다.")
        sys.exit()
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="분석하려는 로그 파일")
    parser.add_argument("foldor", help="분석한 xlsx파일을 저장할 폴더")
    args = parser.parse_args()
    main(args)