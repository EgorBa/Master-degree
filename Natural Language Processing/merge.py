import pandas as pd
import os
from collections import Counter
import random

subs = [
    "submission.csv",
    "submission (1).csv",
    "submission (2).csv",
    "submission (3).csv",
    "submission (4).csv",
    "submission (5).csv",
    "submission (6).csv",
    "submission (7).csv",
]
all_targets = []
for name in subs:
    sample_submission = pd.read_csv(name)
    all_targets.append(sample_submission["target"])
ans = []
y = 0
for i in range(len(all_targets[0])):
    s = []
    for j in range(len(all_targets)):
        s.append(all_targets[j][i])
    r = Counter(s).most_common(len(all_targets))
    if r[0][1] == len(all_targets):
        y += 1
    ans.append(r[0][0])

print(y)
print("absolute same : " + str(y * 100 / len(all_targets[0])))

sample_submission = pd.read_csv("submission.csv")
sample_submission["target"] = ans
sample_submission.to_csv("submission (8).csv", index=False)
