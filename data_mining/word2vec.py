import os
# pprint = p.PrettyPrinter(indent=2)
import pprint

import pandas as pd
from gensim.models import word2vec

cur_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(cur_dir)
data_dir = os.path.join(root_dir, "data")

train_path = os.path.join(data_dir, "train.txt")

print("data_dir :{}".format(data_dir))


def prepare():
    data_path = os.path.join(data_dir, "poems.csv")
    data_df = pd.read_csv(data_path)
    # text = "".join(data_df["内容"].values)
    train_path = os.path.join(data_dir, "train.txt")
    with open(train_path, "w", encoding="utf-8") as f:
        text = "\n".join([" ".join(poem) for poem in data_df["内容"].values])
        f.write(text)


def train(file_path):
    # 加载语料
    sentences = word2vec.Text8Corpus(file_path)
    # 训练模型
    print(file_path)
    model = word2vec.Word2Vec(sentences)
    # 保存模型
    model_name = os.path.basename(file_path).split(".")[0]
    model.save('{}.model'.format(model_name))
    # 选出最相似的10个词
    for e in model.most_similar(positive=['春'], topn=10):
        print(e[0], e[1])
    return model


def main():
    prepare()
    train()


if __name__ == "__main__":
    main()
    exit(1)
    # 加载模型
    model = word2vec.Word2Vec.load('poem.model')
    for word in ["春", '思乡', "梅", "冬", "中秋"]:
        res = model.most_similar(positive=[word], topn=10)
        print(word)
        pprint.pprint(res)
        print("-" * 10)
