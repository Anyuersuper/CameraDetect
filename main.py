import cv2
import time
import os
import subprocess  
import numpy as np

from Yolo4Detect import Yolo4Detect
from VideoBrowser import VideoBrowser
from VideoRecorder import VideoRecorder
from VideoPlayer import VideoPlayer

import tkinter as tk
from tkinter import messagebox, filedialog ,simpledialog
from threading import Thread


# 创建 Tkinter 窗口
class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AI摄像头")
        self.geometry("300x350")
        
        # 创建 VideoRecorder 实例
        self.recorder = VideoRecorder(self)

        # 存储路径变量
        self.storage_path = self.recorder.video_dir  # 直接从 recorder 获取 video_dir
        self.timepoint = self.recorder.timepoint
        
        # 开始录制按钮
        self.start_button = tk.Button(self, text="开始检测", command=self.start_recording)
        self.start_button.pack(pady=10)

        # 停止录制按钮
        self.stop_button = tk.Button(self, text="停止检测", command=self.stop_recording)
        self.stop_button.pack(pady=10)
        self.stop_button.config(state=tk.DISABLED)

        # 查看本地视频按钮
        self.view_button = tk.Button(self, text="查看本地视频", command=self.view_local_videos)
        self.view_button.pack(pady=10)
        
        # 绑定关闭窗口事件
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 时间间隔设置
        self.timepointgrid = tk.Frame(self, width=300 ,height= 100)
        self.timepointgrid.pack(pady=10)  
        tk.Label(self.timepointgrid, text="存储间隔(s):").grid(row=0, column=0)
        self.showtimepoint = tk.Label(self.timepointgrid, width=2,text=self.timepoint, justify="right")  
        self.showtimepoint.grid(row=0, column=1)
        self.changetimepoint = tk.Button(self.timepointgrid, text="...", width=3, command = self.change_timepoint)
        self.changetimepoint.grid(row=0, column=2, padx=5)
        
        # 存储路径布局
        self.savapathgrid = tk.Frame(self, width=300)
        self.savapathgrid.pack(pady=10)
        tk.Label(self.savapathgrid, text="存储路径:").grid(row=0, column=0)
        self.path_label = tk.Label(self.savapathgrid, width=20,text=self.storage_path, justify="right")  # 直接显示路径
        self.path_label.grid(row=0, column=1)
        # 选择路径的按钮
        self.browse_button = tk.Button(self.savapathgrid, text="...", width=3, command=self.changesavepath)
        self.browse_button.grid(row=0, column=2, padx=5)

        # 分辨率布局
        self.fenbianlvgrid = tk.Frame(self, width=300, height=100)
        self.fenbianlvgrid.pack(pady=10) 
        tk.Label(self.fenbianlvgrid, text="分辨率:").grid(row=0, column=0)
        self.p480 = tk.Button(self.fenbianlvgrid, text="480p", width=5, command=self.p480)
        self.p480.grid(row=0, column=1)
        self.p720 = tk.Button(self.fenbianlvgrid, text="720p", width=5, command=self.p720)
        self.p720.grid(row=0, column=2)
        self.p1080 = tk.Button(self.fenbianlvgrid, text="1080p", width=5, command=self.p1080)
        self.p1080.grid(row=0, column=3)
        
        # 帧率控制布局
        self.zhenlvgrid = tk.Frame(self, width=300 ,height= 100)
        self.zhenlvgrid.pack(pady=10)  
        # 帧率切换
        tk.Label(self.zhenlvgrid, text="帧率:").grid(row=0, column=0)
        self.zhen1 = tk.Button(self.zhenlvgrid, text="1", width=5, command=self.fps1)
        self.zhen1.grid(row=0, column=1)
        self.zhen5 = tk.Button(self.zhenlvgrid, text="5", width=5, command=self.fps5)
        self.zhen5.grid(row=0, column=2)
        self.zhen15 = tk.Button(self.zhenlvgrid, text="15", width=5, command=self.fps15)
        self.zhen15.grid(row=0, column=3)
        self.zhen30 = tk.Button(self.zhenlvgrid, text="30", width=5, command=self.fps30)
        self.zhen30.grid(row=0, column=4)
        self.zhen60 = tk.Button(self.zhenlvgrid, text="60", width=5, command=self.fps60)
        self.zhen60.grid(row=0, column=5)


    # Application 类中的分辨率按钮回调函数
    def p480(self):
        self.recorder.setfenbianlv_async(640, 480)  # 异步切换分辨率
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def p720(self):
        self.recorder.setfenbianlv_async(1280, 720)  # 异步切换分辨率
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def p1080(self):
        self.recorder.setfenbianlv_async(1920, 1080)  # 异步切换分辨率
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def fps1(self):
        self.recorder.setfps(1)
    def fps5(self):
        self.recorder.setfps(5)
    def fps15(self):
        self.recorder.setfps(15)
    def fps30(self):
        self.recorder.setfps(30)
    def fps60(self):
        self.recorder.setfps(60)
    
    def changesavepath(self):
        """更新存储路径"""
        # 打开文件对话框选择新路径
        new_path = filedialog.askdirectory(initialdir=self.storage_path, title="选择存储路径")

        if new_path:
            # 更新 VideoRecorder 的 video_dir 属性
            self.recorder.set_video_dir(new_path)

            # 更新界面显示的路径
            self.storage_path = new_path
            self.path_label.config(text=self.storage_path)

            # 读取并修改 config.info 文件中的路径
            with open("config.info", "r") as config_file:
                lines = config_file.readlines()

            # 找到并修改 path 行
            with open("config.info", "w") as config_file:
                for line in lines:
                    if line.startswith('path='):
                        config_file.write(f'path={new_path}\n')
                    else:
                        config_file.write(line)
                        
    def change_timepoint(self):
        # 弹出输入框让用户输入新的时间间隔
        new_timepoint = simpledialog.askinteger("输入新的时间间隔", "请输入新的时间间隔（秒）:", parent=self)
        if new_timepoint:
            # 更新 VideoRecorder 的 video_dir 属性
            self.recorder.settimepoint(new_timepoint)

            # 更新界面显示的路径
            self.timepoint = new_timepoint
            self.showtimepoint.config(text=self.timepoint)

            # 读取并修改 config.info 文件中的路径
            with open("config.info", "r") as config_file:
                lines = config_file.readlines()

            # 找到并修改 path 行
            with open("config.info", "w") as config_file:
                for line in lines:
                    if line.startswith('timepoint='):
                        config_file.write(f'timepoint={new_timepoint}\n')
                    else:
                        config_file.write(line)
        

    
    def start_recording(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.recorder.start_recording()

    def stop_recording(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.recorder.stop_recording()

    def view_local_videos(self):
        """打开本地视频浏览器"""
        VideoBrowser(self.recorder.video_dir)
        
    def on_closing(self):
        """当点击窗口右上角关闭按钮时释放摄像头资源"""
        self.recorder.cap.release()  # 释放摄像头
        self.destroy()  # 关闭窗口

# 启动 Tkinter 应用
if __name__ == "__main__":
    app = Application()
    app.mainloop()



