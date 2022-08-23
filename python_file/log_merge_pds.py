import pandas as pd
import numpy as np
import pathlib
import os, sys

class DF_pds():   
    def __init__(self, folder):
        self.folder = pathlib.Path(os.getcwd()) / folder
        print(self.folder)
        self.file_list = self.folder.glob("*LGE*.log") #log file list
        self.label_Set = [["file_name"],
                          ["Proxy", "Adm State", "Op. State", "ENodeBFunction", "EUtranCellFDD", "FDD"], 
                          ["Proxy", "Adm State", "Op. State", "Equipment", "FRU", "FDD"],
                          ["FRU", "FDD", "Attribute", "Value"],
                          ["FRU", "LNH", "BOARD", "ST", "FAULT", "OPER", "MAINT", "STAT", "PRODUCTNUMBER", "REV", "SERIAL", "DATE", "PMTEMP", "TEMP", "UPT"], 
                          ["XPBOARD", "ST", "FAULT", "OPER", "PRODUCTNUMBER", "REV", "SERIAL/NAME DATE", "TEMP", "MO"],
                          ["ID", "T", "RiL", "BPBP", "BOARD1", "LNH1", "PORT", "R", "LINK", "RATE", "BOARD2", "LNH2", "PORT", "R", "LINK", "RATE", "LENGTH", "MO1_FRU", "MO2_FRU"],
                          ["ID", "LINK", "RiL", "VENDOR1"],
                          ["ID", "LINK", "RiL", "WL1", "TEMP1"],
                          ["ID", "RiL", "BOARD", "SFPLNH"],
                          ["BOARD", "LNH", "PORT"],
                          ["Prio", "ST", "syncRefType", "refStatus", "opQualLevel", "SyncReference"],
                          ["FRU", "LNH", "BOARD", "RF", "BP", "TX", "(W/dBm)", "VSWR", "(RL)", "RX (dBm)", "UEs/gUEs", "SE", "AG", "FDD", "NIOT", "(State:CellIds:PCIs)"]]
        self.dataframe_set = []
        self.Extract_df()
    
    ######################
    def Find_label_idx(self, line, label):
        label_idx = []
        for l in label: # 라벨의 앞 뒤 인덱스 찾기
            i = line.find(l)
            label_idx.append([i, i+len(l)]) # [[첫 라벨 인덱스 시작, 첫 라벨 인덱스 끝],[둘 ~~~],[]]
        return label_idx

    def List_merge(self, l, idx):
        idx.sort(reverse=True)
        for i in idx:
            l = l[:i] + [l[i] + l[i+1]] + l[i+2:]
        return l
    
    def List_split(self, line):
        d = [i for i in line.split(" ") if i not in {"", "\n"}]
        d[-1] = d[-1][:-1]
        return d
    
    def Data_split(self, data, split_t, equal_t, i):
        split_data = data[i]
        del data[i]
        for idx, d in enumerate(split_data.split(split_t)):
            data.insert(i + idx, d.split(equal_t)[1])
        return data
    #############################
    
    #############################
    # 0,1 번 테이블의 데이터 처리
    def ext_tb01(self, table_line, t_idx):
        label = self.label_Set[t_idx] # 라벨 만들기
        data = []
        for d in table_line[2:]:
            buf_data = self.Data_split(self.List_merge(self.List_split(d), [1, 3]), ",", "=", 3)
            data.append(buf_data + [buf_data[4].replace("S", "_").split("_")[-1]])
        return label, data

    # 2번 테이블의 데이터 처리
    def ext_tb2(self, table_line, t_idx):
        label = self.label_Set[t_idx] # 라벨 만들기
        data = []
        for d in table_line[2:]:
            buf_data = self.Data_split(self.List_merge(self.List_split(d), [2]), ",", "=", 0)
            data.append([buf_data[0]] + [buf_data[0].replace("S", "_").split("_")[-1]] + buf_data[1:])
        return label, data

    # 11번 테이블 처리
    def ext_tb11(self, table_line, t_idx):
        label = self.label_Set[t_idx] # 라벨 만들기
        label_idx1 = self.Find_label_idx(table_line[0], label[:11])
        data = []
        for d in table_line[2:]:
            exFDD = "No"
            split_data = self.List_split(d)
            buf_data = split_data[:5]
            d2 = d[label_idx1[-1][1]:]

            label_idx2 = self.Find_label_idx(d2, label[11:])

            buf_data.append(None) if d[label_idx1[5][0]] == "N" else buf_data.append(d[label_idx1[5][0]:].split(" ")[0]) # TX
            buf_data.append(None) if d[label_idx1[6][1]-1] == " " else buf_data.append(d.replace(")", "(").split("(")[1]) # (W/dBm)
            buf_data.append(None) if d[label_idx1[7][0]] == "N" else buf_data.append(d[label_idx1[7][0]:].split(" ")[0]) # VSWR
            buf_data.append(None) if d[label_idx1[8][0]+1] == " " else buf_data.append(d.replace(")", "(").split("(")[3]) # (RL)
            buf_data.append(None) if d[label_idx1[9][0]] == " " else buf_data.append(d[label_idx1[9][0]:].split(" ")[0]) # RX (dBm)
            buf_data.append(None) if d[label_idx1[10][0]] == " " else buf_data.append(d[label_idx1[10][0]:].split(" ")[0]) # UEs/gUEs

            buf_data.append(None) if d2[label_idx2[0][0]] != "S" else buf_data.append(d2[label_idx2[0][0]:].replace("=", " ").split(" ")[1]) # Sector
            buf_data.append(None) if d2[label_idx2[1][0]] != "A" else buf_data.append(d2[label_idx2[1][0]:].replace("=", " ").split(" ")[1]) # AG
            buf_data.append(None) if d2[label_idx2[2][0]] != "F" else buf_data.append(d2[label_idx2[2][0]:].replace("=", " ").split(" ")[1]) # FDD
            
            if "FDD=" in d2[label_idx2[2][1]:]: exFDD = (d2[label_idx2[2][1]:].replace("=", " ").split(" ")[3]) #FDD ex

            buf_data.append(None) if d2[label_idx2[3][0]] != "N" else buf_data.append(d2[label_idx2[3][0]:].replace("=", " ").split(" ")[1]) # NIOT
            buf_data.append(d2[label_idx2[3][1]:].replace(")", ")?").replace("(", "?(").split("?")[1]) if "(" in d2[label_idx2[3][1]:] else buf_data.append(None) # (State:CellIds:PCIs)                
            data.append(buf_data)
            if exFDD != "No":
                buf_data2 = buf_data[:]
                buf_data2[13] = exFDD
                data.append(buf_data2)
        return label, data
    #####################################
    
    def Make_df(self, table_lines, f_idx, t_idx):
#         print("[테이블]" + str(f_idx) + '-' + str(t_idx))
        if t_idx in [1, 2]: 
            label, data = self.ext_tb01(table_lines, t_idx)
        if t_idx in [3]: 
            label, data = self.ext_tb2(table_lines, t_idx)
        if t_idx in [12]:
            label, data = self.ext_tb11(table_lines, t_idx)
        return pd.DataFrame(dict(zip(label, np.array(data).transpose())))
    
    ##시작되는 함수 // log파일에서 테이블 영역 라인 추출
    def Extract_df(self):
        extract_state = 0 # 0은 테이블 탐색중, 1은 테이블 시작, 2는 데이타 시작, 3는 테이블 끝, 4은 dataframe만들기
        table_line_idx = [0, 0]
        for f_idx, file in enumerate(self.file_list):
            with open(file, "r") as log_txt:
                self.dataframe_set.append([])
                self.dataframe_set[f_idx].append(str(file).replace("\\",".").replace("/",".").split(".")[1])
                t_idx = 1
                log_lines = log_txt.readlines()
            
            for l_idx, line in enumerate(log_lines):
                if extract_state == 0:
                    if ("======" in line and "======"in log_lines[l_idx+2]) or ("------" in line and "------"in log_lines[l_idx+2]): # === 또는 --- 처음 발견시 +2 line에 같은 것이 있는지 확인 -> 테이블 시작
                        table_line_idx[0] = l_idx + 1
                        extract_state = 1
                elif extract_state == 1 and ("======" in line or "------" in line): extract_state = 2 # === 또는 --- 두번째 발견시 -> 라벨 끝, 데이타 시작
                elif extract_state == 2 and "======" in line: # === 세번째 발견시 -> 데이타 확실하게 끝 -> dataframe 만들기로 인덱스 넘기고 extract_state 최종상태로
                    table_line_idx[1] = l_idx
                    extract_state = 3
                elif extract_state == 2 and "------" in line: # --- 세번째 발견시 -> 데이타 끝인지 확인 애매 -> 다음줄이 공백이거나 Tip으로 시작하면 테이블 끝
                    if (len(log_lines[l_idx+1]) == 1) or ('Tip' in log_lines[l_idx+1]) or (t_idx == 12):
                        table_line_idx[1] = l_idx
                        extract_state = 3
                if extract_state == 3: # 테이블 pandae frame으로 변환, t_idx는 12까지 있음
                    if t_idx in [1, 2, 3, 12]:
                        df = self.Make_df(log_lines[table_line_idx[0]:table_line_idx[1]], f_idx, t_idx) # 추출한 라인을 테이블로 추출
                        self.dataframe_set[f_idx].append(df)  
                    extract_state = 0
                    t_idx += 1
        self.dataframe_set[:]
                    
    def Save_by_sheet(self, DF_ex, name):
        try:
            # 1. 엑셀 파일 열기 w/ExcelWriterstr()
            writer = pd.ExcelWriter(str(name)+".xlsx", engine='openpyxl')
            # 2. 시트별 데이터 추가하기(1개 시트로 저장할때와 유사)
            for idx_d, d in enumerate(DF_ex):
                # d = d.fillna("")
                d.to_excel(writer, sheet_name = str(self.dataframe_set[idx_d][0]), index=False)
            # 3. 엑셀 파일 저장하기
            writer.save()
        except:
            DF_ex.to_excel(str(name)+".xlsx", index=False)
