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

## **使用方法**
1. 运行 GUI 界面：
   ```bash
   python main.py
   ```
2. 在 GUI 中：
   - 选择本地视频进行播放
   - 进行目标检测
   - 录制视频并调整参数

---

## **未来优化方向**
- **支持多线程，提高视频播放流畅度**
- **更换更高效的目标检测模型（如 YOLOv8）**
- **增强 GUI 交互性，支持更多参数调整**

如果你对本项目有任何建议，欢迎讨论和优化！🚀
