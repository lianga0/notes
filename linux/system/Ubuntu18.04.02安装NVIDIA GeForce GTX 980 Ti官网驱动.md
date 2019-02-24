## Ubuntu18.04.02安装NVIDIA GeForce GTX 980 Ti官网驱动

> 2019.02.24

在一台配有GeForce GTX 980 Ti的PC上安装最新的`Ubuntu18.04.02`镜像后，`sudo update-initramfs -u`命令会产生如下警告信息：

```
update-initramfs: Generating /boot/initrd.img-4.18.0-15-generic
W: Possible missing firmware /lib/firmware/nvidia/gv100/sec2/sig.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/sec2/image.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/sec2/desc.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/nvdec/scrubber.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/gr/sw_method_init.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/gr/sw_bundle_init.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/gr/sw_nonctx.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/gr/sw_ctx.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/gr/gpccs_sig.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/gr/gpccs_data.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/gr/gpccs_inst.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/gr/gpccs_bl.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/gr/fecs_sig.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/gr/fecs_data.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/gr/fecs_inst.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/gr/fecs_bl.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/acr/ucode_unload.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/acr/ucode_load.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/acr/unload_bl.bin for module nouveau
W: Possible missing firmware /lib/firmware/nvidia/gv100/acr/bl.bin for module nouveau
```

看起来是和显卡驱动相关的模块存在些问题，Google查询`nouveau`发现，它是为nVidia显卡提供驱动的一个开源项目。

### [Nouveau: Accelerated Open Source driver for nVidia cards](https://nouveau.freedesktop.org/wiki/)

The nouveau project aims to build high-quality, free/libre software drivers for nVidia cards. Nouveau is composed of a Linux kernel KMS driver (nouveau), Gallium3D drivers in Mesa, and the Xorg DDX (xf86-video-nouveau). The kernel components have also been ported to NetBSD.

不过，既然nouveau看起来有点问题，那么我们就来安装下NVIDIA官网提供的GeForce GTX 980 Ti驱动。从NVIDIA官网发现，GeForce系列最新驱动[LINUX X64 (AMD64/EM64T) DISPLAY DRIVER](https://www.nvidia.com/Download/driverResults.aspx/142958/en-us)版本为418.43，发布时间为 2019.2.22。

下载完成后，发现是`.run`文件，可以直接执行进行驱动的安装。不过，要在Ubuntu上安装NVIDIA官网的驱动，首先需要在Ubuntu中禁用nouveau。

### 在Ubuntu 18.04中禁用Nouveau nvidia驱动

1. Blacklist Nvidia nouveau driver

将nouveau放入组件黑名单中（在黑名单文件末尾加入并保存）：

```
$ sudo bash -c "echo blacklist nouveau > /etc/modprobe.d/blacklist-nvidia-nouveau.conf"
$ sudo bash -c "echo options nouveau modeset=0 >> /etc/modprobe.d/blacklist-nvidia-nouveau.conf"
```

执行成功后，核对文件配置是否如下：

```
$ cat /etc/modprobe.d/blacklist-nvidia-nouveau.conf
blacklist nouveau
options nouveau modeset=0
```

2. Update kernel initramfs

使用命令`sudo update-initramfs -u`来重新生成initramfs。

3. sudo reboot

重启系统，即可完成禁用Nouveau nvidia驱动。重启后执行如下命令，没有输出即为屏蔽好了。

```
lsmod | grep nouveau
```


### 安装NVIDIA官网.run文件

若之前安装过显卡驱动，需要先卸载掉。建议装驱动前都执行以下该指令，有益无害。该指令能卸载驱动并不保留配置文件。

```
sudo apt-get --purge remove nvidia-*
```

使用下面命令安装必要的编译工具，因为.run文件会依赖一些常用的开发工具。

```
sudo apt install build-essential
```

使用如下命令安装NVIDIA驱动，根据提示信息，选择正确的选项即可安装成功。最后，重启系统即可。

```
sudo chmod a+x NVIDIA-Linux-x86_64-410.93.run

sudo ./NVIDIA-Linux-x86_64-410.93.run
```


### 查看显卡驱动版本

可以通过`nvidia-smi`命令查看GPU和驱动程序信息，若出现以下结果，则表明驱动程序安装成功。

```
nvidia-smi 
Sun Feb 24 18:08:23 2019       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 410.93       Driver Version: 410.93       CUDA Version: 10.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce GTX 980 Ti  Off  | 00000000:02:00.0  On |                  N/A |
| 20%   34C    P8    16W / 260W |     99MiB /  6080MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|    0      1285      G   /usr/lib/xorg/Xorg                            35MiB |
|    0      1314      G   /usr/bin/gnome-shell                          60MiB |
+-----------------------------------------------------------------------------+
```

也可以使用`cat /proc/driver/nvidia/version`命令查看驱动程序版本

```
NVRM version: NVIDIA UNIX x86_64 Kernel Module  410.93  Thu Dec 20 17:01:16 CST 2018
GCC version:  gcc version 7.3.0 (Ubuntu 7.3.0-27ubuntu1~18.04) 
```

另外，对于桌面版系统而言，可以使用`nvidia-settings`命令设置一些参数，执行该命令后以弹窗的形式出现。而服务器版系统由于没有桌面环境，执行`nvidia-settings`命令会报错（Unable to init server: Could not connect: Connection refused
ERROR: The control display is undefined; please run `nvidia-settings --help` for usage information.）。

> 最后，也可以采用PPA源方式安装NVIDIA驱动。具体可以参考文章[GeForce GTX 1080Ti GPU NVIDIA Driver Installation in Ubuntu 18.04](https://medium.com/@sh.tsang/geforce-gtx-1080ti-gpu-nvidia-driver-installation-in-ubuntu-18-04-1d3407ecfd5e)

### GeForce GTX 1080Ti GPU NVIDIA Driver Installation in Ubuntu 18.04

There are only few steps to install the GPU driver for GeForce GTX 1080Ti in Ubuntu 18.04.

First, remove any previously installed Nvidia driver by entering the following command in the terminal:

```
sudo apt-get purge nvidia*
```

2. Then, add a repository — PPA (Personal Package Archives):

```
sudo add-apt-repository ppa:graphics-drivers/ppa
```

3. Then update:

```
sudo apt-get update
```

4. After that, we can install the Nvidia driver:

```
sudo apt-get install nvidia-390 nvidia-settings
```

5. After the installation, reboot the system:

```
sudo reboot
```

6. After reboot, to check whether the driver is sucessfully installed:

```
nvidia-smi
```

The following screen should be shown if the driver is successfully installed.

```
 nvidia-smi 
Sun Feb 24 18:08:23 2019       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 410.93       Driver Version: 410.93       CUDA Version: 10.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce GTX 980 Ti  Off  | 00000000:02:00.0  On |                  N/A |
| 20%   34C    P8    16W / 260W |     99MiB /  6080MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|    0      1285      G   /usr/lib/xorg/Xorg                            35MiB |
|    0      1314      G   /usr/bin/gnome-shell                          60MiB |
+-----------------------------------------------------------------------------+
```

GPU Driver is successfully installed.

7. We can also enter the following command to check other details of the GPU:

```
cat /proc/driver/nvidia/gpus/{tab}/information
```

8. I just posted what I have done here. Hope this can be helpful. :)

[Missing firmware warnings during update](https://askubuntu.com/questions/1117305/missing-firmware-warnings-during-update)

[Nouveau: Accelerated Open Source driver for nVidia cards](https://nouveau.freedesktop.org/wiki/)

[How to disable Nouveau nvidia driver on Ubuntu 18.04 Bionic Beaver Linux](https://linuxconfig.org/how-to-disable-nouveau-nvidia-driver-on-ubuntu-18-04-bionic-beaver-linux)

[Ubuntu16.04服务器版安装NVIDIA显卡驱动](https://blog.csdn.net/qq_30163461/article/details/80314630)

[NVIDIA Accelerated Linux Graphics Driver README and Installation Guide](http://us.download.nvidia.com/XFree86/Linux-x86_64/410.93/README/)