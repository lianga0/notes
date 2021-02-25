如何评价rcnn、fast-rcnn和faster-rcnn这一系列方法？

> https://www.zhihu.com/question/35887527

## taokongcn​

> 深度学习（Deep Learning）话题下的优秀答主

提到这两个工作，不得不提到RBG大神[rbg's home page](http://www.rossgirshick.info/)，该大神在读博士的时候就因为dpm获得过pascal voc 的终身成就奖。博士后期间更是不断发力，RCNN和Fast-RCNN就是他的典型作品。

RCNN：RCNN可以看作是RegionProposal+CNN这一框架的开山之作，在imgenet/voc/mscoco上基本上所有top的方法都是这个框架，可见其影响之大。RCNN的主要缺点是重复计算，后来MSRA的kaiming组的SPPNET做了相应的加速。

Fast-RCNN：RCNN的加速版本，在我看来，这不仅仅是一个加速版本，其优点还包括：
(a) 首先，它提供了在caffe的框架下，如何定义自己的层/参数/结构的范例，这个范例的一个重要的应用是python layer的应用，我在这里[支持多label的caffe，有比较好的实现吗？ - 孔涛的回答](https://www.zhihu.com/question/36847520/answer/72824645)也提到了。
(2) training and testing end-to-end 这一点很重要，为了达到这一点其定义了ROIPooling层，因为有了这个，使得训练效果提升不少。
(3) 速度上的提升，因为有了Fast-RCNN，这种基于CNN的 real-time 的目标检测方法看到了希望，在工程上的实践也有了可能，后续也出现了诸如Faster-RCNN/YOLO等相关工作。

这个领域的脉络是：RCNN -> SPPNET -> Fast-RCNN -> Faster-RCNN。关于具体的细节，建议题主还是阅读相关文献吧。

这使我看到了目标检测领域的希望。起码有这么一部分人，他们不仅仅是为了几个百分点的提升，而是切实踏实在做贡献，相信不久这个领域会有新的工作出来。

以上纯属个人观点，欢迎批评指正。

参考：
[1] R-CNN: Girshick R, Donahue J, Darrell T, et al. Rich feature hierarchies for accurate object detection and semantic segmentation[C], CVPR, 2014.
[2] SPPNET: He K, Zhang X, Ren S, et al. Spatial pyramid pooling in deep convolutional networks for visual recognition[C], ECCV, 2014.
[3] Fast-RCNN: Girshick R. Fast R-CNN[C]. ICCV, 2015.
[4] Fater-RCNN: Ren S, He K, Girshick R, et al. Faster r-cnn: Towards real-time object detection with region proposal networks[C]. NIPS, 2015.
[5] YOLO: Redmon J, Divvala S, Girshick R, et al. You Only Look Once: Unified, Real-Time Object Detection[J]. arXiv preprint arXiv:1506.02640, 2015.



## 大雄的机器梦

在个人知乎专栏里写了一个系列：

• [RCNN-将CNN引入目标检测的开山之作](https://zhuanlan.zhihu.com/p/23006190?refer=xiaoleimlnote)

• [SPPNet-引入空间金字塔池化改进RCNN](https://zhuanlan.zhihu.com/p/24774302?refer=xiaoleimlnote)

• [Fast R-CNN](https://zhuanlan.zhihu.com/p/24780395?refer=xiaoleimlnote)

• [Faster R-CNN](https://zhuanlan.zhihu.com/p/24916786?refer=xiaoleimlnote)

• [图解YOLO](https://zhuanlan.zhihu.com/p/25167153?refer=xiaoleimlnote)

• [SSD](https://zhuanlan.zhihu.com/p/24954433?refer=xiaoleimlnote)

• [YOLO2](https://zhuanlan.zhihu.com/p/25167153?refer=xiaoleimlnote)


[晓雷机器学习笔记](https://zhuanlan.zhihu.com/xiaoleimlnote)
