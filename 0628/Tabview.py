"""
単一ファイル解析、
複数ファイル解析の切り替えタブを作成

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
from SingleFileAnalyzerFrame import SingleFileAnalyzerFrame
from MultiFileAnalyzerFrame import MultiFileAnalyzerFrame

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

        # ---------------------------------------------------------- #
        # タブの作成
        # ---------------------------------------------------------- #
        self.add("単一ファイル")
        self.add("複数ファイル")

        # ---------------------------------------------------------- #
        # 単一ファイルの解析
        # ---------------------------------------------------------- #
        self.tab("単一ファイル").grid_propagate(False)
        self.tab("単一ファイル").grid_rowconfigure(index=0, weight=1)
        self.tab("単一ファイル").grid_columnconfigure(index=0, weight=1)

        self.single_file_analyzer_frame = SingleFileAnalyzerFrame(self.tab("単一ファイル"))
        self.single_file_analyzer_frame.grid(row=0, column=0, sticky=ctk.NSEW)
        self.single_file_analyzer_frame.grid_propagate(False)

        # ---------------------------------------------------------- #
        # 複数ファイルの解析
        # ---------------------------------------------------------- #  
        self.tab("複数ファイル").grid_propagate(False)
        self.tab("複数ファイル").grid_rowconfigure(index=0, weight=1)
        self.tab("複数ファイル").grid_columnconfigure(index=0, weight=1)

        self.multi_file_analyzer_frame = MultiFileAnalyzerFrame(self.tab("複数ファイル"))
        self.multi_file_analyzer_frame.grid(row=0, column=0, sticky=ctk.NSEW)
        self.multi_file_analyzer_frame.grid_propagate(False)
        

                   