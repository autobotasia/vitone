# -*- coding: utf-8 -*-
import re
import random
from tqdm import tqdm
error_ng_am_1 = ['ả','ẩ','ẳ','ỏ','ổ','ở','ẻ','ể','ủ','ử','ỉ','ỷ']
error_ng_am_2 = ['ã','ẫ','ẵ','õ','ỗ','ỡ','ẽ','ễ','ũ','ữ','ĩ','ỹ']
error_ph_am_1 = ['ch','d','s','ch','d','s','ch','d','s','ch','d','s']
error_ph_am_2 = ['tr','gi','x','tr','gi','x','tr','gi','x','tr','gi','x']

rep_error_1 = {'ả':'ã','ẩ':'ẩ','ẳ':'ẵ','ỏ':'õ','ổ':'ỗ','ở':'ỡ','ẻ':'ẽ','ể':'ễ','ủ':'ũ','ử':'ữ','ỉ':'ĩ','ỷ':'ỹ'}
rep_error_2 = {'ã':'ả','ẫ':'ẩ','ẵ':'ẳ','õ':'ỏ','ỗ':'ổ','ỡ':'ở','ẽ':'ẻ','ễ':'ể','ũ':'ủ','ữ':'ử','ĩ':'ỉ','ỹ':'ỷ'}
rep_error_3 = {'ch':'tr','d':'gi','s':'x'}
rep_error_4 = {'tr':'ch','gi':'d','x':'s'}

def delete_acc(char):
    char = re.sub("[ạáàảãăắằẳẵặâấầẩẫậ]","a",char)
    char = re.sub("[ôơóòỏõọốồổỗộớờởỡợ]","o",char)
    char = re.sub("[éèẻẽẹêếềểễệ]","e",char)
    char = re.sub("[úùủũụưứừửữự]","u",char)
    char = re.sub("[ìíỉịĩ]","i",char)
    char = re.sub("[ýỳỷỵỹ]","y",char)
    char = re.sub("[ẠẢÃÀÁÂẬẦẤẨẪĂẮẰẶẲẴ]","A",char)
    char = re.sub("[ÓÒỌÕỎÔỘỔỖỒỐƠỜỚỢỞỠ]","O",char)
    char = re.sub("[ÉÈẺẸẼÊẾỀỆỂỄ]","E",char)
    char = re.sub("[ÚÙỤỦŨƯỰỮỬỪỨ]","U",char)
    char = re.sub("ÍÌỊỈĨ","I",char)
    char = re.sub("ÝỲỶỴỸ","Y",char)
    char = re.sub("đ","d",char)
    char = re.sub("Đ","D",char)
    return char

def replace_all(text,dic):
    for m, l in dic.items():
        text = text.replace(m, l)
    return text

class Create_Error():

    def __init__(self,text):
        self.text = text

    def creat(self):
        char = self.text.split()
        #print(char)
        for i in range(len(char)):
            for j in range(len(error_ng_am_1)):
                if error_ng_am_1[j] in char[i]:
                    check = random.randint(1,10)
                    if check == 1:
                        char[i] = replace_all(char[i],rep_error_1)
                        char[i] = '*' + char[i] + '*'
                    i += 1
                    break

                if error_ng_am_2[j] in char[i]:
                    check = random.randint(1,10)
                    if check == 1:
                        char[i] = replace_all(char[i],rep_error_2)
                        char[i] = '*' + char[i] + '*'
                    i += 1
                    break

                if error_ph_am_1[j] in char[i]:
                    check = random.randint(1,10)
                    if check == 1:
                        char[i] = replace_all(char[i],rep_error_3)
                        char[i] = '*' + char[i] + '*'
                    i += 1
                    break

                if error_ph_am_2[j] in char[i]:
                    check = random.randint(1,10)
                    if check == 1:
                        char[i] = replace_all(char[i],rep_error_4)
                        char[i] = '*' + char[i] + '*'
                    i += 1
                    break

                check = random.randint(1,10)
                if check not in [1,2]:
                    char[i] = delete_acc(char[i])
                    i+=1
                    break

        text_new = ''
        for l in range(len(char)):
            text_new += char[l]+ " "
        return text_new


f = open('corpus-full-0.2.txt','r',encoding='utf-8')
with open('text-error.txt','a+',encoding='utf-8') as w:

    for i in tqdm(range(100000)):
        line_old = f.readline()
        line_new = Create_Error(line_old).creat() + '\n'
        w.write(line_new)
