import numpy as np
from keras import Model
from keras.layers import (Embedding, Dropout, Convolution1D, MaxPool1D, concatenate,
                          Bidirectional, LSTM)
from keras.layers import Input, Flatten, Dense
from keras.models import Sequential
from keras.utils.vis_utils import plot_model


def get_text_cnn(vocab_size, max_sequence_len, embedding_dim, num_classes, embedding_matrix=None):
    # 模型结构：词嵌入-卷积池化*3-拼接-全连接-dropout-全连接
    main_input = Input(shape=(max_sequence_len,))
    # 词嵌入（使用预训练的词向量）
    embedder = Embedding(vocab_size, embedding_dim, input_length=max_sequence_len,
                         weights=np.asarray([embedding_matrix]), trainable=False)
    embed = embedder(main_input)
    # 词窗大小分别为3,4,5
    cnn1 = Convolution1D(256, 3, padding='same', strides=1, activation='relu')(embed)
    cnn1 = MaxPool1D(pool_size=4)(cnn1)
    cnn2 = Convolution1D(256, 4, padding='same', strides=1, activation='relu')(embed)
    cnn2 = MaxPool1D(pool_size=4)(cnn2)
    cnn3 = Convolution1D(256, 5, padding='same', strides=1, activation='relu')(embed)
    cnn3 = MaxPool1D(pool_size=4)(cnn3)
    # 合并三个模型的输出向量
    cnn = concatenate([cnn1, cnn2, cnn3], axis=-1)
    flat = Flatten()(cnn)
    drop = Dropout(0.2)(flat)
    output = Dense(num_classes, activation='sigmoid')(drop)
    model = Model(inputs=main_input, outputs=output)
    return model


def get_bi_lstm(vocab_size, max_sequence_len, embedding_dim, num_classes, embedding_matrix=None):
    model = Sequential()
    model.add(Embedding(vocab_size, embedding_dim, input_length=max_sequence_len,
                        weights=np.asarray([embedding_matrix]),
                        trainable=False))
    model.add(Bidirectional(LSTM(256, dropout=0.2, recurrent_dropout=0.1, return_sequences=True)))
    model.add(Bidirectional(LSTM(256, dropout=0.2, recurrent_dropout=0.1)))
    model.add(Dense(num_classes, activation='sigmoid'))
    return model


def get_cnn_pair_rnn(vocab_size, max_sequence_len, embedding_dim, num_classes, embedding_matrix=None):
    """并联 cnn rnn
    # 模型结构：词嵌入-卷积池化-全连接 ---拼接-全连接
    #                -双向GRU-全连接
    :param vocab_size:
    :param max_sequence_len:
    :param embedding_dim:
    :param num_classes:
    :param embedding_matrix:
    :return:
    """
    weights = None
    # train_able=True
    if embedding_matrix:
        weights = np.asarray([embedding_matrix])
    model = Sequential()
    model.add(Embedding(vocab_size, embedding_dim, input_length=max_sequence_len,
                        weights=weights, trainable=True))
    sentence_input = Input(shape=(max_sequence_len,), dtype='float64')
    embed = Embedding(vocab_size, embedding_dim, input_length=max_sequence_len)(sentence_input)
    cnn = Convolution1D(256, 3, padding='same', strides=1, activation='relu')(embed)
    cnn = MaxPool1D(pool_size=4)(cnn)
    cnn = Flatten()(cnn)
    cnn = Dense(256)(cnn)
    rnn = Bidirectional(LSTM(256, dropout=0.2, recurrent_dropout=0.1))(embed)
    rnn = Dense(256)(rnn)
    con = concatenate([cnn, rnn], axis=-1)
    output = Dense(num_classes, activation='sigmoid')(con)
    model = Model(inputs=sentence_input, outputs=output)
    return model


def train():
    vocab_size = 1000
    max_sequence_len = 200
    embedding_dim = 200
    num_classes = 7
    embedding_matrix = None
    model = get_cnn_pair_rnn(vocab_size, max_sequence_len, embedding_dim, num_classes,
                             embedding_matrix=embedding_matrix)
    model.compile(
        loss="binary_crossentropy",  # 'binary_crossentropy',categorical_crossentropy
        optimizer='adam',
        metrics=['accuracy'],
    )
    model.summary()

    plot_model(model, to_file='model.png', show_shapes=True)


if __name__ == "__main__":
    train()
