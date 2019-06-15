from gensim.models import word2vec

from data_mining.config import Config


class DataHelper(object):
    def __init__(self):
        self.init()

    def init(self):
        self.model = word2vec.Word2Vec.load(Config.w2v_model_path)

    def load_poetry(self):
        pass
