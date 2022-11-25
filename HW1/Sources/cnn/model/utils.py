import numpy as np


def pad_inputs(X, pad):
    return np.pad(X, ((0, 0), (pad[0], pad[0]), (pad[1], pad[1]), (0, 0)), 'constant')


def get_batches(data, labels=None, batch_size=256, shuffle=True):
    N = data.shape[1] if len(data.shape) == 2 else data.shape[0]
    num_batches = N // batch_size
    if len(data.shape) == 2:
        data = data.T
    if shuffle:
        shuffled_indices = np.random.permutation(N)
        data = data[shuffled_indices]
        labels = labels[:, shuffled_indices] if labels is not None else None
    if num_batches == 0:
        if labels is not None:
            yield (data.T, labels) if len(data.shape) == 2 else (data, labels)
        else:
            yield data.T if len(data.shape) == 2 else data
    for batch_num in range(num_batches):
        if labels is not None:
            yield (data[batch_num * batch_size:(batch_num + 1) * batch_size].T,
                   labels[:, batch_num * batch_size:(batch_num + 1) * batch_size]) if len(data.shape) == 2 \
                else (data[batch_num * batch_size:(batch_num + 1) * batch_size],
                      labels[:, batch_num * batch_size:(batch_num + 1) * batch_size])
        else:
            yield data[batch_num * batch_size:(batch_num + 1) * batch_size].T if len(data.shape) == 2 else \
                data[batch_num * batch_size:(batch_num + 1) * batch_size]
    if N % batch_size != 0 and num_batches != 0:
        if labels is not None:
            yield (data[num_batches * batch_size:].T, labels[:, num_batches * batch_size:]) if len(data.shape) == 2 else \
                (data[num_batches * batch_size:], labels[:, num_batches * batch_size:])
        else:
            yield data[num_batches * batch_size:].T if len(data.shape) == 2 else data[num_batches * batch_size:]


def evaluate(labels, predictions):
    return np.mean(np.argmax(labels, axis=0) == np.argmax(predictions, axis=0))
