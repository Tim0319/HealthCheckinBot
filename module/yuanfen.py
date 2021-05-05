#缘分.py
#制作：海市蜃楼
import time
import random
print("缘分计算工具 V1.0 仅供娱乐参考，娱乐插件")
t = time.ctime()
ran = random.uniform(90,100)
'''
a = input("请输入男方姓名：")
b = input("请输入女方姓名：")
'''

def yf(a,b):
    try:
        global ran
        lena = len(a)
        lenb = len(b)
        sa = 0
        sb = 0
        for i in range(lena):
            sa = sa + ord(a[i])
        for i in range(lenb):
            sb = sb + ord(b[i])
        sa = str(sa//lena)
        sb = str(sb//lenb)
        def cal(a):
            b = 0
            for i in a:
                b += eval(i)
            return b
        while len(sa)>2:
            sa = str(cal(sa))
        while len(sb)>2:
            sb = str(cal(sb))
        if eval(sa)<eval(sb):
            s = eval(sa)/eval(sb)* ran
        else:
            s = eval(sb)/eval(sa)* ran
        if a == '陈致远' and b == '余芷若' or a == '小陈' and b == '小余':
            s = 99
            ran = 99.999
            temp = "{}和{}真配，赶紧在一起算了，老子酸了，嘤嘤嘤\n".format(a,b)
        else:
            if s >= 95:
                temp = "{}和{}真配，赶紧在一起算了，老子酸了，嘤嘤嘤\n".format(a,b)
            elif s > 70:
                temp = "{}和{}缘份还行，嘻嘻嘻\n".format(a,b)
            else:
                temp = "{}和{}缘份一般，嘿嘿嘿\n".format(a,b)
        s = 100-(100-s)*0.70
        temp += "以下为结果".center(26, '-') + '\n'
        temp += "小哥哥 {} 的神秘值为：{}\n小姐姐 {} 的神秘值为：{}\n".format(a,sa,b,sb)
        temp += "你们的缘分指数是{:.2f}%\n此刻的神秘代码：{}\n计算时间：{}\n".format(s,ran,t)
        temp += "".center(28, '-')
        return temp
    except:
        return "请按照规范输入，比如说\n测缘分 小明 小红\n空格分隔 第一个是小哥哥的名字 第二个是小姐姐的名字"

'''
print()
print("以下为结果".center(35,'-'))
print()
print("小哥哥的神秘值为：{}\n小姐姐的神秘值为：{}\n你们的缘分指数是{:.2f}%\n此刻的神秘代码：{:.2f}\n计算时间：{}\n".format(sa,sb,s,ran,t))
print("".center(40,'-'))
input()
'''