# Server Install

## install requirments
- Resberry Pi 4
- python 2.7
- vidgear
- opencv
```
apt install libzmq3-dev
apt install libhdf5-dev
pip install numpy==1.12
pip install opencv-contrib-python==3.2.0.7
pip install mss
pip install pyzmq
pip install vidgear
```

## install service

```
cd /root
git clone https://github.com/cdyangzhenyu/tb_cam.git
cp emotion-rec-cam.service /etc/systemd/system/
```

## run service

```
systemctl enable emotion-rec-cam
systemctl start emotion-rec-cam
```

## log file
```
tail -f /data/log/tb_cam.log
```

## usb camera
```
apt-get install v4l-utils
v4l2-ctl  --list-devices
v4l2-ctl -d 0 --list-formats-ext 
``` 
