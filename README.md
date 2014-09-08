droydrunner
===========

a docker image for droydrunner test automation tool for android  ( python adb uiautomator on debian:wheezy)



usage
=====

start the container

```
sudo docker run --privileged -v /dev/bus/usb:/dev/bus/usb -ti  -P cocoon/droydrunner /bin/sh
```



use it

to start a phone hub server

```
sudo docker run --privileged -v /dev/bus/usb:/dev/bus/usb -d  -P cocoon/droydrunner droydrun phone hub server start
```


to play with

```
# adb devices
* daemon not running. starting it now on port 5037 *
* daemon started successfully *
List of devices attached
e7f54be6	offline
388897e5	offline

# python
eGenix PyRun 2.7.8 (release 2.0.1, default, Aug 26 2014, 11:43:05)
[GCC 4.6.4]
Thank you for using eGenix PyRun. Type "help" or "license" for details.

>>> from uiautomator import Device
>>> d = Device('e7f54be6')
>>> d.info
{u'displayRotation': 0, u'displaySizeDpY': 640, u'displaySizeDpX': 360, u'displayWidth': 1080, u'productName': u'kltexx', u'currentPackageName': u'com.sec.android.app.launcher', u'sdkInt': 19, u'displayHeight': 1920, u'naturalOrientation': True}
>>> d.press('home')
True
>>>



```