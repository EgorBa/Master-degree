from collections import defaultdict
import heapq


class MinHeapNode:
    def __init__(self, data, freq):
        self.left = None
        self.right = None
        self.data = data
        self.freq = freq

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCodec:

    def __init__(self):
        self.freq = defaultdict(int)
        self.codes = {}
        self.minHeap = []

    def calcFreq(self, str, n):
        for i in range(n):
            self.freq[str[i]] += 1

    def storeCodes(self, root, str):
        if root is None:
            return
        if root.data != '$':
            self.codes[root.data] = str
        self.storeCodes(root.left, str + "0")
        self.storeCodes(root.right, str + "1")

    def HuffmanCodes(self):
        for key in self.freq:
            self.minHeap.append(MinHeapNode(key, self.freq[key]))
        heapq.heapify(self.minHeap)
        while len(self.minHeap) != 1:
            left = heapq.heappop(self.minHeap)
            right = heapq.heappop(self.minHeap)
            top = MinHeapNode('$', left.freq + right.freq)
            top.left = left
            top.right = right
            heapq.heappush(self.minHeap, top)
        self.storeCodes(self.minHeap[0], "")

    def culc_huffman_codes(self, str):
        self.calcFreq(str, len(str))
        self.HuffmanCodes()

    def set_huffman_codes(self, codes):
        self.codes = codes

    def decode_str(self, text):
        res = ""
        f = dict(zip(self.codes.values(), self.codes.keys()))
        while text:
            for k in f:
                if text.startswith(k):
                    res += f[k]
                    text = text[len(k):]
        return res

    def decode_str_as_array(self, text):
        res = self.decode_str(text)
        return [int(x) for x in res.split("|")]

    def encode_str(self, str):
        ans = ""
        for i in str:
            ans += self.codes[i]
        return ans
