# 分割字符
def segment(text, segs):
    words = []
    last = 0
    for i in range(len(segs)):
        if segs[i] == '1':
            words.append(text[last:i+1])
            last = i+1
    words.append(text[last:])
    return words

text = "doyouseethekittyseethedoggydoyoulikethekittylikethedoggy"
seg1 = "0000000000000001000000000010000000000000000100000000000"
seg2 = "0100100100100001001001000010100100010010000100010010000"
seg3 = "0000100100000011001000000110000100010000001100010000001"
segment(text, seg1)

# 评估指标
def evaluate(text, segs):
    words = segment(text, segs)
    text_size = len(words)
    lexicon_size = sum(len(word) + 1 for word in set(words))
    return text_size + lexicon_size
evaluate(text, seg1)

# 模拟退火算法
from random import randint

# 更换一个位置的0-1值
def flip(segs, pos):
    return segs[:pos] + str(1-int(segs[pos])) + segs[pos+1:]

# 更换n个位置的0-1值，其中n由当前温度决定，更换的位置随机的
def flip_n(segs, n):
    for i in range(n):
        segs = flip(segs, randint(0, len(segs)-1))
    return segs

# 退火模拟算法
def anneal(text, segs, iterations, cooling_rate): 
    '''
    text: 文本内容
    segs: 字位串, 长度为len(text)-1
    iterations: 每个温度下的迭代次数
    cooling_rate: 冷却速率, 越大温度下降越快, 模拟轮数也就越少
    '''
    temperature = float(len(segs)) # 初始温度为字位串的长度
    while temperature > 0.5: 
        best_segs, best = segs, evaluate(text, segs) # 当前最佳分割法
        for i in range(iterations): # 在当前温度下开始迭代
            guess = flip_n(segs, round(temperature)) # 随机翻转几个位置，进行猜测
            score = evaluate(text, guess) # 检验猜测结果
            if score < best:
                best, best_segs = score, guess # 如果效果提升，用本次猜测结果来替代最佳结果
                print(evaluate(text, best_segs), segment(text, best_segs))
        score, segs = best, best_segs # 当前温度下的迭代结束，更新最佳得分与字位串
        temperature = temperature / cooling_rate # 冷却，并准备下一轮迭代
    return segs
anneal(text, seg1, 5000, 1.2)