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
        parent):
        """
        ウィジェットの配置を実施
        
        parameters
        ----------
            parent : ctk.CTk 
                作成したフレームの配置先
        """
        super().__init__(master=parent)
        
        # ---------------------------------------------------------- #
        # 行と列の設定(2行1列)
        # ---------------------------------------------------------- #
        self.grid_rowconfigure(index=0, weight=9)
        self.grid_rowconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=0, weight=1)
                        
        # ---------------------------------------------------------- #
        # メンバ変数
        # ---------------------------------------------------------- #
        self.df_data      = None
        self.df_data_name = None
        self.df_data      = None
        self.columns      = None     

        # ---------------------------------------------------------- #
        # グラフのパラメータ
        # ---------------------------------------------------------- #
        # 1度設定したフォントサイズ等を記憶しておく用
        self.title_params_init   = dict(TITLE_PARAMS)   # タイトル
        self.x_params_init       = dict(X_PARAMS)       # X軸
        self.y_params_init       = dict(Y_PARAMS)       # Y軸        
        self.plot_params_init    = dict(PLOT_PARAMS)    # 折れ線グラフ
        self.scatter_params_init = dict(SCATTER_PARAMS) # 散布図
        
        # 更新用
        self.title_params   = dict(TITLE_PARAMS)   # タイトル
        self.x_params       = dict(X_PARAMS)       # X軸
        self.y_params       = dict(Y_PARAMS)       # Y軸        
        self.plot_params    = dict(PLOT_PARAMS)    # 折れ線グラフ
        self.scatter_params = dict(SCATTER_PARAMS) # 散布図
                
        # ---------------------------------------------------------- #
        # Widgetの配置
        # ---------------------------------------------------------- #
        #self.fig = plt.figure() #左はtkinterだとエラーが出るから使わない！
        self.fig = Figure(figsize=(5, 5), dpi=100)

        # Matplotlibの図をTkinterに埋め込む
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=ctk.NSEW)
        
        self.axes = []
        self.graphs = [] # グラフのリスト

        # 新しいフレームを作成して、その中にNavigationToolbar2Tkを配置(←こうしないとエラーなる)
        self.toolbar_frame = ctk.CTkFrame(master=self)
        self.toolbar_frame.grid(row=1, column=0, sticky=ctk.NSEW)
        self.toolbar_frame.grid_propagate(False)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()
        
        # # マウスの動きを検出するイベントを設定
        # self.canvas.mpl_connect('motion_notify_event', self.mouseMove)

        # # クリックイベントを検出する
        # self.canvas.mpl_connect('button_press_event', self.click)
                
        
# ---------------------------------------------------------- #
# メソッド定義
# ---------------------------------------------------------- #
    def readDataFile(self, file_path, read_result_label, x_columns_frame, y_columns_frame, draw_result_label):
        """
        データファイルの読み込み
        
        parameters
        ----------
            file_path : ctk.CTkLabel 
                ファイルパス
            read_result_label : ctk.CTkLabel
                データの読み込みができたかを示すラベル
            x_columns_frame : ctk.CTkScrollableFrame
                x軸の選択候補
            y_columns_frame : ctk.CTkScrollableFrame
                y軸の選択候補
            draw_result_label : ctk.CTkLabel
                グラフの描画ができたかを示すラベル
        """
        # ファイルの読み込み確認
        try:
            with open(file_path, "r") as file: # 左の書き方なら自動でファイル閉じられる
                pass
        except: #ファイルが開かない時
            read_result_label.configure(text="ファイルを\n開けません")
            return 
        
        # スクロールバーと図の初期化
        x_columns_frame.reset()
        y_columns_frame.reset()
        
        self.fig.clf()
        self.canvas.draw()
        
        # DataFrameの作成
        skiprows = 7
        self.df_data = pd.read_csv(file_path, skiprows=skiprows)
        # 時間の追加
        self.df_data["Elapsed_Time"] = [x * 0.01 for x in range(len(self.df_data))]
        # 選択用のカラムの設定
        self.columns = self.df_data.columns
        
        # スクロールバーに反映
        # 横
        x_columns_frame.createWidget(columns=self.columns)
        
        # 縦
        y_columns_frame.createWidget(columns=self.columns)
        
        read_result_label.configure(text="読み込み完了")
        draw_result_label.configure(text="グラフの描画ボタンを押して下さい")

    def drawGraph(self, x_checkboxes, y_checkboxes, output_label):
        """
        グラフの描画
        
        parameters
        ----------
            x_checkbox : list of ctk.ctk.CTkCheckBox 
                x軸のチェックボックス
            y_checkbox : list of ctk.ctk.CTkCheckBox
                y軸のチェックボックス
            output_label : ctk.CTkLabel
                グラフを描画できるかどうかの結果を示すラベル
        """
        # カラムの取得
        # X軸
        x_columns = []
        for checkbox in x_checkboxes:
            if checkbox.get() == 1: # 選択中
                x_columns.append(checkbox.cget("text"))
        
        if len(x_columns) == 0:
            output_label.configure(text="X軸のデータを選択して下さい")
            return 
        elif len(x_columns) > 1:
            output_label.configure(text="X軸のデータは1つのみ選択して下さい")
            return   

        # Y軸
        y_columns = []
        for checkbox in y_checkboxes:
            if checkbox.get() == 1: # 選択中
                y_columns.append(checkbox.cget("text"))
        
        if len(y_columns) == 0:
            output_label.configure(text="Y軸のデータを選択して下さい")
            return 
        
        # 図の描画
        output_label.configure(text="グラフを描画しました")
        self.drawCanvas(x_columns, y_columns)
        
    def drawCanvas(self, x_columns, y_columns):
        """
        キャンバスの更新(グラフの描画)
        
        parameters
        ----------
            x_columns : list of string 
                x軸のカラム名
            y_columns : list of string
                y軸のカラム名
        """
        self.fig.clf()  # figureのクリア
        self.resetPlotParams(x_columns, y_columns) # グラフのパラメータの初期化
        
        # y軸の数だけsubplotを作成(x軸は共有)
        self.axes = self.fig.subplots(nrows=len(y_columns), ncols=1, sharex=True)

        # 1つのAxesしか返ってこなかった場合(y軸を1つだけ選択している)はリストに変換する(enumerateでエラーになるから)
        if not isinstance(self.axes, np.ndarray):
            self.axes = [self.axes]  
        
        for i, ax in enumerate(self.axes):
            if self.y_params["plot_type"][i] == "scatter":
                print("s:{}".format(self.scatter_params["s"]))
                self.graphs.append(ax.scatter(self.df_data[x_columns], 
                                              self.df_data[y_columns[i]], 
                                              s=self.scatter_params["s"][i],
                                              c=self.scatter_params["c"][i]
                                             ))
            else:
                self.graphs.append(ax.plot(self.df_data[x_columns], 
                                           self.df_data[y_columns[i]], 
                                           linewidth=self.plot_params["linewidth"][i],
                                           linestyle=self.plot_params["linestyle"][i],
                                           color=self.plot_params["color"][i],
                                           marker=self.plot_params["marker"][i]
                                          ))
                
            ax.set_ylabel(y_columns[i], fontsize=self.y_params["fontsize"]) # Y軸名を設定
            ax.tick_params(axis='y', labelsize=self.y_params["labelsize"])  # Y軸のメモリの数字の大きさを設定
            ax.tick_params(axis='both', direction='in')                     # メモリ線を内側に設定

        self.axes[0].set_title(self.title_params["title"], fontsize=self.title_params["fontsize"]) # タイトル
        self.axes[-1].set_xlabel(self.x_params["label"], fontsize=self.x_params["fontsize"])       # x軸名
        self.axes[-1].tick_params(axis='x', labelsize=self.x_params["labelsize"])                  # X軸のメモリの数字

        # 図の描画
        self.canvas.draw()
    
    def resetPlotParams(self, x_columns, y_columns):
        """
        グラフパラメータを初期化
        
        parameters
        ----------
            x_columns : list of string 
                x軸のカラム名
            y_columns : list of string
                y軸のカラム名
        """
        # 初期化
        self.title_params   = dict(self.title_params_init)   # タイトル
        self.x_params       = dict(self.x_params_init)       # X軸
        self.y_params       = dict(self.y_params_init)       # Y軸        
        self.plot_params    = dict(self.plot_params_init)    # 折れ線グラフ
        self.scatter_params = dict(self.scatter_params_init) # 散布図
        
        # x軸名
        self.x_params["label"] = x_columns[0]
        
        # Y軸名
        for column in y_columns:
            self.y_params["label"].append(column)
            
        # グラフの種類
        self.y_params["plot_type"] = self.y_params["plot_type"]*len(y_columns)
        
        # プロット
        for key, value in self.plot_params.items():
            self.plot_params[key] = value*len(y_columns)
        
        # 散布図
        for key, value in self.scatter_params.items():
            self.scatter_params[key] = value*len(y_columns)  
    
    def updateTitle(self, title, font_size):
        """
        タイトルの設定を更新
        
        parameters
        ----------
            title : string 
                グラフタイトル
            font_size : string
                タイトルのフォントサイズ
        """   
        # グラフの初期設定に反映
        self.title_params_init["fontsize"] = font_size
    
    def updateFontSize(self):
        """
        フォントサイズの更新
        
        parameters
        ----------
            title : string 
                グラフタイトル
            font_size : string
                タイトルのフォントサイズ
        """  
        pass
        
        





    def mouseMove(self, event):
        if event.inaxes == self.ax:
        # マウスの位置を取得
            x = event.xdata
            y = event.ydata
        
            # クロスヘアの位置を更新
            if x is not None and y is not None:
                self.h_line.set_ydata([y, y])  # クロスヘア1の水平線の更新
                self.v_line.set_xdata([x, x])  # クロスヘア1の垂直線の更新
            
                self.canvas.draw_idle()

    def click(self, event):
        if event.inaxes == self.ax:
            # クリックした点の座標を取得
            x = event.xdata
            y = event.ydata
            
            # if x is not None and y is not None:
            #     # 最も近い散布点を探索
            #     distances = np.sqrt((self.scatter_camera_lng.get_offsets()[:, 0] - x)**2 + (self.scatter_camera_lng.get_offsets()[:, 1] - y)**2)
            #     nearest_index = np.argmin(distances)
                
            #     # インデックスを保存
            #     self.camera_target_index = nearest_index
            #     dist = self.df_camera["camera_lng"][nearest_index]
            #     time = self.df_camera["Elapsed_Time"][nearest_index]
                
            #     diff_dist = round(dist - float(self.vbox_dist_label.cget("text")), 2)
            #     diff_time = time - float(self.vbox_time_label.cget("text"))
            #     # 値をラベルに表示
            #     self.camera_dist_label.configure(text=str(dist))
            #     self.camera_time_label.configure(text=str(time))
            #     self.diff_dist_label.configure(text=str(diff_dist))
            #     self.diff_time_label.configure(text=str(diff_time))
                
            #     # クリックした点を赤くする
            #     self.scatter_camera_lng.set_facecolors(np.where(np.arange(len(self.scatter_camera_lng.get_offsets())) == nearest_index, 'orange', 'red'))
            #     self.canvas_lng.draw_idle()