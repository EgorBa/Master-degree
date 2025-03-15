import re
import string
import numpy as np


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)


class word2vec:
    def __init__(self):
        self.loss = None
        self.w2 = None
        self.w1 = None
        self.index_word = None
        self.word_index = None
        self.words_list = None
        self.v_count = None
        self.n = 20
        self.eta = 0.01
        self.epochs = 10
        self.window_size = 4

    def generate_training_data(self, data):
        word_counts = {}
        for row in data:
            for word in row:
                if word not in word_counts.keys():
                    word_counts[word] = 1
                else:
                    word_counts[word] += 1

        self.v_count = len(word_counts.keys())
        self.words_list = sorted(list(word_counts.keys()), reverse=False)
        self.word_index = dict((word, i) for i, word in enumerate(self.words_list))
        self.index_word = dict((i, word) for i, word in enumerate(self.words_list))

        training_data = []
        for row in data:
            sent_len = len(row)
            for i, word in enumerate(row):
                w_target = self.word2onehot(word)
                w_context = []
                for j in range(i - self.window_size, i + self.window_size + 1):
                    if j != i and sent_len - 1 >= j >= 0:
                        w_context.append(self.word2onehot(row[j]))
                training_data.append([w_target, w_context])
        return training_data

    def word2onehot(self, word):
        word_vec = [0 for i in range(0, self.v_count)]
        word_index = self.word_index[word]
        word_vec[word_index] = 1
        return word_vec

    def forward_pass(self, x):
        h = np.dot(self.w1.T, x)
        u = np.dot(self.w2.T, h)
        y_c = softmax(u)
        return y_c, h, u

    def backprop(self, e, h, x):
        dl_dw2 = np.outer(h, e)
        dl_dw1 = np.outer(x, np.dot(self.w2, e.T))
        self.w1 = self.w1 - (self.eta * dl_dw1)
        self.w2 = self.w2 - (self.eta * dl_dw2)
        pass

    def train(self, training_data):
        self.w1 = np.random.uniform(-0.8, 0.8, (self.v_count, self.n))
        self.w2 = np.random.uniform(-0.8, 0.8, (self.n, self.v_count))
        for i in range(0, self.epochs):
            self.loss = 0
            for w_t, w_c in training_data:
                y_pred, h, u = self.forward_pass(w_t)
                EI = np.sum([np.subtract(y_pred, word) for word in w_c], axis=0)
                self.backprop(EI, h, w_t)
                self.loss += -np.sum([u[word.index(1)] for word in w_c]) + len(w_c) * np.log(np.sum(np.exp(u)))
        pass

    def word_vec(self, word):
        w_index = self.word_index[word]
        v_w = self.w1[w_index]
        return v_w


def clean(inp: str) -> str:
    inp = inp.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    inp = re.sub(r'\s+', ' ', inp.lower())
    return inp


def train(data: str):
    data = [clean(data).split(" ")]
    w2v = word2vec()
    training_data = w2v.generate_training_data(data)
    w2v.train(training_data)
    d = {}
    for k in data[0]:
        d[k] = w2v.word_vec(k)
    return d


print(train("kek lol"))
