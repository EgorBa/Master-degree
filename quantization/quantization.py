import math


class Quantization:

    def __init__(self, b=5):
        self.b = b

    def quant(self, arr):
        ans = []
        for i in arr:
            ans.append(math.ceil(i * (2 ** self.b) + 0.5))
        return ans

    def dequant(self, arr):
        ans = []
        for i in arr:
            ans.append(int(i) / (2 ** self.b))
        return ans
