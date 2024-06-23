"""
データフレームを作成するクラス
インスタンスは持たない

Author: Kenta Matsumura
"""

# ---------------------------------------------------------- #
# サードパーティライブラリのインポート
# ---------------------------------------------------------- #
import customtkinter as ctk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import math

# ---------------------------------------------------------- #
# 自作ライブラリのインポート
# ---------------------------------------------------------- #
from common import *

# ---------------------------------------------------------- #
# クラス定義
# ---------------------------------------------------------- #
class MakeDataFrame():
    def __init__(self):
        """
        データフレームの作成・成形を実施
        """
           
    @staticmethod
    def makeCANDataFrame(file_path, all_columns, camera_columns, vbox_columns, camera_invalid_value, initial_head, is_use_head, output_label):
        """
        データフレームの作成を実施
        
        parameters
        ----------
            file_path : CANログのファイルパス 
                作成したタブの格納先のフレーム
        """
        # ファイルパスの確認
        try:
            with open(file_path, "r") as file: # 左の書き方なら自動でファイル閉じられる
                pass
        except: #ファイルが開かない時
            output_label.configure(text="ファイルを\n開けません")
            return (False, None, None, None)
            
        # skiprows(AutoboxからのCAN出力フォーマットに合わせている)
        skiprows = list(range(0,16)) + list(range(17,28))
        
        # DataFrameの作成
        df_all = pd.read_csv(file_path, skiprows=skiprows, usecols=lambda column:column in all_columns) #選択したカラムがあれば抽出

        # Autobox側でデータをもれなくログ記録設定できてるかを確認(欄が狭いから1データだけ表示)
        for column in all_columns:
            if column not in set(df_all.columns):
                output_label.configure(text="{}が\n取得できていません".format(column))
                return (False, None, None, None)
        
        #カラムにデータの欠損(Nan)が無いかを確認(欄が狭いから1データだけ表示)
        columns_with_nan = df_all.columns[df_all.isnull().any()].tolist()
        if len(columns_with_nan):
            for column in columns_with_nan:
                output_label.configure(text="{}の値に\nNanが含まれています".format(column))
                return (False, None, None, None)
        
        # カラムのデータが全て0ではないかを判定
        # for column in all_columns:
        #     if (self.df_all[column] == 0).all():
        #         output_label.configure(text="{}の値が\n全て0です".format(column))
        #         return False
        
        # 選択したデータは取得できていることを示す
        output_label.configure(text="選択したデータは\n取得できています")
        
        # 経過時間の列の作成        
        df_all["Elapsed_Time"] = [i for i in range(len(df_all))]
                
        df_camera = MakeDataFrame.makeCameraDataFrame(df_all, camera_columns, camera_invalid_value)
        df_vbox   = MakeDataFrame.makeVboxDataFrame(df_all, vbox_columns, initial_head, is_use_head)
        
        return (True, df_all, df_camera, df_vbox)
    
    # カメラのDataFrameの作成
    @staticmethod
    def makeCameraDataFrame(df_all, camera_columns, camera_invalid_value):
        # カメラのカラムを抽出
        df_camera = df_all[camera_columns]

        #物標1と物標3を統合したカメラの値を取得
        df_camera = MakeDataFrame.integrateTarget1AndTarget3(df_camera, camera_columns, camera_invalid_value)     
        
        # 後方カメラの値が変わる最初の行を見つける        
        camera_start_index = MakeDataFrame.findStartIndex(df_camera, camera_columns[1:], camera_invalid_value)
        print("camera_start_index : {}".format(camera_start_index))
        
        # 見つけた行が0行目になるように上にずらす
        df_camera = df_camera.shift(-1*camera_start_index)
        
        # 100ms(100行でスライス)=後方カメラの100msに合わせる
        df_camera = df_camera.iloc[list(range(0, len(df_camera), 100))].reset_index(drop=True)
        
        # camera_distが有効値の行を抽出
        df_camera = df_camera[abs(df_camera['dist_camera'] - camera_invalid_value) > EPSILON]
        
        # NANを含む行を削除
        df_camera = df_camera.dropna().reset_index(drop=True)
        
        return df_camera

    #後方カメラが物標を認識し始めた最初の行を見つける
    #値は100ms毎に代わるが、canは50msで送信の為、同じ値が2回流れるため、基準の行で遅延時間が変わる
    @staticmethod
    def findStartIndex(df_camera, columns, NG):
        #初期値から切り替わった行を探す
        index = len(df_camera)
        print("NG:{}".format(NG))
        print("columns:{}".format(columns))
        for column in columns: #物標1と3で最初に変わったほうを選択
            for i in list(range(len(df_camera))):
                if abs(df_camera[column][i] - NG) > EPSILON:
                    index = min(index, i)

        return index
                    
    #物標1と3の縦距離・横距離の値を1つのカラムに統合してリストの結果をreturn
    @staticmethod
    def integrateTarget1AndTarget3(df_camera, camera_columns, NG):
        result = [] #統合後のリスト
        for i in list(range(len(df_camera))):
            target1 = df_camera[camera_columns[1]][i]
            target3 = df_camera[camera_columns[2]][i]
            select_target = 0
            
            if abs(target1 - NG) < EPSILON and abs(target3 - NG) < EPSILON: #両方無効
                select_target = target1
            elif abs(target1 - NG) > EPSILON and abs(target3 - NG) < EPSILON: #1が有効で3が無効
                select_target = target1
            elif abs(target1 - NG) < EPSILON and abs(target3 - NG)>EPSILON: #1が無効で3が有効
                select_target = target3
            else: #両方有効(1⇒3 or 3⇒1に切り替わりの時)
                if i==0: #1行目なら1を採用
                    select_target = target1
                else: #2行目以降：前回が無効だった方を採用
                    target1_bef = df_camera[camera_columns[0]][i-1]
                    if abs(target1_bef - NG) < EPSILON:
                        select_target = target1
                    else:
                        select_target = target3
            #採用する値を追加
            result.append(select_target)
        
        # copyにしないとwarnigでた
        df_camera_copy = df_camera.copy()
        df_camera_copy["dist_camera"] = result
        
        return df_camera_copy

    # VboxのDataFrameの作成
    @staticmethod
    def makeVboxDataFrame(df_all, vbox_columns, initial_head, is_use_head):
        # Vboxのカラムを抽出
        df_vbox = df_all[vbox_columns]

        # 10ms(10行でスライス)=vboxのcan周期の10msに合わせる
        df_vbox = df_vbox.iloc[list(range(0, len(df_vbox), 10))].reset_index(drop=True)
        
        # Vboxの距離を示すカラムを作成
        MakeDataFrame.makeVboxDistColumn(df_vbox, vbox_columns, initial_head, is_use_head)
        
        # スムージング
        df_vbox["smoothing"] = MakeDataFrame.RunMovingAverages(df_vbox, "vbox_dist", 0)
        
        return df_vbox

    #移動平均
    @staticmethod
    def RunMovingAverages(df_vbox, column, window):
        result = []
        if window == 0: #移動平均無ならそのまま返す
            result = df_vbox[column]
        else:
            result = df_vbox[column].rolling(window, center=True).mean()
        return result
    
    # Vboxの距離を示すカラムを作成
    def makeVboxDistColumn(df_vbox, vbox_columns, initial_head, is_use_head):
        if "True_Heading" in set(vbox_columns): #もしTrueHeadを考慮する必要がある(横距離の時だけ)
            if is_use_head:
                # 傾きを出す
                diff_head = df_vbox["True_Heading"] - [initial_head]*len(df_vbox) #degree
                for i in range(len(diff_head)):
                    if diff_head[i] > 0:
                        diff_head[i] = 90 - diff_head[i]
                    else:
                        diff_head[i] = (90 - abs(diff_head[i])) * -1
                
                # degree⇒radians
                diff_head = [math.radians(deg) for deg in diff_head]
                
                # 点と直線の距離を出す
                vbox_dist = []
                for i in range(len(df_vbox)):
                    rad = diff_head[i]
                    x0  = df_vbox["LatRtg_tg1"][i]
                    y0  = df_vbox["LngRtg_tg1"][i]
                    x1  = df_vbox["Dummy_Y_Po"][i]
                    y1  = 0
                    dist = MakeDataFrame.distanceFromLineToPoint(rad, x0, y0, x1, y1)
                    vbox_dist.append(dist)
                
                df_vbox["vbox_dist"] = vbox_dist
                
            else:
                df_vbox["vbox_dist"] = df_vbox["Dummy_Y_Po"]
        else:
            df_vbox["vbox_dist"] = df_vbox[vbox_columns[1]]
    
    @staticmethod
    def distanceFromLineToPoint(A_rad, x0, y0, x1, y1):
        # 傾き A ラジアンの直線の係数を計算
        tan_A = math.tan(A_rad)
        a = -tan_A
        b = 1
        c = tan_A * x0 - y0
        
        # 点 (x1, y1) と直線 ax + by + c = 0 との距離を計算する
        numerator = abs(a * x1 + b * y1 + c)
        denominator = math.sqrt(a**2 + b**2)
        
        distance = numerator / denominator
        return distance
    
    @staticmethod  
    def makeRAMDataFrame(file_path, output_label):
        # ファイルパスの確認
        try:
            with open(file_path, "r") as file: # 左の書き方なら自動でファイル閉じられる
                pass
        except: #ファイルが開かない時
            output_label.configure(text="ファイルを\n開けません")
            return False, None
        
        df_RAM = pd.read_csv(file_path, usecols=RAM_COLUMNS).dropna().reset_index(drop=True)
        output_label.configure(text="読み込み完了しました")
        
        return True, df_RAM
    
            