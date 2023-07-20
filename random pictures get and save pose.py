import airsim
import os
import numpy as np
import pandas as pd

# 连接到AirSim模拟器
client = airsim.MultirotorClient()
client.confirmConnection()

# 获取图像路径
folder_path = "screen"

# 保存位姿信息的空DataFrame
poses_df = pd.DataFrame(columns=['index', 'x', 'y', 'z', 'yaw', 'pitch', 'roll'])

# 设置随机采样的范围和数量
num_samples = 50  # 需要采样的数量
x_min, x_max, y_min, y_max, z_min, z_max = -4, 4, -4, 4, -5, -2  # 位置范围
yaw_min, yaw_max, pitch_min, pitch_max, roll_min, roll_max = -90, 90, -45, 45, -45, 45  # 姿态范围

# 相机列表
camera_list = ["0", "1", "2", "3", "4"]

# 随机采样并保存图像和位姿信息
poses_list = []
for i in range(num_samples):
    # 随机生成目标位置，并设置姿态朝向
    x = np.random.uniform(x_min, x_max)
    y = np.random.uniform(y_min, y_max)
    z = np.random.uniform(z_min, z_max)
    yaw = np.random.uniform(yaw_min, yaw_max)
    pitch = np.random.uniform(pitch_min, pitch_max)
    roll = np.random.uniform(roll_min, roll_max)
    pose = airsim.Pose(airsim.Vector3r(x, y, z), airsim.to_quaternion(pitch, roll, yaw))
    poses_list.append({'index': i, 'x': x, 'y': y, 'z': z, 'yaw': yaw, 'pitch': pitch, 'roll': roll})
    # 移动到目标位置
    client.simSetVehiclePose(pose, True)

    # # 获取相机图像
    # responses = client.simGetImages([airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)])
    # img_raw = responses[0]

    # 遍历相机列表，获取每个相机的图像
    for j, camera_name in enumerate(camera_list):
        # 获取相机图像
        responses = client.simGetImages([airsim.ImageRequest(camera_name, airsim.ImageType.Scene, False, False)])
        img_raw = responses[0]

        # 将字节流转换为PIL的Image对象
        img1d = np.frombuffer(img_raw.image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(img_raw.height, img_raw.width, 3)

        # 保存PNG格式的图像
        img_filename = "pose_{0}_x_{1:.2f}_y_{2:.2f}_z_{3:.2f}_yaw_{4:.2f}_pitch_{5:.2f}_roll_{6:.2f}_camera_{4}.png".format(i, x, y, z, yaw, pitch, roll, j)
        img_filepath = os.path.join(folder_path, img_filename)
        airsim.write_png(os.path.normpath(img_filepath), img_rgb)

print("全部图像和位姿信息均已保存到文件夹：", folder_path)

# 将位姿信息保存到csv文件中
poses_df = pd.DataFrame(poses_list)
poses_df.to_csv(os.path.join(folder_path, 'poses.csv'), index=False)
'''
airsim.Vector3r函数用于创建一个三维向量，表示无人机在三个轴上的位置信息。
airsim.to_quaternion函数则用于将欧拉角（即pitch、roll、yaw）转换为四元数，表示无人机的姿态信息。

四元数是一种数学工具，用于描述三维空间中的旋转。它是由一个实部和三个虚部组成的，通常表示为q = a + bi + cj + dk，
其中a是实部，b、c、d是虚部，i、j、$k$是虚数单位。四元数可以用来表示旋转的方向和角度，它比欧拉角更加稳定和准确，避免了万向锁等问题。
在机器人、计算机图形学和游戏开发等领域中，四元数被广泛应用。在AirSim中，四元数用于表示无人机的姿态信息。

万向锁是一种旋转表示中常见的问题，它发生在使用欧拉角进行旋转时，当旋转角度过大或旋转轴与旋转顺序不当时，就会出现万向锁问题。
万向锁的表现形式是旋转轴和旋转角度不能被唯一确定，即旋转自由度丧失。这会导致旋转结果不可预测，甚至无法进行旋转。
为了避免万向锁问题，可以使用四元数等其他旋转表示方法。在AirSim中，使用欧拉角进行旋转时，也可能会出现万向锁问题，因此建议使用四元数进行姿态表示。
'''