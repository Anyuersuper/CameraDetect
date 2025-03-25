#视频播放类
import cv2
import tkinter as tk
from PIL import Image, ImageTk

class VideoPlayer(tk.Toplevel):
    def __init__(self, video_source):
        super().__init__()

        self.title("查看视频")
        self.state("zoomed")
        # 视频源
        self.video_source = video_source
        self.vid = cv2.VideoCapture(video_source)

        if not self.vid.isOpened():
            print("无法打开视频文件:", video_source)
            self.destroy()
            return

        # 获取视频的基本信息
        self.frame_count = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.vid.get(cv2.CAP_PROP_FPS))
        self.original_width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.original_height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 默认分辨率（初始化时设为原始分辨率）
        self.width = self.original_width
        self.height = self.original_height

        # 获取屏幕的最大尺寸
        self.max_width = self.winfo_screenwidth()
        self.max_height = self.winfo_screenheight() - 150

        # 限制视频画布的大小
        self.width = min(self.width, self.max_width)
        self.height = min(self.height, self.max_height)

        # 创建 Tkinter 画布
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        # 创建控制按钮
        self.create_controls()

        # 进度条
        self.progress = tk.Scale(self, from_=0, to=self.frame_count, orient=tk.HORIZONTAL, length=500, command=self.set_position)
        self.progress.pack(fill=tk.X)

        # 绑定窗口关闭事件
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # 开始播放
        self.update()

    def create_controls(self):
        """ 创建播放控制按钮 """
        control_frame = tk.Frame(self)
        control_frame.pack()

        # 帧率切换
        tk.Label(control_frame, text="选择帧率:").pack(side=tk.LEFT)
        for fps in [1,5, 10, 15, 30, 60]:
            tk.Button(control_frame, text=f"{fps}帧", width=5, command=lambda f=fps: self.set_fps(f)).pack(side=tk.LEFT)

        # 快进 & 回退
        tk.Button(control_frame, text="回退5秒", command=self.jump_backward).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="快进5秒", command=self.jump_forward).pack(side=tk.LEFT, padx=5)

        # 播放/暂停
        self.pause_button = tk.Button(control_frame, text="⏸ 暂停", command=self.toggle_pause)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        # 分辨率切换
        tk.Label(control_frame, text="分辨率:").pack(side=tk.LEFT)
        tk.Button(control_frame, text="480p", command=lambda: self.set_resolution(854, 480)).pack(side=tk.LEFT)
        tk.Button(control_frame, text="720p", command=lambda: self.set_resolution(1280, 720)).pack(side=tk.LEFT)
        tk.Button(control_frame, text="1080p", command=lambda: self.set_resolution(1920, 1080)).pack(side=tk.LEFT)
        tk.Button(control_frame, text="原始", command=lambda: self.set_resolution(self.original_width, self.original_height)).pack(side=tk.LEFT)

    def update(self):
        """ 更新视频帧 """
        if not hasattr(self, "is_paused") or not self.is_paused:
            ret, frame = self.vid.read()
            if ret:
                self.current_frame = int(self.vid.get(cv2.CAP_PROP_POS_FRAMES))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # 根据当前分辨率调整缩放比例
                frame = cv2.resize(frame, (self.width, self.height))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
                self.canvas.imgtk = imgtk

                # 更新进度条
                self.progress.set(self.current_frame)

        self.after(int(1000 / self.fps), self.update)

    def set_fps(self, fps):
        """ 设置帧率 """
        self.fps = fps

    def set_position(self, val):
        """ 拖动进度条时调整视频位置 """
        frame_number = int(val)
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        self.current_frame = frame_number

        # 让视频画面立即更新
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.width, self.height))
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.imgtk = imgtk

    def jump_forward(self):
        """ 快进 5 秒 """
        target_frame = min(self.current_frame + self.fps * 5, self.frame_count - 1)
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        self.current_frame = target_frame

        # 同步进度条 & 立即更新画面
        self.progress.set(target_frame)
        self.update()

    def jump_backward(self):
        """ 回退 5 秒 """
        target_frame = max(self.current_frame - self.fps * 5, 0)
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        self.current_frame = target_frame

        # 同步进度条 & 立即更新画面
        self.progress.set(target_frame)
        self.update()

    def toggle_pause(self):
        """ 播放/暂停切换 """
        self.is_paused = not getattr(self, "is_paused", False)
        if self.is_paused:
            self.pause_button.config(text="▶️ 播放")
        else:
            self.pause_button.config(text="⏸ 暂停")

    def set_resolution(self, width, height):
        """ 设置分辨率，确保不超过屏幕最大尺寸 """
        self.width, self.height = min(width, self.max_width), min(height, self.max_height)
        self.canvas.config(width=self.width, height=self.height)

    def on_close(self):
        """ 释放资源并关闭窗口 """
        if self.vid.isOpened():
            self.vid.release()
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('200x100')
    video_path = 'videodemo.mp4'
    player = VideoPlayer(video_path)
    root.mainloop()




