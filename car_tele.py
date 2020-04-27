# -*- coding: utf-8 -*-

#将RPi.GPIO 模块映射为GPIO来使用
from RPi import GPIO
#引入time模块
import time
 
#采用BCM引脚顺序编号
GPIO.setmode(GPIO.BCM)
#关闭警告
GPIO.setwarnings(False)

#输入IO
INPUT_PIN0 = 06
INPUT_PIN1 = 13
INPUT_PIN2 = 19
INPUT_PIN3 = 26
# 设置GPIO输入模式, 使用GPIO内置的下拉电阻, 即开关断开情况下输入为LOW，适用于高电平输入
GPIO.setup(INPUT_PIN0, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(INPUT_PIN1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(INPUT_PIN2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(INPUT_PIN3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
# 设置GPIO输入模式, 使用GPIO内置的上拉电阻， 即开关断开情况下输入为HIGH，适用于接地的开关
#GPIO.setup(INPUT_PIN0, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

#输出IO
GPIO_PIN0 = 17
GPIO_PIN1 = 27
GPIO_PIN2 = 22
GPIO_PIN3 = 04
#配置输出IO方向
GPIO.setup(GPIO_PIN0, GPIO.OUT)               
GPIO.setup(GPIO_PIN1, GPIO.OUT) 
GPIO.setup(GPIO_PIN2, GPIO.OUT)
GPIO.setup(GPIO_PIN3, GPIO.OUT)
#输出IO初始化设置为低电平
GPIO.output(GPIO_PIN0, GPIO.LOW)           
GPIO.output(GPIO_PIN1, GPIO.LOW)
GPIO.output(GPIO_PIN2, GPIO.LOW)
GPIO.output(GPIO_PIN3, GPIO.LOW)

# 检测输入LOW -> HIGH的变化
GPIO.add_event_detect(INPUT_PIN0, GPIO.RISING, bouncetime = 200)
GPIO.add_event_detect(INPUT_PIN1, GPIO.RISING, bouncetime = 200)
GPIO.add_event_detect(INPUT_PIN2, GPIO.RISING, bouncetime = 200)
GPIO.add_event_detect(INPUT_PIN3, GPIO.RISING, bouncetime = 200)

#按键自锁判断变量
led0Status = 0
led1Status = 0

def reset():
	GPIO.output(GPIO_PIN0, GPIO.LOW)           
	GPIO.output(GPIO_PIN1, GPIO.LOW)
	GPIO.output(GPIO_PIN2, GPIO.LOW)
	GPIO.output(GPIO_PIN3, GPIO.LOW)

def forward():
	global led0Status
	global led1Status
	if GPIO.event_detected(INPUT_PIN0):
		reset()
		led1Status = 0	#自锁开关切换，双向开关
		led0Status = not led0Status
		if led0Status:
			GPIO.output(GPIO_PIN0, GPIO.HIGH)
			GPIO.output(GPIO_PIN1, GPIO.HIGH)
		else:
			reset()
	time.sleep(0.01)     # 10毫秒的检测间隔

def backward():
	global led0Status
	global led1Status
	if GPIO.event_detected(INPUT_PIN1):
		reset()
		led0Status = 0	#自锁开关切换，双向开关
		led1Status = not led1Status
		if led1Status:
			GPIO.output(GPIO_PIN2, GPIO.HIGH)
			GPIO.output(GPIO_PIN3, GPIO.HIGH)
		else:
			reset()
	time.sleep(0.01)     # 10毫秒的检测间隔

def left():
	global led0Status
	global led1Status
	if led0Status == True:
		while (GPIO.input(INPUT_PIN2) and led0Status == True):
			reset()
			GPIO.output(GPIO_PIN0, GPIO.HIGH)
		else:
			reset()
			GPIO.output(GPIO_PIN0, GPIO.HIGH)
			GPIO.output(GPIO_PIN1, GPIO.HIGH)
		time.sleep(0.01)     # 10毫秒的检测间隔
	if led1Status == True:
		while (GPIO.input(INPUT_PIN2) and led1Status == True):
			reset()
			GPIO.output(GPIO_PIN2, GPIO.HIGH)
		else:
			reset()
			GPIO.output(GPIO_PIN2, GPIO.HIGH)
			GPIO.output(GPIO_PIN3, GPIO.HIGH)
		time.sleep(0.01)     # 10毫秒的检测间隔

def right():
	global led0Status
	global led1Status
	if led0Status == True:
		while (GPIO.input(INPUT_PIN3) and led0Status == True):
			reset()
			GPIO.output(GPIO_PIN1, GPIO.HIGH)
		else:
			if led0Status == True:
				reset()
				GPIO.output(GPIO_PIN0, GPIO.HIGH)
				GPIO.output(GPIO_PIN1, GPIO.HIGH)
		time.sleep(0.01)     # 10毫秒的检测间隔
	if led1Status == True:
		while (GPIO.input(INPUT_PIN3) and led1Status == True):
			reset()
			GPIO.output(GPIO_PIN3, GPIO.HIGH)
		else:
			if led1Status == True:
				reset()
				GPIO.output(GPIO_PIN2, GPIO.HIGH)
				GPIO.output(GPIO_PIN3, GPIO.HIGH)
		time.sleep(0.01)     # 10毫秒的检测间隔


try:
	while True:
		if GPIO.input(INPUT_PIN0):
			forward();
		elif GPIO.input(INPUT_PIN1):
			backward();
		elif GPIO.input(INPUT_PIN2):
			left();
		elif GPIO.input(INPUT_PIN3):
			right();


#程序中止时清理GPIO资源
except KeyboardInterrupt:
        GPIO.cleanup()  
	print('  program stopped !')
