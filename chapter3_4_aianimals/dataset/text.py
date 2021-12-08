import json
import os
import random
import logging
from itertools import permutations

LOG_LEVEL = os.getenv("LOG_LEVEL", logging.DEBUG)
logger = logging.getLogger("main")
logger.setLevel(LOG_LEVEL)
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] [%(funcName)s] %(message)s"
)
handler = logging.StreamHandler()
handler.setLevel(LOG_LEVEL)
handler.setFormatter(formatter)
logger.addHandler(handler)

kudoku = [
    "。",
    "。",
    "。",
    "。",
    "。",
    "。",
    "。",
    "。",
    "。",
    "。",
    "。",
    "。",
    "。",
    "！",
    "！",
    "！",
    "！",
    "！",
    "！",
    "！",
    "！",
    "！！",
    "！！",
    "。",
    "！",
    "！！",
    "。",
    "！",
    "！！",
    "！？",
    "(ΦωΦ)",
    "(^o^)",
    ":D",
    "m(_ _)m",
    "＼(^o^)／",
    "U^ｪ^U",
    "☆彡",
    "☆",
    "★",
    "☆ミ",
]


def do_aisatsu():
    aisatsu = ["こんにちは", "はじめまして", "はろー", "ハロー", "ぜひ見てください"]
    a = random.choice(aisatsu)
    k = random.choice(kudoku)
    return a + k


hyogen = [
    "かわいい",
    "かっこいい",
    "最高",
    "プリチー",
    "ラブリー",
    "キュート",
    "クール",
    "イケメン",
    "美しい",
    "ワイルド",
    "一番",
    "大好き",
    "キャワイイ",
    "きゃわわわわ",
    "はわわわわ",
    "偉そう",
    "わがものがお",
]
gitai = [
    "ふみふみ",
    "めろめろ",
    "メロメロ",
    "キュンキュン",
    "きゅんきゅん",
    "もふもふ",
    "モフモフ",
    "もちもち",
    "てくてく",
    "あむあむ",
    "うきうき",
    "うとうと",
    "ほくほく",
    "もくもく",
    "もきゅもきゅ",
    "るんるん",
    "ルンルン気分",
    "ルンルン",
    "わくわく",
    "ランラン",
    "ドキドキ",
]


def do_hyogen():
    gh = random.randint(0, 1)
    if gh == 0:
        r = random.choice(hyogen)
    else:
        r = random.choice(gitai)
    k = random.choice(kudoku)
    return f"いつも{r}です{k}"


cat_meow = [
    "ニャンニャン",
    "にゃーにゃー",
    "なーなー",
    "にゃあにゃあ",
    "うにゃうにゃ",
    "ウニャン",
    "フニャフニャ",
    "ふにゃふにゃ",
    "みーみー",
    "ミーミー",
    "ミャウミャウ",
    "にーにー",
]
dog_bugh = [
    "わんわん",
    "ワンワン",
    "ばふばふ",
    "バフバフ",
    "わうわう",
]
mb_prepre = ["いつも", "ときどき", "たまに", "強く", "弱々しく", "優しく", "激しく", "大きく", "小さく"]
mb_prefix = [
    "大声で",
    "小声で",
    "怒涛のように",
    "荒波のように",
    "噴火のように",
    "静かに",
    "荒々しく",
    "神々しく",
    "白々しく",
    "隕石が降り注ぐように",
    "大雨のように",
    "暴風雨のように",
    "竜巻のように",
    "大吹雪のように",
    "からっ風のように",
    "季節風のように",
    "怒れる神のように",
    "狂ったように",
    "狂乱のように",
    "清楚に",
    "物静かに",
    "まじめに",
    "凛と",
    "天地がひっくり返ったように",
    "王様のように",
    "神様のように",
    "晴天のように",
    "木漏れ日のように",
    "疲れたように",
    "生き生きとして",
]
mb_suffix = [
    "鳴きます",
    "なきます",
    "言ってます",
    "(ΦωΦ)と鳴きます",
    "＼(^o^)／と鳴きます",
    "(^o^)と鳴きます",
    "(^O^)と鳴きます",
    "Uo･ｪ･oUと鳴きます",
    "と鳴きます",
    "となきます",
    "と言ってます",
]
mb_suffix_past = [
    "鳴いてました",
    "ないてました",
    "言ってました",
    "(ΦωΦ)と鳴いてました",
    "＼(^o^)／と鳴いてました",
    "(^o^)と鳴いてました",
    "(^O^)と鳴いてました",
    "Uo･ｪ･oUと鳴いてました",
    "と鳴いてました",
    "とないてました",
    "と言ってました",
]


def do_naku(is_cat: bool):
    mb = cat_meow if is_cat else dog_bugh
    naku = random.choice(mb)
    if random.random() > 0.95:
        n2 = random.choice(mb)
        if n2 != naku:
            naku = f"{naku}とか{n2}"
    if random.random() > 0.999:
        n3 = random.choice(mb)
        if n3 not in naku:
            naku = f"{naku}とか{n3}"
    mpp = random.choice(mb_prepre)
    mp = random.choice(mb_prefix)
    ms = random.choice(mb_suffix)
    if random.random() > 0.2:
        p = ""
        if random.random() > 0.7:
            p += mpp
        p += mp
        naku = mp + naku
    k = random.choice(kudoku)
    return naku + ms + k


def do_naita(is_cat: bool):
    mb = cat_meow if is_cat else dog_bugh
    naku = random.choice(mb)
    if random.random() > 0.95:
        n2 = random.choice(mb)
        if n2 != naku:
            naku = f"{naku}とか{n2}"
    if random.random() > 0.999:
        n3 = random.choice(mb)
        if n3 not in naku:
            naku = f"{naku}とか{n3}"
    mpp = random.choice(mb_prepre)
    mp = random.choice(mb_prefix)
    ms = random.choice(mb_suffix_past)
    if random.random() > 0.2:
        p = ""
        if random.random() > 0.7:
            p += mpp
        p += mp
        naku = mp + naku
    k = random.choice(kudoku)
    return naku + ms + k


suki = [
    "食べるの",
    "カリカリ",
    "餌",
    "お昼寝",
    "寝るの",
    "ハンモック",
    "食事",
    "遊ぶの",
    "おもちゃ",
    "ぬいぐるみ",
    "ベッド",
    "お風呂",
    "ごはん",
    "遊び回るの",
    "飛び回るの",
    "家",
    "ボール",
    "ふみふみするの",
    "車",
    "お洋服",
    "耳掃除",
    "体を洗うの",
    "お母さん",
    "お父さん",
    "息子",
    "娘",
    "私のこと",
    "オレのこと",
    "わたし",
    "人間",
    "家族",
    "ごはんの時間",
]
neko_suki = [
    "ダンボールに入るの",
    "猫タワー",
    "キャットタワー",
    "こたつ",
    "猫缶",
    "キャットフード",
    "お魚",
    "おさかな",
    "お肉",
    "ネコ草",
    "またたび",
    "猫ケージ",
]
dog_suki = ["お散歩", "歩くの", "外", "外出", "お出かけ"]
suki_suffix = [
    "が好きです",
    "が大好きです",
    "がすごく好きです",
    "がちょっと好きです",
    "がお気に入りです",
    "が好きすぎです",
    "をこよなく愛しています",
    "を愛してます",
    "をすごい愛してます",
    "がすごくお気に入りです",
    "が嫌いじゃないっぽいです",
    "が好きっぽいです",
    "が好きらしいです",
    "がなんとなく好きっぽいです",
    "がなんとなく好きらしいです",
    "がどことなく嫌いじゃないらしいです",
    "がなんとなく嫌いじゃないらしいです",
]


def do_suki(is_cat: bool):
    cd = neko_suki if is_cat else dog_suki
    _suki = [s for s in suki]
    _suki.extend(cd)
    s = random.choice(_suki)
    if random.random() > 0.7:
        s2 = random.choice(_suki)
        if s != s2:
            s = f"{s}と{s2}"
    if random.random() > 0.9:
        s3 = random.choice(_suki)
        if s3 not in s:
            s = f"{s}と{s3}"
    if random.random() > 0.99:
        s4 = random.choice(_suki)
        if s4 not in s:
            s = f"{s}と{s4}"
    ss = random.choice(suki_suffix)
    k = random.choice(kudoku)
    return s + ss + k


name = ["名前は", "お名前は", "この子は"]
cat_suf = ["ちゃん", "くん", "さん", "さま", "様"]
dog_suf = ["ちゃん", "くん", "さん"]
cat_name = [
    "まる",
    "むぎ",
    "マル",
    "ムギ",
    "ソラ",
    "そら",
    "レオ",
    "ココ",
    "たま",
    "タマ",
    "れお",
    "もも",
    "モモ",
    "きなこ",
    "りん",
    "リン",
    "ルナ",
    "るな",
    "マロン",
    "ふく",
    "フク",
    "コテツ",
    "チャチャマル",
    "るい",
    "ルイ",
    "モカ",
    "ベル",
    "さくら",
    "サクラ",
    "なな",
    "ナナ",
    "みー",
    "ミー",
    "トム",
    "レオン",
    "とら",
    "らいおん",
    "ライオン",
    "ちび",
    "チビ",
    "ひめ",
    "ヒメ",
    "ハル",
    "ナツ",
    "アキ",
    "ギン",
    "コウメ",
    "ウメ",
    "ハート",
    "ラブ",
    "ロビン",
    "ハウル",
    "テン",
    "コタロー",
    "ゴクウ",
    "せん",
    "セン",
    "ちー",
    "チー",
    "チイ",
    "もち",
    "モチ",
    "こなん",
    "リク",
    "りく",
    "ジョン",
    "ジョジョ",
    "ジョナ",
    "まこ",
    "マコ",
    "ゆー",
    "ゆう",
    "あかね",
    "きょう",
    "キョウ",
    "らん",
    "ラン",
    "めめ",
    "メメ",
    "りり",
    "リリ",
    "ねね",
    "ネネ",
    "ぺぺ",
    "ペペ",
    "たん",
    "タン",
    "もこ",
    "モコ",
    "なるみ",
    "はな",
    "おき",
    "あお",
    "みどり",
    "カイ",
    "にゃん",
    "あーにゃ",
    "アーニャ",
    "リク",
    "チョコ",
    "クッキー",
    "ピース",
    "ハチ",
    "フク",
    "ロウ",
    "ロン",
    "ニコ",
    "アズキ",
    "クウ",
    "ジン",
    "ケン",
    "リュウ",
    "レタラ",
    "リパ",
    "アシ",
    "フジ",
    "ラン",
    "レン",
    "ルン",
    "ワン",
    "バウ",
    "ゆず",
    "アンズ",
    "ココア",
    "チャコ",
    "ミルク",
    "スシ",
    "ニク",
    "ステーキ",
    "フラン",
    "ミリ",
    "ディア",
    "ラーメン",
    "とんかつ",
    "ワズ",
    "ボブ",
    "ボビー",
    "きんぎょ",
    "つばめ",
    "はと",
    "まろ",
    "しろ",
    "シロ",
    "ヴォルフ",
    "ヴォルタ",
    "ボルト",
    "ぽか",
    "ぱむ",
    "ベッケン",
    "ベッカム",
    "ロビー",
    "ロブ",
    "ジョブ",
    "スティーブ",
    "ジョージ",
    "ミント",
    "アレンビー",
    "フハイ",
    "ドモン",
    "ヒーロ",
    "ヒロ",
    "トロワ",
    "カトル",
    "シャア",
    "セイラ",
    "クワトロ",
    "バジーナ",
    "ブライ",
    "ブライト",
    "アリーナ",
    "クリフト",
    "ケアル",
    "ホイミ",
    "スラ",
    "ホイミン",
    "バーバラ",
    "ミレイ",
    "ミレーユ",
    "ハッサン",
    "ドランゴ",
    "テリー",
    "ロック",
    "ティナ",
    "ティファ",
    "エアリス",
    "クラウド",
    "デュオ",
    "マックス",
    "ミックス",
    "ミント",
    "ババロア",
    "スフレ",
    "プリン",
    "アーモンド",
    "ダンゴ",
    "タンゴ",
    "フルート",
    "フルーツ",
    "オーボエ",
    "ビオラ",
    "ビオレッタ",
    "シー",
    "シズ",
    "サシミ",
    "サラダ",
    "ポンチ",
    "アンコロ",
    "タンタン",
    "カレン",
    "スザク",
    "リズ",
    "コリーン",
    "ファム",
    "ユイ",
    "レイ",
    "シン",
    "サツキ",
    "トロ",
    "ポルコ",
    "ロッソ",
    "ブルー",
    "ルー",
    "アカリ",
    "ミズカ",
    "ミズキ",
    "ゴン",
    "リオ",
    "ピカ",
    "クラ",
    "ニュー",
    "ダム",
    "ガンタ",
    "カンタ",
    "リー",
    "カエル",
    "リーネ",
    "クロノ",
    "ルッカ",
    "ロボ",
    "エイ",
    "ダッチャ",
    "シノブ",
    "キョウコ",
    "ゴダイ",
    "ピコ",
    "コロ",
    "ミコ",
    "ウプ",
    "シェシェ",
    "ラティ",
    "ケニー",
    "カニー",
    "リヴァイ",
    "チェン",
    "ミカサ",
    "デック",
    "リック",
    "ミック",
    "ミニー",
    "シャオ",
    "メル",
    "ゾゾ",
    "メルル",
    "ポップ",
    "ダイ",
    "アバン",
    "くろこ",
    "だい",
    "ミク",
    "ライン",
    "やん",
    "ウェンリー",
    "ハル",
    "ハルキ",
    "ハルヒ",
    "ミサト",
    "リツ",
    "ツツ",
    "スズ",
    "トド",
    "ポポ",
    "ミスタ",
    "ナラン",
    "ボス",
    "ディオ",
    "ディア",
    "ディナ",
    "ランチ",
    "ブレック",
    "ファラ",
    "オヤビン",
    "ゲレゲレ",
    "ビアンカ",
    "フローラ",
    "ピピン",
    "デボラ",
    "ヘンリー",
    "チロル",
    "ボロンゴ",
    "プックル",
    "ぐり",
    "ソロ",
    "ギコギコ",
    "ギンコ",
    "リンクス",
    "アンドレ",
    "メラ",
    "ヒャド",
    "オーラ",
    "ドル",
    "エン",
    "フラン",
    "ルーブル",
    "ルカ",
    "プル",
    "エル",
    "デイン",
    "ギガンテ",
    "ギガ",
    "メガ",
    "テラ",
    "ピコ",
    "ピグミン",
    "ブー",
    "ブウ",
    "リボン",
    "ブック",
    "オルフィー",
    "エルフィン",
    "ビックス",
    "ウェッジ",
    "テンサー",
    "フロー",
    "トーチ",
    "サイキ",
    "ラーン",
    "ら～ん",
    "ナムパイ",
    "パンダ",
    "ぱんだ",
]
dog_name = [
    "むぎ",
    "マル",
    "ムギ",
    "ソラ",
    "そら",
    "ココ",
    "たま",
    "タマ",
    "れお",
    "もも",
    "モモ",
    "きなこ",
    "りん",
    "リン",
    "ルナ",
    "るな",
    "マロン",
    "ふく",
    "フク",
    "コテツ",
    "チャチャマル",
    "るい",
    "ルイ",
    "モカ",
    "ベル",
    "さくら",
    "サクラ",
    "なな",
    "ナナ",
    "トム",
    "ちび",
    "チビ",
    "ひめ",
    "ヒメ",
    "ハル",
    "ナツ",
    "アキ",
    "ギン",
    "コウメ",
    "ウメ",
    "ハート",
    "ラブ",
    "ロビン",
    "ハウル",
    "テン",
    "コタロー",
    "ゴクウ",
    "せん",
    "セン",
    "ちー",
    "チー",
    "チイ",
    "もち",
    "モチ",
    "こなん",
    "リク",
    "りく",
    "ジョン",
    "ジョジョ",
    "ジョナ",
    "まこ",
    "マコ",
    "ゆー",
    "ゆう",
    "あかね",
    "きょう",
    "キョウ",
    "らん",
    "ラン",
    "めめ",
    "メメ",
    "りり",
    "リリ",
    "ねね",
    "ネネ",
    "ぺぺ",
    "ペペ",
    "たん",
    "タン",
    "もこ",
    "モコ",
    "なるみ",
    "はな",
    "おき",
    "あお",
    "みどり",
    "カイ",
    "リク",
    "チョコ",
    "クッキー",
    "ピース",
    "ハチ",
    "フク",
    "ロウ",
    "ロン",
    "ニコ",
    "アズキ",
    "クウ",
    "ジン",
    "ケン",
    "リュウ",
    "レタラ",
    "リパ",
    "アシ",
    "フジ",
    "ラン",
    "レン",
    "ルン",
    "ワン",
    "バウ",
    "ゆず",
    "アンズ",
    "ココア",
    "チャコ",
    "ミルク",
    "スシ",
    "ニク",
    "ステーキ",
    "フラン",
    "ミリ",
    "ディア",
    "ラーメン",
    "とんかつ",
    "ワズ",
    "ボブ",
    "ボビー",
    "きんぎょ",
    "つばめ",
    "はと",
    "まろ",
    "しろ",
    "シロ",
    "ヴォルフ",
    "ヴォルタ",
    "ボルト",
    "ぽか",
    "ぱむ",
    "ベッケン",
    "ベッカム",
    "ロビー",
    "ロブ",
    "ジョブ",
    "スティーブ",
    "ジョージ",
    "ミント",
    "アレンビー",
    "フハイ",
    "ドモン",
    "ヒーロ",
    "ヒロ",
    "トロワ",
    "カトル",
    "シャア",
    "セイラ",
    "クワトロ",
    "バジーナ",
    "ブライ",
    "ブライト",
    "アリーナ",
    "クリフト",
    "ケアル",
    "ホイミ",
    "スラ",
    "ホイミン",
    "バーバラ",
    "ミレイ",
    "ミレーユ",
    "ハッサン",
    "ドランゴ",
    "テリー",
    "ロック",
    "ティナ",
    "ティファ",
    "エアリス",
    "クラウド",
    "デュオ",
    "マックス",
    "ミックス",
    "ミント",
    "ババロア",
    "スフレ",
    "プリン",
    "アーモンド",
    "ダンゴ",
    "タンゴ",
    "フルート",
    "フルーツ",
    "オーボエ",
    "ビオラ",
    "ビオレッタ",
    "シー",
    "シズ",
    "サシミ",
    "サラダ",
    "ポンチ",
    "アンコロ",
    "タンタン",
    "カレン",
    "スザク",
    "リズ",
    "コリーン",
    "ファム",
    "ユイ",
    "レイ",
    "シン",
    "サツキ",
    "トロ",
    "ポルコ",
    "ロッソ",
    "ブルー",
    "ルー",
    "アカリ",
    "ミズカ",
    "ミズキ",
    "ゴン",
    "リオ",
    "ピカ",
    "クラ",
    "ニュー",
    "ダム",
    "ガンタ",
    "カンタ",
    "リー",
    "カエル",
    "リーネ",
    "クロノ",
    "ルッカ",
    "ロボ",
    "エイ",
    "ダッチャ",
    "シノブ",
    "キョウコ",
    "ゴダイ",
    "ピコ",
    "コロ",
    "ミコ",
    "ウプ",
    "シェシェ",
    "ラティ",
    "ケニー",
    "カニー",
    "リヴァイ",
    "チェン",
    "ミカサ",
    "デック",
    "リック",
    "ミック",
    "ミニー",
    "シャオ",
    "メル",
    "ゾゾ",
    "メルル",
    "ポップ",
    "ダイ",
    "アバン",
    "くろこ",
    "だい",
    "ミク",
    "ライン",
    "やん",
    "ウェンリー",
    "ハル",
    "ハルキ",
    "ハルヒ",
    "ミサト",
    "リツ",
    "ツツ",
    "スズ",
    "トド",
    "ポポ",
    "ミスタ",
    "ナラン",
    "ボス",
    "ディオ",
    "ディア",
    "ディナ",
    "ランチ",
    "ブレック",
    "ファラ",
    "オヤビン",
    "ゲレゲレ",
    "ビアンカ",
    "フローラ",
    "ピピン",
    "デボラ",
    "ヘンリー",
    "チロル",
    "ボロンゴ",
    "プックル",
    "ぐり",
    "ソロ",
    "ギコギコ",
    "ギンコ",
    "リンクス",
    "アンドレ",
    "メラ",
    "ヒャド",
    "オーラ",
    "ドル",
    "エン",
    "フラン",
    "ルーブル",
    "ルカ",
    "プル",
    "エル",
    "デイン",
    "ギガンテ",
    "ギガ",
    "メガ",
    "テラ",
    "ピコ",
    "ピグミン",
    "ブー",
    "ブウ",
    "リボン",
    "ブック",
    "オルフィー",
    "エルフィン",
    "ビックス",
    "ウェッジ",
    "テンサー",
    "フロー",
    "トーチ",
    "サイキ",
    "ラーン",
    "ら～ん",
    "ナムパイ",
    "パンダ",
    "ぱんだ",
]
name_suffix = ["と言います", "といいます", "です", "という名前です", "と名付けました", "という名前にしました"]


def do_name(is_cat: bool, an: str = None):
    _n = cat_name if is_cat else dog_name
    _ns = cat_suf if is_cat else dog_suf
    nn = random.choice(name)
    n = random.choice(_n) if an is None else an
    ns = ""
    if random.random() > 0.6:
        ns = random.choice(_ns)
    nns = random.choice(name_suffix)
    k = random.choice(kudoku)
    return nn + n + ns + nns + k


deai_pre = [
    "出会いは",
    "最初は",
    "3年前",
    "2年前",
    "昨年",
    "去年",
    "1年前",
    "夏頃",
    "冬頃",
    "春頃",
    "半年前",
    "秋頃",
    "始まりは",
    "はじめは",
    "偶然",
    "なんと",
    "信じられないことに",
    "4年前",
    "数年前に",
    "数ヶ月前に",
    "だいぶ昔に",
]
deai = [
    "ペットショップで",
    "親戚から",
    "知人から",
    "友人から",
    "子供が",
    "公園で",
    "道端で",
    "旅行先で",
    "家の前で",
    "親が",
    "学校で",
    "職場で",
]
deatta = ["拾いました", "もらいました", "引き取りました", "導かれました"]
deatta_suffix = [
    "一目惚れです",
    "ひとめぼれです",
    "最初は仕方なく・・・だったのですが、今はキュンキュンです",
    "最初はちょっと預かるだけのつもりでした",
    "情が移ってメロメロです",
    "家族です",
    "もはや我が子です",
    "完全に我が子です",
    "完全に家族です",
    "家族の一員です",
]


def do_deai():
    dp = ""
    if random.random() > 0.3:
        dp = random.choice(deai_pre)
    d = random.choice(deai)
    de = random.choice(deatta)
    k = random.choice(kudoku)
    ds = ""
    kk = ""
    if random.random() > 0.5:
        ds = random.choice(deatta_suffix)
        kk = random.choice(kudoku)
    return dp + d + de + k + ds + kk


not_mine_place = [
    "道端で",
    "学校で",
    "旅行先で",
    "旅先で",
    "近所で",
    "友人宅で",
    "職場で",
    "公園で",
    "ペットショップで",
    "河原で",
    "山で",
    "家の近くで",
    "通勤途中で",
    "通学途中で",
    "散歩中に",
    "ドライブ中に",
]

not_mine_when = [
    "昨日",
    "昨夜",
    "一昨日",
    "先週",
    "数日前",
    "数週間前",
    "先月",
    "先々週",
    "さっき",
    "ついさっき",
    "今朝",
    "今日",
    "昼前に",
    "午前に",
    "午後に",
]

not_mine_pre = [
    "偶然",
    "ばったり",
    "久しぶりに",
    "たまたま",
    "突然",
    "運命的に",
    "思いがけず",
]
not_mine = [
    "見つけました",
    "出会いました",
    "遭遇しました",
    "見ました",
    "であいました",
    "みかけました",
    "見かけました",
    "邂逅しました",
    "鉢合わせました",
    "会いました",
    "出くわしました",
    "目が合いました",
    "お目にかかりました",
    "めぐりあいました",
]
not_mine_suf = [
    "一目惚れでした",
    "めろめろでした",
    "運命を感じました",
    "かわいすぎました",
    "最高でした",
    "きゃわわわわでした",
    "胸キュンでした",
    "キュンキュンでした",
    "胸が高鳴りました",
    "心躍りました",
    "ズッキューンでした",
    "ドキっとしました",
    "心がはずみました",
    "幸せでした",
    "心が華やぎました",
    "ときめきました",
    "ドッキューンでした",
    "キュンとしました",
]


def do_not_mine():
    nmp = random.choice(not_mine_place)
    nmw = random.choice(not_mine_when)
    mp = random.choice(not_mine_pre)
    nm = random.choice(not_mine)
    nms = random.choice(not_mine_suf)

    s = ""

    nnn = [nmp, nmw, mp]
    nr = random.randint(1, len(nnn))
    nperm = list(permutations(nnn, nr))
    nps = random.choice(nperm)
    logger.info(nps)
    for np in nps:
        logger.info(np)
        s += np
    s += nm
    if random.random() > 0.3:
        s += random.choice(kudoku)
    if random.random() > 0.6:
        s += nms
        if random.random() > 0.4:
            s += random.choice(kudoku)
    logger.info(s)
    return str(s), nmp, nmw, mp, nm, nms


with open("animal.json", "r") as f:
    data = json.load(f)

dd = {}
for k, v in data.items():
    dd[k] = v
    is_cat = True if v["category"] == 1 else False
    l = []

    if random.random() > 0.7:
        logger.info("yours")
        _n = cat_name if is_cat else dog_name
        an = random.choice(_n)

        firsts = ["aisatsu", "name"]
        first_r = random.randint(0, len(firsts))
        first_perm = list(permutations(firsts, first_r))

        lasts = ["hyogen", "naku", "suki", "deai"]
        last_r = random.randint(0, len(lasts))
        last_perm = list(permutations(lasts, last_r))

        fps = random.choice(first_perm)
        lps = random.choice(last_perm)

        for fp in fps:
            if fp == "aisatsu":
                _ai = do_aisatsu()
                l.append(_ai)
            if fp == "name":
                _na = do_name(is_cat=is_cat, an=an)
                l.append(_na)

        for lp in lps:
            if lp == "hyogen":
                _hy = do_hyogen()
                l.append(_hy)
                if random.random() > 0.9:
                    an = _hy
            if lp == "naku":
                _nk = do_naku(is_cat=is_cat)
                l.append(_nk)
                if random.random() > 0.9:
                    an = _nk
            if lp == "suki":
                _sk = do_suki(is_cat=is_cat)
                l.append(_sk)
                if random.random() > 0.9:
                    an = _sk
            if lp == "deai":
                _de = do_deai()
                l.append(_de)
                if random.random() > 0.9:
                    an = _de

        logger.info(l)
        desc = ""
        for ll in l:
            desc += ll
            if random.random() > 0.5:
                desc += "\n"
        _k = random.choice(kudoku)
        if random.random() > 0.7:
            an += _k
        dd[k]["name"] = an
        dd[k]["description"] = desc
    else:
        logger.info("not yours")
        s, nmp, nmw, mp, nm, nms = do_not_mine()
        logger.info(f"{s}, {nmp}, {nmw}, {mp}, {nm}, {nms}")
        naita = do_naita(is_cat=is_cat)

        l = []
        if random.random() > 0.2:
            if random.random() > 0.4:
                if random.random() > 0.6:
                    l.append(s)
                    l.append(naita)
                elif random.random() > 0.7:
                    l.append(naita)
                    l.append(s)
            elif random.random() > 0.6:
                l.append(s)
            elif random.random() > 0.7:
                l.append(naita)
        logger.info(l)
        desc = ""
        for ll in l:
            logger.info(ll)
            desc += ll
            logger.info(desc)
            if random.random() > 0.5:
                desc += "\n"
                logger.info(desc)

        nmss = [n for n in hyogen]
        nmss.extend(gitai)
        nmss.extend(cat_meow if is_cat else dog_bugh)

        length = 1
        if random.random() > 0.7:
            length += 1
        if random.random() > 0.9:
            length += 1
        if random.random() > 0.9:
            length += 1
        nmss_r = random.randint(1, length)
        nmss_p = list(permutations(nmss, nmss_r))

        nr = random.choice(nmss_p)
        an = "".join(nr)
        if random.random() > 0.8:
            an += random.choice(kudoku)
            if random.random() > 0.6:
                an += nmp
            if random.random() > 0.7:
                an += nmw
            if random.random() > 0.6:
                an += mp
        dd[k]["name"] = an
        dd[k]["description"] = desc

    logger.info(dd[k])

with open("animal.json", "w") as f:
    json.dump(dd, f, indent=4, ensure_ascii=False)
