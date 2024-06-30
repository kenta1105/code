"""
単一ファイル解析用クラス

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
from ScrollableCheckboxFrame import ScrollableCheckboxFrame
from PlotFrame import PlotFrame

# ---------------------------------------------------------- #
# クラス定義
# ---------------------------------------------------------- #
class SingleFileAnalyzerFrame(ctk.CTkFrame):
    def __init__(self, parent):
        """
        単一ファイルの解析用クラス
        
        parameters
        ----------
            parent : ctk.CTkTabview 
                作成したフレームの格納先のタブ
        """
        super().__init__(master=parent)

        # ---------------------------------------------------------- #
        # タブ(機能)の設定
        # ---------------------------------------------------------- #
        
        
        
        
        
        
        
        
        # ---------------------------------------------------------- #
        # フレーム全体の行と列の設定(1行2列)
        # ---------------------------------------------------------- #
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=3)
        self.grid_columnconfigure(index=1, weight=7)

        # ---------------------------------------------------------- #
        # グラフを表示するフレーム(PlotFrameを下でも使うので先に宣言)
        # ---------------------------------------------------------- #      
        self.graph_display_frame = PlotFrame(
            parent=self,
        )
        self.graph_display_frame.grid(row=0, column=1, sticky=ctk.NSEW)
        self.graph_display_frame.grid_propagate(False)
        
        # ---------------------------------------------------------- #
        # グラフの描画設定用フレーム(3行1列)
        # ---------------------------------------------------------- #
        self.graph_property_frame = ctk.CTkFrame(
            master=self,
            **FRAME_PARAMS
        ) 
        self.graph_property_frame.grid(row=0, column=0, sticky=ctk.NSEW)
        self.graph_property_frame.grid_propagate(False)
        
        self.graph_property_frame.grid_rowconfigure(index=0, weight=1)
        self.graph_property_frame.grid_rowconfigure(index=1, weight=8)
        self.graph_property_frame.grid_rowconfigure(index=2, weight=1)
        self.graph_property_frame.grid_columnconfigure(index=0, weight=1)
        
        # ---------------------------------------------------------- #
        # ファイルパス用フレーム(2行4列)
        # ---------------------------------------------------------- #
        self.file_path_frame = ctk.CTkFrame(
            master=self.graph_property_frame, 
            **FRAME_PARAMS
        )
        self.file_path_frame.grid(row=0, column=0, sticky=ctk.NSEW)
        self.file_path_frame.grid_propagate(False)
        self.file_path_frame.grid_rowconfigure(index=0, weight=1)
        self.file_path_frame.grid_rowconfigure(index=1, weight=1)
        self.file_path_frame.grid_columnconfigure(index=0,  weight=1)
        self.file_path_frame.grid_columnconfigure(index=1,  weight=1)       
        self.file_path_frame.grid_columnconfigure(index=2,  weight=1)
        self.file_path_frame.grid_columnconfigure(index=3,  weight=1)
        self.file_path_frame.grid_columnconfigure(index=4,  weight=1)
        self.file_path_frame.grid_columnconfigure(index=5,  weight=1)

        # データファイル
        # ラベル
        self.data_file_path_label = ctk.CTkLabel(
            self.file_path_frame, 
            text = "データファイル", 
            **LABEL_PARAMS)
        self.data_file_path_label.grid(row=0, column=0, columnspan=2, sticky=ctk.NSEW)     
        
        # 入力ボックス
        self.data_file_path_entry = ctk.CTkEntry(
            self.file_path_frame, 
            placeholder_text = "ファイルパス",
            **ENTRY_PARAMS)
        self.data_file_path_entry.grid(row=1, column=0, sticky=ctk.NSEW)
        
        # 参照ボタン
        self.data_file_path_reference_button = ctk.CTkButton(
            self.file_path_frame, 
            text="参照", 
            **BUTTON_PARAMS, 
            command=lambda:selectFilePath( 
                self.data_file_path_entry,
                ftypes=[("すべて","*")], 
            )
        )
        self.data_file_path_reference_button.grid(row=1, column=1, sticky=ctk.NSEW)
        
        # データ名ファイル
        # ラベル
        self.data_name_file_label = ctk.CTkLabel(
            self.file_path_frame, 
            text="データ名の設定ファイル",
            **LABEL_PARAMS
        )
        self.data_name_file_label.grid(row=0, column=2, columnspan=4, sticky=ctk.NSEW)
        
        # 入力ボックス 
        self.data_name_file_path_entry = ctk.CTkEntry(
            self.file_path_frame,
            placeholder_text = "ファイルパス", 
            **ENTRY_PARAMS
        ) 
        self.data_name_file_path_entry.grid(row=1, column=2, sticky=ctk.NSEW)
        
        # 参照ボタン
        self.data_name_file_path_reference_button = ctk.CTkButton(
            self.file_path_frame, 
            text="参照", 
            **BUTTON_PARAMS, 
            command=lambda:selectFilePath(
                self.data_name_file_path_entry,
                ftypes=[("すべて","*")], 
            )
        )
        self.data_name_file_path_reference_button.grid(row=1, column=3, sticky=ctk.NSEW)

        # 読み込み結果
        self.data_read_result_label = ctk.CTkLabel(
            master=self.file_path_frame,
            text="読み込みボタンを\n押してください",
            **LABEL_PARAMS 
        )
        self.data_read_result_label.grid(row=1, column=5, sticky=ctk.NSEW)
        
        # ---------------------------------------------------------- #
        # データ選択用フレーム
        # ---------------------------------------------------------- #
        self.data_select_frame = ctk.CTkFrame(
            master=self.graph_property_frame, 
            **FRAME_PARAMS
        )        
        self.data_select_frame.grid(row=1, column=0, sticky=ctk.NSEW)
        self.data_select_frame.grid_propagate(False)
        
        self.data_select_frame.grid_rowconfigure(index=0, weight=1)
        self.data_select_frame.grid_rowconfigure(index=1, weight=1)   
        self.data_select_frame.grid_columnconfigure(index=0, weight=1)
        self.data_select_frame.grid_columnconfigure(index=1, weight=1)

        # 選択中のデータ名を示すラベル
        # 横軸
        self.selected_data_lat_label = ctk.CTkLabel(
            master=self.data_select_frame,
            text="[選択したデータ]",
            **LABEL_PARAMS 
        )
        self.selected_data_lat_label.grid(row=1, column=0, sticky=ctk.NSEW)
        # 縦軸
        self.selected_data_lng_label = ctk.CTkLabel(
            master=self.data_select_frame,
            text="[選択したデータ]",
            **LABEL_PARAMS 
        )
        self.selected_data_lng_label.grid(row=1, column=1, sticky=ctk.NSEW)

        # 選択フレーム
        # 横軸
        self.x_columns_frame = ScrollableCheckboxFrame(
            parent=self.data_select_frame,
            title="X軸",
            output_label=self.selected_data_lat_label
        )
        self.x_columns_frame.grid(row=0, column=0, sticky=ctk.NSEW)
        
        # 縦軸
        self.y_columns_frame = ScrollableCheckboxFrame(
            parent=self.data_select_frame,
            title="Y軸",
            output_label=self.selected_data_lng_label
        )
        self.y_columns_frame.grid(row=0, column=1, sticky=ctk.NSEW)
        
        # ---------------------------------------------------------- #
        # グラフの描画実行フレーム
        # ---------------------------------------------------------- #
        self.graph_draw_frame = ctk.CTkFrame(
            master=self.graph_property_frame,
            **FRAME_PARAMS
        )        
        self.graph_draw_frame.grid(row=2, column=0, sticky=ctk.NSEW)
        self.graph_draw_frame.grid_propagate(False)
        
        self.graph_draw_frame.grid_rowconfigure(index=0, weight=1) 
        self.graph_draw_frame.grid_columnconfigure(index=0, weight=1)
        self.graph_draw_frame.grid_columnconfigure(index=1, weight=1)
        
        # 描画結果
        self.graph_draw_result_label = ctk.CTkLabel(
            master=self.graph_draw_frame,
            text="グラフの描画ボタンを押して下さい",
            **LABEL_PARAMS 
        )
        self.graph_draw_result_label.grid(row=0, column=1, sticky=ctk.NSEW)
        
        # 描画実行ボタン
        self.graph_draw_button = ctk.CTkButton(
            master=self.graph_draw_frame, 
            text="グラフの描画",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.drawGraph(
                x_checkboxes=self.x_columns_frame.checkboxes,
                y_checkboxes=self.y_columns_frame.checkboxes,
                output_label=self.graph_draw_result_label
            )
        )
        self.graph_draw_button.grid(row=0, column=0, sticky=ctk.NSEW)
        
        # ---------------------------------------------------------- #
        # 読み込み実行ボタン
        # ---------------------------------------------------------- #
        self.data_read_button = ctk.CTkButton(
            master=self.file_path_frame, 
            text="読み込み",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.makeDataFrame(
                file_path=self.data_file_path_entry.get(),
                output_label=self.data_read_result_label,
                x_columns_frame=self.x_columns_frame,
                y_columns_frame=self.y_columns_frame
            )
        )
        self.data_read_button.grid(row=1, column=4, sticky=ctk.NSEW)
            


            
            
        
        
        
        