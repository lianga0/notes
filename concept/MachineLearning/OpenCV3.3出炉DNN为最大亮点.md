## OpenCV3.3出炉，DNN(深层神经网络)为最大亮点

> 冰不语

> 2017-08-06

OpenCV3.3在8月3号正式出炉，想要体验最新特性的朋友可以去官网下载了，反正配置一下只需要几分钟。这次最主要的更新就是，终于把深度学习模块DNN从contrib里面提到主仓库里面，放到了官方发布版中。虽然我配置的一直是OpenCV with contrib，但是对于DNN模块，限于电脑配置太低，一直没有怎么尝试。这次可以借着新版发布抽空尝试一下了。

按照官方介绍，DNN现在有下面几点特性：

### 无需任何依赖

新加入的DNN模块不需要任何依赖，除了protobuf……而protobuf被加入到OpenCV的thirdparty了。简直是贴心至极有没有？

### 支持以下框架

Caffe 1
TensorFlow
Torch/PyTorch

虽然还没有支持caffe2，不过我现在就已经很满足了。

### 支持很多种类的层

AbsVal
AveragePooling
BatchNormalization
Concatenation
Convolution (including dilated convolution)
Crop
Deconvolution, a.k.a. transposed convolution or full convolution
DetectionOutput (SSD-specific layer)
Dropout
Eltwise (+, *, max)
Flatten
FullyConnected
……

还有很多，就不一一列举了， 估计绝大部分人也用不上。。。

### 以下网络经过了测试且可用

AlexNet
GoogLeNet v1 (also referred to as Inception-5h)
ResNet-34/50/…
SqueezeNet v1.1
VGG-based FCN (semantical segmentation network)
ENet (lightweight semantical segmentation network)
VGG-based SSD (object detection network)
MobileNet-based SSD (light-weight object detection network)

但是现在OpenCV貌似只能加载训练好的网络，caffe的，TF的，Torch的，只能训练好之后拿来用，但是不能自己训练网络。

现在看来加入DNN模块算是众望所归，虽然有点晚，虽然功能还不够完善，但是仍然值得期待。
