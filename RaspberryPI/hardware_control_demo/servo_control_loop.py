import RPi.GPIO as GPIO
import time

# 设置GPIO模式为BCM
GPIO.setmode(GPIO.BCM)

# 定义舵机引脚
servo_pin = 18

# 设置舵机引脚为输出
GPIO.setup(servo_pin, GPIO.OUT)

# 创建PWM对象
pwm = GPIO.PWM(servo_pin, 50)  # 使用50Hz的频率

# 启动PWM
pwm.start(0)

# 定义函数控制舵机旋转到指定角度
def rotate(angle):
    # 将角度转换为占空比
    duty_cycle = ((angle / 180.0) * 10) + 2.5
    # 设置舵机占空比
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.02)  # 控制舵机速度的延迟

try:
    while True:
        # 逆时针方向旋转
        for angle in range(0, 181, 5):
            rotate(angle)
        # 顺时针方向旋转
        for angle in range(180, -1, -5):
            rotate(angle)

except KeyboardInterrupt:
    pass

# 停止PWM
pwm.stop()

# 清理GPIO引脚
GPIO.cleanup()
