import airsim
import os
import csv
import numpy as np


client = airsim.MultirotorClient()
client.confirmConnection()

# 设置相机和文件路径
camera_list = ["0", "1", "2", "3", "4"]
folder_path = "E:/FunctionMethod/airsim_images/snow_datasets/square1"

# 读取位姿信息文件（csv格式）
poses_csv_file = open("E:/poses.csv", "r")
pos_reader = csv.DictReader(poses_csv_file)

# 循环采样并保存图像和位姿信息
for i, row in enumerate(pos_reader):
    # 获取姿态信息
    x, y, z = float(row['x']), float(row['y']), float(row['z'])
    yaw, pitch, roll = float(row['yaw']), float(row['pitch']), float(row['roll'])
    pose = airsim.Pose(airsim.Vector3r(x, y, z), airsim.to_quaternion(pitch, roll, yaw))

    # 移动到目标位置
    client.simSetVehiclePose(pose, True)

    # 遍历相机列表，获取每个相机的图像
    for j, camera_name in enumerate(camera_list):
        responses = client.simGetImages([airsim.ImageRequest(camera_name, airsim.ImageType.Scene, False, False)])
        img_raw = responses[0]

        # 将字节流转换为PIL的Image对象
        img1d = np.frombuffer(img_raw.image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(img_raw.height, img_raw.width, 3)

        # 保存PNG格式的图像
        img_filename = "pose_{0}_x_{1:.2f}_y_{2:.2f}_z_{3:.2f}_yaw_{4:.2f}_pitch_{5:.2f}_roll_{6:.2f}_camera_{7}.png".format(i, x, y, z, yaw, pitch, roll, j)
        img_filepath = os.path.join(folder_path, img_filename)
        airsim.write_png(os.path.normpath(img_filepath), img_rgb)

print("图像和位姿信息均已保存到文件夹：", folder_path)
