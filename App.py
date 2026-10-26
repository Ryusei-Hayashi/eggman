#from geomstats.learning import frechet_mean, geometric_median
#from geomstats.geometry.hypersphere import Hypersphere
from datetime import time, timedelta
from gdown import download_folder
from yt_dlp import YoutubeDL
from base64 import b64encode
from tensorflow import keras
from os.path import exists
from requests import get
from pickle import load
import tensorflow as tf
import streamlit as st
import librosa
import numpy

st.set_page_config('EgGMAn', ':musical_note:', 'wide', 'expanded')
st.sidebar.link_button('Contact Us', 'https://forms.gle/A4vWuEAp4pPEY4sf9', use_container_width=True)

if not exists('data'):
    download_folder('https://drive.google.com/drive/folders/1LBq7TRMQOfpIrLJoVTebkYNsBAjw9mod')

class TCV(keras.Model):
    def __init__(self, filters, kernels, strides, padding, groups, activation):
        super().__init__()
        self.cv = keras.layers.Conv1D(filters * groups, kernels, strides, padding, groups=groups)
        self.af = keras.layers.Activation(activation)
        self.ln = keras.layers.LayerNormalization()

    def call(self, x):
        s = tf.shape(x)
        x = tf.transpose(x, (0, 1, 3, 2))
        x = tf.reshape(x, (s[0], s[1], -1))
        x = self.cv(x)
        x = self.ln(x)
        x = self.af(x)
        x = tf.reshape(x, (s[0], tf.shape(x)[1], s[-1], -1))
        return x

class CVT(keras.Model):
    def __init__(self, filters, kernels, strides, padding, groups, activation):
        super().__init__()
        self.cv = keras.layers.Conv1D(filters * groups, kernels, strides, padding, groups=groups)
        self.af = keras.layers.Activation(activation)
        self.ln = keras.layers.LayerNormalization()

    def call(self, x):
        s = tf.shape(x)
        x = tf.reshape(x, (s[0], s[1], -1))
        x = self.cv(x)
        x = self.ln(x)
        x = self.af(x)
        x = tf.reshape(x, (s[0], tf.shape(x)[1], s[-2], -1))
        x = tf.transpose(x, (0, 1, 3, 2))
        return x

class CV4(keras.Model):
    def __init__(self, source, target, kernels, strides, padding, activation):
        super().__init__()
        self.cv1 = TCV(target[0], kernels, strides, padding, source[1], activation)
        self.cv2 = TCV(target[1], kernels, strides, padding, target[0], activation)
        self.cv3 = CVT(target[0], kernels, strides, padding, target[1], activation)
        self.cv4 = CVT(target[1], kernels, strides, padding, source[0], activation)

    def call(self, x):
        return self.cv2(self.cv1(x)) + self.cv3(self.cv4(x))

class MCC(keras.Model):
    def __init__(self, source, target, layers, kernels, strides, padding, activation):
        super().__init__()
        g = numpy.geomspace(source, target, layers + 1).round().astype(int)
        self.cvs = [CV4(g[i], g[i+1], kernels, strides, padding, activation) for i in range(layers)]
        self.pwc = keras.layers.Conv2D(source[1], 1, activation=activation)
        self.gru = keras.layers.GRU(target[1], activation=activation)
        self.fcn = keras.layers.Dense(target[1])

    def call(self, x):
        x = x[:, :, :, None]
        x = self.pwc(x)
        for c in self.cvs:
            x = c(x)
        x = x[:, :, 0, :]
        x = self.gru(x)
        x = self.fcn(x)
        return x

@st.cache_resource(max_entries=1)
def model(p):
    m = MCC((bin, 64), (1, dim), 4, 4, 2, 'same', 'silu')
    m(tf.zeros((1, seq, bin)), training=False)
    m.set_weights(load(open(p, 'rb')))
    return m

@st.cache_data(max_entries=1)
def table(p):
    return load(open(p, 'rb'))

@st.cache_data(max_entries=1)
def music(m):
    if m:
        if isinstance(m, str):
            r = get(m, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            if 'html' in r.headers.get('Content-Type', '').lower():
                yd.download([m])
            else:
                open('music.mp3', 'wb').write(r.content)
        else:
            open('music.mp3', 'wb').write(m.getvalue())
        st.html(f'<audio src="data:audio/mp3;base64,{b64encode(open('music.mp3', 'rb').read()).decode()}" controlslist="nodownload" controls></audio>')
        y = librosa.load('music.mp3', sr=sr, duration=60)[0]
        b = librosa.beat.beat_track(y=y, sr=sr, hop_length=sr//fps)[1]
        s = librosa.feature.melspectrogram(y=y, sr=sr, hop_length=sr//fps, n_mels=bin).T
        return pjt(M.predict(numpy.array([pad(s, b, fps * i) for i in range(20, 40, 6)])))

@st.cache_data(max_entries=2)
def scene(c, t, a, v):
    return D[c].apply(lambda x: set(t) <= set(x)) & v[0] <= D['pn'] <= v[1] & a[0] <= D['ap'] <= a[1]

@st.cache_data(max_entries=2)
def basic(a, s, p):
    return ~D['Artist'].isin(a) & ~D['Site'].isin(s) & p[0].strftime('%M:%S') <= D['Time'] <= p[1].strftime('%M:%S')

def idx(n, v):
    i = n.searchsorted(v)
    return n[i-1:i+1].sum() // 2 if 0 < i < len(n) else v

def pad(s, b, t):
    i, j = idx(b, t - 3 * fps), idx(b, t + 3 * fps)
    return numpy.pad(s[i:j], ((0, max(0, seq + i - j)), (0, 0)))[:seq]

def l2n(z):
    return z / (numpy.linalg.norm(z, 2, -1, True) + 1e-12)

def pjt(z):
    h, f = numpy.split(z, 2, -1)
    return l2n(numpy.mean(numpy.c_[l2n(h), l2n(f)], 0))

def rep(t, a, v, r):
    d = D.loc[scene('hard', t, a, v)]
    c = d['hard'].apply(lambda x: sum(e in t for e in x))
    return l2n(numpy.stack(d.loc[c.nlargest(round(r * len(D))).min() <= c, 'vec']).mean(0))

def opr(z, r):
    return l2n(numpy.r_[z[:len(z)//2], r[len(r)//2:]])

dim = 256
bin = 256
seq = 256
fps = 42
sr = 22050
yd = YoutubeDL({'outtmpl': 'music', 'playlist_items': '1', 'format': 'bestaudio', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}], 'postprocessor_args': ['-ss', '0', '-t', '60'], 'overwrites': True})

M = model('data/model.pkl')
D = table('data/table.pkl')

st.image('imgs/logo.png')
st.html('<center>EgGMAn (Engine of Game Music Analysis) searches for game music balancing game-wise consistency and scene-wise individuality</center>')

st.header('Source Music')
t = st.tabs(['URL Input', 'File Input'])
if t[0].open:
    m = t[0].text_input('URL of Source Music')
if t[1].open:
    m = t[1].file_uploader('File of Source Music')
z = music(m)

st.header('Target Scene')
u = st.multiselect('Tag of Target Scene', ('オープニング', 'エンディング', 'タイトル', 'イベント', 'チュートリアル', 'ゲーム失敗', 'ゲーム成功', 'ハイライト', 'セレクト画面', 'マップ画面', 'フィールド', 'ダンジョン', 'ステージ', 'ショップ', 'マイルーム', 'レストゾーン', '春', '夏', '秋', '冬', '朝', '昼', '夜', '明方', '夕方', '休日', '原始', '古代', '中世', '近代', '現代', '未来', '虹', '星', '晴', '曇', '霧', '雪', '砂', '雷', '雨', '小雨', '大雨', '暴風', '混沌', '朝焼け', '夕焼け', 'オーロラ', '異次元', '虚無', '宇宙', '陸', '海', '空', '東', '西', '南', '北', '氷', '炎', '花', '山', '谷', '坂', '崖', '岩', '島', '浜', '岸', '川', '沼', '湖', '泉', '温泉', '水辺', '水中', '洞窟', '地底', '地上', '砂漠', '草原', '森林', 'サバンナ', 'ジャングル', '仮想空間', '都会', '田舎', '街', '村', '橋', '道', '地下道', '路地裏', '飛行機', '鉄道', '船', '港', '駅', '宿', '店', '飲食店', '飲み屋', '遊園地', '動物園', '水族館', '博物館', '競技場', '公園', '法廷', '学校', '病院', '教会', '神社', '寺', '墓', '畑', '牧場', '工場', '倉庫', '研究所', '監獄', '要塞', '城', '庭', '家', '邸宅', '宮廷', '神殿', '遺跡', '廃墟', '隠れ家', 'ロビー', 'タワー', 'ビル', 'ジム', 'プール', 'エステ', 'カフェ', 'カジノ', 'シアター', 'キャバレー', 'リゾート', 'オフィス', 'ベランダ', 'マスコット', 'ヒーロー', 'ヒロイン', 'ライバル', 'ラスボス', 'ボス', '敵', '孤独', '不穏', '平穏', '裏切者', '人込み', '庶民', '貴族', '偉人', '仲間', '戦闘', '探検', '調査', '潜入', '追跡', '逃走', '走る', '飛ぶ', '泳ぐ', '説明', '話す', '考える', 'お出かけ', '買い物', '遊ぶ', '休憩', '治療', '世話', '準備', '練習', '公演', '結婚', '恋愛', '祭り', '宴会', '食事', '祈り', '弔い', '儀式', '復讐', '破滅', '悪事', '犯罪', '企む', '偽り', 'いたずら', '魅惑', '応援', '称賛', '勝利', '敗北', '騒動', '喧嘩', '和解', '再起', '集結', '登場', '出会い', '別れ', '回想', '感動', '決意', '失意', '混乱', '悩む', '焦る', 'レース', 'スポーツ', 'コメディ', 'ギャンブル'))
st.subheader('Emotion of Target Scene')
c = st.columns(2, gap='medium')
v = c[0].slider('Valence of Target Scene', -1.0, 1.0, (-1.0, 1.0))
a = c[1].slider('Arousal of Target Scene', -1.0, 1.0, (-1.0, 1.0))

st.header('Target Music')
b = st.multiselect('Mute Artist', ('Nash Music Library'))
s = st.multiselect('Mute Site', ('Nash Music Library'))
p = st.slider('Playtime', time(0), time(0, 59), (time(0), time(0, 59)), timedelta(seconds=10), 'mm:ss')
f = st.toggle('Filter by Target Scene')
if st.button('Search', type='primary'):
    try:
        r = rep(u, v, a, 0.01)
        d = D.loc[basic(b, s, p) & (scene('soft', u, a, v) if f else True)]
        st.dataframe(d.iloc[(numpy.stack(d['vec']) @ opr(z, r)).argsort()[:-99:-1], :5].reset_index(drop=True), column_config={'URL': st.column_config.LinkColumn()})
    except:
        st.error('No music matches the conditions')
