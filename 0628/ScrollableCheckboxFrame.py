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
    def __init__(self, parent, title, output_label):
        """
        スクロール可能なチェックボックス付きのフレームを作成する
        
        parameters
        ----------
            parent : ctk.CTkFrame 
                作成したフレームの格納先のフレーム
            title : string
                スクロールバーのタイトル
            output_label : ctk.CTkLabel
                選択したデータ名を表示するラベル
        """
        super().__init__(master=parent, label_text=title)
        
        # widgetの配置
        self.checkboxes = []
        self.row_counter = 0
        self.output_label = output_label
        
    def createWidget(self, columns):
        """
        n行3列のgridにwidgetを配置する
        
        parameters
        ----------
            output_label : ctk.CTKLabel
                選択したデータ名を表示するラベル
            columns : list of string
                カラム名のリスト
        """

        # n行1列に設定
        for i in range(len(columns)):
            self.grid_rowconfigure(index=i, weight=1)
            self.row_counter += 1
    
        self.grid_columnconfigure(index=0, weight=1)
        
        # widgetの配置
        for i, value in enumerate(columns):                
            # チェックボックス
            select_checkbox = ctk.CTkCheckBox(
                master=self, 
                text=value, 
                command=lambda:self.select(),
            )
            select_checkbox.grid(row=i, column=0, sticky=tk.NSEW)
            self.checkboxes.append(select_checkbox)
    
        
    # 選択(選択中のアイテムを表示)
    def select(self):
        """
        選択したデータ名をoutput_labelに表示する
        """
        select_data = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                select_data.append(checkbox.cget("text"))
        # 選択中のデータを表示
        output_text = "[選択中のデータ]\n"
        for data in select_data:
            output_text +=  data + "\n"
        # 表示ラベルの文字を更新
        self.output_label.configure(text=output_text[:-1])    
    
    # リセット
    def reset(self):
        self.checkboxes.clear()
        self.output_label.configure(text="[選択中のデータ]")
                

            

        
    
    