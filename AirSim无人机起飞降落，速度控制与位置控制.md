# AirSim无人机起飞降落，速度控制与位置控制

## AirSim_Drone_fly_up&down

```python
import airsim
# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
# get control
client.enableApiControl(True)
# unlock
client.armDisarm(True)
# Async methods returns Future. Call join() to wait for task to complete.
client.takeoffAsync().join()
client.landAsync().join()
# lock
client.armDisarm(False)
# release control
client.enableApiControl(False)
```

```python
 client = airsim.MultirotorClient()
```

与 AirSim 建立连接，并且返回句柄（`client`），后面的每次操作需要使用这个句柄。

如果是汽车仿真，代码是：`client = airsim.CarClient()`;

```python
 client.confirmConnection()
```

检查通信是否建立成功，并且会在命令行中打印连接情况，这样你就可以潘丹程序是否和AirSim连接正常，如果连接正常会在命令行中打印如下：

```powershell
 Connected!
 Client Ver:1 (Min Req: 1), Server Ver:1 (Min Req: 1)
```

```python
 client.enableApiControl(True)    # get control
 client.enableApiControl(False)   # release control
```

因为安全问题， API 控制默认是不开启的，遥控器有全部的控制权限。所以必须要在程序中使用这个函数来获取控制权。遥控器的操作会抢夺 API 的控制权，同时让 API 获取的控制权失效。使用 `isApiControlEnabled` 可以检查 API 是否具有控制权。

可能会有人问为什么最后结束的时候要释放控制权，反正都是仿真，结束仿真就好了。但是实际上 AirSim 的开发人员希望在仿真中的代码可以直接移到现实中使用，所以对于现实中的安全问题，还是开发了获取控制权和释放控制权、解锁和上锁等一系列安全操作。

```python
 client.armDisarm(True)    # 解锁
 client.armDisarm(False)   # 上锁
```

使用这个函数可以让无人机的旋翼启动和停止旋转。

```python
 client.takeoffAsync().join()   # 起飞
 client.landAsync().join()      # 降落
```

这两个函数可以让无人机起飞和降落。

很多无人机或者汽车控制的函数都有 `Async` 作为后缀，这些函数在执行的时候会立即返回，这样的话，虽然任务还没有执行完，但是程序可以继续执行下去，而不用等待这个函数的任务在仿真中有没有执行完。

如果你想让程序在这里等待任务执行完，则只需要在后面加上`.join()`。本例子就是让程序在这里等待无人机起飞任务完成，然后再执行降落任务。

新的任务会打断上一个没有执行完的任务，所以如果`takeoff`函数没有加 `.join()`，则最后的表现是无人机还没有起飞就降落了，无人机是不会起飞的。

## AirSim_Drone_Position_Control

```python
import airsim
import time

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.enableApiControl(True)   # get control
client.armDisarm(True)          # unlock
client.takeoffAsync().join()    # takeoff

# square flight
client.moveToZAsync(-3, 1).join()               # 上升到3m高度
client.moveToPositionAsync(5, 0, -3, 1).join()  # 飞到（5,0）点坐标
client.moveToPositionAsync(5, 5, -3, 1).join()  # 飞到（5,5）点坐标
client.moveToPositionAsync(0, 5, -3, 1).join()  # 飞到（0,5）点坐标
client.moveToPositionAsync(0, 0, -3, 1).join()  # 回到（0,0）点坐标

client.landAsync().join()       # land
client.armDisarm(False)         # lock
client.enableApiControl(False)  # release control
```

```python
 client.moveToZAsync(-3, 1).join()   # 高度控制
```

`moveToZAsync(z, velocity)` 是高度控制 API，第一个参数是高度，第二个参数是速度。实现的效果是以 1m/s 的速度飞到 3 米高。`.join()` 后缀的意思是程序在这里等待直到任务完成，也就是四旋翼达到 3 米的高度。如果不加`.join()`后缀，则不用等待任务是否完成，函数直接返回，程序继续往下执行。

```python
 client.moveToPositionAsync(5, 0, -3, 1).join()  # 飞到（5,0）点坐标
 client.moveToPositionAsync(5, 5, -3, 1).join()  # 飞到（5,5）点坐标
 client.moveToPositionAsync(0, 5, -3, 1).join()  # 飞到（0,5）点坐标
 client.moveToPositionAsync(0, 0, -3, 1).join()  # 回到（0,0）点坐标
```

`moveToPositionAsync(x, y, z, velocity)` 是水平位置控制 API，x,y,z是全局坐标位置，velocity是速度。实现的效果是以 1m/s 的速度飞到 (5, 0) 点，3m 高的位置。`.join()` 后缀的意思是程序在这里等待直到任务完成，也就是四旋翼到达目标位置点，同时到达设置的高度。如果不加 `.join()` 后缀，则不用等待任务是否完成，函数直接返回，程序继续往下执行。

****

函数定义：

```python
 def moveToPositionAsync(
         self,
         x,          # 位置坐标（北东地坐标系）
         y,
         z,
         velocity,   # 速度
         timeout_sec=3e38,
         drivetrain=DrivetrainType.MaxDegreeOfFreedom,
         yaw_mode=YawMode(),
         lookahead=-1,
         adaptive_lookahead=1,
         vehicle_name="",
     )
```

输入参数包括：

- x,y,z：位置坐标（全局坐标系 - 北东地）
- velocity: 飞行速度（m/s）
- timeout_sec: 如果没有响应，超时时间
- drivetrain，yaw_mode: 设置飞行朝向模式和yaw角控制模式
- lookahead, adaptive_lookahead: 设置路径飞行的时候的yaw角控制模式
- vehicle_name: 控制的四旋翼名字

x, y, z, velocity 这四个参数是必须要设置的量，指示四旋翼以多大的速度飞往哪个坐标点。后面的几个参数都有其默认值，不用设置也可以。

lookahead 和 adaptive_lookahead 这两个参数是设置当四旋翼飞轨迹的时候的朝向，目前还用不到。

vehicle_name 是将指令发送给哪个四旋翼，当做多个四旋翼协同飞行控制的时候，这个参数就派上用场了，后面会有多机协同编队的教程。

drivetrain 和 yaw_mode 这两个参数的组合可以设置四旋翼的偏航角控制模式

****

drivetrain 参数可以设置为两个量：

- `airsim.DrivetrainType.ForwardOnly`： 始终朝向速度方向
- `airsim.DrivetrainType.MaxDegreeOfFreedom`：手动设置yaw角度

yaw_mode 必须设置为 YawMode() 类型的变量，这个结构体类型包含两个属性：

- YawMode().is_rate：True - 设置角速度；False - 设置角度
- YawMode().yaw_or_rate：可以是任意浮点数

下面分几种情况讨论：

**情况1 (不允许)：**

```python
 drivetrain = airsim.DrivetrainType.ForwardOnly
 yaw_mode = airsim.YawMode(True, 0)
 client.moveToPositionAsync(x, y, z, velocity, drivetrain=drivetrain, yaw_mode=yaw_mode).join()
```

当`drivetrain = airsim.DrivetrainType.ForwardOnly` 时，四旋翼始终朝向其飞行的方向，这时 yaw_mode 不允许设置为 YawMode().is_rate = True。因为前面的参数要求四旋翼朝向运动方向，而 yaw_mode 要求四旋翼以一定的角速度旋转，这是矛盾的。

**情况2：**

```python
 drivetrain = airsim.DrivetrainType.ForwardOnly
 yaw_mode = airsim.YawMode(False, 90)
 client.moveToPositionAsync(x, y, z, velocity, drivetrain=drivetrain, yaw_mode=yaw_mode).join()
```

这种情况下，四旋翼的朝向始终与前进方向相差90度，也就是四旋翼始终向左侧方向运动。例如：当四旋翼在绕着一个圆心转圈时，其朝向始终指向圆心（这种飞行状态的代码在下一篇文章中给出）。这里的90度可以任意设置。

**情况3：**

```python
 drivetrain = airsim.DrivetrainType.MaxDegreeOfFreedom
 yaw_mode = airsim.YawMode(False, 0)
 client.moveToPositionAsync(x, y, z, velocity, drivetrain=drivetrain, yaw_mode=yaw_mode).join()
```

这种情况下，不管速度方向是什么，四旋翼的yaw角始终等于0， 也就是其朝向始终指向正北方向。如果是90度，则始终指向正东方向，而-90度，则始终指向正西方向。

**情况4：**

```python
 drivetrain = airsim.DrivetrainType.MaxDegreeOfFreedom
 yaw_mode = airsim.YawMode(True, 10)
 client.moveToPositionAsync(x, y, z, velocity, drivetrain=drivetrain, yaw_mode=yaw_mode).join()
```

这种情况下，四旋翼不管速度方向是什么，yaw角以10度/秒的速度旋转。

下面总结一下这两个参数的设置对效果的影响：

|               | ForwardOnly                          | MaxDegreeOfFreedom                 |
| ------------- | ------------------------------------ | ---------------------------------- |
| is_rate=True  | 不允许                               | yaw角以yaw_or_rate度/秒旋转        |
| is_rate=False | yaw角相对于速度方向偏差yaw_or_rate度 | yaw角相对正北方向偏差yaw_or_rate度 |

## AirSim_Drone_Velocity_Control

```python
def moveByVelocityZAsync(
         self,
         vx,
         vy,
         z,
         duration,
         drivetrain=DrivetrainType.MaxDegreeOfFreedom,
         yaw_mode=YawMode(),
         vehicle_name="",
     )
```

这里的参数有：

- vx：全局坐标系下x轴方向上的速度
- vy：全局坐标系下y轴方向上的速度
- z：全局坐标系下的高度
- duration：持续的时间，单位：秒
- drivetrain, yaw_mode：用来设置偏航控制（上一篇文章讲过简介）
- vehicle_name：在多机协同的时候再用到

**速度控制误差**

****

四旋翼是一个非线性系统，给一个速度指令，它是不可能瞬时达到的，而且这个速度指令与当前的速度之差越大，到达这个速度指令的调节时间就越长。所以在上面的程序中，最后的四旋翼并没有回到起点位置。

为了做对比，可以把速度增大一些，下面的代码是四旋翼以8m/s的速度飞行2秒钟，分别向前右后左四个方向各飞行一次，最后离起点位置偏差更大，大家可以对比一下这两个视频。