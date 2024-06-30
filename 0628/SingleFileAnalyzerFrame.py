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
        # グラフの描画設定用タブ
        # ---------------------------------------------------------- #
        self.graph_property_tabview = ctk.CTkTabview(
            master=self,
            **FRAME_PARAMS
        ) 
        self.graph_property_tabview.grid(row=0, column=0, sticky=ctk.NSEW)
        self.graph_property_tabview.grid_propagate(False)

        # タブの設定
        self.graph_property_tabview.add("グラフの描画")
        self.graph_property_tabview.add("グラフの体裁設定")
        self.graph_property_tabview.add("統計量")
        self.graph_property_tabview.add("データの整形")
            
        # ---------------------------------------------------------- #
        # グラフの描画タブ
        # ---------------------------------------------------------- #
        self.graph_property_tabview.tab("グラフの描画").grid_propagate(False)
        self.graph_property_tabview.tab("グラフの描画").grid_rowconfigure(index=0, weight=1)
        self.graph_property_tabview.tab("グラフの描画").grid_rowconfigure(index=1, weight=8)
        self.graph_property_tabview.tab("グラフの描画").grid_rowconfigure(index=2, weight=1)
        self.graph_property_tabview.tab("グラフの描画").grid_columnconfigure(index=0, weight=1)

        # ---------------------------------------------------------- #
        # ファイルパス用フレーム(2行4列)
        # ---------------------------------------------------------- #
        self.file_path_frame = ctk.CTkFrame(
            master=self.graph_property_tabview.tab("グラフの描画"), 
            **FRAME_PARAMS
        )
        self.file_path_frame.grid(row=0, column=0, sticky=ctk.NSEW)
        self.file_path_frame.grid_propagate(False)
        self.file_path_frame.grid_rowconfigure(index=0, weight=1)
        self.file_path_frame.grid_columnconfigure(index=0,  weight=1)
        self.file_path_frame.grid_columnconfigure(index=1,  weight=1)       
        self.file_path_frame.grid_columnconfigure(index=2,  weight=1)
        self.file_path_frame.grid_columnconfigure(index=3,  weight=1)

        # 入力ボックス
        self.data_file_path_entry = ctk.CTkEntry(
            self.file_path_frame, 
            placeholder_text = "ファイルパス",
            **ENTRY_PARAMS)
        self.data_file_path_entry.grid(row=0, column=0, sticky=ctk.NSEW)
        
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
        self.data_file_path_reference_button.grid(row=0, column=1, sticky=ctk.NSEW)

        # 読み込み結果
        self.data_read_result_label = ctk.CTkLabel(
            master=self.file_path_frame,
            text="読み込みボタンを\n押してください",
            **LABEL_PARAMS 
        )
        self.data_read_result_label.grid(row=0, column=2, sticky=ctk.NSEW)
        
        # ---------------------------------------------------------- #
        # データ選択用フレーム
        # ---------------------------------------------------------- #
        self.data_select_frame = ctk.CTkFrame(
            master=self.graph_property_tabview.tab("グラフの描画"), 
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
            master=self.graph_property_tabview.tab("グラフの描画"),
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
            command=lambda:self.graph_display_frame.readDataFile(
                file_path=self.data_file_path_entry.get(),
                read_result_label=self.data_read_result_label,
                x_columns_frame=self.x_columns_frame,
                y_columns_frame=self.y_columns_frame,
                draw_result_label=self.graph_draw_result_label
            )
        )
        self.data_read_button.grid(row=0, column=3, sticky=ctk.NSEW)

        # ---------------------------------------------------------- #
        # グラフの体裁設定タブ(3行1列)
        # ---------------------------------------------------------- #
        self.graph_property_tabview.tab("グラフの体裁設定").grid_propagate(False)
        self.graph_property_tabview.tab("グラフの体裁設定").grid_rowconfigure(index=0, weight=1)
        self.graph_property_tabview.tab("グラフの体裁設定").grid_rowconfigure(index=1, weight=4)
        self.graph_property_tabview.tab("グラフの体裁設定").grid_rowconfigure(index=2, weight=5)
        self.graph_property_tabview.tab("グラフの体裁設定").grid_rowconfigure(index=3, weight=1)
        self.graph_property_tabview.tab("グラフの体裁設定").grid_columnconfigure(index=0, weight=1)

        # ---------------------------------------------------------- #
        # タイトルの体裁設定フレーム(2行5列)
        # ---------------------------------------------------------- #
        self.title_frame = ctk.CTkFrame(
            master=self.graph_property_tabview.tab("グラフの体裁設定"), 
            **FRAME_PARAMS
        )
        self.title_frame.grid(row=0, column=0, sticky=ctk.NSEW)
        self.title_frame.grid_propagate(False)
        self.title_frame.grid_rowconfigure(index=0, weight=1)
        self.title_frame.grid_rowconfigure(index=1, weight=1)
        self.title_frame.grid_columnconfigure(index=0,  weight=1)
        self.title_frame.grid_columnconfigure(index=1,  weight=1)       
        self.title_frame.grid_columnconfigure(index=2,  weight=1)
        self.title_frame.grid_columnconfigure(index=3,  weight=1)
        self.title_frame.grid_columnconfigure(index=4,  weight=1)
        

        # タイトルのラベル
        self.title_label = ctk.CTkLabel(
            master=self.title_frame,
            text="タイトル",
            **LABEL_PARAMS 
        )
        self.title_label.grid(row=0, column=0, sticky=ctk.NSEW)
        
        # タイトルの入力ボックス
        self.title_entry = ctk.CTkEntry(
            self.title_frame, 
            placeholder_text = "タイトル",
            **ENTRY_PARAMS)
        self.title_entry.grid(row=1, column=0, sticky=ctk.NSEW)
        
        # タイトルの文字サイズのラベル
        self.title_fontsize_label = ctk.CTkLabel(
            master=self.title_frame,
            text="タイトルの文字サイズ",
            **LABEL_PARAMS 
        )
        self.title_fontsize_label.grid(row=0, column=1, columnspan=3, sticky=ctk.NSEW)
        
        # タイトルの文字サイズの値を示すラベル
        self.title_fontsize_value_label = ctk.CTkLabel(
            master=self.title_frame,
            text="16",
            **LABEL_PARAMS 
        )
        self.title_fontsize_value_label.grid(row=1, column=2, sticky=ctk.NSEW)

        # タイトルの文字サイズ減少ボタン     
        self.title_fontsize_down_button = ctk.CTkButton(
            master=self.title_frame,
            width=1,
            text="-",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.updateFontSize(
            )
        )
        self.title_fontsize_down_button.grid(row=1, column=1, sticky=ctk.NSEW)
        
        # タイトルの文字サイズ増加ボタン     
        self.title_fontsize_up_button = ctk.CTkButton(
            master=self.title_frame,
            width=1,
            text="+",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.updateFontSize(
            )
        )
        self.title_fontsize_up_button.grid(row=1, column=3, sticky=ctk.NSEW)           
        
        # 変更結果のラベル
        self.title_update_result_label = ctk.CTkLabel(
            master=self.title_frame,
            text="更新ボタンを押して下さい",
            **LABEL_PARAMS 
        )
        self.title_update_result_label.grid(row=1, column=4, sticky=ctk.NSEW)
        
        # 変更ボタン
        self.title_update_button = ctk.CTkButton(
            master=self.title_frame, 
            text="更新",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.updateTitle(
                title     = self.title_entry.get(),
                font_size = self.title_fontsize_value_label.cget("text")
            )
        )
        self.title_update_button.grid(row=0, column=4, sticky=ctk.NSEW)
        
        # ---------------------------------------------------------- #
        # X軸の体裁設定フレーム(2行4列)
        # ---------------------------------------------------------- #
        self.xlabel_frame = ctk.CTkFrame(
            master=self.graph_property_tabview.tab("グラフの体裁設定"), 
            **FRAME_PARAMS
        )
        self.xlabel_frame.grid(row=1, column=0, sticky=ctk.NSEW)
        self.xlabel_frame.grid_propagate(False)
        self.xlabel_frame.grid_rowconfigure(index=0, weight=1)
        self.xlabel_frame.grid_rowconfigure(index=1, weight=1)
        self.xlabel_frame.grid_rowconfigure(index=2, weight=1)
        self.xlabel_frame.grid_rowconfigure(index=3, weight=1)
        self.xlabel_frame.grid_columnconfigure(index=0, weight=1)
        self.xlabel_frame.grid_columnconfigure(index=1, weight=1)       
        self.xlabel_frame.grid_columnconfigure(index=2, weight=1)

        # ---------------------------------------------------------- #
        # X軸名
        # ---------------------------------------------------------- #
        self.xlabel_label = ctk.CTkLabel(
            master=self.xlabel_frame,
            text="X軸名",
            **LABEL_PARAMS 
        )
        self.xlabel_label.grid(row=0, column=0, sticky=ctk.NSEW)
        
        # X軸名の入力ボックス
        self.xlabel_entry = ctk.CTkEntry(
            master=self.xlabel_frame, 
            placeholder_text = "X軸名",
            **ENTRY_PARAMS)
        self.xlabel_entry.grid(row=1, column=0, sticky=ctk.NSEW)

        # ---------------------------------------------------------- #
        # X軸の文字サイズ
        # ---------------------------------------------------------- #
        self.xlabel_fontsize_frame = ctk.CTkFrame(
            master=self.xlabel_frame
        )
        self.xlabel_fontsize_frame.grid(row=0, rowspan=2 ,column=1, sticky=ctk.NSEW)
        
        self.xlabel_fontsize_frame.grid_propagate(False)
        self.xlabel_fontsize_frame.grid_rowconfigure(index=0, weight=1)
        self.xlabel_fontsize_frame.grid_rowconfigure(index=1, weight=1)
        self.xlabel_fontsize_frame.grid_columnconfigure(index=0,  weight=1)
        self.xlabel_fontsize_frame.grid_columnconfigure(index=1,  weight=1)       
        self.xlabel_fontsize_frame.grid_columnconfigure(index=2,  weight=1)

        # X軸の文字サイズのラベル
        self.xlabel_fontsize_label = ctk.CTkLabel(
            master=self.xlabel_fontsize_frame, 
            text="軸名の文字サイズ",
            **LABEL_PARAMS 
        )
        self.xlabel_fontsize_label.grid(row=0, column=0, columnspan=3, sticky=ctk.NSEW)
        
        # X軸名の文字サイズの値を示すラベル
        self.xlabel_fontsize_value_label = ctk.CTkLabel(
            master=self.xlabel_fontsize_frame,  
            text="14",
            **LABEL_PARAMS 
        )
        self.xlabel_fontsize_value_label.grid(row=1, column=1, sticky=ctk.NSEW)

        # X軸名の文字サイズ減少ボタン     
        self.xlabel_fontsize_down_button = ctk.CTkButton(
            master=self.xlabel_fontsize_frame,  
            width=1,
            text="-",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.updateFontSize(
            )
        )
        self.xlabel_fontsize_down_button.grid(row=1, column=0, sticky=ctk.NSEW)
        
        # X軸名の文字サイズ増加ボタン     
        self.xlabel_fontsize_up_button = ctk.CTkButton(
            master=self.xlabel_fontsize_frame,  
            width=1,
            text="+",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.updateFontSize(
            )
        )
        self.xlabel_fontsize_up_button.grid(row=1, column=2, sticky=ctk.NSEW)   

        # ---------------------------------------------------------- #
        # X軸の目盛りの文字サイズ
        # ---------------------------------------------------------- #
        self.xlabel_labelsize_frame = ctk.CTkFrame(
            master=self.xlabel_frame,
            border_color="white",
            border_width=1
        )
        self.xlabel_labelsize_frame.grid(row=0, rowspan=2 ,column=2, sticky=ctk.NSEW)
        
        self.xlabel_labelsize_frame.grid_propagate(False)
        self.xlabel_labelsize_frame.grid_rowconfigure(index=0, weight=1)
        self.xlabel_labelsize_frame.grid_rowconfigure(index=1, weight=1)
        self.xlabel_labelsize_frame.grid_columnconfigure(index=0, weight=1)
        self.xlabel_labelsize_frame.grid_columnconfigure(index=1, weight=1)       
        self.xlabel_labelsize_frame.grid_columnconfigure(index=2, weight=1)  

        # X軸の目盛りサイズのラベル
        self.xlabel_labelsize_label = ctk.CTkLabel(
            master=self.xlabel_labelsize_frame, 
            text="目盛りの文字サイズ",
            **LABEL_PARAMS 
        )
        self.xlabel_labelsize_label.grid(row=0, column=0, columnspan=3, sticky=ctk.NSEW)
        
        # X軸の目盛りサイズの値を示すラベル
        self.xlabel_labelsize_value_label = ctk.CTkLabel(
            master=self.xlabel_labelsize_frame, 
            text="12",
            **LABEL_PARAMS 
        )
        self.xlabel_labelsize_value_label.grid(row=1, column=1, sticky=ctk.NSEW)

        # X軸の目盛りサイズ減少ボタン     
        self.xlabel_labelsize_down_button = ctk.CTkButton(
            master=self.xlabel_labelsize_frame, 
            width=1,
            text="-",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.updateFontSize(
            )
        )
        self.xlabel_labelsize_down_button.grid(row=1, column=0, sticky=ctk.NSEW)
        
        # X軸の目盛りサイズ増加ボタン     
        self.xlabel_labelsize_up_button = ctk.CTkButton(
            master=self.xlabel_labelsize_frame, 
            width=1,
            text="+",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.updateFontSize(
            )
        )
        self.xlabel_labelsize_up_button.grid(row=1, column=2, sticky=ctk.NSEW)     

        # ---------------------------------------------------------- #
        # X軸の範囲
        # ---------------------------------------------------------- #
        self.xlabel_xlim_frame = ctk.CTkFrame(
            master=self.xlabel_frame,
            border_color="white",
            border_width=1
        )
        self.xlabel_xlim_frame.grid(row=2, rowspan=2 ,column=0, columnspan=2, sticky=ctk.NSEW)
        
        self.xlabel_xlim_frame.grid_propagate(False)
        self.xlabel_xlim_frame.grid_rowconfigure(index=0, weight=1)
        self.xlabel_xlim_frame.grid_rowconfigure(index=1, weight=1)
        self.xlabel_xlim_frame.grid_columnconfigure(index=0, weight=1)
        self.xlabel_xlim_frame.grid_columnconfigure(index=1, weight=1)       
        self.xlabel_xlim_frame.grid_columnconfigure(index=2, weight=1)  
        self.xlabel_xlim_frame.grid_columnconfigure(index=3, weight=1)  
        
        # X軸の目盛り最小値のラベル
        self.xlim_min_label = ctk.CTkLabel(
            master=self.xlabel_xlim_frame,
            text="最小値",
            **LABEL_PARAMS 
        )
        self.xlim_min_label.grid(row=0, column=1, sticky=ctk.NSEW)
        
        # X軸の目盛り最小値の入力ボックス
        self.xlim_min_entry = ctk.CTkEntry(
            master=self.xlabel_xlim_frame, 
            placeholder_text = "最小値",
            **ENTRY_PARAMS)
        self.xlim_min_entry.grid(row=1, column=1, sticky=ctk.NSEW)
        
       # X軸の目盛り最大値のラベル
        self.xlim_max_label = ctk.CTkLabel(
            master=self.xlabel_xlim_frame,
            text="最大値",
            **LABEL_PARAMS 
        )
        self.xlim_max_label.grid(row=0, column=2, sticky=ctk.NSEW)
        
        # X軸の目盛り最大値の入力ボックス
        self.xlim_max_entry = ctk.CTkEntry(
            master=self.xlabel_xlim_frame, 
            placeholder_text = "最大値",
            **ENTRY_PARAMS)
        self.xlim_max_entry.grid(row=1, column=2, sticky=ctk.NSEW)

       # X軸の目盛り間隔のラベル
        self.xlim_step_label = ctk.CTkLabel(
            master=self.xlabel_xlim_frame,
            text="間隔",
            **LABEL_PARAMS 
        )
        self.xlim_step_label.grid(row=0, column=3, sticky=ctk.NSEW)
        
        # X軸の目盛り間隔のラベルの入力ボックス
        self.xlim_step_entry = ctk.CTkEntry(
            master=self.xlabel_xlim_frame, 
            placeholder_text = "間隔",
            **ENTRY_PARAMS)
        self.xlim_step_entry.grid(row=1, column=3, sticky=ctk.NSEW)
        
        # X軸の範囲を変更するかどうかのスイッチ
        self.set_xlim_switch_var = ctk.BooleanVar(value=False)
        self.set_xlim_switch = ctk.CTkSwitch(
            master=self.xlabel_xlim_frame, 
            text="範囲\n変更",
            command=lambda:changeWidgetState(
                self.xlim_min_entry,
                self.xlim_max_entry,
                self.xlim_step_entry
            ),
            variable=self.set_xlim_switch_var,
            onvalue=True,
            offvalue=False,
            **SWITCH_PARAMS
        )
        self.set_xlim_switch.grid(row=0, rowspan=2, column=0, sticky=ctk.NSEW)

        # ---------------------------------------------------------- #
        # X軸の更新
        # ---------------------------------------------------------- #
        self.xlabel_update_result_label = ctk.CTkLabel(
            master=self.xlabel_frame, 
            text="更新ボタンを\n押して下さい",
            **LABEL_PARAMS 
        )
        self.xlabel_update_result_label.grid(row=3, column=2, sticky=ctk.NSEW)
        
        # 変更ボタン
        self.xlabel_update_button = ctk.CTkButton(
            master=self.xlabel_frame,  
            text="更新",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.updateTitle(
                title     = self.title_entry.get(),
                font_size = self.title_fontsize_value_label.cget("text")
            )
        )
        self.xlabel_update_button.grid(row=2, column=2, sticky=ctk.NSEW)
        
    # ---------------------------------------------------------- #
    # Y軸の体裁設定フレーム(1行4列)
    # ---------------------------------------------------------- #
        self.ylabel_frame = ctk.CTkFrame(
            master=self.graph_property_tabview.tab("グラフの体裁設定"), 
            border_color="white",
            border_width=1
        )
        self.ylabel_frame.grid(row=2, column=0, sticky=ctk.NSEW)
        self.ylabel_frame.grid_propagate(False)
        
        self.ylabel_frame.grid_rowconfigure(index=0, weight=1)
        self.ylabel_frame.grid_rowconfigure(index=1, weight=1)
        self.ylabel_frame.grid_columnconfigure(index=0,  weight=1)
        self.ylabel_frame.grid_columnconfigure(index=1,  weight=1)       

        # ---------------------------------------------------------- #
        # 行数と軸名の設定フレーム
        # ---------------------------------------------------------- #
        self.ylabel_row_name_frame = ctk.CTkFrame(
            master=self.ylabel_frame
        )
        self.ylabel_row_name_frame.grid(row=0, column=0, sticky=ctk.NSEW)
        self.ylabel_row_name_frame.grid_propagate(False)
        
        self.ylabel_row_name_frame.grid_rowconfigure(index=0, weight=1)
        self.ylabel_row_name_frame.grid_rowconfigure(index=1, weight=1)
        self.ylabel_row_name_frame.grid_columnconfigure(index=0,  weight=1)
        self.ylabel_row_name_frame.grid_columnconfigure(index=1,  weight=1) 
        
        # ---------------------------------------------------------- #
        # 行数
        # ---------------------------------------------------------- #
        # ラベル
        self.ylabel_row_label = ctk.CTkLabel(
            master=self.ylabel_row_name_frame, 
            text="行番号",
            **LABEL_PARAMS 
        )
        self.xlabel_update_result_label.grid(row=3, column=2, sticky=ctk.NSEW)
        
        
        # 選択肢(コンボボックス)

        # ---------------------------------------------------------- #
        # 軸名
        # ---------------------------------------------------------- #


        # ---------------------------------------------------------- #
        # 軸範囲
        # ---------------------------------------------------------- #

        # ---------------------------------------------------------- #
        # グラフ種類
        # ---------------------------------------------------------- #

        # ---------------------------------------------------------- #
        # グラフの設定
        # ---------------------------------------------------------- #
        
        

        
        
        

    # ---------------------------------------------------------- #
    # 更新ボタン
    # ---------------------------------------------------------- #
        self.graph_update_button = ctk.CTkButton(
            master=self.graph_property_tabview.tab("グラフの体裁設定"),  
            text="更新",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.updateTitle(
                title     = self.title_entry.get(),
                font_size = self.title_fontsize_value_label.cget("text")
            )
        )
        self.graph_update_button.grid(row=3, column=0, sticky=ctk.NSEW)
        
        
            


            
            
        
        
        
        