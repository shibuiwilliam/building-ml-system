import os
from typing import Any, List, Optional, Tuple

import joblib
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
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


def random_split(
    x: pd.DataFrame,
    y: List[List[int]],
    test_size: float = 0.3,
    shuffle: bool = True,
) -> Tuple[pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray]:
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=test_size,
        shuffle=shuffle,
    )
    return x_train, x_test, np.array(y_train), np.array(y_test)


def split_by_qid(
    x: pd.DataFrame,
    y: List[List[int]],
    qids: List[str],
    test_size: float = 0.3,
    shuffle: bool = True,
) -> Tuple[pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray, List[int], List[int]]:
    pass


class Preprocess(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.tokenizer = MeCab.Tagger()
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
            [
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
                        "data_category",
                        "data_subcategory",
                    ],
                ),
                (
                    "description",
                    description_pipeline,
                    "data_description",
                ),
                (
                    "name",
                    name_pipeline,
                    "data_name",
                ),
            ],
            verbose_feature_names_out=True,
        )
        logger.info(f"pipeline: {self.pipeline}")

    def tokenize_description(
        self,
        text: str,
    ) -> List[str]:
        ts = self.tokenizer.parse(text)
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
        ts = self.tokenizer.parse(text)
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

    def fit(
        self,
        x: pd.DataFrame,
        y: Optional[Any] = None,
    ):
        self.pipeline.fit(x)

    def transform(
        self,
        x: pd.DataFrame,
    ):
        return self.pipeline.transform(x)

    def fit_transform(
        self,
        x: pd.DataFrame,
        y=None,
    ):
        return self.pipeline.fit_transform(x)


def dump_pipeline(
    file_path: str,
    preprocess: Preprocess,
) -> str:
    file, ext = os.path.splitext(file_path)
    if ext != ".pkl":
        file_path = f"{file}.pkl"
    logger.info(f"save preprocess pipeline: {file_path}")
    joblib.dump(preprocess, file_path)
    return file_path


def load_pipeline(file_path: str) -> Preprocess:
    logger.info(f"load preprocess pipeline: {file_path}")
    return joblib.load(file_path)
