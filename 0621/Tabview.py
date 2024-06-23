"""
評価用⇔解析用の切り替えタブを作成し、
タブの中身も設定するクラス

Author: Kenta Matsumura
"""

# ---------------------------------------------------------- #
# サードパーティライブラリのインポート
# ---------------------------------------------------------- #
import customtkinter as ctk

# ---------------------------------------------------------- #
# 自作ライブラリのインポート
# ---------------------------------------------------------- #
from common import *
from GraphSetupFrame import GraphSetupFrame
from DelayDiffenceVisualizationFrame import DelayDiffenceVisualizationFrame
from PageCheckAVI import PageCheckAVI

# ---------------------------------------------------------- #
# クラス定義
# ---------------------------------------------------------- #
class Tabview(ctk.CTkTabview):
    def __init__(self, parent):
        """
        グラフ設定⇔グラフ描画の切り替えタブを作成し、
        タブの中身も設定するクラス
        
        parameters
        ----------
            parent : ctk.CTkFrame 
                作成したタブの格納先のフレーム
        """
        super().__init__(master=parent)
        
        # ---------------------------------------------------------- #
        # タブで共通の変数
        # ---------------------------------------------------------- #
        self.CAN_file_path   = "" 
        self.RAM_file_path   = ""
        self.video_file_path = ""
        self.camera_columns  = []
        self.vbox_columns    = []

        # タブの作成
        self.add("グラフの確認")
        self.add("動画の確認")

        # ---------------------------------------------------------- #
        # グラフの確認
        # ---------------------------------------------------------- #
        self.tab("グラフの確認").grid_propagate(False)
        self.tab("グラフの確認").grid_rowconfigure(index=0, weight=1)
        self.tab("グラフの確認").grid_columnconfigure(index=0, weight=1)

        self.delay_difference_visualization_frame = DelayDiffenceVisualizationFrame(self.tab("グラフの確認"))
        self.delay_difference_visualization_frame.grid(row=0, column=0, sticky=ctk.NSEW)
        self.delay_difference_visualization_frame.grid_propagate(False)

        # ---------------------------------------------------------- #
        # 動画の確認タブ
        # ---------------------------------------------------------- #  
        self.tab("動画の確認").grid_propagate(False)
        self.tab("動画の確認").grid_rowconfigure(index=0, weight=1)
        self.tab("動画の確認").grid_columnconfigure(index=0, weight=1)
        
        self.check_avi = PageCheckAVI(self.tab("動画の確認"))
        self.check_avi.grid(row=0, column=0, sticky=ctk.NSEW)
        self.check_avi.grid_propagate(False)
        
    # ---------------------------------------------------------- #
    # タブで共通の関数
    # ---------------------------------------------------------- #
    def setGraphConfigure(self, CAN_file_path, RAM_file_path, camera_columns, vbox_columns, obj1):
        # ファイルパスの設定
        self.CAN_file_path = CAN_file_path
        self.RAM_file_path = RAM_file_path
        # カラムの設定
        self.camera_columns.clear()
        self.vbox_columns.clear() 
        # \nで文字を分ける
        # カメラ 
        camera_columns_lines = camera_columns.splitlines()
        for i in range(1, len(camera_columns_lines)):
            self.camera_columns.append(camera_columns_lines[i])
        # Vbox 
        vbox_columns_lines = vbox_columns.splitlines()
        for i in range(1, len(vbox_columns_lines)):
            self.vbox_columns.append(vbox_columns_lines[i])
        
        # オブジェクトのファイルパスを設定
        obj1.CAN_file_path  = self.CAN_file_path 
        obj1.RAM_file_path  = self.RAM_file_path
        # オブジェクトのカラムを設定
        obj1.camera_columns = self.camera_columns
        obj1.vbox_columns   = self.vbox_columns
        
        # print("CAN_file_path:{}".format(self.CAN_file_path))
        # print("RAM_file_path:{}".format(self.RAM_file_path))
        # print("camera_columns:{}".format(self.camera_columns))
        # print("vbox_columns:{}".format(self.vbox_columns))
        
        # print("CAN_file_path:{}".format(obj1.CAN_file_path))
        # print("RAM_file_path:{}".format(obj1.RAM_file_path))
        # print("camera_columns:{}".format(obj1.camera_columns))
        # print("vbox_columns:{}".format(obj1.vbox_columns))


    # def getGraphConfigure(self, obj):
    #     # フィルパスを設定
    #     obj.CAN_file_path  = self.CAN_file_path 
    #     obj.RAM_file_path  = self.RAM_file_path
    #     # カラムを設定
    #     obj.camera_columns = self.camera_columns
    #     obj.vbox_columns   = self.vbox_columns

    #     print("CAN_file_path:{}".format(obj.CAN_file_path))
    #     print("RAM_file_path:{}".format(obj.RAM_file_path))
    #     print("camera_columns:{}".format(obj.camera_columns))
    #     print("vbox_columns:{}".format(obj.vbox_columns))
                   