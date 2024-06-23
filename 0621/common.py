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
MIDDLE_FONT = ("MSゴシック", 10)
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
ALL_COLUMNS_STATIONARY = ["RCMRDEPLOC1", "RCMRDEPLOC3", "RCMRHOLLOC1", "RCMRHOLLOC3", "LngRsv_tg1", "LatRsv_tg1"]

# ダミー移動(Vbox1台、ドライブユニット1台)
ALL_COLUMNS_MOVE = ["RCMRDEPLOC1", "RCMRDEPLOC3", "RCMRHOLLOC1", "RCMRHOLLOC3", "LngRsv_tg1", "LatRsv_tg1", "LngRtg_tg1", "LatRtg_tg1", "Dummy_Y_Po", "True_Heading"]

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
RAM_COLUMNS = ["FrameCnt", "Timestamp", "X1", "Z1"]

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