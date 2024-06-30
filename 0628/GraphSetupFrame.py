"""
グラフの設定用クラス

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
from ScrollableCheckboxFrame import ScrollableCheckboxFrame

# ---------------------------------------------------------- #
# クラス定義
# ---------------------------------------------------------- #
class GraphSetupFrame(ctk.CTkFrame):
    def __init__(self, parent):
        """
        グラフの設定用フレーム
        
        parameters
        ----------
            parent : ctk.CTkTabview 
                作成したフレームの格納先のタブ
        """
        super().__init__(master=parent)
                
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=8)
        self.grid_rowconfigure(index=2, weight=1)
        self.grid_columnconfigure(index=0, weight=1)

        # ---------------------------------------------------------- #
        # ファイルパス用フレームの設定
        # ---------------------------------------------------------- #
        #ファイルパス用フレーム
        self.file_path_frame = ctk.CTkFrame(
            master=self, 
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
        self.file_path_frame.grid_columnconfigure(index=6,  weight=1)
        self.file_path_frame.grid_columnconfigure(index=7,  weight=1)
        self.file_path_frame.grid_columnconfigure(index=8,  weight=1)
        self.file_path_frame.grid_columnconfigure(index=9,  weight=1)
        
        # フォルダ
        # ラベル
        self.CAN_folder_path_label = ctk.CTkLabel(
            self.file_path_frame, 
            text = "CANフォルダ", 
            **LABEL_PARAMS
        )
        self.CAN_folder_path_label.grid(row=0, column=0, columnspan=2, sticky=ctk.NSEW)
        
        # 入力ボックス
        self.CAN_folder_path_entry = ctk.CTkEntry(
            self.file_path_frame, 
            placeholder_text = "フォルダパス",
            **ENTRY_PARAMS)
        self.CAN_folder_path_entry.grid(row=1, column=0, sticky=ctk.NSEW)
        
        # 決定ボタン
        self.CAN_folder_path_detect_button = ctk.CTkButton(
            self.file_path_frame, 
            text="決定", 
            **BUTTON_PARAMS, 
            command=lambda:changeWidgetState(self.CAN_folder_path_entry)
        )
        self.CAN_folder_path_detect_button.grid(row=1, column=1, sticky=ctk.NSEW)
        
        # ファイルパス
        # ラベル
        self.CAN_file_path_label = ctk.CTkLabel(
            self.file_path_frame, 
            text = "CANファイル", 
            **LABEL_PARAMS)
        self.CAN_file_path_label.grid(row=0, column=2, columnspan=3, sticky=ctk.NSEW)     
        
        # 入力ボックス
        self.CAN_file_path_entry = ctk.CTkEntry(
            self.file_path_frame, 
            placeholder_text = "ファイルパス",
            **ENTRY_PARAMS)
        self.CAN_file_path_entry.grid(row=1, column=2, sticky=ctk.NSEW)
        
        # 参照ボタン
        self.file_path_reference_button = ctk.CTkButton(
            self.file_path_frame, 
            text="参照", 
            **BUTTON_PARAMS, 
            command=lambda:selectFilePath(
                self.CAN_folder_path_entry, 
                self.CAN_file_path_entry,
                ftypes=[("すべて","*")], 
            )
        )
        self.file_path_reference_button.grid(row=1, column=3, sticky=ctk.NSEW)
        
        #決定ボタン
        self.CAN_file_path_detect_button = ctk.CTkButton(
            self.file_path_frame, 
            text="決定",
            **BUTTON_PARAMS,
            command=lambda:changeWidgetState(self.CAN_file_path_entry)
        )
        self.CAN_file_path_detect_button.grid(row=1, column=4, sticky=ctk.NSEW)
        
        # RAM
        # ラベル
        self.RAM_folder_label = ctk.CTkLabel(
            self.file_path_frame, 
            text="RAMフォルダ",
            **LABEL_PARAMS
        )
        self.RAM_folder_label.grid(row=0, column=5, columnspan=2, sticky=ctk.NSEW)
        
        # 入力ボックス
        self.RAM_folder_path_entry = ctk.CTkEntry(
            self.file_path_frame,
            placeholder_text = "フォルダパス",
            **ENTRY_PARAMS
        ) 
        self.RAM_folder_path_entry.grid(row=1, column=5, sticky=ctk.NSEW)
        
        # 決定ボタン
        self.RAM_folder_path_detect_button = ctk.CTkButton(
            self.file_path_frame,
            text="決定",
            **BUTTON_PARAMS,
            command=lambda:changeWidgetState(self.RAM_folder_path_entry)
        )
        self.RAM_folder_path_detect_button.grid(row=1, column=6, sticky=ctk.NSEW)
        
        # RMAファイル
        # ラベル
        self.RAM_file_label = ctk.CTkLabel(
            self.file_path_frame, 
            text="RAMファイル",
            **LABEL_PARAMS
        )
        self.RAM_file_label.grid(row=0, column=7, columnspan=3, sticky=ctk.NSEW)
        
        # 入力ボックス 
        self.RAM_file_path_entry = ctk.CTkEntry(
            self.file_path_frame,
            placeholder_text = "ファイルパス", 
            **ENTRY_PARAMS
        ) 
        self.RAM_file_path_entry.grid(row=1, column=7, sticky=ctk.NSEW)
        
        # 参照ボタン
        self.RAM_file_path_reference_button = ctk.CTkButton(
            self.file_path_frame, 
            text="参照", 
            **BUTTON_PARAMS, 
            command=lambda:selectFilePath(
                self.RAM_folder_path_entry, 
                self.RAM_file_path_entry,
                ftypes=[("すべて","*")], 
            )
        )
        self.RAM_file_path_reference_button.grid(row=1, column=8, sticky=ctk.NSEW)
                
        # 決定ボタン 
        self.RAM_file_path_detect_button = ctk.CTkButton(
            self.file_path_frame,
            text="決定",
            **BUTTON_PARAMS,
            command=lambda:changeWidgetState(self.RAM_file_path_entry)
        )
        self.RAM_file_path_detect_button.grid(row=1, column=9, sticky=ctk.NSEW)        
        
        # ---------------------------------------------------------- #
        # データ選択用フレームの設定
        # ---------------------------------------------------------- #
        # データ選択用フレーム
        self.data_select_frame = ctk.CTkFrame(
            master=self, 
            **FRAME_PARAMS
        )        
        self.data_select_frame.grid(row=1, column=0, sticky=ctk.NSEW)
        self.data_select_frame.grid_propagate(False)
        self.data_select_frame.grid_rowconfigure(index=0, weight=1)
        self.data_select_frame.grid_rowconfigure(index=1, weight=1)
        self.data_select_frame.grid_columnconfigure(index=0, weight=1)
        self.data_select_frame.grid_columnconfigure(index=1, weight=1)
        self.data_select_frame.grid_columnconfigure(index=2, weight=1)
        self.data_select_frame.grid_columnconfigure(index=3, weight=1)
        self.data_select_frame.grid_columnconfigure(index=4, weight=1)
        
        # ---------------------------------------------------------- #
        # 後方カメラ
        # ---------------------------------------------------------- #
        # ラベル
        self.camera_label = ctk.CTkLabel(
            master=self.data_select_frame,
            text="後方カメラ",
            **LABEL_PARAMS 
        )
        self.camera_label.grid(row=0, column=0, sticky=ctk.NSEW)
        
        #選択中のカラムを表示
        self.camera_selected_label = ctk.CTkLabel(
            master=self.data_select_frame,
            text="[選択したデータ]",
            **LABEL_PARAMS 
        )
        self.camera_selected_label.grid(row=0, column=4, sticky=ctk.NSEW)
        
        # チェックボックス用フレーム
        camera_columns = ["RCMRDEPLOC1", "RCMRHOLLOC1", "RCMRDEPLOC3", "RCMRHOLLOC3"]
        self.camera_columns_frame = ScrollableCheckboxFrame(
            parent=self.data_select_frame,
            title="選択候補",
            values=camera_columns,
            output_label=self.camera_selected_label
        )
        self.camera_columns_frame.grid(row=0, column=1, sticky=ctk.NSEW)
        
        #追加用入力ボックス
        self.camera_columns_add_entry = ctk.CTkEntry(
            master=self.data_select_frame, 
            placeholder_text = "追加するデータ名",
            **ENTRY_PARAMS)
        self.camera_columns_add_entry.grid(row=0, column=2, sticky=ctk.NSEW)
        
        #追加ボタン
        self.camera_columns_add_button = ctk.CTkButton(
            master=self.data_select_frame, 
            text="追加",
            **BUTTON_PARAMS,
            command=lambda:self.camera_columns_frame.addData(
                output_label=self.camera_selected_label,
                add_data=self.camera_columns_add_entry
            )
        )
        self.camera_columns_add_button.grid(row=0, column=3, sticky=ctk.NSEW)
                
        # ---------------------------------------------------------- #
        # vbox
        # ---------------------------------------------------------- #
        # ラベル
        self.vbox_label = ctk.CTkLabel(
            master=self.data_select_frame,
            text="後方カメラ",
            **LABEL_PARAMS 
        )
        self.vbox_label.grid(row=1, column=0, sticky=ctk.NSEW)
        
        #選択中のカラムを表示
        self.vbox_selected_label = ctk.CTkLabel(
            master=self.data_select_frame,
            text="[選択したデータ]",
            **LABEL_PARAMS 
        )
        self.vbox_selected_label.grid(row=1, column=4, sticky=ctk.NSEW)
        
        # チェックボックス用フレーム
        vbox_columns = ["LngRsv_tg1", "LatRsv_tg1", "LngRtg_tg1", "LatRtg_tg1", "Dummy_Y_Po"]
        self.vbox_columns_frame = ScrollableCheckboxFrame(
            parent=self.data_select_frame,
            title="選択候補",
            values=vbox_columns,
            output_label=self.vbox_selected_label
        )
        self.vbox_columns_frame.grid(row=1, column=1, sticky=ctk.NSEW)
        
        #追加用入力ボックス
        self.vbox_columns_add_entry = ctk.CTkEntry(
            master=self.data_select_frame, 
            placeholder_text = "追加するデータ名",
            **ENTRY_PARAMS)
        self.vbox_columns_add_entry.grid(row=1, column=2, sticky=ctk.NSEW)
        
        #追加ボタン
        self.vbox_columns_add_button = ctk.CTkButton(
            master=self.data_select_frame, 
            text="追加",
            **BUTTON_PARAMS,
            command=lambda:self.vbox_columns_frame.addData(
                output_label=self.vbox_selected_label,
                add_data=self.vbox_columns_add_entry
            )
        )
        self.vbox_columns_add_button.grid(row=1, column=3, sticky=ctk.NSEW)
        