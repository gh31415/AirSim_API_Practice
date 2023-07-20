## Control_AirSim_Drone_With_Keyboard

​    有时候为了方便在AirSim调试无人机，验证一些视觉模块，使用键盘来控制无人机移动显得十分必要，或者，有时候我们想手动控制验证一下自己实现的底层飞控性能，这时，我们特别希望能够通过自写程序全方位手动控制无人机。AirSim官方提供的键盘控制Demo程序比较简单，每个时刻只能根据一个按键状态来控制无人机进行简单飞行。Demo程序如下所示：

```python
from msvcrt import getch

import airsim

client = airsim.MultirotorClient()
client.confirmConnection()

while True:
    ch = getch()
    if ch == 'w':
        client.moveByAngleThrottleAsync(pitch=-5, throttle=0.5, roll=0, yaw_rate=0, duration=0.1)
    elif ch == 's':
        client.moveByAngleThrottleAsync(pitch=5, throttle=0.5, roll=0, yaw_rate=0, duration=0.1)
    elif ch == 'a':
        client.moveByAngleThrottleAsync(roll=-5, throttle=0.5, pitch=0, yaw_rate=0, duration=0.1)
    elif ch == 'd':
        client.moveByAngleThrottleAsync(roll=5, throttle=0.5, pitch=0, yaw_rate=0, duration=0.1)
    elif ch == 'q':
        client.rotateByYawRateAsync(-20, duration=0.1)
    elif ch == 'e':
        client.rotateByYawRateAsync(20, duration=0.1)
```

​	首先通过 `from msvcrt import getch`导入一个 Python 标准库 `msvcrt` 中的 `getch()` 函数，可以从终端读取一个输入字符，用于控制飞机。然后通过 `import airsim` 导入 AirSim 库，用于实现控制飞机的相关函数。

​	接着创建了一个 `MultirotorClient` 类的实例 `client`，并调用 `confirmConnection()` 方法连接到 AirSim 仿真环境（或者实际无人机）。然后进入一个无限循环，通过 `getch()` 函数读取终端输入的字符，根据不同的输入字符控制飞机的运动。

****

`moveByAngleThrottleAsync()` 是 AirSim 中的一个函数，可以控制多旋翼（或其他类型的飞行器）的运动。

该函数的参数包括：

- `pitch`：飞行器的俯仰角，单位为度。
- `roll`：飞行器的横滚角，单位为度。
- `yaw`：飞行器的偏航角（航向角），单位为度。
- `throttle`：飞行器的油门值，范围是 0 到 1 之间。
- `duration`：运动的持续时间（秒），如果未指定则默认为 1 秒。

通过设定 `pitch`、`roll`、`yaw` 和 `throttle` 四个参数，可以实现多种不同方式的飞行器运动控制。例如，可以通过改变 `pitch` 和 `roll` 的值控制飞机的前后、左右倾斜，从而实现前进、左移、右移等动作。而通过改变 `yaw` 的值可以让飞机绕着竖直轴旋转，实现左右转向。最后，通过调整 `throttle` 的值可以控制飞机的速度。

****

`rotateByYawRateAsync()` 函数是 AirSim 中的一个函数，用于控制飞行器绕自身的竖直轴旋转。

该函数的参数包括：

- `yaw_rate`：旋转的速率，单位为度/秒。
- `duration`：持续时间，如果未指定则默认为 1 秒。

通过设置 `yaw_rate` 参数可以让飞行器以一定的角速度绕自身的竖直轴旋转。旋转方向与 `yaw_rate` 的正负有关，指定负值则飞机将顺时针旋转，正值则反之。

在代码中，该函数配合无限循环和终端输入信号应用，可以实现控制飞行器旋转的功能。例如，当输入字符为 `q` 时，可以调用 `rotateByYawRateAsync(-20, duration=0.1)` 使飞机以 20 度/秒的速率向左旋转，当输入字符为 `e` 时，可以调用 `rotateByYawRateAsync(20, duration=0.1)` 使飞机以 20 度/秒的速率向右旋转。

****

在飞行控制领域，yaw、roll 和 pitch 是描述飞机或无人机运动状态的三个关键参数。

- yaw（偏航角）：指飞行器绕着竖直轴旋转的角度，也即朝向的改变角度。偏航控制通常由方向舵来实现。
- roll（翻滚角）：指飞行器绕横轴旋转的角度，也即左右倾斜角度。翻滚控制通常由副翼来实现。
- pitch（俯仰角）：指飞行器绕纵轴旋转的角度，也即前后俯仰角度。俯仰控制通常由升降舵来实现。

使用这三个参数可以描述飞机或无人机运动状态的姿态，包括俯仰、横滚、偏航等。例如，当一个飞机向右平移时，它的俯仰和偏航角度不变，但是横滚角度会发生变化。因此，了解和掌握这些参数，对于飞行控制的理解和实现都是非常重要的。

![image-20230519174030887](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20230519174030887.png)

## Control_AirSim_Drone_With_Keyboard_improve

```python
import sys
import time
import airsim
import pygame

# >------>>>  pygame settings   <<<------< #
pygame.init()
screen = pygame.display.set_mode((100, 100))
pygame.display.set_caption('keyboard ctrl')
screen.fill((0, 0, 0))

# >------>>>  AirSim settings   <<<------< #
# 这里改为你要控制的无人机名称(settings文件里面设置的)
vehicle_name = "Drone"
AirSim_client = airsim.MultirotorClient()
AirSim_client.confirmConnection()
AirSim_client.enableApiControl(True, vehicle_name=vehicle_name)
AirSim_client.armDisarm(True, vehicle_name=vehicle_name)
AirSim_client.takeoffAsync(vehicle_name=vehicle_name).join()

# 基础的控制速度(m/s)
base_velocity = 2.0
# 设置临时加速比例
speedup_ratio = 10.0
# 用来设置临时加速
speedup_flag = False

# 基础的偏航速率
base_yaw_rate = 5.0

while True:

    yaw_rate = 0.0
    velocity_x = 0.0
    velocity_y = 0.0
    velocity_z = 0.0

    time.sleep(0.02)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    scan_wrapper = pygame.key.get_pressed()

    # 按下空格键加速10倍
    if scan_wrapper[pygame.K_SPACE]:
        scale_ratio = speedup_ratio
    else:
        scale_ratio = speedup_ratio / speedup_ratio

    # 根据 'A' 和 'D' 按键来设置偏航速率变量
    if scan_wrapper[pygame.K_a] or scan_wrapper[pygame.K_d]:
        yaw_rate = (scan_wrapper[pygame.K_d] - scan_wrapper[pygame.K_a]) * scale_ratio * base_yaw_rate

    # 根据 'UP' 和 'DOWN' 按键来设置pitch轴速度变量(NED坐标系，x为机头向前)
    if scan_wrapper[pygame.K_UP] or scan_wrapper[pygame.K_DOWN]:
        velocity_x = (scan_wrapper[pygame.K_UP] - scan_wrapper[pygame.K_DOWN]) * scale_ratio

    # 根据 'LEFT' 和 'RIGHT' 按键来设置roll轴速度变量(NED坐标系，y为正右方)
    if scan_wrapper[pygame.K_LEFT] or scan_wrapper[pygame.K_RIGHT]:
        velocity_y = -(scan_wrapper[pygame.K_LEFT] - scan_wrapper[pygame.K_RIGHT]) * scale_ratio

    # 根据 'W' 和 'S' 按键来设置z轴速度变量(NED坐标系，z轴向上为负)
    if scan_wrapper[pygame.K_w] or scan_wrapper[pygame.K_s]:
        velocity_z = -(scan_wrapper[pygame.K_w] - scan_wrapper[pygame.K_s]) * scale_ratio

    # print(f": Expectation gesture: {velocity_x}, {velocity_y}, {velocity_z}, {yaw_rate}")

    # 设置速度控制以及设置偏航控制
    AirSim_client.moveByVelocityBodyFrameAsync(vx=velocity_x, vy=velocity_y, vz=velocity_z, duration=0.02,
                                               yaw_mode=airsim.YawMode(True, yaw_or_rate=yaw_rate), vehicle_name=vehicle_name)

    # press 'Esc' to quit
    if scan_wrapper[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
```
**一定要记得切换成英文输入法！**

1. **关键函数、代码分析**

`velocity_x = (scan_wrapper[pygame.K_UP] - scan_wrapper[pygame.K_DOWN]) * scale_ratio`

这行代码表示将飞行器在X轴上的速度velocity_x设置为按键盘上的“上箭头”键增加的值减去按“下箭头”键减少的值后乘以比例系数(scale_ratio)。具体来说：

* 当按下“上箭头”键时，scan_wrapper[pygame.K_UP]返回1，而scan_wrapper[pygame.K_DOWN]返回0，因此velocity_x的值会增加scale_ratio。

* 当按下“下箭头”键时，scan_wrapper[pygame.K_DOWN]返回1，而scan_wrapper[pygame.K_UP]返回0，因此velocity_x的值会减少scale_ratio。

* 当“上箭头”键和“下箭头”键同时按下时，velocity_x的值会保持不变。

* 当没有按下“上箭头”键和“下箭头”键时，velocity_x的值为0。

`AirSim_client.moveByVelocityBodyFrameAsync` 

是AirSim提供的一个异步函数，用于控制飞行器沿着指定的速度向前或向后运动，速度是以飞行器体坐标系中的坐标表示。

参数选项：

```python
AirSim_client.moveByVelocityBodyFrameAsync(vx, vy, vz, duration, drivetrain=DrivetrainType.MaxDegreeOfFreedom, yaw_mode=YawMode(), vehicle_name='',vehicle_api=None)
```

- `vx`：飞行器在x轴方向的速度，单位 m/s。
- `vy`：飞行器在y轴方向的速度，单位 m/s。
- `vz`：飞行器在z轴方向的速度，单位 m/s。
- `duration`：持续时间，单位秒。
- `drivetrain`：飞行器的驱动方式，可选 MaxDegreeOfFreedom（完全自由度）、ForwardOnly（仅前进）和 ForwardFirst（优先前进）。默认是 MaxDegreeOfFreedom。
- `yaw_mode`：飞行器的偏航控制方式，可选的有 YawMode、YAW_RATE 和 YAW_ANGLE。默认是 YawMode，即使用迎角制造旋转，注意旋转时，需要设置 yaw_mode 和该值的组合，以获得所需的运动。
- `vehicle_name`：飞行器名称。默认为空字符串，代表所有的飞行器。
- `vehicle_api`：飞行器API。默认为None，代表使用默认API，不需要修改。

`yaw_mode`

`YawMode()` 是AirSim提供的一个类，用于控制飞行器的偏航控制方式。`YawMode()` 不需要传入任何参数，其默认构造函数会返回一个包含默认设置的偏航控制对象，可以在 AirSim 中使用。如果需要自定义偏航控制方案，可以修改生成的控制对象的属性值。`YawMode()` 构造函数的可选参数如下：

- `is_rate`（默认值为False）：是一个布尔型变量，用于表示偏航控制是否使用速率，如果为 True，则会将偏航值作为速率值。例如，如果偏航值为 pi/6，在持续时间 2s 的情况下，偏航速率就是 pi/6/2 = 0.2618 弧度/秒。
- `yaw_or_rate`（默认值为0）：是一个标量变量，用于表示偏航值（以弧度为单位）或速率值（以弧度/秒为单位）。
- `is_absolute`（默认值为 False）：是一个布尔型变量，用于表示偏航控制是否使用全局坐标系（绝对角度）。

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

2. **同时运行AirSim和Pygame时无人机飞行非常卡顿**

这可能是因为打开Pygame后，计算机的CPU和GPU资源被分配给了Pygame进程，导致UE4的渲染速度下降，从而导致无人机的运行变得卡顿。

您可以尝试采取以下措施来解决这个问题：

* 降低Pygame程序的占用资源：例如减小Pygame窗口的大小、减少窗口内的动画效果等，以减轻Pygame对计算机资源的占用。

* 提高UE4的性能：例如关闭不必要的特效、降低渲染设置、减少场景中的面数等，以提高UE4的运行效率。

* 将UE4和Pygame运行在两台不同的计算机上：如果您有多台计算机，可以将UE4和Pygame分别运行在不同的计算机上，以避免它们之间的资源竞争。

****

在UE4中，可以使用以下方法取消勾选非焦点窗口时占用较少计算资源的选项：

1. 在Editor中，单击菜单栏的 `Edit` 按钮，然后从下拉菜单中选择 `Editor Preferences`。
2. 在 `Editor Preferences` 窗口中，选择 `General` 选项卡。
3. 在 `General` 选项卡中，滚动到 `Editor Performance` 部分。
4. 在 `Editor Performance` 部分中，找到`Use Less CPU when in Background` 选项，并将其取消勾选。
5. 在 `Editor Preferences` 窗口底部，单击 `Apply` 按钮保存更改。

这样设置后，当窗口失去焦点时，UE4编辑器将停止非必要的后台计算，从而优化计算资源。可以通过此方法提高编辑器的运行效率，避免因为后台计算资源过多导致编辑器运行缓慢的情况。

****

当然在进行了上述所有操作后，都不能解决卡顿的问题，可以试着修改AirSim的渲染方式为D3D11。（待定）

Pygame和AirSim同时占用了计算机的GPU资源，导致渲染出现冲突，从而导致AirSim的性能受到影响。

1. 减少Pygame的帧率：将Pygame的帧率降低可以减少它占用GPU资源的时间，从而让AirSim能够更好地运行。你可以使用Pygame提供的set_fps()函数将帧率设置为较低的值，比如30或者更低。

2. 降低AirSim的渲染质量：通过降低AirSim的渲染质量可以减少它占用GPU资源的时间，从而提高AirSim的性能。你可以在AirSim的设置面板中将渲染质量设置为较低的值，或者关闭一些不必要的场景特效。

3. 在不同的计算机上运行：如果你的计算机硬件资源有限，可以尝试在不同的计算机上运行Pygame和AirSim。这样可以避免两个应用程序同时占用一台计算机的GPU资源，从而提高它们的性能和稳定性。

4. 使用多GPU的计算机：在部分计算机上可以采用多GPU来运行两种应用程序。
