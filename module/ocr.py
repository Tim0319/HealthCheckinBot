print("OCR识别工具 V1.0 欢迎使用OCR识别工具，采用pytesseract进行识别出首位为1和2的学号")

from PIL import Image

import pytesseract


def ocr(path):
    pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract'
    txt = pytesseract.image_to_string(Image.open(path), lang='chi_sim')
    return txt


def school_number(content):
    sum_num = 0
    temp_str = ''
    temp_list = []
    for i in content:
        temp = ord(i)
        if 57 >= temp >= 48:
            if len(temp_str) == 1:
                if temp_str[0] == '1' or temp_str[0] == '2':
                    sum_num += 1
                    temp_str += i
            elif len(temp_str) == 3:
                if temp_str[2] == '0' or temp_str[2] == '1' or temp_str[2] == '2':
                    sum_num += 1
                    temp_str += i
            else:
                sum_num += 1
                temp_str += i
        elif sum_num != 0:
            sum_num = 0
            temp_str = ''

        if sum_num == 8:
            if temp_str[0] == '1' or temp_str[0] == '2' and temp_str[2] == '0' or temp_str[2] == '1' or temp_str[2] == '2':
                temp_list.append(temp_str)
                sum_num = 0
                temp_str = ''
    return temp_list


def at_schoolnum(temp_list,memberList):
    temp_lis = []
    not_rec = temp_list
    for i in memberList:
        #print(i.id,i.name)
        for j in temp_list:
            #print(j)
            if j in i.name:
                print(i.id,i.name,j)
                temp_lis.append(i.id)
                not_rec.remove(j)
        #print("over")
    return temp_lis, not_rec


