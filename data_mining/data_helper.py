import glob
import json
import os
import sys

import gc
import pandas as pd

cur_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(cur_dir)
data_dir = os.path.join(root_dir, "data")

print("data_dir :{}".format(data_dir))

sys.path.append(root_dir)


def load_gushiwenwang_poet():
    """"""
    # poet_patten = os.path.join(data_dir, "poetry-master", "poet", "*.json")  # 诗人
    poetry_patten = os.path.join(data_dir, "poetry-master", "poetry", "*.json")  # 诗词
    # poet_paths = glob.glob(poet_patten) + glob.glob(poetry_patten)
    poet_paths = glob.glob(poetry_patten)
    poems = []
    for poet_path in poet_paths:
        with open(poet_path, "r", encoding="utf-8") as f:
            poem_json = json.load(f)
        # import ipdb
        # ipdb.set_trace()
        poem_dict = {"title": poem_json["name"],
                     "dynasty": poem_json.get("dynasty", ""),
                     "author": poem_json.get("poet", {}).get("name", ""),
                     "content": poem_json["content"].replace("<br>", "")}
        poems.append(poem_dict)
    return poems


def load_chinese_poetry():
    def parse(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            poem_jsons = json.load(f)
        base_name = os.path.basename(json_path)
        type, dynasty, _, _ = base_name.split(".")
        dynasty = {"song": "宋", "tang": "唐"}[dynasty]
        poem_dicts = []
        for poem_json in poem_jsons:
            if type == "ci":
                title = poem_json["rhythmic"]
            else:
                assert type == "poet"
                title = poem_json["title"]
            poem_dict = {"title": title, "dynasty": dynasty,
                         "author": poem_json["author"],
                         "content": "".join(poem_json["paragraphs"]),
                         "type": type}
            poem_dicts.append(poem_dict)
        return poem_dicts

    chinese_poetry_dir = os.path.join(data_dir, "chinese-poetry")
    ci_dir = os.path.join(chinese_poetry_dir, "ci")
    poetrys = []
    for ci_path in glob.glob(os.path.join(ci_dir, "ci.song.*.json")):
        poetrys.extend(parse(ci_path))
    shi_dir = os.path.join(chinese_poetry_dir, "json")
    for shi_path in glob.glob(os.path.join(shi_dir, "poet.*.json")):
        poetrys.extend(parse(shi_path))
    return poetrys


def load_Poetry():
    Poetry_dir = os.path.join(data_dir, "Poetry")
    data_dfs = [pd.read_csv(csv) for csv in glob.glob(os.path.join(Poetry_dir, "*.csv"))]
    data_df = pd.concat(data_dfs)
    return data_df


def preprocess():
    """ 多份数据整理成需要的格式
    [chinese-poetry:<br>最全中华古诗词数据库](https://github.com/chinese-poetry/chinese-poetry) | 唐宋两朝近一万四千古诗人,<br> 接近5.5万首唐诗加26万宋诗. <br> 两宋时期1564位词人，21050首词 | 只有作者、标题、平仄；<br>无分类赏析打分等信息。 | [诗词周历](https://shici.store/poetry-calendar/) |
    [poetry:古诗词数据库](https://github.com/hujiaweibujidao/poetry) | 2017年从[古诗文网](http://www.gushiwen.org/)爬取,<br>73281首古诗词和3156个诗人的详细数据 | 有赏析分类点赞数目                               | [诗鲸](http://site.pocketpoetry.club)            |
    [Poetry](https://github.com/Werneror/Poetry)                 | 非常全的古诗词数据，收录了从先秦到现代的共计85万余首古诗词。 |         |                                         |                                                  |
    :return:
    """
    data_df = load_Poetry()
    poems = load_chinese_poetry()
    gushiwenwang_poems = load_gushiwenwang_poet()
    # data_dict = defaultdict(list)
    data_dict = {"题目": [], "朝代": [], "作者": [], "内容": []}
    for poem in poems + gushiwenwang_poems:
        # for k, v in poem.items():
        data_dict["题目"].append(poem["title"])
        data_dict["朝代"].append(poem["dynasty"])
        data_dict["作者"].append(poem["author"])
        data_dict["内容"].append(poem["content"])
    poem_df = pd.DataFrame.from_dict(data_dict)
    gc.collect()
    data_df = pd.concat([data_df, poem_df])
    # https://jamesrledoux.com/code/drop_duplicates
    data_df.drop_duplicates(subset=["内容"], keep="first", inplace=True)
    data_df.dropna(subset=['内容'], inplace=True)
    data_df["内容"] = data_df["内容"].replace("<.*?>|—", "", regex=True)
    data_df["作者"] = data_df["作者"].replace({"陸游": "陆游"})
    data_df["朝代"] = data_df["朝代"].replace({
        "秦": "先秦",
        "两汉": "汉",
        "隋代": "隋", "隋末唐初": "隋", '唐代': "唐", "魏晋末南北朝初": "魏晋",
        "唐末宋初": "宋", '宋代': "宋",
        "宋末元初": "宋", "宋末金初": "宋",
        "金朝": "金", "金末元初": "金", "元代": "元", "元末明初": "元",
        "明代": "明", "明末清初": "明",
        "清代": "清", "清末近现代初": "近现代",
        "清末民国初": "民国", "民国末当代初": "民国",
        "近现代末当代初": "近代", "近现代": "近代", "现代": "近代"
    })
    sorter = ["先秦", "汉", "魏晋", "隋", "唐", "五代", "宋", "辽", "金", "元", "明", "清", "民国", "近代", "当代", "未知"]
    data_df["朝代"] = data_df["朝代"].astype("category")
    data_df["朝代"].cat.set_categories(sorter, inplace=True)
    data_df.to_csv(os.path.join(data_dir, "poems.csv"), index=False)
    return data_df


class DataHelper(object):
    def __init__(self):
        pass

    def load_poetry(self):
        pass


if __name__ == "__main__":
    # load_Poetry()
    # load_chinese_poetry()
    preprocess()
