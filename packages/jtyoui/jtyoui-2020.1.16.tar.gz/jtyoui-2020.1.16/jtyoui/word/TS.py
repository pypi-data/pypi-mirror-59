#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2019/6/18 18:01
# @Author: Jtyoui@qq.com
from jtyoui.tools import pips
from jtyoui.data import word_nature


class TextSummary:
    def __init__(self, text, title):
        self.title = title
        self.text = text
        self.keywords = list()
        self.sentences = list()
        self.summary = list()
        self.cut = pips('jieba.posseg', 'jieba').cut  # 自动安装结巴包失败，请手动安装: pip install jieba
        self.extract_tags = pips('jieba.analyse', 'jieba').extract_tags  # 自动安装结巴包失败，请手动安装: pip install jieba

    def __setitem__(self, title, text):
        self.title = title
        self.text = text

    def _split_sentence(self):
        # 通过换行符对文档进行分段
        sections = self.text.split('\n')
        for section in sections:
            if section == '':
                sections.remove(section)

        # 通过分割符对每个段落进行分句
        for i in range(len(sections)):
            section = sections[i]
            text = ''
            k = 0
            for j in range(len(section)):
                char = section[j]
                text = text + char
                if char in '!。？' or j == len(section) - 1:
                    text = text.strip()
                    sentence = dict()
                    sentence['text'] = text
                    sentence['pos'] = dict()
                    sentence['pos']['x'] = i
                    sentence['pos']['y'] = k
                    # 将处理结果加入self.sentences
                    self.sentences.append(sentence)
                    text = ''
                    k = k + 1

        for sentence in self.sentences:
            sentence['text'] = sentence['text'].strip()
            if sentence['text'] == '':
                self.sentences.remove(sentence)

        # 对文章位置进行标注，通过mark列表，标注出是否是第一段、尾段、第一句、最后一句
        last_pos = dict()
        last_pos['x'] = 0
        last_pos['y'] = 0
        last_pos['mark'] = list()
        for sentence in self.sentences:
            pos = sentence['pos']
            pos['mark'] = list()
            if pos['x'] == 0:
                pos['mark'].append('first_section')
            if pos['y'] == 0:
                pos['mark'].append('first_sentence')
                last_pos['mark'].append('last_sentence')
            if pos['x'] == self.sentences[len(self.sentences) - 1]['pos']['x']:
                pos['mark'].append('last_section')
            last_pos = pos
        last_pos['mark'].append('last_sentence')

    def _calc_keywords(self):
        # 计算TF-IDF，取出排名靠前的20个词
        words_best = self.extract_tags(self.text, topK=20)
        # 提取第一段的关键词
        parts = self.text.lstrip().split('\n')
        first_part = ''
        if len(parts) >= 1:
            first_part = parts[0]
        words_best = words_best + self.extract_tags(first_part, topK=5)
        # 提取title中的关键词
        words_best = words_best + self.extract_tags(self.title, topK=3)
        # 将结果合并成一个句子，并进行分词
        text = ''
        for w in words_best:
            text += ' ' + w
        # 计算词性，提取名词和动词
        words = self.cut(text)
        keywords = list()
        for w in words:
            flag = w.flag
            word = w.word
            if flag.find('n') >= 0 or flag.find('v') >= 0:
                if len(word) > 1:
                    keywords.append(word)
        # 保留前20个关键词
        keywords = self.extract_tags(' '.join(keywords), topK=20)
        keywords = list(set(keywords))
        self.keywords = keywords

    def _calc_sentence_weight_by_keywords(self):
        # 计算句子的关键词权重
        for sentence in self.sentences:
            sentence['weightKeywords'] = 0
        for keyword in self.keywords:
            for sentence in self.sentences:
                if sentence['text'].find(keyword) >= 0:
                    sentence['weightKeywords'] += 1

    def _calc_sentence_weight_by_pos(self):
        # 计算句子的位置权重
        for sentence in self.sentences:
            mark = sentence['pos']['mark']
            weight_pos = 0
            if 'first_section' in mark:
                weight_pos = weight_pos + 2
            if 'first_sentence' in mark:
                weight_pos = weight_pos + 2
            if 'last_sentence' in mark:
                weight_pos = weight_pos + 1
            if 'last_section' in mark:
                weight_pos = weight_pos + 1
            sentence['weight_pos'] = weight_pos

    def _calc_sentence_weight_cue_words(self, index=None):
        # 计算句子的线索词权重
        if not index:
            index = word_nature()['adv_freq']
        for sentence in self.sentences:
            sentence['weightCueWords'] = 0
        for i in index:
            for sentence in self.sentences:
                if sentence['text'].find(i) >= 0:
                    sentence['weightCueWords'] = 1

    def _calc_sentence_weight(self, index=None):
        self._calc_sentence_weight_by_pos()
        self._calc_sentence_weight_cue_words(index)
        self._calc_sentence_weight_by_keywords()
        for sentence in self.sentences:
            sentence['weight'] = sentence['weight_pos'] + 2 * sentence['weightCueWords'] + sentence['weightKeywords']

    def calc_summary(self, ratio=0.1, index=None):
        # 清空变量
        self.keywords.clear()
        self.sentences.clear()
        self.summary.clear()

        # 调用方法，分别计算关键词、分句，计算权重
        self._calc_keywords()
        self._split_sentence()
        self._calc_sentence_weight(index)

        # 对句子的权重值进行排序
        self.sentences = sorted(self.sentences, key=lambda k: k['weight'], reverse=True)

        # 根据排序结果，取排名占前X%的句子作为摘要
        for i in range(len(self.sentences)):
            if i < ratio * len(self.sentences):
                sentence = self.sentences[i]
                self.summary.append(sentence['text'])

        return self.summary


if __name__ == '__main__':
    data = """6月17日22时55分，四川长宁县发生6.0级地震，震源深度16千米。地震发生两个小时后，离震中较近的四川省宜宾市珙县
    巡场镇宜宾市矿山急救医院迎来第一个新生儿。医生在余震和医院房屋出现损毁的情况下顶住压力和风险，为产妇接生，母子平安。"""
    ts = TextSummary(data, title='长宁县地震')
    print(ts.calc_summary())
