"""
定数設定用ファイル

Author: Kenta Matsumura
"""

import tkinter as tk
from enum import Enum
import customtkinter as ctk

# ---------------------------------------------------------- #
# widgetの見た目の設定
# ---------------------------------------------------------- #
# フォントの大きさ
BIG_FONT    = ("MSゴシック", 12)
MIDDLE_FONT = ("MSゴシック", 15)
SMALL_FONT  = ("MSゴシック", 20)
# widgetの見た目
# Frame
FRAME_PARAMS = {
    # "border_width" : 1,
    # "fg_color"     : "black",
    # "border_color" : "black"
}

# Label
LABEL_PARAMS = {
    # "corner_radius" : 1,
    # "fg_color"      : "black",
    # "text_color"    : "white",     #文字の色
    "font"          : SMALL_FONT,  #文字の大きさ
}

# entry
ENTRY_PARAMS = {
    # "corner_radius" : 1,
    # "fg_color"      : "black",
    # "text_color"    : "white",     #文字の色
    "font"          : SMALL_FONT,  #文字の大きさ   
}

# button
BUTTON_PARAMS = {
    # "corner_radius" : 1,
    # "border_width"  : 2,
    # "fg_color"      : "white",
    "font"          : SMALL_FONT,  #文字の大きさ   
}

# spinbox
SPINBOX_PARMAS = {
    "bg"    : "white",
    "bd"    : 3,
    "relief": tk.SOLID,
}
# scale
SCALE_PARAMS = {
    "bg"    : "white",
    "bd"    : 3,
    "relief": tk.SOLID,
}

# switch
SWITCH_PARAMS = {
    "font" : SMALL_FONT,
}

# radiobox
RADIOBUTTON_PARMAS = {
    "font" : SMALL_FONT,
}

VALUE_LABEL_PARAMS = {
    # "corner_radius" : 1,
    # "fg_color"      : "black",
    # "text_color"    : "white",     #文字の色
    "font"          : MIDDLE_FONT,  #文字の大きさ
}

# ---------------------------------------------------------- #
# 後方カメラのCAN値
# ---------------------------------------------------------- #
# # 認識できなかった時の送信値
LNG_NG = 12.75 # 後方カメラの縦のNG[m]
LAT_NG = 6.35  # 後方カメラの横のNG[m]

# ---------------------------------------------------------- #
# 浮動小数点の許容誤差
# ---------------------------------------------------------- #
EPSILON = 1e-9

# ---------------------------------------------------------- #
# 統計量
# ---------------------------------------------------------- #
# 縦距離
AREA_LNG_ADULT = [(3, 6), (2, 3), (0.75, 2), (0.75, 6)]
AREA_LNG_CHILD = [(3, 6), (2, 3), (0.5, 2),  (0.5,  6)]

# 横距離
AREA_LAT       = [(-1.5, 1.5)]

# 参考値
# [自車, ダミー] = [静止, 静止]
REFERENCE_SS = {
    ("600", "0")   : [("-35.0±16.6"), ("-2.1±3.8")],
    ("600", "150") : [("-32.5±20.7"), ("-14.0±5.8")],
    ("300", "0")   : [("-25.7±7.8"),  ("-2.7±2.2")],
    ("300", "150") : [("-21.8±17.9"), ("-12.4±6.8")],
    ("100", "0")   : [("-0.8±5.5"),   ("-0.7±1.8")],
    ("100", "150") : [("-7.7±4.7"),   ("-11.7±5.3")],
}

# [自車, ダミー] = [移動, 静止]
REFERENCE_MS_LNG = ["-17.7±28.7", "3.6±13.8", "5.1±10.5"]

REFERENCE_MS_LAT = ["-7.0±3.6", "-2.4±3.7", "-0.7±3.9"]

# [自車, ダミー] = [静止, 移動](横切り)
REFERENCE_SM_SIDE_LNG = ["-18.4±23.9", "-4.7±12.9", "10.7±8.0"]

REFERENCE_SM_SIDE_LAT = ["32.0±7.6", "37.0±4.6", "41.2±16.4"]

# [自車, ダミー] = [静止, 移動](後方)
REFERENCE_SM_BACK_LNG = ["12.2±24.2", "24.9±27.1", "33.6±20.1"]

REFERENCE_SM_BACK_LAT = ["1.6±11.5", "1.8±9.8", "1.6±7.0"]


# [自車, ダミー] = [移動, 移動]
REFERENCE_MM_LNG = ["13.4±10.2"]

REFERENCE_MM_LAT = ["43.3±10.9"]



# ---------------------------------------------------------- #
# グラフの設定
# ---------------------------------------------------------- #

class FrameOptions(Enum):
    INITIAL = 1
    DELETE  = 2
    ADD     = 3
    
class DrawOptions(Enum):
    INITIAL = 1
    UPDATE  = 2

class WidgetType(Enum):
    PLUS_BUTTON  = 1
    MINUS_BUTTON = 2
    SLIDER       = 3
    
class GraphUpdateType(Enum):
    SMOOTHING = 1
    SHIFT     = 2

# グラフで描画する距離の方向
class Direction(Enum):
    LNG = 1
    LAT = 2

# ダミーの動き(ダミーの動きによって使うデータが変わる)
class Dummy(Enum):
    STATIONARY = 1
    MOVE       = 2

class SensorSelect(Enum):
    CAMERA = 1
    VBOX   = 2

# カラム
# ダミー静止(Vbox２台)
ALL_COLUMNS_STATIONARY  = ["RCMRDEPLOC1",  "RCMRDEPLOC3", "RCMRHOLLOC1", "RCMRHOLLOC3", "LngRsv_tg1", "LatRsv_tg1"]
CAMERA_COLUMNS          = ["Elapsed_Time", "RCMRDEPLOC1", "RCMRDEPLOC3", "RCMRHOLLOC1", "RCMRHOLLOC3"]
VBOX_COLUMNS_STATIONARY = ["Elapsed_Time", "LngRsv_tg1",  "LatRsv_tg1"]

# ダミー移動(Vbox1台、ドライブユニット1台)
ALL_COLUMNS_MOVE  = ["RCMRDEPLOC1", "RCMRDEPLOC3", "RCMRHOLLOC1", "RCMRHOLLOC3", "LngRsv_tg1", "LatRsv_tg1", "LngRtg_tg1", "LatRtg_tg1", "Dummy_Y_Po", "True_Heading"]
VBOX_COLUMNS_MOVE = ["Elapsed_Time", "LngRsv_tg1",  "LatRsv_tg1", "LngRtg_tg1", "LatRtg_tg1", "Dummy_Y_Po", "True_Heading"]

# カメラ
CAMERA_LNG_COLUMNS = ["Elapsed_Time", "RCMRDEPLOC1", "RCMRDEPLOC3"]
CAMERA_LAT_COLUMNS = ["Elapsed_Time", "RCMRHOLLOC1", "RCMRHOLLOC3"]

# vbox
# ダミー静止
VBOX_LNG_COLUMNS_STATIONARY = ["Elapsed_Time", "LngRsv_tg1"]
VBOX_LAT_COLUMNS_STATIONARY = ["Elapsed_Time", "LatRsv_tg1"]

# ダミー移動
VBOX_LNG_COLUMNS_MOVE = ["Elapsed_Time", "LngRsv_tg1"]
VBOX_LAT_COLUMNS_MOVE = ["Elapsed_Time", "LatRsv_tg1", "LngRtg_tg1", "LatRtg_tg1", "Dummy_Y_Po", "True_Heading"] # 今は横だけ方位考える(今後縦も追加)

# RAM
RAM_COLUMNS = ["FrameCnt", "Timestamp", "X1", "Z1", "X1_Truth", "Z1_Truth"]


# ---------------------------------------------------------- #
# グラフの体裁
# ---------------------------------------------------------- #
TITLE_PARAMS = {
    "title"     : "hoge",
    "fontsize"  : 16,
} 

# X軸
X_PARAMS = {
    "label"     : "",
    "labelsize" : 12,
    "fontsize"  : 14,
    "xlim"      : [(0, 100, 1)],
    "set_xlim"  : [False]
}

# Y軸
Y_PARAMS = {
    "label"     : [], # 軸名のリスト
    "fontsize"  : 14,
    "labelsize" : 12,
    "plot_type" : ["scatter"],
    "y_lim"     : [(0,100)],
    "set_ylim"  : [False]
}

# 折れ線グラフ
PLOT_PARAMS = {
    "linewidth" : [5],       # 線の太さ
    "linestyle" : ['-'],     # 線の種類
    "color"     : ["black"], # 線の色
    "marker"    : ["None"],  # マーカー
    
}

# 散布図
SCATTER_PARAMS = {
    "s" : [10],      # 点のサイズ
    "c" : ["black"], # 点の色
}

# ---------------------------------------------------------- #
# 共通の関数
# ---------------------------------------------------------- #  
def changeWidgetState(*args):
    """
    widgetの状態を編集可能⇔編集不可能に切り替える。
    
    parameters
    ----------
        args : ctk.Entry or 
            状態を変更する対象のwidget(可変長引数)
    """
    for widget in args:
        if widget.cget("state") == ctk.DISABLED:
            widget.configure(state=ctk.NORMAL)
        else:
            widget.configure(state=ctk.DISABLED)

def selectFilePath(file_path_entry, ftypes=[("すべて","*")]):
    """
    ファイルパスを参照(選択)する
    
    parameters
    ----------
        file_path_entry : ctk.Entry
            ファイルパスの入力先
        ftypes : list of tuple of string, default [("すべて","*")]
            フォルダで表示するファイルの種類
    """
    # 参照開始フォルダの取得
    start_folder = "C:\\Users" 
    index = file_path_entry.get().rfind('/')
    if index != -1:
        start_folder = file_path_entry.get()[:index]
    
    file_path_entry.delete(0, ctk.END) 
            
    # ファイルパスを入力ボックスに格納
    file_path = ctk.filedialog.askopenfilename(filetypes=ftypes, initialdir=start_folder) 
    file_path_entry.insert(0, file_path)