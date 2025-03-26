#视频录制类
import cv2
import time
import os
from threading import Thread
from Yolo4Detect import Yolo4Detect
import tkinter as tk
from tkinter import messagebox, filedialog

class VideoRecorder(tk.Toplevel):
    def __init__(self):
        self.deviceid = 0
        self.width = 640
        self.height = 480
        self.cap = cv2.VideoCapture(self.deviceid)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.fps = 30
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = None
        self.recording = False
        self.start_time = None
        self.timepoint = 60
        self.video_dir = 'videos'  # 视频文件存放目录
        self.frontalfacepath = r"C:\Python311\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml"

        # 如果没有 videos 文件夹，则创建
        if not os.path.exists(self.video_dir):
            os.makedirs(self.video_dir)

    def setfps(self,fps):
        self.fps=fps

    def getmyinfo(self):
        print("video_dir:",self.video_dir)
        print("frontalfacepath:",self.frontalfacepath)

    def cv2init(self):
        self.cap.release()
        self.cap = cv2.VideoCapture(self.deviceid)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def start_recording(self):
        if not self.cap.isOpened():
            self.cv2init()
        # 启动录制线程
        self.thread = Thread(target=self.record_video)
        self.thread.start()

    def stop_recording(self):
        self.recording = False
        if self.out:
            self.out.release()
            self.thread.join()#等待线程关闭结束
        messagebox.showinfo("停止录制", "视频已保存。")
        
    def setfenbianlv(self,width,height):
        # 关线程
        self.recording = False
        if self.out:
            self.out.release()
            self.cap.release()
            self.thread.join()#等待线程关闭结束
        # 切换分辨率
        self.width=width
        self.height=height
        self.cv2init()
        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # 如果实际分辨率与设置的分辨率相同，表示设备支持该分辨率
        if actual_width == width and actual_height == height:
            messagebox.showinfo("分辨率兼容", "切换成功！")
        else:
            messagebox.showinfo("分辨率不兼容", "切换回默认分辨率。")
            self.width=640
            self.height=480
            self.cv2init()
        
        self.thread = Thread(target=self.record_video)
        self.thread.start()

    def record_video(self):
        self.recording = True
        self.start_time = time.time()
        # 生成视频文件名
        video_path = os.path.join(self.video_dir,f"video_" + str(time.time()) + ".mp4")
        self.out = cv2.VideoWriter(video_path, self.fourcc, self.fps, (self.width, self.height))
        # 加载 Haar 分类器
        face_cascade = cv2.CascadeClassifier(self.frontalfacepath)
        # 初始化判断器
        yolodetector = Yolo4Detect()
        while self.recording:
            ret, frame = self.cap.read()
            if not ret:
                print("无法接收视频帧，退出")
                break
            # 转为灰度图像进行人脸检测
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 使用 detectMultiScale 方法检测人脸
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            # 在每个检测到的人脸上绘制矩形框
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #yolo4再检测一轮
            frame = yolodetector.detectbyyolo4(frame)
            # 每 X 秒切换一个新文件
            if time.time() - self.start_time >= self.timepoint:
                if self.out:
                    self.out.release()
                video_path = os.path.join(self.video_dir, f"video_" + str(time.time()) + ".mp4")
                self.out = cv2.VideoWriter(video_path, self.fourcc, self.fps, (self.width, self.height))
                self.start_time = time.time()
            # 记录视频
            self.out.write(frame)
            # 显示视频帧
            cv2.imshow('Camera', frame)
            cv2.waitKey(int(1000/self.fps))
        #self.cap.release()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    root = tk.Tk()
    recorder = VideoRecorder()  # 创建 VideoRecorder 实例
    recorder.getmyinfo()
    root.mainloop()
