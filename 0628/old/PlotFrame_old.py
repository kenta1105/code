"""
グラフを描画するためのフレーム
グラフ関連の機能はここに詰め込む

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
from App import *
from MakeDataFrame import MakeDataFrame 

# ---------------------------------------------------------- #
# クラス定義
# ---------------------------------------------------------- #
class PlotFrame(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        camera_dist_label,
        camera_time_label,
        vbox_dist_label,
        vbox_time_label,
        diff_dist_label,
        diff_time_label):
        """
        ウィジェットの配置を実施
        
        parameters
        ----------
            parent : ctk.CTk 
                作成したフレームの配置先
        """
        super().__init__(master=parent)
        
        # 行と列の設定
        self.grid_rowconfigure(index=0, weight=8)
        self.grid_rowconfigure(index=1, weight=2)
        self.grid_columnconfigure(index=0, weight=1)
        
        # タブの設定
        self.graph_tabview = ctk.CTkTabview(master=self)
        self.graph_tabview.grid(row=0, column=0, sticky=ctk.NSEW)
        self.graph_tabview.grid_propagate(False) 
        
        self.graph_tabview.add("縦距離")
        self.graph_tabview.add("横距離")
        
        # 縦
        self.graph_tabview.tab("縦距離").grid_propagate(False)
        self.graph_tabview.tab("縦距離").grid_rowconfigure(index=0, weight=9)
        self.graph_tabview.tab("縦距離").grid_rowconfigure(index=1, weight=1)
        self.graph_tabview.tab("縦距離").grid_columnconfigure(index=0, weight=1)
        # 横
        self.graph_tabview.tab("横距離").grid_propagate(False)
        self.graph_tabview.tab("横距離").grid_rowconfigure(index=0, weight=9)
        self.graph_tabview.tab("横距離").grid_rowconfigure(index=1, weight=1)
        self.graph_tabview.tab("横距離").grid_columnconfigure(index=0, weight=1)
        
        # df
        self.df_all    = None
        self.df_camera = None
        self.df_vbox   = None
        
        self.df_RAM = None
        
        # カメラが認識できていない時の距離の値
        self.NG = 0
        # 描画用
        self.camera_shift = 0 # シフト押されたら変更する
        self.sensor_type = 1  # カメラを選択
        
        #　選択中のインデックス
        self.camera_target_index = -1
        self.vbox_target_index   = -1
        
        # 結果表示用
        self.camera_dist_label = camera_dist_label
        self.camera_time_label = camera_time_label
        self.vbox_dist_label = vbox_dist_label
        self.vbox_time_label = vbox_time_label
        self.diff_dist_label = diff_dist_label
        self.diff_time_label = diff_time_label
        
        # グラフの設定
        self.title = ""
        self.x_label = "Elapsed_Time[ms]"
        self.y_label = "Distance[m]"
        self.ylim = None

        #self.fig = plt.figure() #左はtkinterだとエラーが出るから使わない！
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.scatter_camera = None
        self.scatter_vbox   = None

        # Matplotlibの図をTkinterに埋め込む
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_tabview.tab("縦距離"))
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=ctk.NSEW)

        # 新しいフレームを作成して、その中にNavigationToolbar2Tkを配置(←こうしないとエラーなる)
        self.toolbar_frame = ctk.CTkFrame(master=self.graph_tabview.tab("縦距離"))
        self.toolbar_frame.grid(row=1, column=0, sticky=ctk.NSEW)
        self.toolbar_frame.grid_propagate(False)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()

        # クロスヘア用の縦線と横線を初期化
        self.h_line = self.ax.axhline(y=0, color='black', linestyle='--', linewidth=1)
        self.v_line = self.ax.axvline(x=0, color='black', linestyle='--', linewidth=1)
        
        # マウスの動きを検出するイベントを設定
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

        # クリックイベントを検出する
        self.canvas.mpl_connect('button_press_event', self.on_click)
        
        # 統計量表示用フレーム
        # 初期表示用フレーム
        self.statistics_frame_initial = ctk.CTkFrame(master=self)
        self.statistics_frame_initial.grid(row=1, column=0, sticky=ctk.NSEW)
        self.statistics_frame_initial.grid_propagate("False")
        
        
        # ---------------------------------------------------------- #
        # [自車,ダミー] = [静止, 静止]
        # ---------------------------------------------------------- #
        self.statistics_frame_ss = ctk.CTkFrame(master=self)
        self.statistics_frame_ss.grid(row=1, column=0, sticky=ctk.NSEW)
        self.statistics_frame_ss.grid_propagate("False")
        
        # 3行4列に設定
        self.statistics_frame_ss.grid_rowconfigure(index=0, weight=1)
        self.statistics_frame_ss.grid_rowconfigure(index=1, weight=1)
        self.statistics_frame_ss.grid_rowconfigure(index=2, weight=1)
        self.statistics_frame_ss.grid_columnconfigure(index=0, weight=1)
        self.statistics_frame_ss.grid_columnconfigure(index=1, weight=1)
        self.statistics_frame_ss.grid_columnconfigure(index=2, weight=1)
        self.statistics_frame_ss.grid_columnconfigure(index=3, weight=1)

        # 評価エリア
        self.area_label_ss = ctk.CTkLabel(
            self.statistics_frame_ss, 
            text="評価地点[cm]",
            **LABEL_PARAMS
        )
        self.area_label_ss.grid(row=0, column=0, columnspan=2, sticky=ctk.NSEW)
        
        # Z方向
        self.area_Z_label1_ss = ctk.CTkLabel(
            self.statistics_frame_ss, 
            text="Z方向",
            **LABEL_PARAMS
        )
        self.area_Z_label1_ss.grid(row=1, column=0, sticky=ctk.NSEW)
        
        self.area_Z_label2_ss = ctk.CTkLabel(
            self.statistics_frame_ss, 
            text="0",
            **LABEL_PARAMS
        )
        self.area_Z_label2_ss.grid(row=2, column=0, sticky=ctk.NSEW)

        # X方向
        self.area_X_label1_ss = ctk.CTkLabel(
            self.statistics_frame_ss, 
            text="X方向",
            **LABEL_PARAMS
        )
        self.area_X_label1_ss.grid(row=1, column=1, sticky=ctk.NSEW)

        self.area_X_label2_ss = ctk.CTkLabel(
            self.statistics_frame_ss, 
            text="0",
            **LABEL_PARAMS
        )
        self.area_X_label2_ss.grid(row=2, column=1, sticky=ctk.NSEW)

        # 認識精度
        self.accuracy_label_ss = ctk.CTkLabel(
            self.statistics_frame_ss, 
            text="認識精度(μ±σ)[cm]",
            **LABEL_PARAMS
        )
        self.accuracy_label_ss.grid(row=0, column=2, columnspan=2, sticky=ctk.NSEW)
        
        # 結果
        self.accuracy_label1_ss = ctk.CTkLabel(
            self.statistics_frame_ss, 
            text="結果",
            **LABEL_PARAMS
        )
        self.accuracy_label1_ss.grid(row=1, column=2, sticky=ctk.NSEW)
        
        self.accuracy_label2_ss = ctk.CTkLabel(
            self.statistics_frame_ss, 
            text="",
            **LABEL_PARAMS
        )
        self.accuracy_label2_ss.grid(row=2, column=2, sticky=ctk.NSEW)
        
        # 参考
        self.reference_label_ss = ctk.CTkLabel(
            self.statistics_frame_ss, 
            text="参考",
            **LABEL_PARAMS
        )
        self.reference_label_ss.grid(row=1, column=3, sticky=ctk.NSEW)

        self.reference_value_label1_ss = ctk.CTkLabel(
            self.statistics_frame_ss, 
            text="",
            **LABEL_PARAMS
        )
        self.reference_value_label1_ss.grid(row=2, column=3, sticky=ctk.NSEW)
        
        # ---------------------------------------------------------- #
        # [自車,ダミー] = [移動, 静止]
        # ---------------------------------------------------------- #
        self.statistics_frame_ms = ctk.CTkFrame(master=self)
        self.statistics_frame_ms.grid(row=1, column=0, sticky=ctk.NSEW)
        self.statistics_frame_ms.grid_propagate("False")
        
        # 5行4列に設定
        self.statistics_frame_ms.grid_rowconfigure(index=0, weight=1)
        self.statistics_frame_ms.grid_rowconfigure(index=1, weight=1)
        self.statistics_frame_ms.grid_rowconfigure(index=2, weight=1)
        self.statistics_frame_ms.grid_rowconfigure(index=3, weight=1)
        self.statistics_frame_ms.grid_rowconfigure(index=4, weight=1)
        self.statistics_frame_ms.grid_columnconfigure(index=0, weight=1)
        self.statistics_frame_ms.grid_columnconfigure(index=1, weight=1)
        self.statistics_frame_ms.grid_columnconfigure(index=2, weight=1)
        self.statistics_frame_ms.grid_columnconfigure(index=3, weight=1)

        # 評価エリア
        self.area_label_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="評価エリア[cm]",
            **LABEL_PARAMS
        )
        self.area_label_ms.grid(row=0, column=0, columnspan=2, sticky=ctk.NSEW)
        
        # Z方向
        self.area_Z_label1_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="Z方向",
            **LABEL_PARAMS
        )
        self.area_Z_label1_ms.grid(row=1, column=0, sticky=ctk.NSEW)
        
        self.area_Z_label2_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="300≦L≦600",
            **LABEL_PARAMS
        )
        self.area_Z_label2_ms.grid(row=2, column=0, sticky=ctk.NSEW)

        self.area_Z_label3_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="200≦L<300",
            **LABEL_PARAMS
        )
        self.area_Z_label3_ms.grid(row=3, column=0, sticky=ctk.NSEW)

        self.area_Z_label4_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="50(※)≦L<200",
            **LABEL_PARAMS
        )
        self.area_Z_label4_ms.grid(row=4, column=0, sticky=ctk.NSEW)

        # X方向
        self.area_X_label1_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="X方向",
            **LABEL_PARAMS
        )
        self.area_X_label1_ms.grid(row=1, column=1, sticky=ctk.NSEW)

        self.area_X_label2_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="-150≦W≦150",
            **LABEL_PARAMS
        )
        self.area_X_label2_ms.grid(row=2, column=1, sticky=ctk.NSEW)

        self.area_X_label3_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="同上",
            **LABEL_PARAMS
        )
        self.area_X_label3_ms.grid(row=3, column=1, sticky=ctk.NSEW)

        self.area_X_label4_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="同上",
            **LABEL_PARAMS
        )
        self.area_X_label4_ms.grid(row=4, column=1, sticky=ctk.NSEW)

        # 注意書き
        self.area_note_label_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="※大人ダミーの下限は75cm",
            **LABEL_PARAMS
        )
        self.area_note_label_ms.grid(row=5, column=0, columnspan=2, sticky=ctk.NSEW)

        # 認識精度
        self.accuracy_label_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="認識精度(μ±σ)[cm]",
            **LABEL_PARAMS
        )
        self.accuracy_label_ms.grid(row=0, column=2, columnspan=2, sticky=ctk.NSEW)
        
        # 結果
        self.accuracy_label1_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="結果",
            **LABEL_PARAMS
        )
        self.accuracy_label1_ms.grid(row=1, column=2, sticky=ctk.NSEW)
        
        self.accuracy_value_label1_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="",
            **LABEL_PARAMS
        )
        self.accuracy_value_label1_ms.grid(row=2, column=2, sticky=ctk.NSEW)

        self.accuracy_value_label2_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="",
            **LABEL_PARAMS
        )
        self.accuracy_value_label2_ms.grid(row=3, column=2, sticky=ctk.NSEW)
        
        self.accuracy_value_label3_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="",
            **LABEL_PARAMS
        )
        self.accuracy_value_label3_ms.grid(row=4, column=2, sticky=ctk.NSEW)
        
        # 参考
        self.reference_label_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="参考",
            **LABEL_PARAMS
        )
        self.reference_label_ms.grid(row=1, column=3, sticky=ctk.NSEW)

        self.reference_value_label1_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="",
            **LABEL_PARAMS
        )
        self.reference_value_label1_ms.grid(row=2, column=3, sticky=ctk.NSEW)

        self.reference_value_label2_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="",
            **LABEL_PARAMS
        )
        self.reference_value_label2_ms.grid(row=3, column=3, sticky=ctk.NSEW)

        self.reference_value_label3_ms = ctk.CTkLabel(
            self.statistics_frame_ms, 
            text="",
            **LABEL_PARAMS
        )
        self.reference_value_label3_ms.grid(row=4, column=3, sticky=ctk.NSEW)        
        # ---------------------------------------------------------- #
        # [自車,ダミー] = [静止, 移動]
        # ---------------------------------------------------------- #
        self.statistics_frame_sm = ctk.CTkFrame(master=self)
        self.statistics_frame_sm.grid(row=1, column=0, sticky=ctk.NSEW)
        self.statistics_frame_sm.grid_propagate("False")
        # 5行4列に設定
        self.statistics_frame_sm.grid_rowconfigure(index=0, weight=1)
        self.statistics_frame_sm.grid_rowconfigure(index=1, weight=1)
        self.statistics_frame_sm.grid_rowconfigure(index=2, weight=1)
        self.statistics_frame_sm.grid_rowconfigure(index=3, weight=1)
        self.statistics_frame_sm.grid_rowconfigure(index=4, weight=1)
        self.statistics_frame_sm.grid_rowconfigure(index=5, weight=1)
        self.statistics_frame_sm.grid_columnconfigure(index=0, weight=1)
        self.statistics_frame_sm.grid_columnconfigure(index=1, weight=1)
        self.statistics_frame_sm.grid_columnconfigure(index=2, weight=1)
        self.statistics_frame_sm.grid_columnconfigure(index=3, weight=1)
        self.statistics_frame_sm.grid_columnconfigure(index=4, weight=1)

        # 評価エリア
        self.area_label_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="評価エリア[cm]",
            **LABEL_PARAMS
        )
        self.area_label_sm.grid(row=0, column=0, columnspan=2, sticky=ctk.NSEW)
        
        # Z方向
        self.area_Z_label1_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="Z方向",
            **LABEL_PARAMS
        )
        self.area_Z_label1_sm.grid(row=1, column=0, sticky=ctk.NSEW)
        
        self.area_Z_label2_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="300≦L≦600",
            **LABEL_PARAMS
        )
        self.area_Z_label2_sm.grid(row=2, column=0, sticky=ctk.NSEW)

        self.area_Z_label3_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="200≦L<300",
            **LABEL_PARAMS
        )
        self.area_Z_label3_sm.grid(row=3, column=0, sticky=ctk.NSEW)

        self.area_Z_label4_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="50(※)≦L<200",
            **LABEL_PARAMS
        )
        self.area_Z_label4_sm.grid(row=4, column=0, sticky=ctk.NSEW)

        # X方向
        self.area_X_label1_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="X方向",
            **LABEL_PARAMS
        )
        self.area_X_label1_sm.grid(row=1, column=1, sticky=ctk.NSEW)

        self.area_X_label2_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="-150≦W≦150",
            **LABEL_PARAMS
        )
        self.area_X_label2_sm.grid(row=2, column=1, sticky=ctk.NSEW)

        self.area_X_label3_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="同上",
            **LABEL_PARAMS
        )
        self.area_X_label3_sm.grid(row=3, column=1, sticky=ctk.NSEW)

        self.area_X_label4_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="同上",
            **LABEL_PARAMS
        )
        self.area_X_label4_sm.grid(row=4, column=1, sticky=ctk.NSEW)

        # 注意書き
        self.area_note_label_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="※大人ダミーの下限は75cm",
            **LABEL_PARAMS
        )
        self.area_note_label_sm.grid(row=5, column=0, columnspan=2, sticky=ctk.NSEW)

        # 認識精度
        self.accuracy_label_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="認識精度(μ±σ)[cm]",
            **LABEL_PARAMS
        )
        self.accuracy_label_sm.grid(row=0, column=2, columnspan=2, sticky=ctk.NSEW)
        
        # 結果
        self.accuracy_label2_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="結果",
            **LABEL_PARAMS
        )
        self.accuracy_label2_sm.grid(row=1, column=2, sticky=ctk.NSEW)
        
        self.accuracy_value_label1_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="",
            **LABEL_PARAMS
        )
        self.accuracy_value_label1_sm.grid(row=2, column=2, sticky=ctk.NSEW)

        self.accuracy_value_label2_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="",
            **LABEL_PARAMS
        )
        self.accuracy_value_label2_sm.grid(row=3, column=2, sticky=ctk.NSEW)
        
        self.accuracy_value_label3_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="",
            **LABEL_PARAMS
        )
        self.accuracy_value_label3_sm.grid(row=4, column=2, sticky=ctk.NSEW)
        
        # 参考(横切り)
        self.reference_side_label_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="参考(横切り)",
            **LABEL_PARAMS
        )
        self.reference_side_label_sm.grid(row=1, column=3, sticky=ctk.NSEW)

        self.reference_side_value_label1_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="",
            **LABEL_PARAMS
        )
        self.reference_side_value_label1_sm.grid(row=2, column=3, sticky=ctk.NSEW)

        self.reference_side_value_label2_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="",
            **LABEL_PARAMS
        )
        self.reference_side_value_label2_sm.grid(row=3, column=3, sticky=ctk.NSEW)

        self.reference_side_value_label3_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="",
            **LABEL_PARAMS
        )
        self.reference_side_value_label3_sm.grid(row=4, column=3, sticky=ctk.NSEW)

        # 参考(縦)
        self.reference_back_label_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="参考(後方)",
            **LABEL_PARAMS
        )
        self.reference_back_label_sm.grid(row=1, column=4, sticky=ctk.NSEW)

        self.reference_back_value_label1_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="",
            **LABEL_PARAMS
        )
        self.reference_back_value_label1_sm.grid(row=2, column=4, sticky=ctk.NSEW)

        self.reference_back_value_label2_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="",
            **LABEL_PARAMS
        )
        self.reference_back_value_label2_sm.grid(row=3, column=4, sticky=ctk.NSEW)

        self.reference_back_value_label3_sm = ctk.CTkLabel(
            self.statistics_frame_sm, 
            text="",
            **LABEL_PARAMS
        )
        self.reference_back_value_label3_sm.grid(row=4, column=4, sticky=ctk.NSEW)
        
        # ---------------------------------------------------------- #
        # [自車,ダミー] = [移動, 移動]
        # ---------------------------------------------------------- #
        self.statistics_frame_mm = ctk.CTkFrame(master=self)
        self.statistics_frame_mm.grid(row=1, column=0, sticky=ctk.NSEW)
        self.statistics_frame_mm.grid_propagate("False")
        # 3行4列に設定
        self.statistics_frame_mm.grid_rowconfigure(index=0, weight=1)
        self.statistics_frame_mm.grid_rowconfigure(index=1, weight=1)
        self.statistics_frame_mm.grid_rowconfigure(index=2, weight=1)
        self.statistics_frame_mm.grid_rowconfigure(index=3, weight=1)
        self.statistics_frame_mm.grid_columnconfigure(index=0, weight=1)
        self.statistics_frame_mm.grid_columnconfigure(index=1, weight=1)
        self.statistics_frame_mm.grid_columnconfigure(index=2, weight=1)
        self.statistics_frame_mm.grid_columnconfigure(index=3, weight=1)
        # ラベルの設定
        # 評価エリア
        self.area_label_mm = ctk.CTkLabel(
            self.statistics_frame_mm, 
            text="評価エリア[cm]",
            **LABEL_PARAMS
        )
        self.area_label_mm.grid(row=0, column=0, columnspan=2, sticky=ctk.NSEW)
        
        self.area_Z_label1_mm = ctk.CTkLabel(
            self.statistics_frame_mm, 
            text="Z方向",
            **LABEL_PARAMS
        )
        self.area_Z_label1_mm.grid(row=1, column=0, sticky=ctk.NSEW)

        self.area_X_label1_mm = ctk.CTkLabel(
            self.statistics_frame_mm, 
            text="X方向",
            **LABEL_PARAMS
        )
        self.area_X_label1_mm.grid(row=1, column=1, sticky=ctk.NSEW)

        self.area_Z_label2_mm = ctk.CTkLabel(
            self.statistics_frame_mm, 
            text="50(※)≦L≦600",
            **LABEL_PARAMS
        )
        self.area_Z_label2_mm.grid(row=2, column=0, sticky=ctk.NSEW)

        self.area_X_label2_mm = ctk.CTkLabel(
            self.statistics_frame_mm, 
            text="-150≦W≦150",
            **LABEL_PARAMS
        )
        self.area_X_label2_mm.grid(row=2, column=1, sticky=ctk.NSEW)

        self.area_note_label_mm = ctk.CTkLabel(
            self.statistics_frame_mm, 
            text="※大人ダミーの下限は75cm",
            **LABEL_PARAMS
        )
        self.area_note_label_mm.grid(row=3, column=2, columnspan=2, sticky=ctk.NSEW)


        # 認識精度
        self.accuracy_label_mm = ctk.CTkLabel(
            self.statistics_frame_mm, 
            text="認識精度(μ±σ)[cm]",
            **LABEL_PARAMS
        )
        self.accuracy_label_mm.grid(row=0, column=2, columnspan=2, sticky=ctk.NSEW)
        
        # 結果
        self.accuracy_label2_mm = ctk.CTkLabel(
            self.statistics_frame_mm, 
            text="結果",
            **LABEL_PARAMS
        )
        self.accuracy_label2_mm.grid(row=1, column=2, sticky=ctk.NSEW)
        
        self.accuracy_value_label1_mm = ctk.CTkLabel(
            self.statistics_frame_mm, 
            text="",
            **LABEL_PARAMS
        )
        self.accuracy_value_label1_mm.grid(row=2, column=2, sticky=ctk.NSEW)

        self.reference_label_mm = ctk.CTkLabel(
            self.statistics_frame_mm, 
            text="参考",
            **LABEL_PARAMS
        )
        self.reference_label_mm.grid(row=1, column=3, sticky=ctk.NSEW)

        self.reference_value_label_mm = ctk.CTkLabel(
            self.statistics_frame_mm, 
            text="",
            **LABEL_PARAMS
        )
        self.reference_value_label_mm.grid(row=2, column=3, sticky=ctk.NSEW)
        
        self.statistics_frame_ss.tkraise()
        
        
        
# ---------------------------------------------------------- #
# メソッド定義
# ---------------------------------------------------------- #
    def on_mouse_move(self, event):
        if event.inaxes == self.ax:
            # マウスの位置を取得
            x = event.xdata
            y = event.ydata
            
            # クロスヘアの位置を更新
            if x is not None and y is not None:
                self.h_line.set_ydata([y, y])  # クロスヘア1の水平線の更新
                self.v_line.set_xdata([x, x])  # クロスヘア1の垂直線の更新
                
                self.canvas.draw_idle()
    
    def on_click(self, event):
        if event.inaxes == self.ax:
            # クリックした点の座標を取得
            x = event.xdata
            y = event.ydata
            
            if x is not None and y is not None:
                if self.sensor_type == 1: # カメラ
                    # 最も近い散布点を探索
                    distances = np.sqrt((self.scatter_camera.get_offsets()[:, 0] - x)**2 + (self.scatter_camera.get_offsets()[:, 1] - y)**2)
                    nearest_index = np.argmin(distances)
                    
                    # インデックスを保存
                    self.camera_target_index = nearest_index
                    dist = self.df_camera["dist_camera"][nearest_index]
                    time = self.df_camera["Elapsed_Time"][nearest_index]
                    
                    diff_dist = round(dist - float(self.vbox_dist_label.cget("text")), 2)
                    diff_time = time - float(self.vbox_time_label.cget("text"))
                    # 値をラベルに表示
                    self.camera_dist_label.configure(text=str(dist))
                    self.camera_time_label.configure(text=str(time))
                    self.diff_dist_label.configure(text=str(diff_dist))
                    self.diff_time_label.configure(text=str(diff_time))
                    
                    # クリックした点を赤くする
                    self.scatter_camera.set_facecolors(np.where(np.arange(len(self.scatter_camera.get_offsets())) == nearest_index, 'orange', 'red'))
                    self.canvas.draw_idle()
                    
                    # クリックした座標の動画フレームを見つける
                    
                    # クリックした座標の動画フレームを見つける
                    
                    # クリックした座標の動画フレームを見つける

                else: # Vbox
                    # 最も近い散布点を探索
                    distances = np.sqrt((self.scatter_vbox.get_offsets()[:, 0] - x)**2 + (self.scatter_vbox.get_offsets()[:, 1] - y)**2)
                    nearest_index = np.argmin(distances)

                    # インデックスを保存
                    self.vbox_target_index = nearest_index
                    dist = round(self.df_vbox["smoothing"][nearest_index], 2)
                    time = self.df_vbox["Elapsed_Time"][nearest_index]
                    
                    diff_dist = round(float(self.camera_dist_label.cget("text")) - dist, 2)
                    diff_time = float(self.camera_time_label.cget("text")) - time
                    
                    # 値を表示
                    self.vbox_dist_label.configure(text=str(dist))
                    self.vbox_time_label.configure(text=str(time))
                    self.diff_dist_label.configure(text=str(diff_dist))
                    self.diff_time_label.configure(text=str(diff_time))
                    
                    # クリックした点を赤くする
                    self.scatter_vbox.set_facecolors(np.where(np.arange(len(self.scatter_vbox.get_offsets())) == nearest_index, 'orange', 'blue'))
                    self.canvas.draw_idle()
                
    # グラフを描画しなおす関数(シフトとか無し！)
    def drawGraph(self, file_path, distance_direction, dummy_action, initial_head, is_use_head, initial_shift, output_label, smoothing_slider, shift_slider, smoothing_value_label,
                  shift_value_label, car_action, dummy_type, dummy_pos_LNG, dummy_pos_LAT):
        # スライダーの値と表示のリセット
        # スムージング
        smoothing_slider.set(0)
        smoothing_value_label.configure(text="0")
        
        # 時間シフト(初期値に合わせる)
        shift_slider.set(initial_shift) 
        shift_value_label.configure(text=str(initial_shift))
        
        # クリックした点のインデックスのクリア
        self.camera_target_index = -1
        self.vbox_target_index   = -1
        
        # クリックした点情報の表示
        self.camera_dist_label.configure(text="0")
        self.camera_time_label.configure(text="0")
        self.vbox_dist_label.configure(text="0")
        self.vbox_time_label.configure(text="0")
        self.diff_dist_label.configure(text="0")
        self.diff_time_label.configure(text="0")
        
        # 描画に使用するカラム名とタイトル等の設定
        all_columns    = []
        camera_columns = []
        vbox_columns   = []
        camera_invalid_value = 0
        # 距離の方向、ダミーの動きによって使うカラム名とタイトル等を変更する
        if distance_direction == 1: # 縦
            # カラム名
            camera_columns = CAMERA_LNG_COLUMNS
            if dummy_action == 1: # 静止
                vbox_columns = VBOX_LNG_COLUMNS_STATIONARY
                all_columns  = ALL_COLUMNS_STATIONARY
            else:
                vbox_columns = VBOX_LNG_COLUMNS_MOVE
                all_columns  = ALL_COLUMNS_MOVE
            
            # グラフの設定
            self.title = "Camera vs Vbox(LNG)" 
            self.ylim = [-5, LNG_NG]
            
            # カメラのCAN初期値の値
            camera_invalid_value = LNG_NG
        else: # 横
            # カラム名
            camera_columns = CAMERA_LAT_COLUMNS
            if dummy_action == 1: # 静止
                vbox_columns = VBOX_LAT_COLUMNS_STATIONARY
                all_columns  = ALL_COLUMNS_STATIONARY
            else:
                vbox_columns = VBOX_LAT_COLUMNS_MOVE
                all_columns  = ALL_COLUMNS_MOVE

            # グラフの設定
            self.title = "Camera vs Vbox(LAT)" 
            self.ylim = [-1*LAT_NG, LAT_NG]
            
            # カメラのCAN初期値の値
            camera_invalid_value = LAT_NG
        
        # データフレームの作成
        (is_successful, self.df_all, self.df_camera, self.df_vbox) = MakeDataFrame.makeCANDataFrame(
                                                                file_path            = file_path,
                                                                all_columns          = all_columns, 
                                                                camera_columns       = camera_columns,
                                                                vbox_columns         = vbox_columns,
                                                                camera_invalid_value = camera_invalid_value,
                                                                initial_head         = initial_head,
                                                                is_use_head          = is_use_head,
                                                                output_label         = output_label
                                                            ) 
        
        if is_successful:
            self.df_all.to_csv("all.csv")
            self.df_camera.to_csv("camera.csv")
            self.df_vbox.to_csv("vbox.csv")
            
            # 描画
            self.camera_shift = initial_shift
            self.drawCanvas()
        
            # 統計量の算出
            statics_list = MakeDataFrame.compute_statics(self.df_all, self.df_camera, self.df_vbox, self.camera_shift, dummy_type)
            # 自車とダミーの動きによって見せるフレームを変更
            if car_action == 1 and dummy_action == 1:   # 自車静止、ダミー静止
                self.statistics_frame_ss.tkraise()
                # 評価地点
                self.area_Z_label2_ss.configure(text=dummy_pos_LNG)
                self.area_X_label2_ss.configure(text=dummy_pos_LAT)
                
                # 認識結果
                self.accuracy_label2_ss.configure(text=statics_list[0])
                
                # 参考値
                key = (dummy_pos_LNG, dummy_pos_LAT)
                if distance_direction == 1: # 縦
                    if key in REFERENCE_SS:
                        value = REFERENCE_SS[key][0]
                        self.reference_value_label1_ss.configure(text=value)
                    else:
                        self.reference_value_label1_ss.configure(text="-")
                else: # 横
                    if key in REFERENCE_SS:
                        value = REFERENCE_SS[key][1]
                        self.reference_value_label1_ss.configure(text=value)
                    else:
                        self.reference_value_label1_ss.configure(text="-")
                
            elif car_action == 2 and dummy_action == 1: # 自車移動, ダミー静止
                self.statistics_frame_ms.tkraise()
                
                # 認識結果
                self.accuracy_value_label1_ms.configure(text=statics_list[1])
                self.accuracy_value_label2_ms.configure(text=statics_list[2])
                self.accuracy_value_label3_ms.configure(text=statics_list[3])
                
                # 参考値
                if distance_direction == 1: # 縦
                    self.reference_value_label1_ms.configure(text=REFERENCE_MS_LNG[0])
                    self.reference_value_label2_ms.configure(text=REFERENCE_MS_LNG[1])
                    self.reference_value_label3_ms.configure(text=REFERENCE_MS_LNG[2])
                else: # 横
                    self.reference_value_label1_ms.configure(text=REFERENCE_MS_LAT[0])
                    self.reference_value_label2_ms.configure(text=REFERENCE_MS_LAT[1])
                    self.reference_value_label3_ms.configure(text=REFERENCE_MS_LAT[2])

                
            elif car_action == 1 and dummy_action == 2: # 自車静止, ダミー移動
                self.statistics_frame_sm.tkraise()

                # 認識結果
                self.accuracy_value_label1_sm.configure(text=statics_list[1])
                self.accuracy_value_label2_sm.configure(text=statics_list[2])
                self.accuracy_value_label3_sm.configure(text=statics_list[3])
                
                # 参考値(横)
                if distance_direction == 1: # 縦
                    self.reference_side_value_label1_sm.configure(text=REFERENCE_SM_SIDE_LNG[0])
                    self.reference_side_value_label2_sm.configure(text=REFERENCE_SM_SIDE_LNG[1])
                    self.reference_side_value_label3_sm.configure(text=REFERENCE_SM_SIDE_LNG[2])
                else: # 横
                    self.reference_side_value_label1_sm.configure(text=REFERENCE_SM_SIDE_LAT[0])
                    self.reference_side_value_label2_sm.configure(text=REFERENCE_SM_SIDE_LAT[1])
                    self.reference_side_value_label3_sm.configure(text=REFERENCE_SM_SIDE_LAT[2])

                # 参考値(後ろ)
                if distance_direction == 1: # 縦
                    self.reference_back_value_label1_sm.configure(text=REFERENCE_SM_BACK_LNG[0])
                    self.reference_back_value_label2_sm.configure(text=REFERENCE_SM_BACK_LNG[1])
                    self.reference_back_value_label3_sm.configure(text=REFERENCE_SM_BACK_LNG[2])
                else: # 横
                    self.reference_back_value_label1_sm.configure(text=REFERENCE_SM_BACK_LAT[0])
                    self.reference_back_value_label2_sm.configure(text=REFERENCE_SM_BACK_LAT[1])
                    self.reference_back_value_label3_sm.configure(text=REFERENCE_SM_BACK_LAT[2])
                
            else:                                       # 自車移動, ダミー移動
                self.statistics_frame_mm.tkraise()
                # 認識結果
                self.accuracy_value_label1_mm.configure(text=statics_list[4])
                # 参考値
                if distance_direction == 1: # 縦
                    self.reference_value_label_mm.configure(text=REFERENCE_MM_LNG[0])
                else: # 横
                    self.reference_value_label_mm.configure(text=REFERENCE_MM_LAT[0])
        

    # Canvasの更新
    def drawCanvas(self):
        #描画
        self.ax.clear()
        colors = np.where(self.df_camera["dist_camera"] != self.NG, 'red', 'gray')
        #labels = np.where(self.df_camera["dist_camera"] != NG, '後方カメラ', '後方カメラ(不認識)')
        
        self.scatter_vbox = self.ax.scatter(self.df_vbox["Elapsed_Time"], self.df_vbox["smoothing"]*-1, s=5, c="blue", label="Vbox") # vbox(後方カメラと正負逆)
        
        self.scatter_camera = self.ax.scatter(self.df_camera["Elapsed_Time"]+self.camera_shift , self.df_camera["dist_camera"], s=5, c=colors, label="Camera")  # 後方カメラ
        
        self.ax.set_title(self.title)        
        self.ax.set_ylabel(self.y_label)
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylim(self.ylim)
        self.ax.legend()
        
        # クロスヘアの再登録
        self.h_line = self.ax.axhline(y=0, color='black', linestyle='--', linewidth=1)
        self.v_line = self.ax.axvline(x=0, color='black', linestyle='--', linewidth=1)
    
        #図をframeに配置
        self.canvas.draw()
    
    # 遅延とかスムージングに対応
    def updateGraph(self, widget_type, slider_var, slider_value_label, update_type, value_min, value_max):
        if self.df_all is None or self.df_all.empty:
            return
        
        value = slider_var.get()
        # どのウィジェットから呼ばれたかで値の更新方法を変更
        if widget_type == WidgetType.MINUS_BUTTON: # マイナスボタン
            value -= 1
            if value < value_min:
                value = value_min
        elif  widget_type == WidgetType.PLUS_BUTTON: # プラスボタン
            value += 1
            if value > value_max:
                value = value_max      
        else: # スライダー
            pass #処理無
        
        # スライダーの値の表示内容を変更
        slider_value_label.configure(text=str(value))
        slider_var.set(value)
        
        # スムージングかシフトで内容変更
        if update_type == GraphUpdateType.SMOOTHING:
            self.df_vbox["smoothing"] = MakeDataFrame.RunMovingAverages(self.df_vbox, "dist_vbox", value//10)
        else:
            self.camera_shift = value
            # 値をラベルに表示
            if self.camera_target_index >= 0:
                time = self.df_camera["Elapsed_Time"][self.camera_target_index] + value
                diff_time = time - float(self.vbox_time_label.cget("text"))
                self.camera_time_label.configure(text=str(time))
                self.diff_time_label.configure(text=str(diff_time))
        
        # 描画
        # カメラのシフトを0にする
        self.drawCanvas()

    # 遅延とかスムージングに対応
    def updateGraphBySlider(self, slider_var, slider_value_label, update_type):
        if self.df_all is None or self.df_all.empty:
            return
        
        value = slider_var.get()
        # スライダーの値の表示内容を変更
        slider_value_label.configure(text=str(value))
        
        # スムージングかシフトで内容変更
        if update_type == GraphUpdateType.SMOOTHING:
            self.df_vbox["smoothing"] = MakeDataFrame.RunMovingAverages(self.df_vbox, "dist_vbox", value//10)
        else:
            self.camera_shift = value
            # 値をラベルに表示
            if self.camera_target_index >= 0:
                time = self.df_camera["Elapsed_Time"][self.camera_target_index] + value
                diff_time = time - float(self.vbox_time_label.cget("text"))
                self.camera_time_label.configure(text=str(time))
                self.diff_time_label.configure(text=str(diff_time))
        
        # 描画
        # カメラのシフトを0にする
        self.drawCanvas()
        
    def setSensorType(self, sensor_type):
        self.sensor_type = sensor_type
    
    def makeRAMDataFrame(self, file_path, output_label):
        (is_successful, self.df_RAM) = MakeDataFrame.makeRAMDataFrame(file_path, output_label)
        if is_successful:
            self.df_RAM.to_csv("RAM.csv")
    
    def jumpToVideoFrameTime(self, video_frame_entry, distance_direction, output_label):
        # データの確認
        if self.df_camera is None or self.df_camera.empty:
            output_label.configure(text="CANのログファイルを読み込んで下さい")
            return 
        elif self.df_RAM is None or self.df_RAM.empty:
            output_label.configure(text="RAMのログファイルを読み込んで下さい")
            return
        elif video_frame_entry.get() == "":
            output_label.configure(text="動画フレームを入力して下さい")
            return
        
        # 動画フレームの時のカメラの認識位置を見つける
        (distance_list, target_index) = self.getDistanceAtVideoFrameTime(int(video_frame_entry.get()), distance_direction)
        if distance_list == []:
            output_label.configure(text="動画フレームを見つけることができません")
            return 
        
        # 合致するcameraのインデックスを見つける
        (is_found, index_camera) = self.findMatchingIndex(distance_list, target_index, list(self.df_camera["dist_camera"]))
        if is_found == False:
            output_label.configure(text="動画フレームと一致する時刻が見つかりません")
            return 
        else:
            output_label.configure(text="動画フレームと一致する時刻を見つけました")

        print("index:{}".format(index_camera))
        
        # 見つけたインデックスの時の時刻、距離を表示
        camera_dist = round(self.df_camera["dist_camera"][index_camera], 2)
        camera_time = round(self.df_camera["Elapsed_Time"][index_camera], 2)
        
        self.camera_dist_label.configure(text=str(camera_dist))
        self.camera_time_label.configure(text=str(camera_time))       
        
        diff_dist = round(camera_dist - -1*float(self.vbox_time_label.cget("text")), 2)
        diff_time = camera_time - float(self.vbox_time_label.cget("text"))
        self.diff_dist_label.configure(text=str(diff_dist))
        self.diff_time_label.configure(text=str(diff_time))
        
        # canvasに描画
        # クリックした点を赤くする
        self.scatter_camera.set_facecolors(np.where(np.arange(len(self.scatter_camera.get_offsets())) == index_camera, 'black', 'red'))
        self.canvas.draw_idle()
        
    def getDistanceAtVideoFrameTime(self, video_frame, distance_direction):
        # 動画フレームの時のRAMcsvのインデックスを見つける
        frame_index_list = self.df_RAM.index[self.df_RAM["FrameCnt"] == video_frame].tolist()
        frame_index = 0
        if frame_index_list == []:
            return frame_index_list, None
        else:
            frame_index = frame_index_list[0]
            print("frame_index:{}".format(frame_index))
        
        # 見つけたインデックスから前後2この合計5個の値のリストを作成
        # 前2つと後ろ2つを取りたいので範囲を計算
        distance_list = []
        if distance_direction == 1: #縦
            distance_list = list(self.df_RAM["Z1"])
        else:
            distance_list = list(self.df_RAM["X1"])
        
        start = max(frame_index - 2, 0)
        end   = min(frame_index + 3, len(self.df_RAM))
        
        print("start:{}, end:{}".format(start, end))
        
        # 範囲内のリストを取得
        surrounding_elements = distance_list[start:end]
        target_index = 2 # 範囲内のリスト中の動画フレームの時の距離の値を示すインデックス
        
        print("Before list:{}, index:{}".format(surrounding_elements, target_index))   
        
        
        # 要素数が5に満たない場合は、前後から補完
        while len(surrounding_elements) < 5:
            if start > 0:
                start -= 1 # 目的の値のインデックスが2から+1ずれる
                surrounding_elements.insert(0, distance_list[start])
                target_index += 1
            elif end < len(self.df_RAM):
                surrounding_elements.append(distance_list[end])
                end += 1
                target_index -= 1 # 目的の値のインデックスが2から-1ずれる
            else:
                break
        print("After list:{}, index:{}".format(surrounding_elements, target_index))    
        
        return surrounding_elements, target_index
    
    def findMatchingIndex(self, distance_list, target_index, camera_list):
        start_value = distance_list[0]
        print("distancelist:{}, target_index:{}, camera_list:{}, start_value:{}".format(distance_list, target_index, camera_list, start_value))
        for i, value in enumerate(camera_list):
            if abs(value - start_value) < EPSILON: # 浮動小数点なので許容誤差で考える
                # 5こ連続で一致してるか見る
                cnt = 1
                while cnt <= 4 and i+cnt < len(camera_list):
                    if abs(distance_list[cnt] - camera_list[i+cnt]) < EPSILON: # 浮動小数点なので許容誤差で考える
                        cnt += 1
                    else:
                        break
                
                # 5こ連続で一致してたかの判定
                if cnt == 5:
                    return True, i+target_index # 5このリスト中のフレームのインデックスを返す
        
        return False, 0
    
    # 統計量を示す
    
    
    
    
        
        
                
        
    

        
        
        
                    
        