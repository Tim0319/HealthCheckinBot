import time, random
print("真心话大冒险 V1.0 Truth or Dare 制作：Tim")


def tord():
    content = ''
    s = eval(time.strftime("%Y%m%d%H%M", time.gmtime()))
    '''s = s * eval(a)
    s = s * eval(b)'''
    # print("等待8秒出结果")
    # time.sleep(8)
    # print("种子是{}".format(s))
    # random.seed(s)
    if str(s)[-2] in ["1", "3", "5", "7", "9"]:
        file = open(r"module\tord\truth.txt", encoding = "UTF-8")
        content += "---真心话---\n"
    else:
        file = open(r"module\tord\dare.txt", encoding = "UTF-8")
        content += "---大冒险---\n"
    lis = []
    for i in file.readlines():
        lis.append(i)
    rand = random.randint(0, len(lis) - 1)
    # content += "\n神秘数值是{}\n".format(rand + 1)
    file.close()
    content += lis[rand][:-1]
    # time.sleep(60)
    return content
