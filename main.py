from tkinter import *
from random import randint
import time

#Константы

SIZE_E = 50
SIZE_A = 30
SIZE_X = 1000
SIZE_Y = 1000

#Разлинейка поля

def draw_cells(canv):
	for i in range(0, 1000, 50):
		canv.create_line(i, 0, i, 1000, fill = 'white')
	for i in range(50, 1000, 50):
		canv.create_line(0, i, 1000, i, fill = 'white')

#Инициализация окна

root = Tk()
canv = Canvas(width = SIZE_X, height = SIZE_Y, bg = 'black')
canv.pack()
draw_cells(canv)

#Функция движения

def move(snake):

	body = snake.body
	#print(body, 'x')
	#Устанавливаем координаты змейки вручную
	if snake.direct == 'r':
		head = [body[-1][0] + 1, body[-1][1]]
	if snake.direct == 'u':
		head = [body[-1][0], body[-1][1] - 1]
	if snake.direct == 'd':
		head = [body[-1][0], body[-1][1] + 1]
	if snake.direct == 'l':
		head = [body[-1][0] - 1, body[-1][1]]

	#Каждый блок змейки становится на блока перед ним

	for el in range(len(body) - 1):
		body[el] = body[el + 1]

	#Добавляем голову к телу
	body[-1] = head
	
	#print(body, 'y')
	return body

def check(snake):
	#Проверяем вышла ли змейка за поле и нет ли столкновения блоков
	for el in snake.body:
		if el[0] < 1 or el[0] > SIZE_X // SIZE_E or el[1] < 0 or el[1] > SIZE_Y // SIZE_E or snake.body.count(el) > 1:
			return False
	return True

class Apple:

	#Инициализация
	def __init__(self):

		self.x = randint(1, 10)
		self.y = randint(1, 10)

class Snake:

	#Инициализация
	def __init__(self):
		
		self.len = 4
		self.direct = 'r'
		self.body = []
		start_x = randint(1, 10)
		start_y = randint(1, 20)
		#Формируем тело змейки
		for i in range(4):
			self.body.append([start_x + i, start_y])

#Функция для выхода из игры
def exit_f():
	exit(0)

def draw_snake(Snake, App):
	
	#Чистим поле
	canv.delete('all')
	draw_cells(canv)
	#Если змейка прошла проверку то отрисовываем блоки тела
	if check(snake):
		for el in snake.body:
			canv.create_rectangle((el[0] - 1) * SIZE_E, (el[1] - 1) * SIZE_E, el[0] * SIZE_E, el[1] * SIZE_E, fill = 'green')
		
		if [App.x, App.y] in snake.body:
			if snake.direct == 'r':
				snake.body.append([snake.body[-1][0] + 1, snake.body[-1][1]])
			if snake.direct == 'l':
				snake.body.append([snake.body[-1][0] - 1, snake.body[-1][1]])
			if snake.direct == 'd':
				snake.body.append([snake.body[-1][0], snake.body[-1][1] + 1])
			if snake.direct == 'u':
				snake.body.append([snake.body[-1][0], snake.body[-1][1] - 1])
			snake.len = snake.len + 1
		#Генерируем новую позицию яблока если змейка съела его
		while [App.x, App.y] in snake.body:
			App.x = randint(1, 16)
			App.y = randint(1, 20)
		canv.create_rectangle((App.x - 1) * 50 + 10, (App.y - 1) * 50 + 10, App.x * 50 - 10, App.y * 50 - 10, fill = 'red')
	else:
		#Если змейка не прошла проверку, то выводим результат и прерываем игру
		canv.delete('all')
		canv.create_text(500, 500, text = 'Game over! Score: {}'.format(snake.len - 4), fill = 'yellow')
		root.after(800, exit_f)

#Инициализируем змейку и яблоко и отрисовываем их
snake = Snake()
apple = Apple()
draw_snake(snake, apple)

#Функции для проверки возможности движения в 4 стороны, если движение возможно, то передаём тело в фунцию move
def up_dir(event):
	#print('eee')
	#print(snake.body)
	if snake.body[-2][1] >= snake.body[-1][1]:
		snake.direct = 'u'
		#print(snake.body)
		snake.body = move(snake)
		#print(snake.body)
		draw_snake(snake, apple)

def down_dir(event):
	if snake.body[-2][1] <= snake.body[-1][1]:
		snake.direct = 'd'
		snake.body = move(snake)
		#print(snake.body)
		draw_snake(snake, apple)

def right_dir(event):
	if snake.body[-2][0] <= snake.body[-1][0]:
		snake.direct = 'r'
		snake.body = move(snake)
		#print(snake.body)
		draw_snake(snake, apple)

def left_dir(event):
	if snake.body[-2][0] >= snake.body[-1][0]:
		snake.direct = 'l'
		snake.body = move(snake)
		#print(snake.body)
		draw_snake(snake, apple)

#Если нажата одна из стрелочек, то вызываем соответствующую функцию
root.bind('<Up>', up_dir)
root.bind('<Down>', down_dir)
root.bind('<Right>', right_dir)
root.bind('<Left>', left_dir)

#Функция для автоматического движения змейки
def motion():
	snake.body = move(snake)
	draw_snake(snake, apple)
	root.after(200, motion)

motion()

root.mainloop()