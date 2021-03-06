# -*- coding: utf-8 -*-
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import jieba
import re
PAD_ID = 0
UNK_ID=1
_PAD="_PAD"
_UNK="UNK"

imprisonment_mean=26.2
imprisonment_std=33.5

def token_string_as_list(string,tokenize_style='word'):
    #string=string.decode("utf-8")
    string=replace_money_value(string)  #TODO add normalize number ADD 2018.06.11

    length=len(string)
    if tokenize_style=='char':
        listt=[string[i] for i in range(length)]
    elif tokenize_style=='word':
        listt=jieba.lcut(string)
    listt=[x for x in listt if x.strip()]
    return listt

def replace_money_value(string):
    moeny_list = [1,2,5,7,10, 20, 30,50, 100, 200, 500, 800,1000, 2000, 5000,7000, 10000, 20000, 50000, 80000,100000,200000, 500000, 1000000,3000000,5000000,1000000000]
    double_patten = r'\d+\.\d+'
    int_patten = r'[\u4e00-\u9fa5,，.。；;]\d+[元块万千百十余，,。.;；]'
    doubles=re.findall(double_patten,string)
    ints=re.findall(int_patten,string)
    ints=[a[1:-1] for a in ints]
    #print(doubles+ints)
    sub_value=0
    for value in (doubles+ints):
        for money in moeny_list:
            if money >= float(value):
                sub_value=money
                break
        string=re.sub(str(value),str(sub_value),string)
    return string

def pad_truncate_list(x_list, maxlen, value=0,truncating='pre',padding='pre'):
    """
    :param x_list:e.g. [1,10,3,5,...]
    :return:result_list:a new list,length is maxlen
    """
    result_list=[0 for i in range(maxlen)] #[0,0,..,0]
    length_input=len(x_list)
    if length_input>maxlen: #need to trancat===>no need to pad
        start_point = (length_input - maxlen)
        x_list=x_list[start_point:]
        for i, element in enumerate(x_list):
            result_list[i] = element
    else:#sequence is to short===>need to pad something===>no need to trancat. [1,2,3], max_len=1000.
        x_list.reverse() #[3,2,1]
        for i in range(length_input):
            result_list[i] = x_list[i]
        result_list.reverse()
    return result_list

#x_list=[1,2,3] #[0, 0, 0, 0, 0, 0, 0, 1, 2, 3]
#x_list=[1,2,3,4,5,6,7,8,9,10,11,12,13]#===>[4,5,6,7,8,9,10,11,12,13]
#result_list=pad_truncate_list(x_list, 10, value=0,truncating='pre',padding='pre')
#print(result_list)



def load_word_vocab(file_path):
    """
    load vocab of word given file path
    :param file_path:
    :return: a dict, named:vocab_word2index
    """
    file_object=open(file_path,mode='r') #TODO add encoding='utf8' for version python3
    lines=file_object.readlines()
    vocab_word2index={}
    vocab_word2index[_PAD] = PAD_ID
    vocab_word2index[_UNK] = UNK_ID
    for i,line in enumerate(lines):
        line=line.decode("utf-8").strip() #TODO add .decode("utf-8") for python 2.7
        if "::" in line:
            word=":"
        else:
            word,_=line.split(":") #wor,_="元:272339"
        vocab_word2index[word] = i + 2
    return vocab_word2index

def load_label_dict_accu(file_path):
    """
     load vocab of label given file path
     :param file_path:
     :return: a dict, named:label2index_dict
     """
    file_object = open(file_path, mode='r') #TODO add encoding='utf8' for version python 3
    lines = file_object.readlines()
    label2index_dict = {}
    for i, label in enumerate(lines):
        label = label.decode("utf-8").strip() #TODO .decode("utf-8") for python 2.7
        label2index_dict[label] = i
    return label2index_dict

def load_label_dict_article(file_path):
    """
     load vocab of label given file path
     :param file_path:
     :return: a dict, named:label2index_dict
     """
    file_object = open(file_path, mode='r') #TODO add  encoding='utf8' for version python3
    lines = file_object.readlines()
    label2index_dict = {}
    for i, label in enumerate(lines):
        label = int(label.strip())
        label2index_dict[label] = i
    return label2index_dict


big_feature_list=[]
feature_list_0 = [u'从轻', u'减轻', u'从重', u'坦白', u'自首', u'谅解', u'认罪', u'数罪', u'并罚', u'主动', u'投案', u'如实', u'供述', u'和解',u'轻伤', u'重伤', u'死亡', u'轻微伤', u'减轻', u'处罚', u'巨大']
big_feature_list.append(feature_list_0)
# 0.非法收购、运输、加工、出售国家重点保护植物、国家重点保护植物制品:0.0
feature_list_1 = [u'林业', u'红豆杉', u'株', u'棵', u'树', u'二级', u'保护', u'植物']
big_feature_list.append(feature_list_1)
# 1.经济犯:0.0
feature_list_2 = [u'假', u'虚', u'销售', u'盗版', u'非法', u'出版', u'营利', u'假药', u'虚构', u'合同', u'生成', u'假冒', u'虚开', u'增值税']
big_feature_list.append(feature_list_2)
# 2.爆炸:0.0
feature_list_3 = [u'爆炸', u'火', u'烧毁', u'公共安全', u'爆破', u'爆', u'炸药', u'制造', u'制', u'扑灭', u'点燃', u'炸']
big_feature_list.append(feature_list_3)
# 3.洗钱:0.0
feature_list_4 = [u'虚假', u'投资', u'隐瞒', u'掩盖', u'银行', u'账户', u'金融', u'管理', u'秩序', u'非法', u'吸收', u'公众', u'存款', u'违法', u'所得', u'转账', u'合法', u'收益', u'资金']
big_feature_list.append(feature_list_4)
# 4.打击报复证人:0.0
feature_list_5 = [u'证', u'怨', u'证人', u'怨气', u'记恨', u'证实', u'证人', u'报复', u'举报', u'指证', u'作证', u'公安机关', u'判刑', u'一案',u'出庭', u'怀恨']
big_feature_list.append(feature_list_5)
# 5.过失损坏广播电视设施、公用电信设施:0.0
feature_list_6 = [u'光缆', u'挖', u'断', u'挖断', u'挖掘机', u'施工', u'驾驶', u'挖掘', u'中断', u'通信', u'电信', u'移动', u'设施', u'损失',u'长达', u'小时', u'分钟']
big_feature_list.append(feature_list_6)
# 6.非法制造、买卖、运输、储存危险物质:0.0
feature_list_7 = [u'非法', u'买卖', u'销售', u'运输', u'储存', u'剧毒', u'毒', u'危险', u'物质', u'成分', u'老鼠', u'鼠', u'药', u'危险', u'化学',u'鉴定', u'中心', u'克', u'公斤']
big_feature_list.append(feature_list_7)
# 7.过失投放危险物质:0.0
feature_list_8 = [u'过失投放危险物质', u'过失', u'投放', u'危险', u'物质', u'农药', u'动物', u'死亡', u'毒', u'羊', u'检出', u'误食', u'为', u'为了防',u'为了', u'为防', u'中毒', u'玉米', u'粒']
big_feature_list.append(feature_list_8)
# 8.高利转贷:0.0 --》套取金融机构信贷资金高息转借他人
feature_list_9 = [u'套取金融机构信贷资金高息转借他人', u'套取', u'金融', u'机构', u'信贷', u'资金', u'高息', u'转借', u'利息', u'月利', u'虚构', u'合同', u'贷款', u'欺骗', u'银行', u'房子', u'房屋', u'转贷', u'转借', u'高利', u'非法', u'获']
big_feature_list.append(feature_list_9)
# 9.虐待被监管人:0.0
feature_list_10 = [u'监管', u'监室', u'看守所', u'看守', u'殴打', u'打', u'在押', u'监', u'民警', u'轻伤', u'罪犯', u'管教']
big_feature_list.append(feature_list_10)
# 10.巨额财产来源不明:0.0
feature_list_11 = [u'说明合法来源', u'不能', u'说明', u'来源', u'明显', u'超过', u'合法', u'收入', u'职务', u'担任', u'便利']
big_feature_list.append(feature_list_11)
# 11.金融凭证诈骗
feature_list_12 = [u'非法占有为目的', u'非法', u'占有', u'目的', u'存单', u'数额', u'巨大', u'伪造', u'虚构', u'储蓄', u'凭证', u'合同', u'事实']
big_feature_list.append(feature_list_12)
# 12.聚众冲击国家机关:0.0
feature_list_13 = [u'派出所', u'公安局', u'民警', u'殴打', u'无法', u'正常', u'聚众', u'冲击国家机关', u'冲击', u'国家', u'机关', u'工作', u'进行',u'大门', u'交通', u'政府', u'无法正常工作']
big_feature_list.append(feature_list_13)
# 13.伪造货币:0.0
feature_list_14 = [u'伪造有价票证罪', u'伪造', u'货币', u'面值', u'面额', u'邮票', u'伪', u'仿', u'假', u'假币', u'加工', u'制作', u'印制', u'印刷',u'鉴定', u'人民币']
big_feature_list.append(feature_list_14)
# 14.非法收购、运输、出售珍贵、濒危野生动物、珍贵、濒危野生动物制品:0.0
feature_list_15 = [u'非法', u'收购', u'运输', u'出售', u'珍贵', u'濒危', u'野生', u'动物', u'制作', u'国家', u'重点', u'保护', u'制品', u'牙',u'角']
big_feature_list.append(feature_list_15)
# 15.徇私舞弊不移交刑事案件:0.0
feature_list_16 = [u'徇私舞弊', u'行政执法', u'移交', u'司法机关', u'担任', u'应当', u'未', u'没有', u'明知', u'', u'公安', u'伪造']
big_feature_list.append(feature_list_16)
# 16.窝藏、转移、收购、销售赃物:0.0
feature_list_17 = [u'赃物', u'购', u'收购', u'购买', u'卖', u'销售', u'明知', u'盗窃', u'抢', u'窃']
big_feature_list.append(feature_list_17)
# 17.强迫卖淫
feature_list_18 = [u'卖淫', u'宾馆', u'发廊', u'限制', u'强迫', u'逃跑', u'逃', u'骗', u'旅馆', u'旅店', u'威胁']
big_feature_list.append(feature_list_18)
# 17.利用影响力受贿:0.0
feature_list_19 = [u'利用', u'贿', u'任', u'职权', u'职位', u'职务', u'便利', u'行贿', u'贿赂', u'收受', u'工程', u'项目']
big_feature_list.append(feature_list_19)
# 18.以危险方法危害公共安全:0.0
feature_list_20 = [u'撞', u'驶', u'相撞', u'行驶', u'车', u'方向盘', u'公交车', u'死亡', u'受伤', u'事故', u'乙醇', u'血液', u'煤气', u'逃逸', u'火', u'燃']
big_feature_list.append(feature_list_20)
# 19.破坏交通工具:0.0
feature_list_21 = [u'交通工具', u'交通', u'维修', u'故意', u'费用', u'车', u'车辆', u'破坏', u'驶', u'故障', u'事故', u'司法', u'鉴定', u'损']
big_feature_list.append(feature_list_21)
# 20.帮助毁灭、伪造证据:0.0
feature_list_22 = [u'帮助', u'毁灭', u'伪造', u'证据', u'藏', u'毁', u'抛', u'修', u'扔', u'帮助', u'拆', u'虚']
big_feature_list.append(feature_list_22)
# 21.聚众哄抢:0.0
feature_list_23 = [u'聚众哄抢', u'哄抢', u'聚众', u'抢', u'价值']
big_feature_list.append(feature_list_23)
# 22.走私:0.0
feature_list_24 = [u'走私', u'境', u'边境', u'入境', u'出境', u'海关', u'缉私', u'进出口', u'检验', u'检疫', u'查获']
big_feature_list.append(feature_list_24)
# 23.过失以危险方法危害公共安全:0.0
feature_list_25 = [u'过失', u'电', u'野', u'触电', u'电网', u'轻信', u'死', u'野猪', u'信', u'亡']
big_feature_list.append(feature_list_25)
# 24.窃取、收买、非法提供信用卡信息:0.0
feature_list_26 = [u'窃取', u'购买', u'信用卡', u'信息', u'银行', u'银行卡', u'密码', u'骗', u'诈骗', u'器', u'结账']
big_feature_list.append(feature_list_26)
# 25.挪用特定款物:0.0
feature_list_27 = [u'挪用', u'移民', u'拨', u'拨付', u'扶持', u'其余', u'专项', u'扶贫', u'结余', u'领', u'款']
big_feature_list.append(feature_list_27)

def get_data_mining_features(input_string,dimension=28):
    """
    get data mininig features from input stirng(a law cases) using rules.
    :param input: input_string is a law case.
    :return: a 50 dimension vector
    """
    feature_list_return=[0 for j in range(dimension)]
    for i,sub_list in enumerate(big_feature_list):
        sub_sum=activate_or_not_return_sum(input_string, sub_list)
        #print(i,sub_sum)
        feature_list_return[i]=float(sub_sum)/float(len(sub_list))
    return feature_list_return


def activate_or_not_return_sum(input_string,feature_list):
    sum=0
    for keyword in feature_list:
        if keyword in input_string:
            sum=sum+1
    return sum
def one_hot(strings,listt):
    one_hot_feature=[0 for i in range(len(listt))]
    for i,element in enumerate(listt):
        if element in strings:
            one_hot_feature[i]=1
    return one_hot_feature


#input_string=u'门源县人民检察院指控，2014年7月，被告人杨某某从县农牧水利和扶贫开发局领出某乡某村的7.8万元扶贫款，缴纳2964元税金后，将剩余的66900元专项款擅自以平均每户300元发给本村223户村民手中，并与马某甲、包某甲、妥某某等人将下剩的8136元用于报销上访、调查农机具价格产生的费用。针对上述指控的事实，公诉机关向法庭宣读、出示了书证，证人证言，被告人供述等证据材料，指控被告人杨某某的行为触犯了《中华人民共和国刑法》××之规定，构成××'
#result=get_data_mining_features(input_string)
#print("result:",result)