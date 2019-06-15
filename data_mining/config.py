import os

cur_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(cur_dir)
data_dir = os.path.join(root_dir, "data")


class Config:
    w2v_model_path = os.path.join(data_dir, "model.png")
