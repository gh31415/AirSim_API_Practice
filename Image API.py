import airsim
import numpy as np
import cv2

# 连接到AirSim模拟器
client = airsim.MultirotorClient()
client.confirmConnection()
# 一次获取一张图片
# response = client.simGetImage(camera_name, image_type, vehicle_name='')

# 无人机摄像头编号及含义(camera_name)
'''
摄像机0：无人机的前方视角
摄像机1：无人机的后方视角
摄像机2：无人机的底部视角，可以用于检测地面和障碍物
摄像机3：无人机的顶部视角，可以用于拍摄俯视图或进行目标跟踪
摄像机4：无人机的左侧视角
摄像机5：无人机的右侧视角
'''

# 使用图像API能够获取到的8种图像类型
'''
Scene：场景视图图片，即俯视图，可以看到整个场景的情况。                                   airsim.ImageType.Scene
DepthPlanar：平面深度图片，可以获取场景中每个像素点到相机的距离。                          airsim.ImageType.DepthPlanar
DepthPerspective：透视深度图片，可以获取场景中每个像素点到相机的距离。                     airsim.ImageType.DepthPerspective
DepthVis：深度可视化图片，可以将深度图像转换为RGB图像，方便观察。                          airsim.ImageType.DepthVis
DisparityNormalized：视差归一化图片，可以获取场景中每个像素点的视差值，用于计算深度信息。     airsim.ImageType.DisparityNormalized
Segmentation：分割图片，可以将场景中的不同物体或区域分别标记出来，方便进行目标检测和分割。      airsim.ImageType.Segmentation
SurfaceNormals：表面法线图片，可以获取场景中每个像素点的法线方向，用于计算光照和阴影效果。      airsim.ImageType.SurfaceNormals
Infrared：红外线图片，可以获取场景中的红外线图像，用于热成像和红外线探测等应用。               airsim.ImageType.Infrared
'''
# 1.直接使用simGetImage获取PNG格式的彩色图，并保存成 .png 格式的图片文件。
# response = client.simGetImage('0', airsim.ImageType.Scene, vehicle_name='Drone')
# f = open('screen/scene.png', 'wb')
# f.write(response)
# f.close()

# 2.使用 simGetImages 获取PNG格式的分割图，并保存成 .png 格式的图片文件。
# responses = client.simGetImages([airsim.ImageRequest(0, airsim.ImageType.Segmentation, pixels_as_float=False, compress=True)])
# f = open('screen/seg.png', 'wb')
# f.write(responses[0].image_data_uint8)
# f.close()
'''
图像类型	        compress	         pixels_as_float	                适合保存的图片类型
PNG格式	          True	                  False	                  彩色图、分割图、表面法线图、红外图
Array格式	      False	                  False	                  彩色图、分割图、表面法线图、红外图
浮点型格式	      False	                  True	                             深度图
'''

# 3.使用 simGetImages 同时获取PNG格式的红外图和表面法线图，并保存成2个.png格式的图片文件。
# responses = client.simGetImages([airsim.ImageRequest(0, airsim.ImageType.Infrared, pixels_as_float=False, compress=True), airsim.ImageRequest(0, airsim.ImageType.SurfaceNormals, pixels_as_float=False, compress=True)])
# # print(responses)
# # 保存红外图
# f = open('screen/infrared.png', 'wb')
# f.write(responses[0].image_data_uint8)
# f.close()
# # 保存表面法线图
# f = open('screen/surface.png', 'wb')
# f.write(responses[1].image_data_uint8)
# f.close()

# 4.保存Array格式图像
# 读取图像数据，array格式
# responses = client.simGetImages([
#     airsim.ImageRequest(0, airsim.ImageType.Scene, pixels_as_float=False, compress=False)])
# # 将bytes格式转换为 array格式 fromstring
# img_1d = np.frombuffer(responses[0].image_data_uint8, dtype=np.uint8)
# img_bgr = img_1d.reshape(responses[0].height, responses[0].width, 3)
# # 保存为图片文件
# cv2.imwrite('scene.png', img_bgr)  # 保存为.png格式的图像文件
# cv2.imwrite('scene.jpg', img_bgr)  # 保存为.jpg格式的图像文件
# cv2.imwrite('scene.tif', img_bgr)  # 保存为.tif格式的图像文件
# cv2.imwrite('scene.bmp', img_bgr)  # 保存为.bmp格式的图像文件
'''
.jpg 格式：不带透明通道的有损压缩格式，广泛应用于互联网和数码相机领域；
.png 格式：便携式网络图形，无损压缩的位图，有较高的压缩比；
.tif 格式：非失真的压缩格式，占用空间较大，通常用于书籍和海报等教专业的领域；
.bmp 格式：是Windows操作系统中的标准图像文件格式，通常不压缩，文件所占空间较大。
'''