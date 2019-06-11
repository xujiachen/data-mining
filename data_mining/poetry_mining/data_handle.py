import os
import sys

cur_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(cur_dir)
data_dir = os.path.join(root_dir, "data")

sys.path.append(root_dir)


def preprocess():
    """ 多份数据整理成需要的格式
    [chinese-poetry:<br>最全中华古诗词数据库](https://github.com/chinese-poetry/chinese-poetry) | 唐宋两朝近一万四千古诗人,<br> 接近5.5万首唐诗加26万宋诗. <br> 两宋时期1564位词人，21050首词 | 只有作者、标题、平仄；<br>无分类赏析打分等信息。 | [诗词周历](https://shici.store/poetry-calendar/) |
    [poetry:古诗词数据库](https://github.com/hujiaweibujidao/poetry) | 2017年从[古诗文网](http://www.gushiwen.org/)爬取,<br>73281首古诗词和3156个诗人的详细数据 | 有赏析分类点赞数目                               | [诗鲸](http://site.pocketpoetry.club)            |
    [Poetry](https://github.com/Werneror/Poetry)                 | 非常全的古诗词数据，收录了从先秦到现代的共计85万余首古诗词。 |         |                                         |                                                  |
    :return:
    """
    poetry1_dir = os.path.join(data_dir, "chinese-poetry")
    poetry2_dir = os.path.join(data_dir, "poetry")
    poetry3_dir = os.path.join(data_dir, "Poetry")


class DataHelper(object):
    def __init__(self):
        pass

    def load_poetry(self):
        pass
