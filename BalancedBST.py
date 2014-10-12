freqs = [.05, .4, .08, .04, .1, .1, .23]
exam_freqs = [.2, .05, .17, .1, .2, .03, .25]
n = len(freqs)

subtrees = {}

for s in range(0, n):
    for i in range(n-s):
        probs = 0
        for k in range(i, i+s+1):
            probs += exam_freqs[k]
        candidates = []
        for r in range(i, i+s+1):
            cand = probs
            if i <= r-1:
                cand += subtrees[(i, r-1)]
            if r+1 <= i+s:
                cand += subtrees[(r+1, i+s)]
            candidates.append(round(cand, 2))
        subtrees[(i, i+s)] = min(candidates)
        print i, i + s, subtrees[(i, i+s)]
    print