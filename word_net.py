## WordNet与googletrans
from nltk.corpus import words, wordnet

def wn_dict(word="synonym", num=100):
    """使用wordnet查看单词的同义词集,定义,例句,反义词;"""
    groups = wordnet.synsets(word)
    if len(groups) == 0:
        return "Can' find!"
    for i, group in enumerate(groups):
        if i < num:
            syn = group.lemma_names()  ##同义词集
            ex = group.examples()  ##例子
            Def = group.definition()  ##定义
            ant = [
                l.name()  # 反义词
                for lm in group.lemmas()
                if lm.antonyms()
                for l in lm.antonyms()
            ]

            print("#{} {}".format(i + 1, group.name()))
            print("-" * 32)

            print("[syn]: {}".format(",".join(syn)))
            print("[def]: {}".format(Def))

            if len(ex) != 0:
                print("[exm]: {}".format("; ".join(ex)))
            if len(ant) != 0:
                print("[ant]: {}".format(",".join(ant)))
            print()
