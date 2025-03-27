# 📹 摄像头检测系统

<div align="center">

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

一个基于 Python 的智能摄像头检测系统，集成了实时目标检测、视频录制和播放功能。

[开始使用](#快速开始) | [功能特性](#功能特性) | [安装说明](#安装说明) | [使用指南](#使用指南)

</div>

## 🌟 功能特性

- 🎥 实时摄像头画面显示
- 🔍 YOLOv4 目标检测
- ⏺️ 视频录制功能
- ▶️ 视频播放和浏览
- 💻 简洁的图形用户界面

## 🚀 快速开始

### 环境要求

- Python 3.7+
- OpenCV
- PyQt5
- NumPy
- Pillow

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/Anyuersuper/CameraDetect.git
cd CameraDetect
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 📖 使用指南

### 运行程序
```bash
python main.py
```

### 界面操作
- 🔘 点击"打开摄像头"按钮启动摄像头
- 🔘 使用"开始录制"按钮录制视频
- 🔘 使用"停止录制"按钮结束录制
- 🔘 使用"播放视频"按钮查看录制的视频

## 📁 项目结构

```
CameraDetect/
├── main.py              # 主程序入口
├── VideoRecorder.py     # 视频录制模块
├── VideoPlayer.py       # 视频播放模块
├── VideoBrowser.py      # 视频浏览模块
├── Yolo4Detect.py       # YOLOv4 目标检测模块
├── videos/              # 录制的视频存储目录
└── yolo/                # YOLOv4 模型文件目录
```

## 📸 界面展示

### 主界面
<div align="center">
<img src="https://github.com/user-attachments/assets/f21b1d75-81d7-479e-9ff4-b75a64f40418" alt="主界面" width="600"/>
</div>

### 目标检测效果
<div align="center">
<img src="https://github.com/user-attachments/assets/14a9866a-d362-402f-91a6-23294244d693" alt="识别效果" width="600"/>
</div>

### 读取本地视频
<div align="center">
<img src="https://github.com/user-attachments/assets/04ae31dd-1379-4d95-9d04-389955ee225b" alt="读取视频" width="600"/>
</div>

## ⚠️ 注意事项

- 首次运行前请确保已安装所有依赖包
- 确保摄像头设备可用
- 录制的视频将保存在 `videos` 目录下

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目！

## 📞 联系方式

如有问题或建议，请通过以下方式联系我们：
- 提交 [Issue](https://github.com/Anyuersuper/CameraDetect/issues)
- 发送邮件至：[your-email@example.com]

---

<div align="center">
如果这个项目对您有帮助，请考虑给它一个 ⭐️
</div> 