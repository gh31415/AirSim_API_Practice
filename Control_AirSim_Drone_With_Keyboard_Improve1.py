# 显示子图的AirSim的settings.json文件配置
"""
{
    "SettingsVersion": 1.2,
    "SeeDocsAt": "https://github.com/Microsoft/AirSim/blob/master/docs/settings.md",
    "SimMode": "Multirotor",
    "ViewMode": "FlyWithMe",
    "SubWindows": [
        {
            "WindowID": 0,
            "CameraName": "front_center_custom",
            "ImageType": 0,
            "Visible": true,
            "ImageSize": [480, 270],
            "CameraPosition": [0.0, 0.0, -2.5],
            "CameraRotation": [0.0, 0.0, 0.0]
        },
        {
            "WindowID": 1,
            "CameraName": "front_center_custom",
            "ImageType": 3,
            "Visible": true,
            "ImageSize": [480, 270],
            "CameraPosition": [0.0, 0.0, -2.5],
            "CameraRotation": [0.0, 0.0, 0.0]
        },
	{
	    "WindowID": 2,
            "CameraName": "front_center_custom",
            "ImageType": 5,
            "Visible": true,
            "ImageSize": [480, 270],
            "CameraPosition": [0.0, 0.0, -2.5],
            "CameraRotation": [0.0, 0.0, 0.0]
	}
    ],
    "Vehicles": {
    "Drone": {
        "VehicleType": "SimpleFlight",
        "DisplayName": "My First Drone",
        "AutoCreate": true
	}
    }
}
"""
# 图像类型及其编号
"""
Scene（场景）: 0
Depth（深度）: 1
Semantic Segmentation（语义分割）: 2
Instance Segmentation（实例分割）: 3
Surface Normals（表面法线）: 4
DisparityNormalized（规范化视差）: 5
OptFlow（光流）: 6
Segmentation（分割）: 7
Object type（对象类型）: 8
Object ID（对象ID）: 9
"""

import sys
import time
import airsim
import pygame

# >------>>>  pygame settings   <<<------< #
pygame.init()
screen = pygame.display.set_mode((320, 240))
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
vehicle_velocity = 2.0
# 设置临时加速比例
speedup_ratio = 10.0
# 用来设置临时加速
speedup_flag = False

# 基础的偏航速率
vehicle_yaw_rate = 5.0

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
        yaw_rate = (scan_wrapper[pygame.K_d] - scan_wrapper[pygame.K_a]) * scale_ratio * vehicle_yaw_rate

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

    if scan_wrapper[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
