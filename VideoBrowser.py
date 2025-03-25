#浏览本地视频类
import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from VideoPlayer import VideoPlayer


class VideoBrowser(tk.Toplevel):
    def __init__(self, video_dir):
        super().__init__()

        self.title("本地视频浏览器")
        self.geometry("400x300")
        self.video_dir = video_dir

        # 列表框
        self.listbox = tk.Listbox(self, width=50, height=15)
        self.listbox.pack(pady=10)

        # 绑定双击事件
        self.listbox.bind("<Double-Button-1>", self.open_selected_file)

        # 加载视频列表
        self.load_videos()

    def load_videos(self):
        """加载 videos 目录下的所有 .mp4 文件"""
        if not os.path.isdir(self.video_dir):
            messagebox.showerror("错误", "视频目录不存在！")
            return
        
        mp4_files = [f for f in os.listdir(self.video_dir) if f.endswith('.mp4')]
        self.listbox.delete(0, tk.END)  # 清空列表
        for file in mp4_files:
            self.listbox.insert(tk.END, file)

    def open_selected_file(self, event):
        """双击打开选中的 MP4 文件"""
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_file = self.listbox.get(selected_index)  # 获取选中的文件名
            file_path = os.path.join(self.video_dir, selected_file)  # 构造完整路径
            vp = VideoPlayer(file_path)
        else:
            messagebox.showerror("错误", "文件不存在！")

# 确保 main 函数启动
if __name__ == "__main__":
    # 指定视频目录路径
    video_dir = "videos"  # 修改为实际视频文件夹路径
    root = tk.Tk()  # 创建主窗口
    video_browser = VideoBrowser(video_dir)  # 创建 VideoBrowser 实例
    root.mainloop()  # 启动主事件循环





