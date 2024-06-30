import tkinter as tk
import os, sys
from PIL import Image, ImageTk
import cv2
import numpy as np

from common import *


# 動画ファイルの確認ページ
class PageCheckAVI(ctk.CTkFrame):
    # __init__: 初期設定, 部品配置
    def __init__(self, parent):
        self.big_font = ("MSゴシック", "12", "bold")
        self.middle_font = ("MSゴシック", "10", "bold")
        self.small_font = ("MSゴシック", "9", "bold")
        
        super().__init__(parent)
        
        self.delay = 3
        self.frame_rgb = None
        self.cap = None
        self.avi_play_state = False
        
        # 行と列の作成
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # ---------------------------------------------------------- #
        # 各コンポーネント用のフレームを用意
        # ---------------------------------------------------------- #
        # 1. ファイルパス
        self.input_frame = tk.LabelFrame(
            self, text="ファイルパス", font=self.middle_font, bd=2, bg="white", relief=tk.SOLID
        )
        self.input_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.input_frame.grid_propagate(False)
        
        # 2. 動画
        self.movie_frame = tk.LabelFrame(
            self, text="動画", font=self.middle_font, bd=2, bg="white", relief=tk.SOLID
        )
        self.movie_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.movie_frame.grid_propagate(False)
        
        # 3. コマ送り
        self.swap_frame = tk.Frame(self)
        self.swap_frame.grid(row=2, column=0, sticky=tk.NSEW)
        self.swap_frame.grid_propagate(False)

        # 4. ページ遷移
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=3, column=0, sticky=tk.NSEW)
        self.button_frame.grid_propagate(False)
        
        # ---------------------------------------------------------- #
        # 各コンポーネントに部品を配置
        # ---------------------------------------------------------- #
        # 1. ファイルパス
        # フレームの行と列の設定
        self.input_frame.grid_rowconfigure(0, weight=1)
        for iter in range(13):
            self.input_frame.grid_columnconfigure(iter, weight=1)

        # 1-1. フォルダパスの指定
        self.folder_path_label = tk.Label(
            self.input_frame, text="フォルダ", font=self.small_font, fg="black"
        ) 
        self.folder_path_label.grid(row=0, column=0, sticky=tk.NSEW)
        self.folder_path_input = tk.Entry(self.input_frame) 
        self.folder_path_input.grid(row=0, column=1, sticky=tk.NSEW)
        self.folder_detect = tk.Button(
            self.input_frame,
            text="決定",
            font=self.small_font,
            command=lambda:changeWidgetState(self.folder_path_input)
        )
        self.folder_detect.grid(row=0, column=2, sticky=tk.NSEW)
        
        # 1-2. ファイルパスの指定
        self.file_path_label = tk.Label(
            self.input_frame, text="ファイル", fg="black", font=self.small_font)
        self.file_path_label.grid(row=0, column=3, sticky=tk.NSEW)     
        self.file_path_input = tk.Entry(self.input_frame)
        self.file_path_input.grid(row=0, column=4, sticky=tk.NSEW)
        self.file_path_reference = tk.Button(
            self.input_frame,
            text="参照",
            font=self.small_font,
            command=lambda:self.readAVIFile()
        )
        self.file_path_reference.grid(row=0, column=5, sticky=tk.NSEW)
        self.file_path_detect = tk.Button(
            self.input_frame, text="決定", font=self.small_font, command=lambda:changeWidgetState(self.file_path_input)
        )
        self.file_path_detect.grid(row=0, column=6, sticky=tk.NSEW)
        
        # 2. 動画
        # フレームの行と列の設定
        self.movie_frame.grid_rowconfigure(0, weight=5)
        self.movie_frame.grid_rowconfigure(1, weight=1)
        # self.movie_frame.grid_rowconfigure(2, weight=3)
        self.movie_frame.grid_columnconfigure(0, weight=3)
        self.movie_frame.grid_columnconfigure(1, weight=1)
        self.movie_frame.grid_columnconfigure(2, weight=1)
        self.movie_frame.grid_columnconfigure(3, weight=1)
        
        # 2-1. 動画フレームの表示
        self.avi_frame_canvas = tk.Canvas(
            self.movie_frame,
            bg="gray"
        )
        self.avi_frame_canvas.grid(row=0, column=0, columnspan=4, sticky=tk.NSEW)
        
        # 2-2. 動画読込状態ダイアログ
        self.avi_state_label = tk.Label(
            self.movie_frame, text="AVIファイルを読み込んでください", fg="black", font=self.small_font
        )
        self.avi_state_label.grid(row=1, column=0, sticky=tk.NSEW)   
        
        # 2-3. 動画操作ボタン
        self.play_button = tk.Button(self.movie_frame, text="再生", font=self.middle_font, command=lambda:self.setPlayState())
        self.play_button.grid(row=1, column=1, sticky=tk.NSEW)
        
        self.stop_button = tk.Button(self.movie_frame, text="停止", font=self.middle_font, command=lambda:self.clearPlayState())
        self.stop_button.grid(row=1, column=2, sticky=tk.NSEW)
        
        self.head_button = tk.Button(self.movie_frame, text="先頭", font=self.middle_font, command=lambda:self.returnHead())
        self.head_button.grid(row=1, column=3, sticky=tk.NSEW)
        
        # 3. コマ送り
        # フレームの行と列の設定
        self.swap_frame.grid_rowconfigure(0, weight=1)
        self.swap_frame.grid_columnconfigure(0, weight=16)
        self.swap_frame.grid_columnconfigure(1, weight=1)
        self.swap_frame.grid_columnconfigure(2, weight=1)
        self.swap_frame.grid_columnconfigure(3, weight=3)

        # 3-1. コマ送り
        # 3-1-1. コマ送りシークバー
        self.scale_var = tk.IntVar(self.swap_frame)
        self.frames_scale = tk.Scale(
            self.swap_frame,
            from_=1,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.scale_var,
            command=lambda x: self.updateFrame()
        )
        self.frames_scale.grid(row=0, column=0, sticky=tk.NSEW)
        
        # 2-4-2. スピンボックス
        self.frames_spinbox = tk.Spinbox(
            self.swap_frame,
            from_=1,
            to=100,
            textvariable=self.scale_var,
            command=lambda:self.updateFrame()
        )
        self.frames_spinbox.grid(row=0, column=1, sticky=tk.NSEW)

        # 2-4-3. 最大フレーム数
        self.max_frame_label = tk.Label(self.swap_frame, text="最大フレーム : 1", fg="black", font=self.small_font)
        self.max_frame_label.grid(row=0, column=2, sticky=tk.NSEW)

    
    # readAVIFile: 参照した動画ファイルを読み込む
    def readAVIFile(self):
        selectFilePath(self.file_path_input, ftypes=[("AVI",".avi")])
        self.cap = cv2.VideoCapture(self.file_path_input.get())
        ret, frame = self.cap.read()
        
        if self.file_path_input.get():
            if ret:
                self.frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(
                    cv2.resize(self.frame_rgb, (self.movie_frame.winfo_width(), int(self.movie_frame.winfo_height() * 5 / 6)))
                )
                self.imgtk = ImageTk.PhotoImage(image=image)
                self.canvas_image = self.avi_frame_canvas.create_image(0, 0, anchor="nw", image=self.imgtk)
                
                self.avi_state_label.config(text="AVIファイル読込み完了", fg="blue")

                self.scale_var.set(0)

                #スケールとスピンボックスの最大値を動画のフレーム数に更新
                total_frame_cnt = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
                self.frames_scale.config(to=total_frame_cnt)
                self.frames_spinbox.config(to=total_frame_cnt)
                #フレームの最大値を表示
                self.max_frame_label.config(text="最大フレーム: {}".format(total_frame_cnt) )

            else:
                self.avi_state_label.config(text="AVIファイルが壊れています", fg="red")
                
    # setPlayState: 再生ボタンを押したら、再生状態にセットする
    def setPlayState(self):
        self.frames_scale.config(state="disabled")   #scaleを操作不可能に変更
        self.frames_spinbox.config(state="disabled") #spinboxを操作不可能に変更
        
        if self.cap and not self.avi_play_state:
            self.avi_play_state = True
            self.update()
    
    # clearPlayState: 停止ボタンを押したら、停止状態にセットする
    def clearPlayState(self):
        self.avi_play_state = False
        self.frames_scale.config(state="normal")    #scaleを操作可能に変更
        self.frames_spinbox.config(state="normal")  #spinboxを操作可能に変更   
    
    # returnHead: 先頭フレームに戻る
    def returnHead(self):
        self.avi_play_state = False

        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.scale_var.set(0)
            ret, frame = self.cap.read()
            self.frames_scale.config(state="normal")   #scaleを操作不可能に変更
            self.frames_spinbox.config(state="normal") #spinboxを操作不可能に変更
            if ret:
                self.frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(
                    cv2.resize(self.frame_rgb, (self.movie_frame.winfo_width(), int(self.movie_frame.winfo_height() * 5 / 6)))
                )
                self.imgtk = ImageTk.PhotoImage(image=image)
                self.avi_frame_canvas.itemconfig(self.canvas_image, image=self.imgtk)
    
    # update: 動画の再生
    def update(self):
        if self.avi_play_state:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.scale_var.get())

            ret, frame = self.cap.read()
            if ret:
                self.frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(
                    cv2.resize(self.frame_rgb, (self.movie_frame.winfo_width(), int(self.movie_frame.winfo_height() * 5 / 6)))
                )
                self.imgtk = ImageTk.PhotoImage(image=image)
                self.avi_frame_canvas.itemconfig(self.canvas_image, image=self.imgtk)
                self.after(self.delay, self.update)
            else:
                self.clearPlayState()

            self.scale_var.set(int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)))


    # スピンボックスの値で動画を移動する
    def updateFrame(self):
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(self.scale_var.get()))
            ret, frame = self.cap.read()
            if ret:
                self.frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(
                    cv2.resize(self.frame_rgb, (self.movie_frame.winfo_width(), int(self.movie_frame.winfo_height() * 5 / 6)))
                )
                self.imgtk = ImageTk.PhotoImage(image=image)
                self.avi_frame_canvas.itemconfig(self.canvas_image, image=self.imgtk)