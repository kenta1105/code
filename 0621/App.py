"""
アプリケーションのメインウィンドウを作成するクラス

Author: Kenta Matsumura
"""
# ---------------------------------------------------------- #
# サードパーティライブラリのインポート
# ---------------------------------------------------------- #
import customtkinter as ctk
import pandas as pd

# ---------------------------------------------------------- #
# 自作ライブラリのインポート
# ---------------------------------------------------------- #
from common import *
from Tabview import Tabview
# ---------------------------------------------------------- #
# アプリケーションクラス
# ---------------------------------------------------------- #
class App(ctk.CTk):
    """
    アプリケーションのメインウィンドウを作成するクラス
    """    
    def __init__(self):
        super().__init__()
        """
        フォルダパスのタブ、データ確認用のタブを作成。 
        """
        # ---------------------------------------------------------- #
        # windowの設定
        # ---------------------------------------------------------- #
        self.title("後方カメラ測距性能評価用ツール")
        self.state('zoomed')
        ctk.set_appearance_mode("dark")
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1)
        
        # ---------------------------------------------------------- #
        # 全クラス(ページ)で共通の変数
        # ---------------------------------------------------------- #
        self.df = pd.DataFrame() #空のデータフレーム        
        self.frame_number = 0 #フレームNo
                
        # ---------------------------------------------------------- #
        # タブの設定
        # ---------------------------------------------------------- #
        self.tabview = Tabview(parent=self)
        self.tabview.grid(row=0, column=0, sticky=ctk.NSEW)
        self.tabview.grid_propagate(False) 

    # ---------------------------------------------------------- #
    # 全クラス(ページ)で共通の関数
    # ---------------------------------------------------------- #

        
    def addToListbox(self, entry, listbox):
        """
        entryに入力したアイテムをlistboxに追加
        
        parameters
        ----------
            entry : ctk.Entry
                listboxに追加するアイテムが入力されてるentry
            listbox : ctk.Listbox
                アイテムを追加する先のlistbox
        """
        item = entry.get()
        if item != "":
            listbox.insert(ctk.END, item)

    def removeFromListbox(self, listbox):
        """
        リストボックスで選択した全アイテムを削除
        
        parameters
        ----------
            listbox : ctk.Listbox
                アイテムを削除するlistbox
        """
        selected_indices = listbox.curselection()
        for index in reversed(selected_indices): #終わり側のインデックスから削除しないと全部まとめて削除できない(削除したindexから詰められる)
            listbox.delete(index)

    def copyAllFromListbox1ToListbox2(self, listbox1, listbox2):
        """
        リストボックス1の全アイテムをリストボックス2にコピー
        
        parameters
        ----------
            listbox1 : ctk.Listbox
                コピー元のリストボックス
            listbox2 : ctk.Listbox
                コピー先のリストボックス
        """
        #リストボックス2の値をクリア
        listbox2.delete(0, ctk.END)
        
        all_items = listbox1.get(0, ctk.END)
        for item in all_items:
            listbox2.insert(ctk.END, item)

    def copyFromListbox1ToListbox2(self, listbox1, listbox2):
        """
        リストボックス1の選択したアイテムをリストボックス2にコピー
        
        parameters
        ----------
            listbox1 : ctk.Listbox
                コピー元のリストボックス
            listbox2 : ctk.Listbox
                コピー先のリストボックス
        """
        # リストボックス1から選択された項目をリストで取得
        selected_items = [listbox1.get(idx) for idx in listbox1.curselection()]

        for item in selected_items:
            listbox2.insert(ctk.END, item)
    
        