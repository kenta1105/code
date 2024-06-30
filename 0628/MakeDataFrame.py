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
    def makeCANDataFrame(file_path, all_columns, camera_columns, vbox_columns, initial_head, is_use_head, output_label):
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
                
        df_camera = MakeDataFrame.makeCameraDataFrame(df_all, camera_columns)
        df_vbox   = MakeDataFrame.makeVboxDataFrame(df_all, vbox_columns, initial_head, is_use_head)
        
        return (True, df_all, df_camera, df_vbox)
    
    # カメラのDataFrameの作成
    @staticmethod
    def makeCameraDataFrame(df_all, camera_columns):
        # カメラのカラムを抽出
        df_camera = df_all[camera_columns]

        #物標1と物標3を統合したカメラの値を取得
        df_camera = MakeDataFrame.integrateTarget1AndTarget3(df_camera)     
        
        # 後方カメラの値が変わる最初の行を見つける        
        camera_start_index = MakeDataFrame.findStartIndex(df_camera)
        print("camera_start_index : {}".format(camera_start_index))
        
        # 見つけた行が0行目になるように上にずらす
        df_camera = df_camera.shift(-1*camera_start_index)
        
        # 100ms(100行でスライス)=後方カメラの100msに合わせる
        df_camera = df_camera.iloc[list(range(0, len(df_camera), 100))].reset_index(drop=True)
        
        # camera_distが有効値の行を抽出(なんでこれしてる？)
        df_camera = df_camera[(abs(df_camera["camera_lng"] - LNG_NG) > EPSILON) & (abs(df_camera["camera_lat"] - LAT_NG) > EPSILON)]
        
        # NANを含む行を削除
        df_camera = df_camera.dropna().reset_index(drop=True)
        
        return df_camera
                    
    #物標1と3の縦距離・横距離の値を1つのカラムに統合してリストの結果をreturn
    @staticmethod
    def integrateTarget1AndTarget3(df_camera):
        lng_result = [] #統合後のリスト
        lat_result = []
        for i in list(range(len(df_camera))):
            # 縦
            target1_lng = df_camera["RCMRDEPLOC1"][i]
            target1_lat = df_camera["RCMRHOLLOC1"][i]
            # 横
            target3_lng = df_camera["RCMRDEPLOC3"][i]
            target3_lat = df_camera["RCMRHOLLOC3"][i]
            
            # 物標1・3の有効無効結果
            is_valid_target1 = abs(target1_lng - LNG_NG) > EPSILON and abs(target1_lat - LAT_NG) > EPSILON
            is_valid_target3 = abs(target3_lng - LNG_NG) > EPSILON and abs(target3_lat - LAT_NG) > EPSILON
            
            # 最終的に選択した値
            select_lng = 0
            select_lat = 0
            
            if (is_valid_target1 == False and is_valid_target3 == False) or (is_valid_target1 == True and is_valid_target3 == False): #両方無効 or 1が有効で3が無効
                select_lng = target1_lng
                select_lat = target1_lat
            elif  is_valid_target1 == False and is_valid_target3 == True: #1が無効で3が有効
                select_lng = target3_lng
                select_lat = target3_lat
            else: #両方有効(1⇒3 or 3⇒1に切り替わりの時)
                if i==0: #1行目なら1を採用
                    select_lng = target1_lng
                    select_lat = target1_lat
                else: #2行目以降：前回値が無効だった方を採用
                    target1_lng_bef = df_camera["RCMRDEPLOC1"][i-1]
                    target1_lat_bef = df_camera["RCMRHOLLOC1"][i-1]
                    is_valid_target1_bef =  abs(target1_lng_bef - LNG_NG) > EPSILON and abs(target1_lat_bef - LAT_NG) > EPSILON
                    if is_valid_target1_bef == False:
                        select_lng = target1_lng
                        select_lat = target1_lat
                    else:
                        select_lng = target3_lng
                        select_lat = target3_lat
            #採用する値を追加
            lng_result.append(select_lng)
            lat_result.append(select_lat)
        
        # copyにしないとwarnigでた
        df_camera_copy = df_camera.copy()
        df_camera_copy["camera_lng"] = lng_result
        df_camera_copy["camera_lat"] = lat_result
        
        return df_camera_copy

    #後方カメラが物標を認識し始めた最初の行を見つける
    #値は100ms毎に代わるが、canは50msで送信の為、同じ値が2回流れるため、基準の行で遅延時間が変わる
    @staticmethod
    def findStartIndex(df_camera):
        #初期値から切り替わった行を探す
        index = len(df_camera)

        for i in list(range(len(df_camera))):
            if (abs(df_camera["camera_lng"][i] - LNG_NG) > EPSILON) and (abs(df_camera["camera_lat"][i] - LAT_NG) > EPSILON):
                index = i
                break

        return index

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
        df_vbox["smoothing_lng"] = MakeDataFrame.RunMovingAverages(df_vbox, "vbox_lng", 0)
        df_vbox["smoothing_lat"] = MakeDataFrame.RunMovingAverages(df_vbox, "vbox_lat", 0)
        
        return df_vbox
    
    # Vboxの距離を示すカラムを作成
    def makeVboxDistColumn(df_vbox, vbox_columns, initial_head, is_use_head):
        # 縦距離
        df_vbox["vbox_lng"] = df_vbox["LngRsv_tg1"]
        
        # 横距離
        # ダミー移動かどうかで変わる
        if "Dummy_Y_Po" in set(vbox_columns): # ダミー移動時
            if is_use_head: # 傾きを考慮する時
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
                dist_vbox = []
                for i in range(len(df_vbox)):
                    rad = diff_head[i]
                    x0  = df_vbox["LatRtg_tg1"][i]
                    y0  = df_vbox["LngRtg_tg1"][i]
                    x1  = df_vbox["Dummy_Y_Po"][i]
                    y1  = 0
                    dist = MakeDataFrame.distanceFromLineToPoint(rad, x0, y0, x1, y1)
                    dist_vbox.append(dist)
                
                df_vbox["vbox_lat"] = dist_vbox
            else: # 傾きを考慮しない時
                df_vbox["vbox_lat"] = df_vbox["Dummy_Y_Po"]
        else: # ダミー静止時
            df_vbox["vbox_lat"] = df_vbox["LatRsv_tg1"]
    
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

    #移動平均
    @staticmethod
    def RunMovingAverages(df_vbox, column, window):
        result = []
        if window == 0: #移動平均無ならそのまま返す
            result = df_vbox[column]
        else:
            result = df_vbox[column].rolling(window, center=True).mean()
        return result
        
    @staticmethod
    def computeStatics(df_all, df_camera, df_vbox, shift_time, dummy_type):
        # カメラの時間をシフト
        df_camera_copy = df_camera.copy()
        df_camera_copy["Elapsed_Time"] = df_camera_copy["Elapsed_Time"] + shift_time
        
        # vboxをコピー
        df_vbox_copy = df_vbox.copy()
        
        # df_allと同じ大きさのdfを作成
        df_statics = pd.DataFrame()
        df_statics["Elapsed_Time"] = list(range(len(df_all)))
        
        # ElapsedTimeを基準にvboxのdfを合体
        df_statics = pd.merge(df_statics, df_vbox_copy, on='Elapsed_Time', how='outer')
        
        # Nan値を前の値で引き継ぐ(10ms間は同じ値)
        df_statics = df_statics.ffill()
        
        # カメラのdfと合体(カメラとVboxの両方のdfに共通する時間の行だけを抽出)
        df_statics = pd.merge(df_statics, df_camera_copy, on='Elapsed_Time', how='inner')
        
        # 差分を算出
        df_statics["diff_lng"] = df_statics["camera_lng"] - (-1*df_statics["smoothing_lng"]) # 縦
        df_statics["diff_lat"] = df_statics["camera_lat"] - (-1*df_statics["smoothing_lat"]) # 横
        
        # 差分の統計量を算出
        statics_result = []

        # 全部考慮
        mean_lng = round(df_statics["diff_lng"].mean()*100, 1) # m⇒cmに変換して少数第一位まで表示
        std_lng  = round(df_statics["diff_lng"].std()*100, 1)  # m⇒cmに変換して少数第一位まで表示
        value_lng = str(mean_lng) + "±" + str(std_lng)

        mean_lat = round(df_statics["diff_lat"].mean()*100, 1) # m⇒cmに変換して少数第一位まで表示
        std_lat  = round(df_statics["diff_lat"].std()*100, 1)  # m⇒cmに変換して少数第一位まで表示        
        value_lat = str(mean_lat) + "±" + str(std_lat)
        
        statics_result.append((value_lng, value_lat))
        
        # 距離ごとに抽出
        area_lng = None
        if dummy_type == 1: # 大人
            area_lng = AREA_LNG_ADULT
        else:
            area_lng = AREA_LNG_CHILD
        
        # 自車・ダミー片方だけ移動の時
        for i in range(len(area_lng)-1):
            min_LNG = area_lng[i][0]
            max_LNG = area_lng[i][1]
            min_LAT = AREA_LAT[0][0]
            max_LAT = AREA_LAT[0][1]
            
            # Vbox(真値)の縦と横がエリア内の行を抽出
            df_filterd = df_statics[(df_statics['smoothing_lng']*-1 >= min_LNG) & (df_statics['smoothing_lng']*-1 < max_LNG) & 
                                    (df_statics['smoothing_lat']*-1 >= min_LAT) & (df_statics['smoothing_lat']*-1 < max_LAT)]
            
            # 縦
            mean_lng  = round(df_filterd["diff_lng"].mean()*100, 1) # m⇒cmに変換して少数第一位まで表示
            std_lng   = round(df_filterd["diff_lng"].std()*100,  1) # m⇒cmに変換して少数第一位まで表示
            value_lng = str(mean_lng) + "±" + str(std_lng)
            
            # 横
            mean_lat  = round(df_filterd["diff_lat"].mean()*100, 1) # m⇒cmに変換して少数第一位まで表示
            std_lat   = round(df_filterd["diff_lat"].std()*100,  1) # m⇒cmに変換して少数第一位まで表示
            value_lat = str(mean_lat) + "±" + str(std_lat)
            
            statics_result.append((value_lng, value_lat))
            
        
        # 両方移動時(縦距離の条件が<=なので分けた)
        min_LNG = area_lng[-1][0]
        max_LNG = area_lng[-1][1]
        min_LAT = AREA_LAT[0][0]
        max_LAT = AREA_LAT[0][1]
            
        # Vbox(真値)の縦と横がエリア内の行を抽出
        df_filterd = df_statics[(df_statics['smoothing_lng']*-1 >= min_LNG) & (df_statics['smoothing_lng']*-1 <= max_LNG) & 
                                (df_statics['smoothing_lat']*-1 >= min_LAT) & (df_statics['smoothing_lat']*-1 <= max_LAT)]

        # 縦
        mean_lng  = round(df_filterd["diff_lng"].mean()*100, 1) # m⇒cmに変換して少数第一位まで表示
        std_lng   = round(df_filterd["diff_lng"].std()*100,  1) # m⇒cmに変換して少数第一位まで表示
        value_lng = str(mean_lng) + "±" + str(std_lng)
        
        # 横
        mean_lat  = round(df_filterd["diff_lat"].mean()*100, 1) # m⇒cmに変換して少数第一位まで表示
        std_lat   = round(df_filterd["diff_lat"].std()*100,  1) # m⇒cmに変換して少数第一位まで表示
        value_lat = str(mean_lat) + "±" + str(std_lat)

        statics_result.append((value_lng, value_lat))
        
        return statics_result

    @staticmethod  
    def makeRAMDataFrame(file_path, output_label):
        # ファイルパスの確認
        try:
            with open(file_path, "r") as file: # 左の書き方なら自動でファイル閉じられる
                pass
        except: #ファイルが開かない時
            output_label.configure(text="ファイルを\n開けません")
            return False, None
        
        df_RAM = pd.read_csv(file_path, usecols=lambda column:column in RAM_COLUMNS).dropna().reset_index(drop=True)
        output_label.configure(text="読み込み完了しました")
        
        return True, df_RAM
    
    @staticmethod
    def makeRAMTruthDataFrame(df_camera, df_RAM):
        # CANの結果にも値があるRAMだけを抽出する
        # CANの結果をタプルの集合にする
        CAN_set = set()
        for i in range(len(df_camera)): 
            lng = round(df_camera["camera_lng"][i], 2) # 集合での比較ができるように少数第２位で四捨五入
            lat = round(df_camera["camera_lat"][i], 2) # 集合での比較ができるように少数第２位で四捨五入
            CAN_set.add((lng, lat))
        
        print("CAN_set:{}".format(CAN_set))
        
        # RAMの結果をタプルのリストにする
        RAM_list = []
        for i in range(len(df_RAM)): 
            lng = round(df_RAM["Z1"][i], 2)
            lat = round(df_RAM["X1"][i], 2)
            RAM_list.append((lng, lat))
        
        print("RAM_list:{}".format(RAM_list))
        
        # CANの結果にあるRAMのインデックスを抽出
        index_list = []
        for i, value in enumerate(RAM_list):
            if value in CAN_set:
                index_list.append(i)
        
        # CANの結果にあるRAMだけを抽出
        df_RAM_extract = df_RAM.loc[index_list]
        
        # 抽出したやつをdf_cameraに結合
        
        
        return df_RAM_extract
                
        
        
    
            