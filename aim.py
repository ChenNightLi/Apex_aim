import win32api
import win32con
import time
import math

SPEED = 1378 # 311.464 // 0.226
CPS = 64

def move_to(x, y):
	nx = round(x * 65535 / win32api.GetSystemMetrics(0))
	ny = round(y * 65535 / win32api.GetSystemMetrics(1))
	win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE, nx, ny)

def move(dx, dy, smooth=False): 
	if smooth == False:
		cord = win32api.GetCursorPos() # (win32api.GetSystemMetrics(0) // 2, win32api.GetSystemMetrics(1) // 2)
		move_to(cord[0] + dx, cord[1] + dy)
	else:
		t = 1000 / SPEED
		for i in range(0, CPS, 2):
			move(int(dx/CPS), int(dy/CPS))
			time.sleep(t/CPS)

if __name__ == '__main__':
	move(1000, 0, smooth=True)