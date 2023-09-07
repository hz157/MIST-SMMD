# 社交媒体多模态数据中提取城市洪涝灾害时空信息 - 社交媒体数据获取

<p align="left">🇨🇳 中文简体  |  <a title="中文简体" href="README_en.md">🇬🇧 English</a></p>

## 说明
通过查看网络请求发现s.weibo.com可返回具有文章编码的信息内容，m.weibo.cn可通过该编码请求具体数据，进而使用Python程序模拟浏览器请求，使用requests向微博发起检索请求。（**该方法需要登录微博获取微博的Cookie**)
通过服务器运行，获取特定关键字信息并将原始数据保存至数据库，在进行数据分析之时，将原始数据进行数据清洗（删除不必要的数据，例如HTML编码、emoji表情、微博话题等）

[//]: # ([![s.weibo.com]&#40;https://image.heiankyo.link:2096/i/2023/02/08/63e3410bd34aa.png&#41;]&#40;https://image.heiankyo.link:2096/i/2023/02/08/63e3410bd34aa.png&#41;)

[//]: # ([![m.weibo.cn]&#40;https://image.heiankyo.link:2096/i/2023/02/08/63e34137acf73.png&#41;]&#40;https://image.heiankyo.link:2096/i/2023/02/08/63e34137acf73.png&#41;)

## 关联Article
2023



## 人工智能库
> 支持GPU加速的人工智能库建议使用针对Nvidia Cuda加速版本

| 库  | 模型  | 作用       | 链接                                                                                         |
|----|----|----------|--------------------------------------------------------------------------------------------|
| spaCy |zh_core_web_md| NLP      | [spacy.io](https://spacy.io/)                                                              |
| Transformers | dimbat_disaster_distilbert | 灾害相关程度推测 | [sacculifer/dimbat_disaster_distilbert](https://huggingface.co/sacculifer/dimbat_disaster_distilbert) |
| Transformers | opus-mt-zh-en    | 翻译(中译英)  | [Helsinki-NLP/opus-mt-zh-en](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en)                                      |


### Spacy Models Install
需要使用zh_core_web_md模型, 请使用下述命令进行安装
```shell
python -m spacy download zh_core_web_md
```

### Transformers Models Git clone
```shell
git lfs install
git clone 'transformers Model huggingface url'

# if you want to clone without large files – just their pointers
# prepend your git clone with the following env var:
GIT_LFS_SKIP_SMUDGE=1
```

## 支持库列表
请使用下述命令进行安装支持库，中国境内建议使用清华大学镜像源（https://pypi.tuna.tsinghua.edu.cn/simple)
```shell
# 默认源安装
pip install -r requirements.txt
# 使用清华大学镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 项目结构
- Config
  - config.ini (配置信息，Cookie\数据库连接信息)
  - config.py (配置文件)
  - dev.py ()
  - prop.py ()
- Database
  - Mysql.py (数据库连接引擎)
- logs (运行日志)
- Main
- Model
  - models.py (ORM数据库模型)
- Network
  - Files.py (文件操作)
  - Sina.py (新浪微博API操作)
- static
  - output (输出文件)
- Utils
  - clean.py (数据清洗模块)
  - convert.py (格式转换模块)
  - logutils.py (日志模块)
  - nlputils.py (自然语言处理模块)
  - timeutils.py (时间模块)
- venv (Python 环境)

## 引用
- nlputils.py() 引用https://github.com/downdawn/Similarity