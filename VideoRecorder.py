#视频录制类
import os
import cv2
import time
import threading

from Yolo4Detect import Yolo4Detect

import tkinter as tk
from tkinter import messagebox, filedialog

from threading import Thread


class VideoRecorder(tk.Toplevel):
    def __init__(self, root):
        self.deviceid = 0
        self.root = root
        self.width = 640
        self.height = 480
        self.cap = cv2.VideoCapture(self.deviceid)
        
        # 从 config.info 文件中读取路径配置
        self.load_config()
        
        # 设置视频捕获的宽高
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        self.fps = 30
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = None
        self.recording = False
        self.start_time = None

        # 如果没有视频存储目录，则创建
        if not os.path.exists(self.video_dir):
            os.makedirs(self.video_dir)

    def settimepoint(self,times):
        self.timepoint= times

    def load_config(self):
        """读取 config.info 文件并设置 video_dir 和 frontalfacepath"""
        try:
            with open('config.info', 'r') as file:
                for line in file:
                    # 查找配置项 path
                    if line.startswith("path="):
                        self.video_dir = line.strip().split('=')[1]
                    # 查找配置项 frontalfacepath
                    elif line.startswith("frontalface="):
                        self.frontalfacepath = line.strip().split('=')[1]
                    elif line.startswith("timepoint="):
                        self.timepoint = line.strip().split('=')[1]
        except Exception as e:
            print(f"读取 config.info 时发生错误: {e}")
            # 如果读取配置文件出错，使用默认目录和默认人脸分类器路径
            self.video_dir = 'videos'
            self.frontalface = "cvxml/haarcascade_frontalface_default.xml"
            self.timepoint = 60

        
    def set_video_dir(self,new_path):
        self.video_dir = new_path
    def setfps(self, fps):
        self.fps = fps

    def getmyinfo(self):
        print("video_dir:", self.video_dir)

    def cv2init(self):
        """重新初始化摄像头"""
        self.cap.release()
        self.cap = cv2.VideoCapture(self.deviceid)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def start_recording(self):
        """开始录制视频"""
        if not self.cap.isOpened():
            self.cv2init()
        self.thread = Thread(target=self.record_video)  # 启动录制线程
        self.thread.start()

    def stop_recording(self):
        """停止录制视频"""
        self.recording = False
        if self.out:
            self.out.release()
            self.thread.join()  # 等待线程关闭结束
        messagebox.showinfo("停止录制", "视频已保存。")

    def record_video(self):
        """视频录制线程函数"""
        self.recording = True
        self.start_time = time.time()
        video_path = os.path.join(self.video_dir, f"video_" + str(time.time()) + ".mp4")  # 生成视频文件名
        self.out = cv2.VideoWriter(video_path, self.fourcc, self.fps, (self.width, self.height))
        
        print(self.frontalfacepath)
        face_cascade = cv2.CascadeClassifier("cvxml/haarcascade_frontalface_default.xml")  # 加载 opencv-Haar 分类器
        yolodetector = Yolo4Detect()  # 初始化 yolov4 判断器
        
        while self.recording:
            ret, frame = self.cap.read()
            if not ret:
                print("无法接收视频帧，退出")
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转为灰度图像进行人脸检测
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            frame = yolodetector.detectbyyolo4(frame)  # yolo4再检测一轮
            
            # 每 X 秒切换一个新文件
            if time.time() - self.start_time >= int(self.timepoint):
                if self.out:
                    self.out.release()
                video_path = os.path.join(self.video_dir, f"video_" + str(time.time()) + ".mp4")
                self.out = cv2.VideoWriter(video_path, self.fourcc, self.fps, (self.width, self.height))
                self.start_time = time.time()
            
            self.out.write(frame)  # 记录视频
            cv2.imshow('Camera', frame)  # 显示视频帧
            cv2.waitKey(int(1000 / self.fps))
        
        cv2.destroyAllWindows()

    def setfenbianlv(self, width, height):
        """设置分辨率"""
        if self.recording:
            # 停止当前录制
            self.recording = False
            if self.out:
                self.out.release()
                #self.cap.release()
                self.thread.join()  # 等待线程关闭结束

            self.width = width
            self.height = height
            self.cv2init()
            # 检查是否支持该分辨率
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            if actual_width == width and actual_height == height:
                # 使用 after() 将消息框更新操作放到主线程
                self.root.after(100, self.show_resolution_message, "分辨率兼容", "切换成功！")
                #self.cv2init()  # 重新初始化摄像头
                self.thread = Thread(target=self.record_video)
                self.thread.start()
            else:
                self.root.after(100, self.show_resolution_message, "分辨率不兼容", "已切换回默认分辨率")
                self.width = 640
                self.height = 480
                self.cv2init()  # 切换回默认分辨率
                self.thread = Thread(target=self.record_video)
                self.thread.start()
        else:
            self.recording = False
            if self.out:
                self.out.release()
                self.cap.release()
                self.thread.join()
            self.width = width
            self.height = height
            self.cv2init()  # 重新初始化摄像头
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # 检查摄像头是否支持该分辨率
            if actual_width == width and actual_height == height:
                self.root.after(100, self.show_resolution_message, "分辨率兼容", "切换成功！")
                self.thread = Thread(target=self.record_video)
                self.thread.start()
            else:
                self.root.after(100, self.show_resolution_message, "分辨率不兼容", "切换回默认分辨率。")
                self.width = 640
                self.height = 480
                self.cv2init()  # 切换回默认分辨率
            


    def setfenbianlv_async(self, width, height):
        """异步设置分辨率"""
        threading.Thread(target=self.setfenbianlv, args=(width, height)).start()

    def show_resolution_message(self, title, message):
        """显示分辨率切换的提示信息"""
        messagebox.showinfo(title, message)


if __name__ == "__main__":
    root = tk.Tk()
    recorder = VideoRecorder(root)  # 创建 VideoRecorder 实例
    recorder.getmyinfo()
    root.mainloop()
