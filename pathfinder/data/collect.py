import cv2
import numpy as np
import win32gui
import win32con
import win32api
import time
import random
import math

def make_window_borderless(hwnd):	
	style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
	style &= ~win32con.WS_OVERLAPPEDWINDOW
	style |= win32con.WS_POPUP
	win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
	win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
	win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

class Point(object):
	def __init__(self, id, size=4, rgb=(0, 255, 255)):
		super(Point, self).__init__()
		self.id = id
		self.name = "mask" + str(id)
		self.size = size
		self.screen = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
		# cv2.namedWindow(self.name, cv2.NORMAL_WINDOW)
		img = np.ones((size, size, 3), np.uint8)
		img[:, :, 0] = rgb[2]
		img[:, :, 1] = rgb[1]
		img[:, :, 2] = rgb[0]
		cv2.imshow(self.name, img)
		self.hwnd = win32gui.FindWindow(0, self.name)
		make_window_borderless(self.hwnd)
		win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWNORMAL)
		win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
		win32gui.MoveWindow(self.hwnd, 0, 0, size, size, True)
		self.hide()

	def move(self, x, y):
		cv2.moveWindow(self.name, x - self.size // 2, y - self.size // 2)
		cv2.waitKey(1)

	def hide(self):
		self.move(self.screen[0] - self.size, self.screen[1] - self.size)

	def move_to_percent(self, dx, dy):
		self.move(self.screen[0] + int((self.screen[2] - self.screen[0]) * dx), self.screen[1] + int((self.screen[3] - self.screen[1]) * dy))

def random_cord():
	screen = (win32gui.GetWindowRect(win32gui.GetDesktopWindow())[2], win32gui.GetWindowRect(win32gui.GetDesktopWindow())[3])
	return (random.randint(0, screen[0]), random.randint(0, screen[1]))

def is_hit(b, size):
	a = win32api.GetCursorPos()
	return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 < (size / 2) ** 2

if __name__ == '__main__':
	trials = 50
	size = 20
	tick = 128
	time_limit = 5
	point = Point(0, size, (0, 0, 0))
	datain = []
	dataout = []

	for i in range(trials):
		a = win32api.GetCursorPos()
		b = random_cord()
		point.move(*b)
		while win32api.GetCursorPos() == a:
			pass
		t = time.time()
		out = [a]
		while not is_hit(b, size):
			time.sleep(1 / tick)
			out.append(win32api.GetCursorPos())
		datain.append([a[0], a[1], b[0], b[1], int((time.time() - t) * 1000)])
		dataout.append(out[:tick * time_limit])

	text = ""
	for data in datain:
		for item in data:
			text += f"{item} "
		text += "\n"
	f = open(f"datain.{int(time.time())}.txt", "w")
	f.write(text)
	f.close()
	text = ""
	for data in dataout:
		for item in data:
			for i in item:
				text += f"{i} "
		text += "\n"
	f = open(f"dataout.{int(time.time())}.txt", "w")
	f.write(text)
	f.close()