"""
スクロール可能なチェックボックス付きのフレーム

Author: Kenta Matsumura
"""

# ---------------------------------------------------------- #
# サードパーティライブラリのインポート
# ---------------------------------------------------------- #
import customtkinter as ctk
import tkinter as tk

# ---------------------------------------------------------- #
# 自作ライブラリのインポート
# ---------------------------------------------------------- #
from common import *

# ---------------------------------------------------------- #
# クラス定義
# ---------------------------------------------------------- #
class ScrollableCheckboxFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, title, values, output_label):
        """
        スクロール可能なチェックボックス付きのフレームを作成する
        
        parameters
        ----------
            parent : ctk.CTkFrame 
                作成したフレームの格納先のフレーム
            title : string
                スクロールバーのタイトル
            values : list of string
                チェックボックスの値
            output_label : ctk.CTkLabel
                選択したデータ名を表示するラベル
        """
        super().__init__(master=parent, label_text=title)
        
        # widgetの配置
        self.values = set(values)
        self.select_checkboxes = []
        self.delete_checkboxes = []
        self.delete_checkbox_var = []
        self.row_counter = 0
        
        self.createWidget(output_label, options=FrameOptions.INITIAL)
        
    def createWidget(self, output_label, options=FrameOptions.INITIAL, add_data=None):
        """
        n行3列のgridにwidgetを配置する
        
        parameters
        ----------
            output_label : ctk.CTKLabel
                選択したデータ名を表示するラベル
            is_first : bool
                初回かどうかを示すフラグ
        """
        if options == FrameOptions.INITIAL:
            # n行3列に設定
            for i in range(len(self.values)):
                self.grid_rowconfigure(index=i, weight=1)
                self.row_counter += 1
        
            self.grid_columnconfigure(index=0, weight=1)
            
            # widgetの配置
            for i, value in enumerate(list(self.values)):                
                # チェックボックス
                select_checkbox = ctk.CTkCheckBox(
                    master=self, 
                    text=value, 
                    command=lambda:self.select(output_label),
                )
                select_checkbox.grid(row=i, column=0, sticky=tk.NSEW)
                self.select_checkboxes.append(select_checkbox)
        
        else: # 追加          
            self.row_counter += 1
            self.grid_rowconfigure(index=self.row_counter, weight=1)      
            # チェックボックス
            select_checkbox = ctk.CTkCheckBox(
                master=self, 
                text=add_data, 
                command=lambda:self.select(output_label),
            )
            select_checkbox.grid(row=self.row_counter, column=0, sticky=tk.NSEW)
            self.select_checkboxes.append(select_checkbox)
        
    # 選択(選択中のアイテムを表示)
    def select(self, output_label):
        """
        選択したデータ名をoutput_labelに表示する
        
        parameters
        ----------
            output_label : ctk.CTKLabel
                選択したデータ名を表示するラベル
        """
        select_data = []
        for i, checkbox in enumerate(self.select_checkboxes):
            if checkbox.get() == 1:
                select_data.append(checkbox.cget("text"))
        # 選択中のデータを表示
        output_text = "[選択中のデータ]\n"
        for data in select_data:
            output_text +=  data + "\n"
        # 表示ラベルの文字を更新
        output_label.configure(text=output_text[:-1])    
                
    def addData(self, output_label, add_data):
        """
        入力したデータ名を選択候補に追加する
        
        parameters
        ----------
            output_label : ctk.CTKLabel
                選択したデータ名を表示するラベル
            add_data : ctk.CTKEntry
                追加するデータ名
        """
        # popupを表示
        
        # すでにあるなら追加させない
        if add_data.get() in self.values:
            pass
        else:
            self.values.add(add_data.get())
            self.createWidget(output_label, options=FrameOptions.ADD, add_data=add_data.get())
            

        
    
    