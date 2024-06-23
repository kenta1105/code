"""
遅延量推定用クラス

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
from PlotFrame import PlotFrame
from MakeDataFrame import MakeDataFrame 

# ---------------------------------------------------------- #
# クラス定義
# ---------------------------------------------------------- #
class DelayDiffenceVisualizationFrame(ctk.CTkFrame):
    def __init__(self, parent):
        """
        後方カメラとVboxのデータ遅延量の差を推定するクラス
        
        parameters
        ----------
            parent : ctk.CTkTabview 
                作成したフレームの格納先のタブ
        """
        super().__init__(master=parent)
        # ---------------------------------------------------------- #
        # メンバ変数
        # ---------------------------------------------------------- #

        
        # ---------------------------------------------------------- #
        # グラフの描画タブの行と列の設定
        # ---------------------------------------------------------- #
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)
        
        # ---------------------------------------------------------- #
        # グラフの描画設定用フレーム
        # ---------------------------------------------------------- #
        self.graph_property_frame = ctk.CTkFrame(
            master=self,
            **FRAME_PARAMS
        ) 
        self.graph_property_frame.grid(row=0, column=0, sticky=ctk.NSEW)
        self.graph_property_frame.grid_propagate(False)
        
        self.graph_property_frame.grid_rowconfigure(index=0, weight=1)
        self.graph_property_frame.grid_rowconfigure(index=1, weight=1)
        self.graph_property_frame.grid_rowconfigure(index=2, weight=1)
        self.graph_property_frame.grid_rowconfigure(index=3, weight=1)
        self.graph_property_frame.grid_rowconfigure(index=4, weight=1)
        self.graph_property_frame.grid_columnconfigure(index=0, weight=1)

        # ---------------------------------------------------------- #
        # ファイルパス
        # ---------------------------------------------------------- #
        #ファイルパス用フレーム
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
        
        # CANログ
        # ラベル
        self.CAN_file_path_label = ctk.CTkLabel(
            self.file_path_frame, 
            text = "CAN", 
            **LABEL_PARAMS)
        self.CAN_file_path_label.grid(row=0, column=0, columnspan=2, sticky=ctk.NSEW)     
        
        # 入力ボックス
        self.CAN_file_path_entry = ctk.CTkEntry(
            self.file_path_frame, 
            placeholder_text = "ファイルパス",
            **ENTRY_PARAMS)
        self.CAN_file_path_entry.grid(row=1, column=0, sticky=ctk.NSEW)
        
        # 参照ボタン
        self.file_path_reference_button = ctk.CTkButton(
            self.file_path_frame, 
            text="参照", 
            **BUTTON_PARAMS, 
            command=lambda:selectFilePath( 
                self.CAN_file_path_entry,
                ftypes=[("すべて","*")], 
            )
        )
        self.file_path_reference_button.grid(row=1, column=1, sticky=ctk.NSEW)
        
        # RMAファイル
        # ラベル
        self.RAM_file_label = ctk.CTkLabel(
            self.file_path_frame, 
            text="RAM",
            **LABEL_PARAMS
        )
        self.RAM_file_label.grid(row=0, column=2, columnspan=2, sticky=ctk.NSEW)
        
        # 入力ボックス 
        self.RAM_file_path_entry = ctk.CTkEntry(
            self.file_path_frame,
            placeholder_text = "ファイルパス", 
            **ENTRY_PARAMS
        ) 
        self.RAM_file_path_entry.grid(row=1, column=2, sticky=ctk.NSEW)
        
        # 参照ボタン
        self.RAM_file_path_reference_button = ctk.CTkButton(
            self.file_path_frame, 
            text="参照", 
            **BUTTON_PARAMS, 
            command=lambda:selectFilePath(
                self.RAM_file_path_entry,
                ftypes=[("すべて","*")], 
            )
        )
        self.RAM_file_path_reference_button.grid(row=1, column=3, sticky=ctk.NSEW)
                
        # ---------------------------------------------------------- #
        # カメラとVboxの遅延量の差を表示
        # ---------------------------------------------------------- #        
        self.delay_frame = ctk.CTkFrame(
            master=self.graph_property_frame,
            **FRAME_PARAMS
        ) 
        self.delay_frame.grid(row=3, column=0, sticky=ctk.NSEW)
        self.delay_frame.grid_propagate(False)
        self.delay_frame.grid_rowconfigure(index=0, weight=1)
        self.delay_frame.grid_rowconfigure(index=1, weight=1)
        self.delay_frame.grid_rowconfigure(index=2, weight=1)
        self.delay_frame.grid_columnconfigure(index=0, weight=1)
        self.delay_frame.grid_columnconfigure(index=1, weight=1)
        self.delay_frame.grid_columnconfigure(index=2, weight=1)
        self.delay_frame.grid_columnconfigure(index=3, weight=1)
        self.delay_frame.grid_columnconfigure(index=4, weight=1)
        
        # 距離のラベル
        self.distance_label = ctk.CTkLabel(
            master=self.delay_frame,
            text="距離[m]",
            **LABEL_PARAMS 
        )
        self.distance_label.grid(row=1, column=0, sticky=ctk.NSEW) 
        
        # 時間のラベル
        self.time_label = ctk.CTkLabel(
            master=self.delay_frame,
            text="時間[ms]",
            **LABEL_PARAMS 
        )
        self.time_label.grid(row=2, column=0, sticky=ctk.NSEW) 
        
        # ---------------------------------------------------------- #
        # 後方カメラ
        # ---------------------------------------------------------- #
        # ラベル   
        self.delay_camera_label = ctk.CTkLabel(
            master=self.delay_frame,
            text="カメラ",
            **LABEL_PARAMS 
        )
        self.delay_camera_label.grid(row=0, column=1, sticky=ctk.NSEW)       
        
        # 距離
        self.distance_camera_label = ctk.CTkLabel(
            master=self.delay_frame,
            text="0",
            **LABEL_PARAMS 
        )
        self.distance_camera_label.grid(row=1, column=1, sticky=ctk.NSEW)    
        
        # 時間   
        self.time_camera_label = ctk.CTkLabel(
            master=self.delay_frame,
            text="0",
            **LABEL_PARAMS 
        )
        self.time_camera_label.grid(row=2, column=1, sticky=ctk.NSEW)    
        
        # ---------------------------------------------------------- #
        # Vbox
        # ---------------------------------------------------------- #
        self.delay_vbox_label = ctk.CTkLabel(
            master=self.delay_frame,
            text="Vbox",
            **LABEL_PARAMS 
        )
        self.delay_vbox_label.grid(row=0, column=2, sticky=ctk.NSEW)
        
        # 距離
        self.distance_vbox_label = ctk.CTkLabel(
            master=self.delay_frame,
            text="0",
            **LABEL_PARAMS 
        )
        self.distance_vbox_label.grid(row=1, column=2, sticky=ctk.NSEW)    
        
        # 時間   
        self.time_vbox_label = ctk.CTkLabel(
            master=self.delay_frame,
            text="0",
            **LABEL_PARAMS 
        )
        self.time_vbox_label.grid(row=2, column=2, sticky=ctk.NSEW)   

        # ---------------------------------------------------------- #
        # 差分
        # ---------------------------------------------------------- #
        self.delay_difference_label = ctk.CTkLabel(
            master=self.delay_frame,
            text="差分",
            **LABEL_PARAMS 
        )
        self.delay_difference_label.grid(row=0, column=3, sticky=ctk.NSEW)
        
        # 距離
        self.distance_difference_label = ctk.CTkLabel(
            master=self.delay_frame,
            text="0",
            **LABEL_PARAMS 
        )
        self.distance_difference_label.grid(row=1, column=3, sticky=ctk.NSEW)    
        
        # 時間   
        self.time_difference_label = ctk.CTkLabel(
            master=self.delay_frame,
            text="0",
            **LABEL_PARAMS 
        )
        self.time_difference_label.grid(row=2, column=3, sticky=ctk.NSEW)
        
        # ---------------------------------------------------------- #
        # RAMの設定フレーム(Plotの内容使うからここに入れる)
        # ---------------------------------------------------------- # 
        self.RAM_frame = ctk.CTkFrame(
            master=self.graph_property_frame,
        )
        self.RAM_frame.grid(row=4, column=0, sticky=ctk.NSEW)
        self.RAM_frame.grid_propagate(False)
        
        # 2行3列に設定
        self.RAM_frame.grid_rowconfigure(index=0, weight=1)
        self.RAM_frame.grid_rowconfigure(index=1, weight=1)
        self.RAM_frame.grid_columnconfigure(index=0, weight=1)
        self.RAM_frame.grid_columnconfigure(index=1, weight=1)
        self.RAM_frame.grid_columnconfigure(index=2, weight=1)
        
        # 読み込み結果のラベル
        self.read_RAM_result_label = ctk.CTkLabel(
            master=self.RAM_frame,
            text="RAMファイルを読み込んでください",
            **LABEL_PARAMS 
        )
        self.read_RAM_result_label.grid(row=0, column=1, columnspan=2, sticky=ctk.NSEW)
        
        # videoFrameのラベル
        self.video_frame_label = ctk.CTkLabel(
            master=self.RAM_frame,
            text="動画フレーム",
            **LABEL_PARAMS 
        )
        self.video_frame_label.grid(row=1, column=0, sticky=ctk.NSEW)
        
        # videoFrameの入力ボックス
        self.video_frame_entry = ctk.CTkEntry(
            master=self.RAM_frame, 
            placeholder_text = "動画フレーム",
            **ENTRY_PARAMS
        )
        self.video_frame_entry.grid(row=1, column=1, sticky=ctk.NSEW)               
        
        # ---------------------------------------------------------- #
        # グラフの表示用フレーム(PlotFrameを下でも使うので先に宣言)
        # ---------------------------------------------------------- #      
        self.graph_display_frame = PlotFrame(
            parent=self,
            camera_dist_label=self.distance_camera_label,
            camera_time_label=self.time_camera_label,
            vbox_dist_label=self.distance_vbox_label,
            vbox_time_label=self.time_vbox_label,
            diff_dist_label=self.distance_difference_label,
            diff_time_label=self.time_difference_label
        )
        self.graph_display_frame.grid(row=0, column=1, sticky=ctk.NSEW)
        self.graph_display_frame.grid_propagate(False)

        # ---------------------------------------------------------- #
        # 後方カメラとVboxどっちを選択するかを決めるラジオボタン(Plotを使うからここに定義)
        # ---------------------------------------------------------- #
        self.sensor_select_frame = ctk.CTkFrame(
            master=self.delay_frame,
            **FRAME_PARAMS
        )
        self.sensor_select_frame.grid(row=0, rowspan=3, column=4, sticky=ctk.NSEW)
        self.sensor_select_frame.grid_propagate(False)
        self.sensor_select_frame.grid_rowconfigure(index=0, weight=1)
        self.sensor_select_frame.grid_rowconfigure(index=1, weight=1)
        self.sensor_select_frame.grid_columnconfigure(index=0, weight=1)
        
        self.sensor_select_radio_var = ctk.IntVar(value=1)
        # カメラ
        self.camera_select_radiobutton = ctk.CTkRadioButton(
            master=self.sensor_select_frame, 
            text="カメラ",
            command=lambda:self.graph_display_frame.setSensorType(self.sensor_select_radio_var.get()), 
            variable= self.sensor_select_radio_var, 
            value=1,
            **RADIOBUTTON_PARMAS
        )
        self.camera_select_radiobutton.grid(row=0, column=0, sticky=ctk.NSEW)
        
        # Vbox
        self.vbox_select_radiobutton = ctk.CTkRadioButton(
            master=self.sensor_select_frame, 
            text="Vbox",
            command=lambda:self.graph_display_frame.setSensorType(self.sensor_select_radio_var.get()), 
            variable= self.sensor_select_radio_var, 
            value=2,
            **RADIOBUTTON_PARMAS
        )
        self.vbox_select_radiobutton.grid(row=1, column=0, sticky=ctk.NSEW)

        # ---------------------------------------------------------- #
        # RAMフレームのボタン(Plotを使うからここに定義)
        # ---------------------------------------------------------- #
        # RAM読み込みボタン
        self.RAM_read_button = ctk.CTkButton(
            self.RAM_frame, 
            text="RAMファイル\n読み込み",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.makeRAMDataFrame(
                self.RAM_file_path_entry.get(),
                self.read_RAM_result_label
            )
        )
        self.RAM_read_button.grid(row=0, column=0, sticky=ctk.NSEW)
        
        # # ---------------------------------------------------------- #
        # # グラフの描画実行フレーム
        # # ---------------------------------------------------------- #        
        self.graph_draw_frame = ctk.CTkFrame(
            master=self.graph_property_frame,
            **FRAME_PARAMS
        ) 
        self.graph_draw_frame.grid(row=1, column=0, sticky=ctk.NSEW)
        self.graph_draw_frame.grid_propagate(False)
        self.graph_draw_frame.grid_rowconfigure(index=0, weight=1)
        self.graph_draw_frame.grid_rowconfigure(index=1, weight=1)
        self.graph_draw_frame.grid_rowconfigure(index=2, weight=1)
        self.graph_draw_frame.grid_columnconfigure(index=0, weight=1)
        self.graph_draw_frame.grid_columnconfigure(index=1, weight=1)
        self.graph_draw_frame.grid_columnconfigure(index=2, weight=1)
        self.graph_draw_frame.grid_columnconfigure(index=3, weight=1)
        self.graph_draw_frame.grid_columnconfigure(index=4, weight=1)
        self.graph_draw_frame.grid_columnconfigure(index=5, weight=10)
        
        # 距離の方向
        # ラベル
        self.direction_label = ctk.CTkLabel(
            master=self.graph_draw_frame,
            text="方向",
            **LABEL_PARAMS 
        )
        self.direction_label.grid(row=0, column=0, sticky=ctk.NSEW)
        
        # ラジオボタン
        self.direction_radio_var = ctk.IntVar(value=1)
        # 縦
        self.graph_lng_radiobutton = ctk.CTkRadioButton(
            self.graph_draw_frame, 
            text="縦",
            command=None, 
            variable=self.direction_radio_var, 
            value=1,
            **RADIOBUTTON_PARMAS
        )
        self.graph_lng_radiobutton.grid(row=1, column=0, sticky=ctk.NSEW)
        
        # 横
        self.graph_lat_radiobutton = ctk.CTkRadioButton(
            self.graph_draw_frame, 
            text="横",
            command=None, 
            variable=self.direction_radio_var, 
            value=2,
            **RADIOBUTTON_PARMAS
        )
        self.graph_lat_radiobutton.grid(row=2, column=0, sticky=ctk.NSEW)
        
        # 自車の動き
        # ラベル
        self.car_label = ctk.CTkLabel(
            master=self.graph_draw_frame,
            text="自車",
            **LABEL_PARAMS 
        )
        self.car_label.grid(row=0, column=1, sticky=ctk.NSEW)
        
        # ラジオボタン
        self.car_radio_var = ctk.IntVar(value=1)
        # 静止
        self.car_stationary_radiobutton = ctk.CTkRadioButton(
            self.graph_draw_frame, 
            text="静止",
            command=None, 
            variable=self.car_radio_var, 
            value=1,
            **RADIOBUTTON_PARMAS
        )
        self.car_stationary_radiobutton.grid(row=1, column=1, sticky=ctk.NSEW)
        
        # 移動
        self.car_move_radiobutton = ctk.CTkRadioButton(
            self.graph_draw_frame, 
            text="移動",
            command=None, 
            variable=self.car_radio_var, 
            value=2,
            **RADIOBUTTON_PARMAS
        )
        self.car_move_radiobutton.grid(row=2, column=1, sticky=ctk.NSEW)     
        
        # ダミーの動き
        # ラベル
        self.dummy_label = ctk.CTkLabel(
            master=self.graph_draw_frame,
            text="ダミー",
            **LABEL_PARAMS 
        )
        self.dummy_label.grid(row=0, column=2, sticky=ctk.NSEW)
        
        # ラジオボタン
        self.dummy_radio_var = ctk.IntVar(value=1)
        # 静止
        self.dummy_stationary_radiobutton = ctk.CTkRadioButton(
            self.graph_draw_frame, 
            text="静止",
            command=None, 
            variable=self.dummy_radio_var, 
            value=1,
            **RADIOBUTTON_PARMAS
        )
        self.dummy_stationary_radiobutton.grid(row=1, column=2, sticky=ctk.NSEW)
        
        # 移動
        self.dummy_move_radiobutton = ctk.CTkRadioButton(
            self.graph_draw_frame, 
            text="移動",
            command=None, 
            variable=self.dummy_radio_var, 
            value=2,
            **RADIOBUTTON_PARMAS
        )
        self.dummy_move_radiobutton.grid(row=2, column=2, sticky=ctk.NSEW)     
        
        # 自車の方位
        # ラベル[deg]
        self.head_label = ctk.CTkLabel(
            master=self.graph_draw_frame,
            text="自車方位の\n初期値[deg]",
            **LABEL_PARAMS 
        )
        self.head_label.grid(row=0, column=3, sticky=ctk.NSEW)          
        
        # 入力ボックス
        self.head_entry_var = ctk.StringVar(value="20")
        self.head_entry = ctk.CTkEntry(
            master=self.graph_draw_frame, 
            textvariable=self.head_entry_var,
            placeholder_text = "方位[deg]",
            **ENTRY_PARAMS)
        self.head_entry.grid(row=1, column=3, sticky=ctk.NSEW)
        
        # 方位を使用するかのスイッチ
        self.head_use_switch_var = ctk.BooleanVar(value=False)
        self.head_use_switch = ctk.CTkSwitch(
            master=self.graph_draw_frame,
            text="方位の補正",
            command=lambda:changeWidgetState(self.head_entry),
            variable=self.head_use_switch_var,
            onvalue=True,
            offvalue=False,
            **SWITCH_PARAMS
        )
        self.head_use_switch.grid(row=2, column=3, sticky=ctk.NSEW)
        
        # 遅延の初期値
        self.initial_shift_label = ctk.CTkLabel(
            master=self.graph_draw_frame,
            text="カメラ遅延\n初期値[ms]",
            **LABEL_PARAMS 
        )
        self.initial_shift_label.grid(row=0, column=4, sticky=ctk.NSEW)   
        
        # 入力ボックス
        self.initial_shift_var = ctk.StringVar(value="0")
        self.initial_shift_entry = ctk.CTkEntry(
            master=self.graph_draw_frame, 
            textvariable=self.initial_shift_var,
            placeholder_text = "遅延[ms]",
            **ENTRY_PARAMS)
        self.initial_shift_entry.grid(row=1, rowspan=2, column=4, sticky=ctk.NSEW)
        
        # データが正しく選ばれてるかの判定結果を示すラベル
        self.graph_draw_label = ctk.CTkLabel(
            master=self.graph_draw_frame,
            text="",
            **LABEL_PARAMS 
        )
        self.graph_draw_label.grid(row=1, rowspan=2, column=5, sticky=ctk.NSEW)
                
        # ---------------------------------------------------------- #
        # グラフの設定変更
        # ---------------------------------------------------------- #        
        self.update_graph_frame = ctk.CTkFrame(
            master=self.graph_property_frame,
            **FRAME_PARAMS
        ) 
        self.update_graph_frame.grid(row=2, column=0, sticky=ctk.NSEW)
        self.update_graph_frame.grid_propagate(False)
        self.update_graph_frame.grid_rowconfigure(index=0, weight=1)
        self.update_graph_frame.grid_rowconfigure(index=1, weight=1)
        self.update_graph_frame.grid_rowconfigure(index=2, weight=2)
        self.update_graph_frame.grid_rowconfigure(index=3, weight=1)
        self.update_graph_frame.grid_rowconfigure(index=4, weight=1)
        self.update_graph_frame.grid_rowconfigure(index=5, weight=2)
        self.update_graph_frame.grid_columnconfigure(index=0, weight=1)
        self.update_graph_frame.grid_columnconfigure(index=1, weight=1)
        self.update_graph_frame.grid_columnconfigure(index=2, weight=1)
        
        # ---------------------------------------------------------- #
        # Vboxのスムージング
        # ---------------------------------------------------------- #
        # ラベル
        self.smoothing_label = ctk.CTkLabel(
            master=self.update_graph_frame,
            text="Vboxの平滑化[ms]",
            **LABEL_PARAMS 
        )
        self.smoothing_label.grid(row=0, column=0, columnspan=3, sticky=ctk.NSEW)
        
        # スライダーの値を示すラベル
        self.smoothing_value_label = ctk.CTkLabel(
            master=self.update_graph_frame,
            text="0",
            **LABEL_PARAMS 
        )
        self.smoothing_value_label.grid(row=1, column=1, sticky=ctk.NSEW)

        # スライダー
        self.smoothing_slider_var = tk.IntVar()
        self.smoothing_slider = ctk.CTkSlider(
            master=self.update_graph_frame, 
            from_=0, 
            to=3000, 
            number_of_steps=3000,
            variable=self.smoothing_slider_var,
            command=lambda x:self.graph_display_frame.updateGraphBySlider(
                self.smoothing_slider_var,
                self.smoothing_value_label,
                GraphUpdateType.SMOOTHING
            )
        )
        self.smoothing_slider.grid(row=2, column=1, sticky=ctk.NSEW)     
        
        # スライダーの値減少ボタン     
        self.smoothing_dwon_button = ctk.CTkButton(
            master=self.update_graph_frame, 
            text="Down\nMin:3000[ms]",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.updateGraph(
                WidgetType.MINUS_BUTTON, 
                self.smoothing_slider_var,  
                self.smoothing_value_label,
                GraphUpdateType.SMOOTHING,
                value_min=0,
                value_max=3000
            )
        )
        self.smoothing_dwon_button.grid(row=1, rowspan=2, column=0, sticky=ctk.NSEW)   
        
        # スライダーの値増加ボタン     
        self.smoothing_up_button = ctk.CTkButton(
            master=self.update_graph_frame, 
            text="Up\nMax:3000[ms]",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.updateGraph(
                WidgetType.PLUS_BUTTON, 
                self.smoothing_slider_var,  
                self.smoothing_value_label,
                GraphUpdateType.SMOOTHING,
                value_min=0,
                value_max=3000
            )
        )
        self.smoothing_up_button.grid(row=1, rowspan=2, column=2, sticky=ctk.NSEW)

        # ---------------------------------------------------------- #
        # 後方カメラの時間シフト
        # ---------------------------------------------------------- #
        # ラベル
        self.shift_label = ctk.CTkLabel(
            master=self.update_graph_frame,
            text="後方カメラの時間シフト[ms]",
            **LABEL_PARAMS 
        )
        self.shift_label.grid(row=3, column=0, columnspan=3, sticky=ctk.NSEW)
        
        # スライダーの値を示すラベル
        self.shift_value_label = ctk.CTkLabel(
            master=self.update_graph_frame,
            text="0",
            **LABEL_PARAMS
        )
        self.shift_value_label.grid(row=4, column=1, sticky=ctk.NSEW)

        # スライダー
        self.shift_slider_var = tk.IntVar()
        self.shift_slider = ctk.CTkSlider(
            master=self.update_graph_frame, 
            from_=-3000, 
            to=3000, 
            number_of_steps=6000,
            variable=self.shift_slider_var,
            command=lambda x:self.graph_display_frame.updateGraphBySlider(
                self.shift_slider_var,
                self.shift_value_label,
                GraphUpdateType.SHIFT
            )
        )
        self.shift_slider.grid(row=5, column=1, sticky=ctk.NSEW)        

        # スライダーの値減少ボタン     
        self.shift_dwon_button = ctk.CTkButton(
            master=self.update_graph_frame, 
            text="Down\n(Min:-3000[ms])",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.updateGraph(
                WidgetType.MINUS_BUTTON, 
                self.shift_slider_var, 
                self.shift_value_label,
                GraphUpdateType.SHIFT,
                value_min=-3000,
                value_max=3000
            )
        )
        self.shift_dwon_button.grid(row=4, rowspan=2, column=0, sticky=ctk.NSEW)
                
        # スライダーの値増加ボタン     
        self.shift_up_button = ctk.CTkButton(
            master=self.update_graph_frame, 
            text="Up\n(Max:3000[ms])",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.updateGraph(
                WidgetType.PLUS_BUTTON, 
                self.shift_slider_var, 
                self.shift_value_label,
                GraphUpdateType.SHIFT,
                value_min=-3000,
                value_max=3000
            )
        )
        self.shift_up_button.grid(row=4, rowspan=2, column=2, sticky=ctk.NSEW)
        
        
        # ---------------------------------------------------------- #
        # グラフの描画実行ボタン
        # ---------------------------------------------------------- #    
        self.graph_draw_button = ctk.CTkButton(
            master=self.graph_draw_frame, 
            text="グラフの描画",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.drawGraph(
                file_path             = self.CAN_file_path_entry.get(),
                distance_direction    = self.direction_radio_var.get(),
                dummy_action          = self.dummy_radio_var.get(),
                initial_head          = float(self.head_entry.get()),
                is_use_head           = self.head_use_switch_var.get(),
                initial_shift         = int(self.initial_shift_entry.get()),
                output_label          = self.graph_draw_label,
                smoothing_slider      = self.smoothing_slider,
                shift_slider          = self.shift_slider,
                smoothing_value_label = self.smoothing_value_label,
                shift_value_label     = self.shift_value_label
            )
        )
        self.graph_draw_button.grid(row=0, column=5, sticky=ctk.NSEW)
        
        # ---------------------------------------------------------- #
        # グラフの描画実行ボタン
        # ---------------------------------------------------------- #   
        self.jump_to_video_frame_button = ctk.CTkButton(
            self.RAM_frame, 
            text="Jump",
            **BUTTON_PARAMS,
            command=lambda:self.graph_display_frame.jumpToVideoFrameTime(
                video_frame_entry  = self.video_frame_entry,
                distance_direction = self.direction_radio_var.get(),
                output_label       = self.read_RAM_result_label
            )
        )
        self.jump_to_video_frame_button.grid(row=1, column=2, sticky=ctk.NSEW)

        