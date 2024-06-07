modulname = 'Ma_14_SudokuEinfachTS'
_c_ = '(c) 2022 copyright: Matthias Mittelstein , Hauptstraße 23, 23816 Neversdorf, and , Am Fahrenberg 8 , 23570 Lübeck , Germany ,, Matthias@Mittelstein.name'
'''
Das Spiel 'Sudoku'.
Diese Klasse implentiert ein Spielfeld.
Das Feld kann mit einigen Ziffern vorgefüllt werden
und dann eine automatische Befüllung aller anderen
Kästchen beauftragt wird. 
Falls es mehrere Lösungen gibt, wird von den
Methoden dieser Basisklasse nur eine gefunden.

TS = threat safe = für Mehrprozessbetrieb geeignet
'''

import copy
import random
import threading
from   Ma_14_Rahmen import Rahmen
import time


class SudokuVerklemmt(Exception):
	
	def __init__(self,text,zeile,spalte,rateTiefe):
		self.text        = text
		self.zeile       = zeile
		self.spalte      = spalte
		self.rateTiefe   = rateTiefe
		
		
		
	
	
class SudokuEinfachTS():
	#hier:
	# feld        = []
	# unbekannt   = 81
	# rateTiefe   = 0
	# verbose     = 9
	# rateHinweis = 0 # 0=kleinste, 1=Zufall, 2=größte
	# anzahlRaten = 0
	#
	# TS = threat safe = für Mehrprozessbetrieb geeignet
	
	def __init__(self):
		#elf.feld        = []
		#elf.unbekannt   = 81
		self.rateTiefe   = 0
		self.verbose     = 9
		self.rateHinweis = 0 # 0=kleinste, 1=Zufall, 2=größte
		#elf.anzahlRaten = 0
		self.bremse      = 0.1 # Sekunden
		self.rlock       = threading.RLock()
		self.lösche()
	
	def lösche(self):
		#def baueLeeresFeld():
		self.rlock.acquire()
		self.feld =[]
		for z in range(9):
			zeile = []
			for s in range(9):
				zeile.append( [ #deb (z+1)*10+s+1
				              0 ,True,True,True,True,True,True,True,True,True])
			self.feld.append( zeile )
		self.unbekannt   = 9*9
		self.anzahlRaten = 0
		self.rlock.release()
		
	def setzeVerbose(self,plaudergrad):
		# ohne rlock
		if plaudergrad >= 0:
			self.verbose = plaudergrad
		else:
			self.verbose = 0
	
	def setzeFeld9(self,neunStrings):
		self.rlock.acquire()
		unbekannt = 0
		for z in range(9):
			for s in range(9):
				zahl = neunStrings[z][s]
				if zahl == ' ' or zahl == '.' or zahl == '0':
					self.setzeZahl(z,s,0)
					unbekannt += 1
				else:
					self.setzeZahl(z,s,int(zahl),grund='Aufgabe')
		# Die setzte...-Methoden haben zwar versucht zu zählen.
		# Aber da dies keine Änderungen sondern initiales Setzen 
		# war, war das Zählen zwecklos, Also:
		self.unbekannt   = unbekannt
		#war falsch bis 2020-04-10.09:02 self.anzahlRaten = 0
		self.rlock.release()
		
	def setzeFeld1(self,einString):
		self.rlock.acquire()
		unbekannt = 0
		for z in range(9):
			for s in range(9):
				zahl = einString[z*9+s]
				if zahl == ' ' or zahl == '.' or zahl == '0':
					self.setzeZahl(z,s,0)
					unbekannt += 1
				else:
					self.setzeZahl(z,s,int(zahl),grund='Aufgabe')
		# Die setzte...-Methoden haben zwar versucht zu zählen.
		# Aber da dies keine Änderungen sondern initiales Setzen 
		# war, war das Zählen zwecklos, Also:
		self.unbekannt   = unbekannt
		#war falsch bis 2020-04-10.09:02 self.anzahlRaten = 0
		self.rlock.release()
	
	def gebeFeld1(self,leer='.'):
		self.rlock.acquire()
		fs = ''
		for z in range(9):
			for s in range(9):
				zahl = self.feld[z][s][0]
				if zahl != 0:
					fs += str(zahl)
				else:
					fs += leer
		self.rlock.release()
		return fs
	
	def löscheZahl(self,z,s):
		self.rlock.acquire()
		vorher = self.feld[z][s][0]
		self.feld[z][s] = [0,True,True,True,True,True,True,True,True,True]
		if vorher != 0:
			self.unbekannt += 1
		self.rlock.release()
	
	def setzeZahl(self,z,s,zahl,grund=''):
		self.rlock.acquire()
		if zahl == 0:
			self.löscheZahl(z,s)
		else:
			vorher = self.feld[z][s][0]
			self.feld[z][s] = [zahl,False,False,False,False,False,False,False,False,False]
			if grund != '':
				self.feld[z][s].append(grund )
			if zahl >= 1 and zahl <= 9:
				self.feld[z][s][(zahl-1+1)] = True
			if vorher == 0:
				self.unbekannt -= 1
		self.rlock.release()
	
	def setzeRateKleinste(self):
		# ohne rlock
		self.rateHinweis = 0
	
	def setzeRateGrößte(self):
		# ohne rlock
		self.rateHinweis = 2
	
	def setzeRateZufällig(self):
		# ohne rlock
		self.rateHinweis = 1
		
	def getZahlenVonZeile(self,z,s):
		self.rlock.acquire()
		erg = []
		for si in  range(9):
			zahl = self.feld[z][si][0]
			if zahl != 0:
				erg.append(zahl)
		self.rlock.release()
		return erg
			
	def getZahlenVonSpalte(self,z,s):
		self.rlock.acquire()
		erg = []
		for zi in  range(9):
			zahl = self.feld[zi][s][0]
			if zahl != 0:
				erg.append(zahl)
		self.rlock.release()
		return erg
	
	def getZahlenVonQuadrat(self,z,s):
		self.rlock.acquire()
		erg = []
		zq = int(z/3)
		sq = int(s/3)
		for zi in zq*3, zq*3+1, zq*3+2 :
			for si in sq*3, sq*3+1, sq*3+2 :
				zahl = self.feld[zi][si][0]
				#deb print(zi,si,zahl)
				if zahl != 0:
					erg.append(zahl)
		self.rlock.release()
		return erg
		
	def getVerboteneZahlen(self,z,s):
		self.rlock.acquire()
		erg = self.getZahlenVonZeile(z,s)
		erg.extend(self.getZahlenVonSpalte(z,s))
		erg.extend(self.getZahlenVonQuadrat(z,s))
		#erg.sort()
		#erg.unique()
		self.rlock.release()
		return erg
	
	def verbieteZahlen(self,z,s):
		self.rlock.acquire()
		verboten = self.getVerboteneZahlen(z,s)
		#deb print(z,s,':verboten:',verboten)
		for zahl in verboten:
			self.feld[z][s][zahl-1+1] = False
		anzahlVerboten = 0
		for zahlIndex in range(9):
			zahl = zahlIndex + 1
			if self.feld[z][s][zahlIndex+1]:
				erlaubtZB = zahl # überschreibbar, die letzte bleibt sichtbar
			else:
				anzahlVerboten += 1
		if anzahlVerboten == 8:
			self.setzeZahl(z,s,erlaubtZB)
			self.rlock.release()
		elif anzahlVerboten > 8:
			if self.verbose >= 2:
				print('   Im Kasten '+str(z+1)+','+str(s+1)+' ist nichts mehr möglich !')
			self.rlock.release()
			raise SudokuVerklemmt('Keine Zahl mehr erlaubt in ',z+1,s+1,self.rateTiefe)
		else:
			self.rlock.release()
	
	def verbieteZahlenÜberall(self):	
		for z in range(9):
			for s in range(9):
				self.rlock.acquire()
				if self.feld[z][s][0] == 0:
					schonAcht = self.verbieteZahlen(z,s)
				self.rlock.release()
				# Möchte jemand anders auch mal ?
				print('sleep("5") z='+str(z+1)+' s='+str(s+1))
				time.sleep(self.bremse) 
	
	def löseDirekt(self):
		self.rlock.acquire()
		vorher = 777
		noch = self.unbekannt
		sperre = 100
		while noch > 0 and sperre > 0 and noch < vorher:
			
			self.rlock.release()
			# Möchte jemand anders auch mal ?
			print('sleep("4")')
			time.sleep(self.bremse)
			self.rlock.acquire()
			if noch > 0 and sperre > 0 and noch < vorher: # immer noch?
			
				vorher = noch
				self.verbieteZahlenÜberall()
				noch = self.unbekannt
				sperre -= 1
				if self.verbose >= 1:
					print('noch unbekannt: '+str(noch))
		self.rlock.release()
		
	def löse(self,context=None):
		# context ist hier unbenutzt.
		
		if self.verbose >= 5:
			print('   ==> löse() mit self.unbekannt: '+str(self.unbekannt))
		self.löseDirekt() # rlock.t sich selbst
		
		self.rlock.acquire()
		while self.unbekannt > 0:
			self.rlock.release()
			# Möchte jemand anders auch mal ?
			print('sleep("1")')
			time.sleep(0.11)
			self.rlock.acquire()
			if self.unbekannt > 0: # immer noch?
				if self.verbose >= 1:
					print('   Ich muss raten.')
				for z in range(9):
					for s in range(9):
						if self.feld[z][s][0] == 0:
							# Dieser Kasten ist noch leer.
							if self.rateHinweis == 1:
								alleIndices = random.sample(range(9),k=9)
							elif self.rateHinweis == 2:
								alleIndices = range(8,-1,-1)
							else:
								alleIndices = range(9)
							for zahlIndex in alleIndices:
								if self.feld[z][s][1+zahlIndex]: # Diese Zahl wäre noch erlaubt
									self.anzahlRaten += 1
									zahl = zahlIndex + 1
									nochHeilesSpiel = copy.deepcopy(self.feld) , self.unbekannt
									self.setzeZahl(z,s,zahl,grund='geraten')
									self.rlock.release()
									print('sleep("2")')
									time.sleep(0.12)
									self.rateTiefe += 1
									try:
										if self.verbose >= 2:
											print('   In Kästchen '+str(z+1)+','+str(s+1)
											       +' probiere ich '+str(zahl)+' . Ratetiefe:'
											       + str(self.rateTiefe-1)+'-->'+str(self.rateTiefe))
										
										self.löse()
										
										# Here is an invisible break from the for-loop.
										# A successful solution will clear the condition
										#  self.feld[z][s][0] == 0
										#   for all higher (or other) digits.
									except SudokuVerklemmt as err:
										if self.verbose >= 2:
											print('   Sackgasse: ',err.text,err.zeile,err.spalte
											     , ' .')
										self.feld , self.unbekannt = nochHeilesSpiel
										if self.verbose >= 1:
											print(str(self.unbekannt) +
											      ' <-- Jetzt sind wieder mehr unbekannt.')
									if self.verbose >= 2:
										print('   Ratetiefe: '+str(self.rateTiefe-1)+' <-- '+str(self.rateTiefe))
									self.rateTiefe -= 1
									self.rlock.acquire()
								#endif Diese Zahl wäre noch erlaubt
							#endfor zahlIndex
							
							# Ich bin auf dem Aufstiegsweg aus der löse()-Rekursion.
								
							if self.unbekannt > 0:
								if self.verbose >= 2:
									print('   In Kästchen '+str(z+1)+','+str(s+1)+' alles durchprobiert')
								self.rlock.release()
								raise SudokuVerklemmt('jede Möglichkeit durchprobiert ',z+1,s+1
								                     ,self.rateTiefe)
						#endif Kasten leer
					#endfor s
				#endfor z
			#endif immer noch
		#endwhile unbekannt
		self.rlock.release()
	
	def gebeUnbekannt(self):
		self.rlock.acquire()
		erg = self.unbekannt
		self.rlock.release()
		return erg
	
	def gebeAnzahlRaten(self):
		self.rlock.acquire()
		return self.anzahlRaten
		self.rlock.release()
	
	def gebeZahl(self,z,s):
		self.rlock.acquire()
		zahl = self.feld[z][s][0]
		if len(self.feld[z][s]) > 1+9:
			grund = self.feld[z][s][10]
		else:
			grund = ''
		self.rlock.release()
		return zahl,grund
		
	def gebeZahlOS(self,z,s): # ohne Sperre
		#self.rlock.acquire()
		zahl = self.feld[z][s][0]
		if len(self.feld[z][s]) > 1+9:
			grund = self.feld[z][s][10]
		else:
			grund = ''
		#self.rlock.release()
		return zahl,grund
		
	def printZahlen(self):
		self.rlock.acquire()
		for z in range(9):
			for s in range(9):
				print( self.feld[z][s][0], end = '  ')
			print()
		self.rlock.release
			
	def printZahlenSchön(self,leer='.'):
		self.rlock.acquire()
		print('|-----------|-----------|-----------|')
		for z in range(9):
			print('| ',end='')
			for s in range(9):
				zahl = self.feld[z][s][0]
				if zahl:
					print(zahl, end = ' ')
				else:
					print(leer, end = ' ')
				if s % 3 == 2:
					print('|', end = ' ')
				else:
					print(' ', end = ' ')
			print()
			if z % 3 == 2:
				print('|-----------|-----------|-----------|')
			#elses:
			#	print()
		self.rlock.release()
	
	def printZahlenSehrSchön(self,einVon=1,leer='.'):
		'''
		einVon : wieviel Sudokubilder sollen auf eine Bildschirmseite
		         bei Hochkantausgabe passen?
		         Sinnvolle (und erwartete) Werte: 1, 2 oder 3
		'''
		self.rlock.acquire()
		if einVon == 2:
			fs = 18
		elif einVon == 3:
			fs = 12
		else: # == 1
			fs = 32
		r = Rahmen()
		r.setzeSchriftgröße(points=fs)
		print(r.gebeS81a1SehrSchön(self.gebeFeld1(leer=leer)))
		r.setzeNormaleSchrift()
		self.rlock.release()
	
	
	def gebeZahlenSehrSchön(self):
		self.rlock.acquire()
		r = Rahmen()
		f = self.gebeFeld1(leer=' ')
		ret = r.gebeS81a1SehrSchön(f)
		self.rlock.release()
		return ret
		
	
	
	def gebeVergleichS81a1(self,r9x9,selbstLinks=True):
		self.rlock.acquire()
		r = Rahmen()
		l = self.gebeFeld1()
		if selbstLinks:
			rs = r.gebeS81a1PaarSehrSchön(l,r9x9)
		else:
			rs = r.gebeS81a1PaarSehrSchön(r9x9,l)
		self.rlock.release()
		return rs
		
	def printFeld(self):
		self.rlock.acquire()
		for z in range(9):
			for s in range(9):
				if self.feld[z][s][0] :
					print( self.feld[z][s][0], end = '        ')
				else:
					for n in range(9):
						if self.feld[z][s][n+1]:
							print('.',end = '')
						else:
							print('-',end = '')
				print(' ', end='')
			print()
		self.rlock.release()
	
	def printFeldDetails(self):
		self.rlock.acquire()
		for z in range(9):
			# 1. Teilzeile
			for s in range(9):
				print( self.feld[z][s][0], end = '         ')
			print()
			# 2. Teilzeile
			for s in range(9):
				for n in range(9):
					if self.feld[z][s][n+1]:
						print('+',end = '')
					else:
						print('-',end = '')
				print(' ', end='')
			print()
			# 3. Teilzeile
			for s in range(9):
				if len(self.feld[z][s]) > 1+9 :
					print( '{0:9s} '.format(self.feld[z][s][10]), end = '')
				else:
					print( '{0:9s} '.format(' '), end = '')
			print()
		self.printUnbekannt()
		self.rlock.release()
	
	def printUnbekannt(self):
		self.rlock.acquire()
		print( 'noch unbekannt: ', self.unbekannt )
		self.rlock.release()
	
	def printAbschlussbericht(self):
		self.rlock.acquire()
		if self.unbekannt == 0:
			print('Die Sudoku-Aufgabe ist gelöst.')
		else:
			print('Die Sudoku-Aufgabe ist noch nicht gelöst!')
			print('Es sind noch '+str(self.unbekannt)+' Felder nicht besetzt.')
		self.rlock.release()
		
if __name__ == '__main__':
	print(modulname,'  --  Selbsttest')
		
	f = SudokuEinfachTS()
	f.lösche()
	f.printZahlen()
	f.setzeZahl(3,4,0)
	f.setzeZahl(4,5,6)
	f.printFeld()
	f.printFeldDetails()
	
	f.setzeFeld9(['.9.   8.3'
	             ,'7149  ...'
	             ,'... 12...'
	             ,'6 8...95 '
	             ,'45 6..   '
	             ,'   .45 7 '
	             ,'...49 ...'
	             ,'... 7 16.'
	             ,'2..3  ..7'])
	f.printFeldDetails()
	print('Spalte(1,3) : ',f.getZahlenVonSpalte(1,3))
	print('Zeile(1,3)  : ',f.getZahlenVonZeile(1,3))
	print('Quadrat(1,3): ',f.getZahlenVonQuadrat(1,3))

	test = 2
	if test == 1:
		f.verbieteZahlenÜberall()
		f.printFeldDetails()
		f.verbieteZahlenÜberall()
		f.printFeldDetails()
		f.verbieteZahlenÜberall()
		f.printUnbekannt()
		f.verbieteZahlenÜberall()
		f.printUnbekannt()
		f.verbieteZahlenÜberall()
		f.printUnbekannt()
		f.verbieteZahlenÜberall()
		f.printUnbekannt()
		f.verbieteZahlenÜberall()
		f.printUnbekannt()
		f.verbieteZahlenÜberall()
		f.printFeld()
		f.printUnbekannt()
	elif test == 2:
		print('Test printZahlenSchön ... ')
		f.printZahlenSchön()
		print('Test printZahlenSehrSchön ... ')
		f.printZahlenSehrSchön()
		print('Test löseDirekt ... ')
		f.löseDirekt()
		print('Test printZahlenSchön ... ')
		f.printZahlenSchön()
		print('Test print(gebeZahl(3,4)) ... ')
		print(f.gebeZahl(3,4))
		print('Test printAbschlussbericht ... ')
		f.printAbschlussbericht()
		print('')
		print('Test print(gebeZahlenSehrSchön)')
		print(f.gebeZahlenSehrSchön())
		print('Test print(gebeFeld1) ... ')
		print(f.gebeFeld1())
		print('Test gebe2x9x9SehrSchön ... ')
		print(' -fehlt- ')
		print('Test gebeVergleichS81a1 ... ')
		s1 = f.gebeFeld1()
		s2 = s1[0:11] + 't' + s1[12:]
		print(f.gebeVergleichS81a1(s2,selbstLinks=False))
	elif test == 3:
		f.löse()
		f.printAbschlussberichtc()
