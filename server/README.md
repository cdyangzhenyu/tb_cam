# Server Install

## install requirments
- centos 7
- python 2.7
- vidgear
- opencv
```
yum install libzmq3-devel
pip install numpy==1.12
pip install opencv-contrib-python==3.2.0.7
pip install mss
pip install pyzmq
wget http://download1.rpmfusion.org/free/el/updates/7/x86_64/r/rpmfusion-free-release-7-4.noarch.rpm
rpm -ivh rpmfusion-free-release-7-4.noarch.rpm 
yum install ffmpeg
pip install vidgear
```

## install service

```
cd /root
git clone https://github.com/cdyangzhenyu/tb_cam.git
cp tb-camera-server.service /etc/systemd/system/
```

## run service

```
systemctl enable tb-camera-server
systemctl start tb-camera-server
```
## log file
```
tailf /var/log/tb_camera.log
```

## thingsboard widget

- add a new widget and add the HTML code:

```
<img src="http://your_camera_http_public_ip:15000/video_feed" height="100%" width="100%">
```
