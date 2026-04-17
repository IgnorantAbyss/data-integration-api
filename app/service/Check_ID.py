def get_ID_char(IDstring):
    # 第一個數字非1或2不合規
    if IDstring[0] not in ['1','2'] or len(IDstring) != 9:
        return []
    # 加權後的字母數字映射字典
    letter_dict = {1: 'A', 10: 'B', 19: 'C', 28: 'D', 37: 'E', 
                   46: 'F', 55: 'G', 64: 'H', 39: 'I', 73: 'J', 
                   82: 'K', 2: 'L', 11: 'M', 20: 'N', 48: 'O', 
                   29: 'P', 38: 'Q', 47: 'R', 56: 'S', 65: 'T', 
                   74: 'U', 83: 'V', 21: 'W', 3: 'X', 12: 'Y', 30: 'Z'}
    # 直接產出ID加權後數字
    ID_sum = sum([int(IDstring[i])*(8-i) for i in range(8)])
    # 檢查碼
    check_num = int(IDstring[-1])
    
    candidate_character = []
    for k,v in letter_dict.items():
        if (ID_sum + k + check_num) % 10 == 0:
            candidate_character.append(v)

    return candidate_character

# if __name__ == '__main__':
#     import re
#     a = '''A=10  台北市       J=18 新竹縣       S=26  高雄縣
#         B=11  台中市       K=19 苗栗縣       T=27  屏東縣
#         C=12  基隆市       L=20 台中縣       U=28  花蓮縣
#         D=13  台南市       M=21 南投縣       V=29  台東縣
#         E=14  高雄市       N=22 彰化縣     * W=32  金門縣
#         F=15  台北縣     * O=35 新竹市       X=30  澎湖縣
#         G=16  宜蘭縣       P=23 雲林縣       Y=31  陽明山特區
#         H=17  桃園縣       Q=24 嘉義縣     * Z=33  連江縣
#         * I=34  嘉義市       R=25 台南縣 '''
#     b = re.sub(r'[\u4e00-\u9fff]', '', a)
#     b = b.replace('*','')
#     c = b.split()
#     print(c)
#     c = sorted(c,key=lambda x:x[0])
#     letter_dict = {}
#     for i in c:
#         d = i.split('=')
#         # print(d[0],d[1])
#         n1 = int(d[1][0]) * 1
#         n2 = int(d[1][1]) * 9
        
#         letter_dict[n1+n2] = d[0]
#     print(letter_dict)
#     print((get_ID_char('123456789')))

