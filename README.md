# 摄像头检测系统

这是一个基于 Python 的摄像头检测系统，使用 OpenCV 和 YOLOv4 进行实时目标检测，并提供视频录制和播放功能。

## 功能特性

- 实时摄像头画面显示
- YOLOv4 目标检测
- 视频录制功能
- 视频播放和浏览
- 简洁的图形用户界面

## 环境要求

- Python 3.7+
- OpenCV
- PyQt5
- NumPy
- Pillow

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/你的用户名/CameraDetect.git
cd CameraDetect
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 运行主程序：
```bash
python main.py
```

2. 使用界面功能：
   - 点击"打开摄像头"按钮启动摄像头
   - 使用"开始录制"按钮录制视频
   - 使用"停止录制"按钮结束录制
   - 使用"播放视频"按钮查看录制的视频

## 项目结构

- `main.py`: 主程序入口
- `VideoRecorder.py`: 视频录制模块
- `VideoPlayer.py`: 视频播放模块
- `VideoBrowser.py`: 视频浏览模块
- `Yolo4Detect.py`: YOLOv4 目标检测模块
- `videos/`: 录制的视频存储目录
- `yolo/`: YOLOv4 模型文件目录

## 注意事项

- 首次运行前请确保已安装所有依赖包
- 确保摄像头设备可用
- 录制的视频将保存在 `videos` 目录下

## 许可证

MIT License

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目。

## 联系方式

如有问题或建议，请通过 Issue 与我们联系。 
