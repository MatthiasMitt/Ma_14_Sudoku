modulname = 'Ma_14_GraphischMT'
_c_ = '(c) 2022copyright: Matthias Mittelstein , Hauptstraße 23, 23816 Neversdorf, und , Am Fahrenberg 8 , 23570 Lübeck-Travemünde , Germany ,, Matthias@Mittelstein.name'
'''
Eine graphische Oberfläche, um sich ein Sudoko lösen zu lassen.
Der Benutzer sieht ein leeres Spielfeld mit 9 mal 9 Kästchen.
Durch anklicken kann man dort eine "1" hineinbekommen. Durch mehrfaches 
Anklicken auch jede andere Ziffer.
wenn die Vorlage gänzlich nachgebildet ist. sollte die "Löse"-Taste
gedrückt werden.

MT = Multi Threaded
'''

from scene import *
# from random import shuffle
#from functools import partial
import sound
import time
import threading
#from Ma_14_SudokuEinfachTS import SudokuEinfachTS
from Ma_14_SudokuEinfach   import SudokuEinfach  

class BildSudoku (Scene):
	
	def setup(self):
		self.bilderzähler = 0
		self.arbeitend    = False
		self.kindTread    = None
		self.kindSudoku   = None
		#self.root_layer = Layer(self.bounds)
		for effect in ['Click_1', 'Click_2', 'Coin_2', 'Coin_5']:
			sound.load_effect(effect)
		
		self.new_game() # self.leeresBlatt()
	
	#def draw(self):
	#	background(0.0, 0.2, 0.3)
	#	self.root_layer.update(self.dt)
	#	self.root_layer.draw()
	
	def leeresBlatt(self):
		#self.root_layer.sublayers = []
		self.kästen = [] # für 9*9 Kästchen
		lücke = 30
		rand  = 5
		landscape = self.size.w > self.size.h
		maxQ = self.size.w if self.size.w < self.size.h else self.size.h
		maxQ -= 10 * rand + 2 * lücke
		kasten_size = maxQ // 9
		width = rand + (kasten_size + rand) * 9 + lücke * 2
		offset = Point((self.size.w - width)/2 + kasten_size/2 ,
		               (self.size.h - width)/2 + kasten_size/2 )
		print( 'jeder Kasten: '+str(kasten_size)+'  w='+str(width)+' offset='+str(offset) )
		for i in range(81):
			x, y = i % 9 , i // 9
			# class scene.SpriteNode([texture, position=(0, 0), z_position=0.0, scale=1.0, x_scale=1.0, y_scale=1.0, alpha=1.0, speed=1.0, parent=None, size=None, color='white', blend_mode=0])
			# class scene.LabelNode(text, font=('Helvetica', 20), *args, **kwargs)
			cx =               ( offset.x + x * (kasten_size + rand) )
			cy = self.size.h - ( offset.y + y * (kasten_size + rand) )
			if x >= 3:
				cx += lücke
			if x >= 6:
				cx += lücke
			if y >= 3:
				cy -= lücke
			if y >= 6:
				cy -= lücke
			#deb print(x,cx,y,cy)
			kasten = LabelNode( ' '
			                , font=('Helvetica', 36)
			                , position=(cx,cy)
			                , color=(x/18+0.5,y/18+0.5,0.5,1)
			                )
			kasten.texture = Texture('Mouse_Face')
			kasten.background = (0.2,0.2,0.3,1)
			self.add_child(kasten)
			self.kästen.append([kasten,0,x,y])
			
		if landscape:
			cx = self.size.w - 50
			cy = self.size.h /  2
		else:
			cx = self.size.w /  2
			cy = self.size.h - 30
		self.kommandoLöse = LabelNode( 'Löse !'
			                           , font=('Helvetica', 36)
			                           , position=(cx,cy)
			                           , color=(0.1,1,0.1,1)
			                           )
		self.add_child(self.kommandoLöse)
		self.touch_disabled = False
	
	def touch_began(self, touch):
		if self.touch_disabled or len(self.kästen) == 0:
			return
		for kasten in self.kästen:
			if touch.location in kasten[0].frame:
				zahl = kasten[1]
				zahl += 1
				if zahl > 9:
					zahl = 0
				zahlStr = str(zahl) if zahl > 0 else ' '
				kasten[1] = zahl
				kasten[0].text = zahlStr
				#sound.play_effect('Click_1')
				break
		if touch.location in self.kommandoLöse.frame:
			self.kommandoLöse.text = 'arb.' # das wird aber nicht sofort sichtbar !
			self.kindSudoku = SudokuEinfach() #SudokuEinfachTS()
			st = ''
			for kasten in self.kästen:
				st = st + str(kasten[1])
			print('Setze :'+str(st))
			self.kindSudoku.setzeFeld1(st)
			self.kindSudoku.setzeVerbose(1)
			print('Löse !')
			sound.play_effect('Click_1')
			print('sleep(1.03)')
			#time.sleep(1.03)
			
			anz4kB = 140 # gut 120 # 80  # 40
			try:
				print(str(threading.stack_size()))
				print('threading.stack_size(int(...*4*1024))')
				threading.stack_size(int(anz4kB*4*1024))
			except AttributeError as e: 
				print(e)
				print('threading.stack_size(int(...*4*1024)) --> AttributeError')
				threading.stack_size(int(77))
			except ValueError as e: 
				print(e)
				print('threading.stack_size(int(...*4*1024)) --> ValueError')
				threading.stack_size(int(88))
			print(str(threading.stack_size()))
			
			
			
			print('Tread')
			self.kindTread = threading.Thread( target=self.kindSudoku.löse, name='kindSudoku' )
			'''
						This constructor should always be called with keyword arguments. Arguments are:
						
						group should be None; reserved for future extension when a ThreadGroup class is implemented.
						
						target is the callable object to be invoked by the run() method. Defaults to None, meaning nothing is called.
						
						name is the thread name. By default, a unique name is constructed of the form “Thread-N” where N is a small decimal number.
						
						args is the argument tuple for the target invocation. Defaults to ().
						
						kwargs is a dictionary of keyword arguments for the target invocation. Defaults to {}.
			'''
			print('kindTread.start')
			self.kindTread.start() # ruft dann 'run()'
			self.arbeitend = True
			sound.play_effect('Coin_2')
			# Wann self.kindTread.join()
			#print('Gelöst ?')
			#self.kindSudoku.printZahlenSchön()
			#self.delay(10.5, partial(sound.play_effect, 'Powerup_2'))
			#self.bildVomKind()
					#deb jj = 0
					#deb jk = 37 / jj
					#self.draw()
			#self.kindSudoku.printAbschlussbericht()
			# self.root_layer.remove_layer()
			#self.delay(10.5, partial(sound.play_effect, 'Powerup_2'))
			#raise 
	
	def bildVomKind(self):
		for z in range(9):
			for s in range(9):
				zahl,grund = self.kindSudoku.gebeZahlOS(z,s)
				#deb print('...',z,s,'-->',zahl,grund)
				self.kästen[z*9+s][0].text = str(zahl)
				self.kästen[z*9+s][1]      =     zahl
				if grund == 'geraten':
					col = (1,0,0,1)
				elif grund == 'Aufgabe':
					col = (0.4,0.4,1,1)
				elif zahl == 0:
					col = (0.1,0.3,0.1,1)
				else:
					col = (0,1,0,1)
				self.kästen[z*9+s][0].color = col
					
	def update(self):
		self.bilderzähler += 1
		dt = self.dt # float: delta time
		#deb print('Bild '+str(self.bilderzähler)+' nach '+str(round(dt,3))+' s')

		if self.arbeitend:
			self.bildVomKind()
			if self.kommandoLöse != None:
				self.kommandoLöse.font = font=('Helvetica', 12 )
				self.kommandoLöse.text = str(self.bilderzähler) + ' / ' + str(self.kindSudoku.gebeUnbekannt())
		else:
			if self.kommandoLöse != None:
				self.kommandoLöse.font = font=('Helvetica', 12 )
				self.kommandoLöse.text = str(self.bilderzähler) + ' / ' + 'n.a.'
				
	def discard_selection(self):
		None
	
	def check_selection(self):
		None
	
	def new_game(self):
		sound.play_effect('Coin_2')
		self.leeresBlatt()
	#	self.root_layer.animate('scale_x', 1.0)
	#	self.root_layer.animate('scale_y', 1.0)
	
	def win(self):
		self.delay(0.5, partial(sound.play_effect, 'Powerup_2'))
		font_size = 100 if self.size.w > 700 else 50
		text_layer = TextLayer('Well Done!', 'Futura', font_size)
		text_layer.frame.center(self.bounds.center())
		overlay = Layer(self.bounds)
		overlay.background = Color(0, 0, 0, 0)
		overlay.add_layer(text_layer)
		self.add_layer(overlay)
		overlay.animate('background', Color(0.0, 0.2, 0.3, 0.7))
		text_layer.animate('scale_x', 1.3, 0.3, autoreverse=True)
		text_layer.animate('scale_y', 1.3, 0.3, autoreverse=True)
		self.touch_disabled = True
		self.root_layer.animate('scale_x', 0.0, delay=2.0,
								curve=curve_ease_back_in)
		self.root_layer.animate('scale_y', 0.0, delay=2.0,
								curve=curve_ease_back_in,
								completion=self.new_game)


run(BildSudoku())
