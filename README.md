#  电子相框（DigitalPhotoFrame）
使用Python的PIL和TKinter编写的电子相框，用于Raspberry PI。

## 功能描述
* 读取指定目录下的照片
* 自动播放
* 手动播放、暂停、上一张、下一张

  当处于播放状态下，点击屏幕中间位置为暂停。点击左侧位置为上一张，右侧位置为下一张，再次点击中间位置为播放。

## 安装配置
* 硬件环境
Raspberry Pi3

![image](https://github.com/mrwangyu2/DigitalPhotoFrame/tree/master/images/1.png)

![image](https://github.com/mrwangyu2/DigitalPhotoFrame/tree/master/images/2.png)

* 系统环境
  * Raspberry Pi OS [NOOBS](https://www.raspberrypi.org/downloads/)
  * PIL 安装

    ```
    $sudo easy_install PIL
    ```

  * 启动配置

    编辑/home/pi/.config/lxsession/LXDE/autostart 

    添加 @/home/pi/digital_photos_frame.py

  * 关闭屏幕休眠

    编辑/etc/lightdm/lightdm.conf, 找到[SeatDefaults]段下的'xserver-command',取消注释,修改为如下: 

    ```
    xserver-command=X -s 0 -dpms
    ```

* 配置
  * 配置照片路径

    digital_photos_frame.py 中的PHOTOS_PATH变量，指定了照片的存放路径

  * 播放间隔时间

    digital_photos_frame.py 中的INTERVAL变量，为照片的播放间隔时间

