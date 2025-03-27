# **基于 OpenCV 和 YOLOv4 的目标检测与视频录制系统**

## **项目简介**
本项目实现了以下功能：
- **人脸检测**：使用 OpenCV 进行面部检测。
- **目标检测**：利用 YOLOv4 进行车辆和行人检测。
- **GUI 设计**：基于 Tkinter 进行界面开发。
- **视频处理**：
  - 录制视频，并支持分辨率和帧率的动态切换。
  - 播放本地保存的视频，并可调节分辨率和帧率。

---

## **界面预览**
### **主界面**
![主界面](https://github.com/user-attachments/assets/6483c651-c072-4fac-9ad4-ad7ec83b80c8)

### **目标检测效果**
![识别效果](https://github.com/user-attachments/assets/14a9866a-d362-402f-91a6-23294244d693)

### **读取本地视频**
![读取视频](https://github.com/user-attachments/assets/04ae31dd-1379-4d95-9d04-389955ee225b)

---

## **依赖安装**
请先安装所需依赖：
```bash
pip install opencv-python numpy pillow tkinter
```

---

## **核心代码**

### **1. 导入库**
```python
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
```

---

### **2. GUI 设计**
```python
class VideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("目标检测与视频处理系统")
        
        # 创建视频显示区域
        self.video_label = tk.Label(root)
        self.video_label.pack()
        
        # 选择视频按钮
        self.btn_open = tk.Button(root, text="打开视频", command=self.open_video)
        self.btn_open.pack()

        # 录制按钮
        self.btn_record = tk.Button(root, text="开始录制", command=self.start_recording)
        self.btn_record.pack()

        # 停止按钮
        self.btn_stop = tk.Button(root, text="停止录制", command=self.stop_recording)
        self.btn_stop.pack()

        self.cap = None
        self.recording = False

    def open_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
        if file_path:
            self.cap = cv2.VideoCapture(file_path)
            self.play_video()

    def play_video(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img_tk = ImageTk.PhotoImage(img)
                self.video_label.imgtk = img_tk
                self.video_label.config(image=img_tk)
                self.root.after(30, self.play_video)

    def start_recording(self):
        self.recording = True
        self.video_writer = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"XVID"), 20, (640, 480))

    def stop_recording(self):
        self.recording = False
        if hasattr(self, "video_writer"):
            self.video_writer.release()
```

---

### **3. 人脸检测（OpenCV）**
```python
def detect_faces(frame):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    return frame
```

---

### **4. 目标检测（YOLOv4）**
```python
def load_yolo():
    net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return net, output_layers

def detect_objects(frame, net, output_layers):
    height, width = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x, center_y, w, h = (
                    int(detection[0] * width),
                    int(detection[1] * height),
                    int(detection[2] * width),
                    int(detection[3] * height),
                )
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    for i in indices:
        x, y, w, h = boxes[i]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return frame
```

---

### **5. 运行程序**
```python
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root)
    root.mainloop()
```

---

## **总结**
本项目利用 OpenCV 进行人脸检测，使用 YOLOv4 进行目标检测，并结合 Tkinter 开发了 GUI 进行视频处理，包括视频录制、回放及参数调整。你可以根据需求进行优化，比如增加更多检测功能、支持不同格式的视频等。

### **未来优化方向**
- **支持多线程，提高视频播放流畅度**
- **更换更高效的目标检测模型（如 YOLOv8）**
- **增强 GUI 交互性，支持更多参数调整**

如果你对本项目有任何建议，欢迎讨论和优化！🚀
