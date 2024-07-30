#import sensor
#import image

#import time, pyb
#import struct
#from pyb import UART
#import math


## 初始化摄像头
#sensor.reset()
## 设置摄像头像素格式为RGB565（也可以设置为灰度但是颜色识别就无法使用了）
#sensor.set_pixformat(sensor.RGB565)
## 设置摄像头像素大小为QVGA（320x240）
#sensor.set_framesize(sensor.QQVGA)
#led = pyb.LED(3) # Red LED = 1, Green LED = 2, Blue LED = 3, IR LEDs = 4.

#uart = UART(3, 115200)

## 假设你已经得到了幕布中心和正方形四个顶点在像素坐标系中的坐标
#center_pixel_coord = (79, 51)
#square_pixel_coords = [(43, 15), (111, 14), (118, 82), (44, 87)]

## 计算像素坐标系中的正方形的宽度和高度
#pixel_width = max(coord[0] for coord in square_pixel_coords) - min(coord[0] for coord in square_pixel_coords)
#pixel_height = max(coord[1] for coord in square_pixel_coords) - min(coord[1] for coord in square_pixel_coords)

## 计算像素单位到幕布单位（cm）的映射比例
#pixel_to_cm_ratio_x = 50.0 / pixel_width
#pixel_to_cm_ratio_y = 50.0 / pixel_height

## 定义红色的阈值，这个阈值可能需要根据实际的环境进行调整
#red_threshold = (1, 94, 104, 22, -100, 52)
##(38, 88, 90, 29, -91, 85)
##red_threshold = (38, 88, 90, 29, -91, 85)



## 定义一个函数，将像素坐标转换为幕布坐标
#def pixel_to_physical(pixel_coord):
#    pixel_x = pixel_coord[0]
#    pixel_y = pixel_coord[1]

#    average_x = (square_pixel_coords[0][0] + square_pixel_coords[3][0]) / 2
#    average_y = (square_pixel_coords[0][1] + square_pixel_coords[1][1]) / 2

#    physical_x = (pixel_x - average_x) * pixel_to_cm_ratio_x
#    physical_y = abs((pixel_y - average_y) - pixel_height) * pixel_to_cm_ratio_y

#    return (physical_x, physical_y)



#def angle(point, center):
#    return math.atan2(point[1] - center[1], point[0] - center[0])



#shrink_pixels = 3
##def send_coordinates(coords):
##    data = b'\xAA'  # 帧头
##    for coord in coords:
##        x, y = coord
##        data += struct.pack('ff', x, y)
##    data += b'\xCC'  # 帧尾
##    uart.write(data)
##    print((data))
#def interpolate_points(p1, p2, num_points):#插值函数
#    x1, y1 = p1
#    x2, y2 = p2
#    return [(x1 + i * (x2 - x1) / (num_points - 1), y1 + i * (y2 - y1) / (num_points - 1)) for i in range(num_points)]

#shrink_pixels = 3
#num_points_per_edge = 20
#target_point_index = 0
#distance_threshold = 2  # 你需要根据实际情况设置这个值

#red_coord =(0,0)

#time.sleep(2)
#while(True):

#    img = sensor.snapshot().lens_corr(strength = 0.5, zoom = 1.0)
#    led.on()
#    # 在主循环中找到红色光电的坐标
##    red_blobs = img.find_blobs([red_threshold])
##    if red_blobs:
##        max_blob = max(red_blobs, key=lambda b: b.pixels())
##        img.draw_rectangle(max_blob.rect())
##        img.draw_cross(max_blob.cx(), max_blob.cy())
##        red_coord = (max_blob.cx(), max_blob.cy())


#    for r in img.find_rects(threshold = 25000):
#        img.draw_rectangle(r.rect(), color = (0, 0, 255))

#        # 获取四个角点的坐标
#        corners = list(r.corners())  # 将元组转换为列表

#        # 计算四个角点的中心
#        cx = sum([p[0] for p in corners]) / 4
#        cy = sum([p[1] for p in corners]) / 4

#        # 根据每个点相对于中心的角度进行排序
#        corners.sort(key=lambda p: angle(p, (cx, cy)))

#        # 在四个角点上画出数字1、2、3和4
#        for i in range(4):
#            img.draw_string(corners[i][0], corners[i][1], str(i+1), color=(255, 255, 255), scale=2)




#        all_points = []
#        for i in range(4):
#            all_points += interpolate_points(corners[i], corners[(i+1)%4], num_points_per_edge)



#        if math.sqrt((red_coord[0] - all_points[target_point_index][0])**2 + (red_coord[1] - all_points[target_point_index][1])**2) < distance_threshold:
#            target_point_index = (target_point_index + 1) % len(all_points)
#        # 打包数据
##        data = bytes([0xAA,red_coord[0] >> 8, red_coord[0] & 0xFF, red_coord[1] >> 8, red_coord[1] & 0xFF,
##                            (int)(all_points[target_point_index][0] ) >> 8, (int)(all_points[target_point_index][0] ) & 0xFF,
##                            (int)(all_points[target_point_index] [1]) >> 8, (int)(all_points[target_point_index] [1]) & 0xFF, 0xCC])
##        time.sleep(1)
#        red_coord = pixel_to_physical(red_coord)
#        all_points[target_point_index] = pixel_to_physical(all_points[target_point_index])
#        if red_coord[0] < 60 and red_coord[1] < 60 and red_coord[0] > 0 and red_coord[1] > 0 :
#            if all_points[target_point_index][0] < 60 and all_points[target_point_index][1] < 60 and all_points[target_point_index][0] > 0 and all_points[target_point_index][1] > 0:
#                data =  b'\xFF' + "%d,%d" % (red_coord[0], red_coord[1]) +  b'\xFE' +  b'\xAA' + "%d,%d" % (all_points[target_point_index][0], all_points[target_point_index][1]) +  b'\xCC'

#                # 发送数据
##                uart.write(data)
#    #           print(uart.read(4))
#                print(red_coord[0], red_coord[1])

#                print(all_points[target_point_index][0], all_points[target_point_index][1])



import sensor
import image
import time, pyb
import struct
from pyb import UART
import math

# 初始化摄像头
sensor.reset()
# 设置摄像头像素格式为RGB565
sensor.set_pixformat(sensor.RGB565)
# 设置摄像头像素大小为QVGA（320x240）
sensor.set_framesize(sensor.QQVGA)
led = pyb.LED(3) # Red LED = 1, Green LED = 2, Blue LED = 3, IR LEDs = 4.

uart = UART(3, 115200)


#coord_chess = {}

# 颜色值
red_threshold = (30,100,15,127,15,127)  #红色
green_threshold=(30,100,-64,-8,-32,32)  #绿色
blue_threshold=(0,64,-128,-8,-128,0)  #蓝色
black_threshold=(11, 4, 3, -23, -12, 11)
white_threshold=(76, 84, -71, 4, -39, 17)


def angle(point, center):
    return math.atan2(point[1] - center[1], point[0] - center[0])

# 颜色追踪
def find_color_blob(color_threshold):
    blobs = img.find_blobs([color_threshold], pixels_threshold=200, area_threshold=200)
    if blobs:
        return max(blobs,key=lambda b:b.pixels())
    return None

# 圆形检测
def find_circles():
    circles = img.find_circles(threshold=4000, x_margin=10, y_margin=10, r_margin=10,r_min=2, r_max=100,r_step=2)
    if circles:
        return sorted(circles,key=lambda c: c.r(),reverse=True)
    return None

def judge_IOchessboard():


while (True):

    img = sensor.snapshot().lens_corr(strength = 1.6, zoom = 1.0)
    led.on()

    for r in img.find_rects(threshold = 38000):
        img.draw_rectangle(r.rect(), color = (255, 0, 0))
         # 获取四个角点的坐标
        corners = list(r.corners())  # 将元组转换为列表
         # 计算四个角点的中心
        cx = sum([p[0] for p in corners]) / 4
        cy = sum([p[1] for p in corners]) / 4
         # 根据每个点相对于中心的角度进行排序
        corners.sort(key=lambda p: angle(p, (cx, cy)))
         # 在四个角点上画出数字1、2、3和4
        for i in range(4):
            img.draw_string(corners[i][0], corners[i][1], str(i+1), color=(0, 255, 0), scale=2)

        #查找黑棋
        black_blob = find_color_blob(black_threshold)
        if black_blob:
            img.draw_rectangle(black_blob.rect())
            img.draw_cross(black_blob.cx(),black_blob.cy(),color=(255,0,0))
        #查找白棋
        white_blob = find_color_blob(white_threshold)
        if white_blob:
            img.draw_rectangle(white_blob.rect())
            img.draw_cross(white_blob.cx(),white_blob.cy(),color=(0,255,0))

#        #查找圆形
#        circles =find_circles()
#        if circles:
#            for circle in circles:
#                img.draw_circle(circle.x(),circle.y(),circle.r(),color=(255,0,0))

        #每个棋盘格的中心坐标
        chessboard_1 = ((corners[0][0] + corners[1][0]) / 6, (corners[0][1] + corners[3][1]) / 6)
        chessboard_2 = (3 * (corners[0][0] + corners[1][0]) / 6), (corners[0][1] + corners[3][1]) / 6)
        chessboard_3 = (5 * (corners[0][0] + corners[1][0]) / 6), (corners[0][1] + corners[3][1]) / 6)
        chessboard_4 = ((corners[0][0] + corners[1][0]) / 6, 3 * (corners[0][1] + corners[3][1]) / 6)
        chessboard_5 = (3 * (corners[0][0] + corners[1][0]) / 6, 3 * (corners[0][1] + corners[3][1]) / 6)
        chessboard_6 = (5 * (corners[0][0] + corners[1][0]) / 6, 3 * (corners[0][1] + corners[3][1]) / 6)
        chessboard_7 = ((corners[0][0] + corners[1][0]) / 6, 5 * (corners[0][1] + corners[3][1]) / 6)
        chessboard_8 = (3 * (corners[0][0] + corners[1][0]) / 6, 5 * (corners[0][1] + corners[3][1]) / 6)
        chessboard_9 = (5 * (corners[0][0] + corners[1][0]) / 6, 5 * (corners[0][1] + corners[3][1]) / 6)
        #建立棋盘数据类型，0：无棋子，1：白棋子，2：黑棋子。eg：(2,chessboard_1)表示chessboard_1位置有黑棋子
        chessboard = ((0, chessboard_1), (0, chessboard_2), (0, chessboard_3),
                      (0, chessboard_4), (0, chessboard_5), (0, chessboard_6),
                      (0, chessboard_7), (0, chessboard_8), (0, chessboard_9))






        if uart.any() != 0:
            while(True):
                if uart.readchar() == -1:
                    print(-1)
                elif uart.readchar() == 1:
                    print(1)
                elif uart.readchar() == 2:
                    print(2)
                elif uart.readchar() == 3:
                    print(3)
                elif uart.readchar() == 4:
                    print(4)





