import pygame, sys, random
from pygame import mixer
from pygame.locals import *
from pygame.constants import K_ESCAPE, K_SPACE, KEYUP
from network import Network

WIDTHOFSCREEN = 1000
HEIGHTOFSCREEN = 600

pygame.init()
#Set music
mixer.init()
mixer.music.load('music.mp3')
mixer.music.set_volume(0.5)
#mixer.music.play()



class Baddie():

	def __init__(self, xBaddie, yBaddie, sizeBaddie, speedBaddie):
		self.xBaddie = xBaddie
		self.yBaddie = yBaddie
		self.sizeBaddie = sizeBaddie
		self.speedBaddie = speedBaddie

		'''self.maxSizeOfObtacle= 100
		self.minSizeOfObtacle= 100
		self.maxSpeedOfObtacle = 5
		self.minSpeedOfObtacle = 2

		self.sizeOfE = 50'''

	def baddie_trajectory(self):
		self.yBaddie += self.speedBaddie

class Bullet():
	def __init__(self, xBullet, yBullet):
		self.xBullet = xBullet
		self.yBullet = yBullet
		self.sizeBullet = 30
		self.speedBullet = 4
		
		self.bulletSound = mixer.Sound('laser.wav')

	def sound(self):  # Âm thanh bắn
		self.bulletSound.play()

	def bulletPath(self):
		self.yBullet -= self.speedBullet
	
class Player():
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.speed = 3
		self.score = 0

		self.moveUp = self.moveDown = self.moveLeft = self.moveRight = False
		
		self.fire = False
		self.numberBullet = 5
		self.listBullet = []

	def move(self):
		if self.moveLeft & (self.x > 0):
			self.x -= self.speed
		if self.moveRight & (self.x + self.width < WIDTHOFSCREEN):
			self.x += self.speed
		if self.moveUp & (self.y > 0):
			self.y -= self.speed 
		if self.moveDown & (self.y + self.height < HEIGHTOFSCREEN):
			self.y += self.speed

	def fireBullet(self):
		if len(self.listBullet) < self.numberBullet:			
			newBullet = Bullet(self.x + self.width/2 - 25, self.y - self.height/2)
			newBullet.sound()
			self.listBullet.append(newBullet)	

class Game():

	def __init__(self):
		self.network = Network()
		self.t1 = Player(200,500,50,50)
		self.t2 = Player(800,500,50,50)
		self.players = [self.t1 , self.t2]
		self.canvas = Canvas()
		self.listE = []
		self.id = self.network.id
		if self.id == 1:
			self.urlPlayer1='planes.png'
			self.urlPlayer2='planes2.png'
		else:
			self.urlPlayer1='planes2.png'
			self.urlPlayer2='planes.png'

	def addnewBaddie(self):

		if (len(self.listE) < 6):
			sendDataE = str(self.network.id) + ':' + '-2'

			xE = self.receiveDataAboutE(self.sendData(sendDataE))

			if xE == -5:
				newBaddie = Baddie(random.randint(0, self.canvas.widthOfWin - 100), 5, 40, 0.5)
				self.listE.append(newBaddie)

				sendDataNewE = str(self.network.id) + ':' + str(newBaddie.xBaddie)
				print('data e random '+ sendDataNewE)
				checkSuccess = self.receiveDataAboutE(self.sendData(sendDataNewE))
				if checkSuccess != -1:
					print('check -1')
					return False
			else:
				newBaddie = Baddie(xE, 5, 40, 0.5)
				self.listE.append(newBaddie)

		return True

	def sendData(self, data):
		print('data se gui: '+ data)
		mess = self.network.send(data)
		return mess

	def receiveDataAboutE(self, dataE):
		try:
			print("data nhan ve "+ dataE)

			if len(dataE) <= 6:
				dataEAboutPosition = dataE.split(':')[1]
				return int(dataEAboutPosition)

		except:
			print('loi nhan e')

	def redrawE(self):
		for enemy in self.listE:
			print ("toa do cua xE " + str(enemy.xBaddie))
			self.canvas.image_draw('virus.png', enemy.xBaddie, enemy.yBaddie, enemy.sizeBaddie, enemy.sizeBaddie)
			enemy.baddie_trajectory()
			if enemy.yBaddie > 1000: 
				self.listE.remove(enemy)

	def checkBulletsCollision(self, listBullet):
		for bullet in listBullet:
			if self.checkedCollision(bullet.xBullet, bullet.yBullet, bullet.sizeBullet, bullet.sizeBullet):
				listBullet.remove(bullet)
				return True

	def checkedCollision(self, xObj, yObj, widthOfObj, heightOfObj):
		for enemy in self.listE:
			checkHeadX = enemy.xBaddie <= xObj <= enemy.xBaddie + enemy.sizeBaddie
			checkTailX = enemy.xBaddie <= xObj + widthOfObj <= enemy.xBaddie + enemy.sizeBaddie
			checkHeadY = enemy.yBaddie <= yObj <= enemy.yBaddie + enemy.sizeBaddie
			checkTailY = enemy.yBaddie <= yObj + heightOfObj <= enemy.yBaddie + enemy.sizeBaddie
				
			if checkHeadX or checkTailX:
				if checkHeadY or checkTailY:
					self.listE.remove(enemy)
					return True
		return False

	def sendDataAboutPlayer(self): #send data of player t1 to server
		fireConvertInInt = lambda x: 1 if x else 0

		data = str(self.network.id) + ':' + str(self.t1.x) + ',' + str(self.t1.y) + ';' + str(fireConvertInInt(self.t1.fire))
		#print('client send: ' + data)
		mess = self.network.send(data)
		return mess

	def receiveDataAboutPlayer(self, data): #receive data from server then set for player t2
		try:
			#print(data)
			dataWithoutId = data.split(':')[1].split(';') 
			dataAboutPosition = dataWithoutId[0].split(',')
			dataAboutFireOrNot = dataWithoutId[1]
			fireConvertIntToBool = lambda x: True if x == '1' else False
			
			return int(dataAboutPosition[0]), int(dataAboutPosition[1]), fireConvertIntToBool(dataAboutFireOrNot)
		except:
			print('loi')
			return 0,0

	def receiveScore(self, data):
		try:
			print("data nhan ve "+ data)
			score = dataE.split(':')[1]
			return int(score)
		except:
			print('loi nhan e')

	def run(self):
		clock = pygame.time.Clock()
		run = True

		while run:
			clock.tick(60) #set fps=60

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
				if event.type == K_ESCAPE:
					run = False

				if event.type == KEYDOWN:
					if event.key == pygame.K_DOWN :
						self.t1.moveDown = True
					if event.key == pygame.K_UP:
						self.t1.moveUp = True
					if event.key == pygame.K_LEFT :
						self.t1.moveLeft = True
					if event.key == pygame.K_RIGHT:
						self.t1.moveRight = True
					if event.key == pygame.K_SPACE:
						self.t1.fire = True
	
				if event.type == KEYUP:	#make all key become 
					if event.key == pygame.K_DOWN :
						self.t1.moveDown = False
					if event.key == pygame.K_UP: 
						self.t1.moveUp = False
					if event.key == pygame.K_LEFT:
						self.t1.moveLeft = False
					if event.key == pygame.K_RIGHT:
						self.t1.moveRight = False
					
			#take new coordinates for player t1 and 2
			self.t1.move()
			#send data about t1 and receive data about player 2 from server
			self.t2.x, self.t2.y, self.t2.fire = self.receiveDataAboutPlayer(self.sendDataAboutPlayer())
			
			self.canvas.drawScreen() #priority command
			self.canvas.drawText('Player 1: %s' %self.t1.score, 20, 10, 48)
			self.canvas.drawText('Player 2: %s' %self.t2.score, 650, 10, 48)

			if self.addnewBaddie() == False:
				run = False

			self.redrawE()
			
			#use for both player t1 and t2
			for player in self.players:
				#fire Bullet
				if player.fire:
					player.fireBullet()
					player.fire = False
				self.canvas.reDrawListBulet(player.listBullet)
				
				#move both player on screen
				#self.canvas.image_draw('planes.png', player.x, player.y, player.width, player.height)
				self.canvas.image_draw(self.urlPlayer1, self.t1.x, self.t1.y, self.t1.width, self.t1.height)
				self.canvas.image_draw(self.urlPlayer2, self.t2.x, self.t2.y, self.t2.width, self.t2.height)
				
				#check player's bullet hitted enemy yet
				if self.checkBulletsCollision(player.listBullet):
					player.score += 100

				#check player hit 
				if self.checkedCollision(player.x, player.y, player.width, player.height):
					run = False
					

			self.canvas.updateScreen()
		

		#when game over	
		#self.t2.score = receiveScore(sendData(str(self.id) + ':' + '-3' + ':' + str(self.t1.score)))
		pygame.mixer.music.stop()

		#gameOverSound.play() #turn on gameOver music
		self.canvas.drawScreen()
		self.canvas.drawText('GAME OVER', 450, 200, 48)
		self.canvas.drawText('Player 1: %s' %self.t1.score, 300, 250, 48)
		self.canvas.drawText('Player 2: %s' %self.t2.score, 300, 300, 48)
		self.canvas.updateScreen()

		run = True
		while run:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
				if event.type == K_ESCAPE:
					run = False

		pygame.quit()

	


class Canvas():

	def __init__(self):
		self.widthOfWin = WIDTHOFSCREEN
		self.heightOfWin = HEIGHTOFSCREEN
		self.screen = pygame.display.set_mode((self.widthOfWin, self.heightOfWin))
		self.background = pygame.image.load('background.jpg')
		self.playerImage = pygame.image.load('planes.png')
		self.urlImageBullet = 'bullet.png'
		pygame.display.set_caption('Shoot & Dodge')

	def image_draw(self, url, x, y, xImg, yImg):  # In ra hình ảnh
			objImg = pygame.image.load(url)
			objImg = pygame.transform.scale(objImg, (xImg, yImg))  # change size image
			self.screen.blit(objImg, (x, y))

	def drawScreen(self):
		self.screen.blit(self.background,  (0,0))

	def updateScreen(self):
		pygame.display.update()

	def drawText(self, text, x, y, size):
		font = pygame.font.SysFont('comicsans', size)
		textobj = font.render(text, 1, (255,255,255))
		textrect = textobj.get_rect()
		textrect.topleft = (x, y)
		self.screen.blit(textobj, textrect)

	def reDrawListBulet(self, listBullet):
		for bullet in listBullet:
			self.image_draw('bullet.png', bullet.xBullet, 
					bullet.yBullet, bullet.sizeBullet, bullet.sizeBullet)  # In ra bullet
			#self.listBullet[index].drawBullet()
			bullet.bulletPath()
			if bullet.yBullet <= 5:  # nếu toạn độ Y phía trên nàm hình thì xóa
				listBullet.remove(bullet)

	
if __name__ == '__main__': #make the program run correctly
	game =Game()
	game.run()