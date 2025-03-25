#Yolo4检测类
import cv2
import os
import numpy as np


class Yolo4Detect:
    def __init__(self):
        self.yolo_cfg = "yolo/yolov4.cfg"
        self.yolo_weights = "yolo/yolov4.weights"
        self.yolo_classes = "yolo/coco.names"
        
        # 读取类别名称
        with open(self.yolo_classes, "r") as f:
            self.class_names = f.read().strip().split("\n")
        
        # 只检测车辆相关类别（COCO 数据集 ID）
        self.vehicle_classes = ["car", "bus", "truck", "motorbike","person"]
        
        # 加载 YOLO
        self.net = cv2.dnn.readNet(self.yolo_weights, self.yolo_cfg)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)  # 使用 OpenCV DNN 加速
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)  # 运行在 CPU（可修改为 DNN_TARGET_CUDA 以使用 GPU）
        
        # 获取 YOLO 的输出层
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
    
    def detectbyyolo4(self, image, conf_threshold=0.5, nms_threshold=0.4, show_result=False, save_result=False, save_path="detected_image.jpg"):
        """
        进行车辆检测
        :param image: 可以是图片路径(str) 或 OpenCV 读取的 numpy 数组
        """
        # 如果传入的是路径，则读取图片
        if isinstance(image, str):
            image = cv2.imread(image)
            if image is None:
                print(f"无法读取图片: {image_path}")
                return None

        height, width = image.shape[:2]

        # YOLO 需要 416x416 或 608x608 输入
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)

        # 前向传播
        outputs = self.net.forward(self.output_layers)

        # 解析检测结果
        boxes, confidences, class_ids = [], [], []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                # 只检测车辆类别，并设定置信度阈值
                if self.class_names[class_id] in self.vehicle_classes and confidence > conf_threshold:
                    center_x, center_y, w, h = (detection[:4] * [width, height, width, height]).astype("int")

                    # 计算矩形框的左上角坐标
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # NMS 去重
        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = boxes[i]
                label = f"{self.class_names[class_ids[i]]}: {confidences[i]:.2f}"
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            yuer = 1
            #print("没有检测到任何目标！")

        # 显示或保存检测结果
        if show_result:
            cv2.imshow("Vehicle Detection", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        if save_result:
            cv2.imwrite(save_path, image)
            print(f"检测结果已保存到 {save_path}")

        return image

    
if __name__ == "__main__": 
    yolodetector = Yolo4Detect()
    yolodetector.detectbyyolo4("11.png",show_result=True)
    





