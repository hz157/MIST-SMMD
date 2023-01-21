import json
import os

"""
BIO Text convert ArcGis Json 
BIO form example:
今 B-Time
天 I-Time
是 O
除 B-Time
夕 I-Time
夜 I-Time

alter conversion Json form example:
{"id": 1, "text": "今天是除夕夜", labels:[[0,2,"Time“],[3,6,"Time"]]}
"""

# Global Param
splitKeyword = [] # Split Keyword 
outputFile = 'BIO_Convert/output/2023_01_21_stand_local.json' # json output file path
inputFile = [] # BIO input file Path, (allow multiple)
textLine = 1 # data line 
necessaryKeyword = [['Time', 'TIME', 'time'],
                    ['Local', 'local', 'LOC', 'loc', 'Loc', 'Localtion', 'location', 'address']]
standKeyword = ['TIME', 'LOC'] # output stand label



def TextBioConvertJson(file):
    """TextBioConvertJson
    读取BIO标注文本文件, 并转换为Json格式文本, 并将转换后的数据写入.json文件
    Read the BIO annotation text file, convert it to Json format text, and write the converted data into the .json file
    Args:
        file (_type_): BIO 标注文本文件
        file (_type_): BIO label text file
    """
    global textLine, splitKeyword # 全局变量 golbal param
    with open(file, 'r', encoding="utf-8") as f:
        text = '' # 原始文本内容
        label = [] # 单个NLP标签
        labels = [] # NLP标签集合
        isInner = 0 # Inner有效范围内
        # 遍历txt行数
        for line in f.readlines():
            # 判断是否空行，不为空行继续执行
            if line is not '\n':
                # 切割单行数据
                line = line.replace('\n','')
                lineSplit = line.split(splitKeyword[0])
                # 拼接原始字符串
                text = text + lineSplit[0]
                # 判断是否为Other，不为Other进入if
                if lineSplit[1] != 'O':
                    # 切割单行BIO
                    bioLabelSplit = lineSplit[1].split(splitKeyword[1])
                    # 判断是否为Begin
                    if bioLabelSplit[0] == 'B':
                        # 出现两个begin相连的情况，判断label当中是否有数据，有则进入else写入数据，并重新给label赋值起始位置
                        if not label:
                            label.append(len(text) - 1) # 赋值起始位置
                            tempLabel = bioLabelSplit[1] # label name
                        else:
                            label.append(len(text) - 1) # 赋值结束位置
                            label.append(tempLabel) # add label name
                            tempLabel = bioLabelSplit[1] # label name
                            if Legitimate(label):
                                labels.append(label) # 添加进总标签
                            label = []
                            label.append(len(text) - 1) # 赋值起始
                    # 判断是否为Inner
                    if bioLabelSplit[0] == 'I':
                        isInner = 1
                # 判断是否为Other，为Other为begin&end赋空值
                else:
                    # 判断前一行是否为Inner
                    if isInner == 1:
                        isInner = 0 # 重置flag
                        label.append(len(text) - 1) # 赋值结束位置
                        label.append(tempLabel) # 添加NLP标签
                        if Legitimate(label):
                            labels.append(label) # 添加进总标签
                        label = []
            # 为空行，结束单条数据转换，并给textline+1，清空变量数据
            else:
                if labels:
                    print(f'正在处理第{textLine}条数据')
                    textLineDic = {'id': textLine, 'text': text, 'labels': labels, "Comments":[]} # 单条数据DICT
                    WriteJson(textLineDic)
                    textLine = textLine + 1 # 条数累加
                # 重置原始文本与NLP标签集合
                text = ''
                labels = []



def Legitimate(label: list):
    """Legitimate
    验证标签数据有效性, 是否为3位参数, 并且是否需要该数据
    Verify the validity of the tag data, whether it is a 3-digit parameter, and whether the data is required
    Args:
        label (list): 单条标签
        label (list): single label

    Returns:
        _type_: True or False True 符合要求, False 不符合要求
        _type_: True or False True is meet the requirements, False is non-compliant
    """
    if len(label) == 3:
        for i in range(0,len(necessaryKeyword)):
            if label in necessaryKeyword[i]:
                label[2] = standKeyword[i]
                return True
    return False



def ReadJsonFile(file):
    global textLine
    with open(file, 'r', encoding="utf-8") as f:
        for line in f.readlines():
            print(f'正在处理第{textLine}条数据')
            json_data = json.loads(line)
            analysis = JsonConvertJson(textLine, json_data)
            textLine = textLine + 1
            WriteJson(analysis)




def JsonConvertJson(id: int, json_data: dict=None):
    data_dicr = {'id': id}
    tagList = []
    # 为返回字典赋值Text
    data_dicr['text'] = json_data['text']
    # 拆分原有labels
    labels = json_data['label']
    # 遍历字典Key
    for i in labels:
        # 遍历二级字典Key
        for j in labels[i]:
            # label数据
            labelList = []
            # 分割二级字典数据
            number = 0
            for position in str(labels[i][j]).replace('[','').replace(']','').split(','):
                if number == 1:
                    number = 0
                    labelList.append(int(position) + 1)
                else:
                    number = number + 1
                    labelList.append(int(position))
            # 添加label Title
            labelList.append(i)
            # 添加到总目录
            tagList.append(labelList)
    # 为返回字典labels赋值
    data_dicr['labels'] = tagList
    data_dicr['Comments'] = []
    # 返回数据
    return data_dicr


def WriteJson(data: dict):
    """WriteText 
    向输出文件追加Json数据
    Args:
        data (dict): 单行数据字典
    """
    mode = 'a'
    if not os.path.exists(outputFile):
        mode = 'w+'
    Note = open(outputFile, mode, encoding = "utf-8")
    jsonData = json.dumps(data, ensure_ascii=False)
    Note.write(f'{jsonData}\n') #\n 换行符
    Note.close # 关闭文件



def GetSplitChar(file: str):
    print(file)
    """GetSplitChar
    随机读取100-300行, 判断是以Tab或者是以Space进行分割BIO的, label是以-或是以_分割
    Args:
        file (_type_): 文件位置
    """
    global splitKeyword
    splitKeyword = [] # 分割字符串关键字 全局变量 Split Keyword Global param
    with open(file, 'r', encoding="utf-8") as f:
        while not splitKeyword:
            for line in f.readlines():
                splitLine = list(line)
                # 只有当有数据的时候才进行判断
                if len(splitLine) > 4:
                    splitKeyword.append(splitLine[1])
                    splitKeyword.append(splitLine[3])
                    return



if __name__ == '__main__':
    textFolder = 'BIO_Convert/dataset/txt' # 原始数据TEXT文件路径 text origin file path 
    for filename in os.listdir(textFolder):
        GetSplitChar(f'{textFolder}/{filename}')
        TextBioConvertJson(f'{textFolder}/{filename}')
    jsonFolder = 'BIO_Convert/dataset/json' # 原始数据JSON文件数据 json origin file path
    for filename in os.listdir(jsonFolder):
        ReadJsonFile(f'{jsonFolder}/{filename}')

