import os
import random
from typing import Any, Dict, List, Optional, Tuple

import cloudpickle
import MeCab
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from src.dataset.schema import RawData, SplitData
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


def make_query_id(
    phrases: str,
    animal_category_id: Optional[int],
    animal_subcategory_id: Optional[int],
) -> str:
    return f"{phrases}_{animal_category_id}_{animal_subcategory_id}"


def random_split(
    raw_data: RawData,
    test_size: float = 0.3,
) -> SplitData:
    logger.info("random split")
    x_train, x_test, y_train, y_test = train_test_split(
        raw_data.data,
        raw_data.target,
        test_size=test_size,
        shuffle=True,
    )
    return SplitData(
        x_train=pd.DataFrame(x_train),
        x_test=pd.DataFrame(x_test),
        y_train=np.array(y_train),
        y_test=np.array(y_test),
        q_train=None,
        q_test=None,
    )


def split_by_qid(
    raw_data: RawData,
    test_size: float = 0.3,
) -> SplitData:
    logger.info("split by qid")
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    q_train = []
    q_test = []
    _data: Dict[str, List[Tuple]] = {}
    for r, t in zip(raw_data.data, raw_data.target):
        qid = make_query_id(
            phrases=".".join(sorted(r["query_phrases"])),
            animal_category_id=r["query_animal_category_id"],
            animal_subcategory_id=r["query_animal_subcategory_id"],
        )
        if qid in _data.keys():
            _data[qid].append((r, t))
        else:
            _data[qid] = [(r, t)]
    for qid, rts in _data.items():
        if len(rts) == 1:
            x_train.append(rts[0][0])
            y_train.append(rts[0][1])
            q_train.append(1)
        else:
            l = len(rts)
            if l > 10000:
                l = 10000
            _rts = random.sample(rts, l)
            train_size = int(l * (1 - test_size))
            for i, rt in enumerate(_rts):
                if i < train_size:
                    x_train.append(rt[0])
                    y_train.append(rt[1])
                else:
                    x_test.append(rt[0])
                    y_test.append(rt[1])
            q_train.append(train_size)
            q_test.append(l - train_size)
    return SplitData(
        x_train=pd.DataFrame(x_train),
        x_test=pd.DataFrame(x_test),
        y_train=np.array(y_train),
        y_test=np.array(y_test),
        q_train=q_train,
        q_test=q_test,
    )


class Preprocess(BaseEstimator, TransformerMixin):
    def __init__(self):
        # self.tokenizer = MeCab.Tagger()
        self.stop_words = [
            "あそこ",
            "あたり",
            "あちら",
            "あっち",
            "あと",
            "あな",
            "あなた",
            "あれ",
            "いくつ",
            "いつ",
            "いま",
            "いや",
            "いろいろ",
            "うち",
            "おおまか",
            "おまえ",
            "おれ",
            "がい",
            "かく",
            "かたち",
            "かやの",
            "から",
            "がら",
            "きた",
            "くせ",
            "ここ",
            "こっち",
            "こと",
            "ごと",
            "こちら",
            "ごっちゃ",
            "これ",
            "これら",
            "ごろ",
            "さまざま",
            "さらい",
            "さん",
            "しかた",
            "しよう",
            "すか",
            "ずつ",
            "すね",
            "すべて",
            "する",
            "ない",
            "くださる",
            "っぽい",
            "れる",
            "ん",
            "さっき",
            "の",
            "たつ",
            "カ",
            "生",
            "見る",
            "ぜんぶ",
            "そう",
            "そこ",
            "そちら",
            "そっち",
            "そで",
            "それ",
            "それぞれ",
            "それなり",
            "たくさん",
            "たち",
            "たび",
            "ため",
            "だめ",
            "ちゃ",
            "ちゃん",
            "てん",
            "とおり",
            "とき",
            "どこ",
            "どこか",
            "ところ",
            "どちら",
            "どっか",
            "どっち",
            "どれ",
            "なか",
            "なかば",
            "なに",
            "など",
            "なん",
            "はじめ",
            "はず",
            "はるか",
            "ひと",
            "ひとつ",
            "ふく",
            "ぶり",
            "べつ",
            "へん",
            "ぺん",
            "ほう",
            "ほか",
            "まさ",
            "まし",
            "まとも",
            "まま",
            "みたい",
            "みつ",
            "みなさん",
            "みんな",
            "もと",
            "もの",
            "もん",
            "やつ",
            "よう",
            "よそ",
            "わけ",
            "わたし",
            "ハイ",
            "上",
            "中",
            "下",
            "字",
            "年",
            "月",
            "日",
            "時",
            "分",
            "秒",
            "週",
            "火",
            "水",
            "木",
            "金",
            "土",
            "国",
            "都",
            "道",
            "府",
            "県",
            "市",
            "区",
            "町",
            "村",
            "各",
            "第",
            "方",
            "何",
            "的",
            "度",
            "文",
            "者",
            "性",
            "人",
            "他",
            "今",
            "部",
            "課",
            "係",
            "外",
            "類",
            "達",
            "気",
            "室",
            "口",
            "誰",
            "用",
            "界",
            "会",
            "首",
            "男",
            "女",
            "別",
            "話",
            "私",
            "屋",
            "店",
            "家",
            "場",
            "等",
            "見",
            "際",
            "観",
            "段",
            "略",
            "例",
            "系",
            "論",
            "形",
            "間",
            "地",
            "員",
            "線",
            "点",
            "書",
            "品",
            "力",
            "法",
            "感",
            "作",
            "元",
            "手",
            "数",
            "彼",
            "彼女",
            "内",
            "輪",
            "頃",
            "化",
            "境",
            "俺",
            "奴",
            "高",
            "校",
            "婦",
            "伸",
            "紀",
            "誌",
            "レ",
            "行",
            "列",
            "事",
            "士",
            "台",
            "集",
            "様",
            "所",
            "歴",
            "器",
            "名",
            "情",
            "連",
            "毎",
            "式",
            "簿",
            "回",
            "匹",
            "個",
            "席",
            "束",
            "歳",
            "目",
            "通",
            "面",
            "円",
            "玉",
            "枚",
            "前",
            "後",
            "左",
            "右",
            "次",
            "先",
            "一",
            "二",
            "三",
            "四",
            "五",
            "六",
            "七",
            "八",
            "九",
            "十",
            "百",
            "千",
            "万",
            "億",
            "兆",
            "下記",
            "上記",
            "時間",
            "今回",
            "前回",
            "場合",
            "一つ",
            "年生",
            "自分",
            "ヶ所",
            "ヵ所",
            "カ所",
            "箇所",
            "ヶ月",
            "ヵ月",
            "カ月",
            "箇月",
            "名前",
            "本当",
            "確か",
            "時点",
            "全部",
            "関係",
            "近く",
            "方法",
            "我々",
            "違い",
            "多く",
            "扱い",
            "新た",
            "その後",
            "半ば",
            "結局",
            "様々",
            "以前",
            "以後",
            "以降",
            "未満",
            "以上",
            "以下",
            "幾つ",
            "毎日",
            "自体",
            "向こう",
            "何人",
            "手段",
            "同じ",
            "感じ",
        ]
        self.define_pipeline()

    def define_pipeline(self):
        logger.info("init pipeline")
        numerical_pipeline = Pipeline(
            [
                (
                    "simple_imputer",
                    SimpleImputer(
                        missing_values=np.nan,
                        strategy="constant",
                        fill_value=None,
                    ),
                ),
                (
                    "scaler",
                    MinMaxScaler(),
                ),
            ]
        )
        categorical_pipeline = Pipeline(
            [
                (
                    "simple_imputer",
                    SimpleImputer(
                        missing_values=np.nan,
                        strategy="constant",
                        fill_value=None,
                    ),
                ),
                (
                    "one_hot_encoder",
                    OneHotEncoder(
                        sparse=True,
                        handle_unknown="ignore",
                    ),
                ),
            ]
        )
        description_pipeline = Pipeline(
            [
                (
                    "description_tfids_vectorizer",
                    TfidfVectorizer(
                        max_features=500,
                        tokenizer=self.tokenize_description,
                        stop_words=self.stop_words,
                    ),
                ),
            ]
        )
        name_pipeline = Pipeline(
            [
                (
                    "name_tfidf_vectorizer",
                    TfidfVectorizer(
                        max_features=300,
                        tokenizer=self.tokenize_name,
                    ),
                ),
            ]
        )
        self.pipeline = ColumnTransformer(
            transformers=[
                (
                    "numerical",
                    numerical_pipeline,
                    ["likes"],
                ),
                (
                    "categorical",
                    categorical_pipeline,
                    [
                        "query_phrases",
                        "query_animal_category_id",
                        "query_animal_subcategory_id",
                        "animal_category_id",
                        "animal_subcategory_id",
                    ],
                ),
                (
                    "description",
                    description_pipeline,
                    "description",
                ),
                (
                    "name",
                    name_pipeline,
                    "name",
                ),
            ],
            remainder="drop",
            verbose_feature_names_out=True,
        )
        logger.info(f"pipeline: {self.pipeline}")

    def tokenize_description(
        self,
        text: str,
    ) -> List[str]:
        tokenizer = MeCab.Tagger()
        ts = tokenizer.parse(text)
        ts = ts.split("\n")
        tokens = []
        for t in ts:
            if t == "EOS":
                break
            s = t.split("\t")
            r = s[1].split(",")
            w = ""
            if r[0] == "名詞":
                w = s[0]
            elif r[0] in ("動詞", "形容詞"):
                w = r[6]
            if w == "":
                continue
            tokens.append(w)
        return tokens

    def tokenize_name(
        self,
        text: str,
    ) -> List[str]:
        tokenizer = MeCab.Tagger()
        ts = tokenizer.parse(text)
        ts = ts.split("\n")
        tokens = []
        for t in ts:
            if t == "EOS":
                break
            s = t.split("\t")
            w = s[0]
            if w == "":
                continue
            tokens.append(w)
        return tokens

    def preprocess(self, x: pd.DataFrame) -> pd.DataFrame:
        types = {
            "animal_id": "str",
            "query_phrases": "str",
            "query_animal_category_id": "str",
            "query_animal_subcategory_id": "str",
            "likes": "int64",
            "animal_category_id": "str",
            "animal_subcategory_id": "str",
            "name": "str",
            "description": "str",
        }
        x = x.astype(types)
        return x

    def fit(
        self,
        x: pd.DataFrame,
        y: Optional[Any] = None,
    ):
        x = self.preprocess(x=x)
        self.pipeline.fit(x)

    def transform(
        self,
        x: pd.DataFrame,
    ):
        x = self.preprocess(x=x)
        return self.pipeline.transform(x)

    def fit_transform(
        self,
        x: pd.DataFrame,
        y=None,
    ):
        x = self.preprocess(x=x)
        X = self.pipeline.fit_transform(x)
        return X

    def save(
        self,
        file_path: str,
    ) -> str:
        file, ext = os.path.splitext(file_path)
        if ext != ".pkl":
            file_path = f"{file}.pkl"
        logger.info(f"save preprocess pipeline: {file_path}")
        with open(file_path, "wb") as f:
            cloudpickle.dump(self.pipeline, f)
        return file_path

    def load(
        self,
        file_path: str,
    ):
        logger.info(f"load preprocess pipeline: {file_path}")
        with open(file_path, "wb") as f:
            self.pipeline = cloudpickle.load(f)
