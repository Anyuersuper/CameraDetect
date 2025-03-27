# AI摄像头系统

<div align="center">
  <img src="https://img.shields.io/badge/python-3.11-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/opencv-4.5.5-green.svg" alt="OpenCV Version">
  <img src="https://img.shields.io/badge/PyQt5-5.15.9-orange.svg" alt="PyQt5 Version">
</div>

## 📝 项目简介

AI摄像头系统是一个基于Python开发的智能视频监控系统，集成了实时视频录制、目标检测和视频播放等功能。系统采用PyQt5构建图形界面，使用OpenCV进行视频处理，并集成了YOLOv4目标检测模型，支持人脸和车辆等多种目标的实时检测。

## ✨ 主要功能

- 🎥 实时视频录制
  - 支持多种分辨率（480p/720p/1080p）
  - 可配置录制时间间隔
  - 自动分段存储

- 🔍 智能目标检测
  - 人脸检测
  - 车辆检测
  - 实时检测框显示

- 📺 视频播放
  - 支持多种播放分辨率
  - 可调节播放帧率
  - 进度条控制
  - 快进/后退功能

- ⚙️ 系统配置
  - 存储路径设置
  - 录制参数配置
  - 检测参数调整

## 🚀 快速开始

### 环境要求

- Python 3.11
- OpenCV 4.5.5
- PyQt5 5.15.9
- NumPy 1.21.6
- Pillow 11.1.0

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/yourusername/AI摄像头系统.git
cd AI摄像头系统
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行程序
```bash
python main.py
```

## 📋 使用说明

### 视频录制

1. 点击"开始检测"按钮开始录制
2. 选择所需的分辨率（480p/720p/1080p）
3. 点击"停止检测"按钮结束录制

### 目标检测

1. 在录制过程中，系统会自动进行目标检测
2. 检测结果会实时显示在视频画面中
3. 支持人脸和车辆等多种目标的检测

### 视频播放

1. 在视频列表中选择要播放的视频
2. 使用播放控制按钮控制播放
3. 可以调整播放分辨率和帧率

## 📁 项目结构

```
AI摄像头系统/
├── main.py              # 主程序入口
├── VideoRecorder.py     # 视频录制模块
├── VideoPlayer.py       # 视频播放模块
├── Yolo4Detect.py       # 目标检测模块
├── config.info          # 配置文件
├── requirements.txt     # 项目依赖
└── README.md           # 项目说明文档
```

## 🔧 配置说明

系统配置文件 `config.info` 包含以下设置：

- 存储路径
- 录制时间间隔
- 检测参数
- 播放参数

## 📝 测试报告

系统已通过完整的测试验证，包括：

- 基础功能测试
- 目标检测测试
- 视频播放测试
- 异常处理测试
- 性能测试

详细测试报告请参考 `AI摄像头系统测试报告.docx`。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👥 作者

- 作者：[您的名字]
- 邮箱：[您的邮箱]

## 🙏 致谢

感谢所有为本项目提供帮助和建议的贡献者。

---

## 基于 OpenCV 和 YOLOv4 的目标检测与视频录制系统

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


