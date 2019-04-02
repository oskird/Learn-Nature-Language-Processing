import nltk
def pos_features(sentence, i, history):
    features = {"suffix(1)": sentence[i][-1:], # 特征：单词的尾字母
                 "suffix(2)": sentence[i][-2:], # 特征：单词结尾两个字母
                 "suffix(3)": sentence[i][-3:]} # 特征：单词结尾三个字母
    if i == 0:
        features["prev-word"] = "<START>" # 特征：单词的前一个词，如果为局首词标注<START>
        features["prev-tag"] = "<START>"  # 特征：单词的前一个词的词性，如果为局首词标注<START>
    else:
        features["prev-word"] = sentence[i-1]
        features["prev-tag"] = history[i-1]
    return features

class ConsecutivePosTagger(nltk.TaggerI):

    def __init__(self, train_sents):
        train_set = [] # 训练集
        for tagged_sent in train_sents: # 提取训练文本中的句子
            untagged_sent = nltk.tag.untag(tagged_sent) # 去掉标注
            history = [] # 标注集
            for i, (word, tag) in enumerate(tagged_sent): # 对句子中的每个(序号, (词，词性))形式
                featureset = pos_features(untagged_sent, i, history) # 对单词训练特征
                train_set.append((featureset, tag)) # 向训练集中添加特征和标签
                history.append(tag) # 向标注集中添加标注
        self.classifier = nltk.NaiveBayesClassifier.train(train_set) # 训练模型

    def tag(self, sentence): # 测试集的标注过程
        history = []
        for i, word in enumerate(sentence):
            featureset = pos_features(sentence, i, history)
            tag = self.classifier.classify(featureset) # 对于每个单词，预测词性
            history.append(tag) # 将预测结果添加到标注集里
        return zip(sentence, history)
tagged_sents = brown.tagged_sents(categories='news')[:1000]
size = int(len(tagged_sents) * 0.1)
train_sents, test_sents = tagged_sents[size:], tagged_sents[:size]
tagger = ConsecutivePosTagger(train_sents)
print('the accuracy of train set {}'.format(tagger.evaluate(train_sents)))
print('the accuracy of test set {}'.format(tagger.evaluate(test_sents)))