import nltk

class ConsecutiveNPChunkTagger(nltk.TaggerI):
    '''标注器
    train_sents：训练文本(已词性标注)
    train_set：训练集(包含特征和类别)
    history：标注集
    '''
    def __init__(self, train_sents, verbose=1):
        train_set = []
        for tagged_sent in train_sents: # 提取训练文本中的句子
            untagged_sent = nltk.tag.untag(tagged_sent) # 去掉标注
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = npchunk_features(untagged_sent, i, history) # 提取特征
                train_set.append((featureset, tag)) # 向训练集中添加数据
                history.append(tag)
        if verbose==1: print("finish extracting features")
        self.classifier = nltk.MaxentClassifier.train(train_set, trace=0)
        if verbose==1: print("finish training model")

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = npchunk_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)

class ConsecutiveNPChunker(nltk.ChunkParserI):
    '''分块器
    train_sents：训练文本(包含词、词性标注和IOB标注)
    tagged_sents：将词和词性作为X部分，IOB标注作为需要预测的Y部分
    conlltags：将预测后的结果还原为(词, 词性标注, IOB标注)的形式
    '''
    def __init__(self, train_sents):
        tagged_sents = [[((w,t),c) for (w,t,c) in
                         nltk.chunk.tree2conlltags(sent)]
                        for sent in train_sents] # 将(词, 词性标注, IOB标注)形式的三元组重塑为((词, 词性标注), IOB标注)的形式
        self.tagger = ConsecutiveNPChunkTagger(tagged_sents) # 利用之前之前创建的Tagger来预测IOB标注

    def parse(self, sentence):
        tagged_sents = self.tagger.tag(sentence) # 预测IOB标注
        conlltags = [(w,t,c) for ((w,t),c) in tagged_sents] # 将((词, 词性标注), IOB标注)形式返回为三元组(词, 词性标注, IOB标注)
        return nltk.chunk.conlltags2tree(conlltags)
		
test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
# 添加特征
def tags_since_dt(sentence, i):
    tags = set()
    for word, pos in sentence[:i]:
        if pos == 'DT':
            tags = set()
        else:
            tags.add(pos)
    return '+'.join(sorted(tags))
def npchunk_features(sentence, i, history):
    word, pos = sentence[i]
    if i == 0:
        prevword, prevpos = "<START>", "<START>"
    else:
        prevword, prevpos = sentence[i-1]
    if i == len(sentence)-1:
        nextword, nextpos = "<END>", "<END>"
    else:
        nextword, nextpos = sentence[i+1]
    return {"pos": pos,                                    # 当前词性
            "word": word,                                  # 当前词
            "prevpos": prevpos,                            # 前一个词的词性
            "nextpos": nextpos,                            # 下一个词的词性
            "prevpos+pos": "%s+%s" % (prevpos, pos),       # 前一个词与当前词的词性组合
            "pos+nextpos": "%s+%s" % (pos, nextpos),       # 当前词与后一个词的词性组合
            "tags-since-dt": tags_since_dt(sentence, i)}   # 自从上一个限定词后至今包含的所有词性(依靠tags_since_dt函数)
chunker = ConsecutiveNPChunker(train_sents[:100])
print(chunker.evaluate(test_sents))