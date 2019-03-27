# 索引上下文本
import nltk
class IndexedText(object):

    def __init__(self, stemmer, text):
        self._text = text # 文本内容
        self._stemmer = stemmer # 使用的词干提取器
        self._index = nltk.Index((self._stem(word), i)
                                 for (i, word) in enumerate(text)) # 生成(词干,索引)的组合

    def concordance(self, word, width=40): # 找到上下文函数：需要指定单词和上下文宽度
        key = self._stem(word) # key为单词经过词干提取后的形式
        wc = int(width/4)                # 上下文的词数
        for i in self._index[key]: # 尽管单词形式可以不同，但只要满足词干相同，就会被匹配到
            lcontext = ' '.join(self._text[i-wc:i])
            rcontext = ' '.join(self._text[i:i+wc])
            ldisplay = '{:>{width}}'.format(lcontext[-width:], width=width)
            rdisplay = '{:{width}}'.format(rcontext[:width], width=width)
            print(ldisplay, rdisplay)

    def _stem(self, word): # 词干提取函数(并转化成小写)
        return self._stemmer.stem(word).lower()
porter = nltk.PorterStemmer()
grail = nltk.corpus.webtext.words('grail.txt')
text = IndexedText(porter, grail)
text.concordance('lie', 20)