# 基于 OpenCV 和 YOLOv4 的目标检测与视频录制系统

## 项目简介
本项目实现了以下功能：

- 人脸检测：使用 OpenCV 进行面部检测。
- 目标检测：利用 YOLOv4 进行车辆和行人检测。
- GUI 设计：基于 Tkinter 进行界面开发。
- 视频处理：
  - 录制视频，并支持分辨率和帧率的动态切换。
  - 播放本地保存的视频，并可调节分辨率和帧率。
  - 定时保存视频：录制过程中支持定时自动保存当前视频文件，便于避免丢失数据。

---

## 使用教程：
1. 克隆项目：
   ```bash
   git clone https://github.com/Anyuersuper/CameraDetect
   ```
   
3. 安装依赖：

   ```bash
   pip install opencv-python
   pip install -r requirements.txt
   ```

4. 运行程序：

   ```bash
   python main.py
   ```

## 界面预览

### 主界面
![主界面](https://github.com/user-attachments/assets/6483c651-c072-4fac-9ad4-ad7ec83b80c8)

### 目标检测效果
![识别效果](https://github.com/user-attachments/assets/14a9866a-d362-402f-91a6-23294244d693)

### 读取本地视频
![读取视频](https://github.com/user-attachments/assets/04ae31dd-1379-4d95-9d04-389955ee225b)

---

## 总结
本项目利用 OpenCV 进行人脸检测，使用 YOLOv4 进行目标检测，并结合 Tkinter 开发了 GUI 进行视频处理，包括视频录制、回放及参数调整。你可以根据需求进行优化，比如增加更多检测功能、支持不同格式的视频等。

---


