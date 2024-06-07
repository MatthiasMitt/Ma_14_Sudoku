modulname = 'Ma_14_SudokuEinfach'
_c_ = '(c) 2020 copyright: Matthias Mittelstein , Hauptstraße 23, 23816 Neversdorf, Germany ,, Matthias@Mittelstein.name'
'''
Das Spiel 'Sudoku'.
Diese Klasse implentiert ein Spielfeld.
Das Feld kann mit einigen Ziffern vorgefüllt werden
und dann eine automatische Befüllung aller anderen
Kästchen beauftragt wird. 
Falls es mehrere Lösungen gibt, wird von den
Methoden dieser Basisklasse nur eine gefunden.
'''

import copy
import random
import time
from   Ma_14_Rahmen import Rahmen


class SudokuVerklemmt(Exception):
	
	def __init__(self,text,zeile,spalte,rateTiefe):
		self.text        = text
		self.zeile       = zeile
		self.spalte      = spalte
		self.rateTiefe   = rateTiefe
		
	
	
class SudokuEinfach():
	#hier:
	# feld        = []
	# unbekannt   = 81
	# rateTiefe   = 0
	# verbose     = 9
	# rateHinweis = 0 # 0=kleinste, 1=Zufall, 2=größte
	# anzahlRaten = 0
	
	def __init__(self):
		#elf.feld        = []
		#elf.unbekannt   = 81
		self.rateTiefe   = 0
		self.verbose     = 9
		self.rateHinweis = 0 # 0=kleinste, 1=Zufall, 2=größte
		#elf.anzahlRaten = 0
		self.bremse      = 0.001 # 0.1 # Sekunden
		self.lösche()
	
	def lösche(self):
		#def baueLeeresFeld():
		self.feld =[]
		for z in range(9):
			zeile = []
			for s in range(9):
				zeile.append( [ #deb (z+1)*10+s+1
				              0 ,True,True,True,True,True,True,True,True,True])
			self.feld.append( zeile )
		self.unbekannt   = 9*9
		self.anzahlRaten = 0
		
	def setzeVerbose(self,plaudergrad):
		if plaudergrad >= 0:
			self.verbose = plaudergrad
		else:
			self.verbose = 0
	
	def setzeFeld9(self,neunStrings):
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
		
	def setzeFeld1(self,einString):
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
	
	def gebeFeld1(self,leer='.'):
		fs = ''
		for z in range(9):
			for s in range(9):
				zahl = self.feld[z][s][0]
				if zahl != 0:
					fs += str(zahl)
				else:
					fs += leer
		return fs
	
	def löscheZahl(self,z,s):
		vorher = self.feld[z][s][0]
		self.feld[z][s] = [0,True,True,True,True,True,True,True,True,True]
		if vorher != 0:
			self.unbekannt += 1
	
	def setzeZahl(self,z,s,zahl,grund=''):
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
	
	def setzeRateKleinste(self):
		self.rateHinweis = 0
	
	def setzeRateGrößte(self):
		self.rateHinweis = 2
	
	def setzeRateZufällig(self):
		self.rateHinweis = 1
		
	def getZahlenVonZeile(self,z,s):
		erg = []
		for si in  range(9):
			zahl = self.feld[z][si][0]
			if zahl != 0:
				erg.append(zahl)
		return erg
			
	def getZahlenVonSpalte(self,z,s):
		erg = []
		for zi in  range(9):
			zahl = self.feld[zi][s][0]
			if zahl != 0:
				erg.append(zahl)
		return erg
	
	def getZahlenVonQuadrat(self,z,s):
		erg = []
		zq = int(z/3)
		sq = int(s/3)
		for zi in zq*3, zq*3+1, zq*3+2 :
			for si in sq*3, sq*3+1, sq*3+2 :
				zahl = self.feld[zi][si][0]
				#deb print(zi,si,zahl)
				if zahl != 0:
					erg.append(zahl)
		return erg
		
	def getVerboteneZahlen(self,z,s):
		erg = self.getZahlenVonZeile(z,s)
		erg.extend(self.getZahlenVonSpalte(z,s))
		erg.extend(self.getZahlenVonQuadrat(z,s))
		#erg.sort()
		#erg.unique()
		return erg
	
	def verbieteZahlen(self,z,s):
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
		elif anzahlVerboten > 8:
			if self.verbose >= 2:
				print('   Im Kasten ',z+1,',',s+1,' ist nichts mehr möglich !')
			raise SudokuVerklemmt('Keine Zahl mehr erlaubt in ',z+1,s+1,self.rateTiefe)
	
	def verbieteZahlenÜberall(self):
		for z in range(9):
			for s in range(9):
				if self.feld[z][s][0] == 0:
					schonAcht = self.verbieteZahlen(z,s)
				time.sleep(self.bremse)
	
	def löseDirekt(self):
		vorher = 777
		noch = self.unbekannt
		sperre = 100
		while noch > 0 and sperre > 0 and noch < vorher:
			time.sleep(self.bremse)
			vorher = noch
			self.verbieteZahlenÜberall()
			noch = self.unbekannt
			sperre -= 1
			if self.verbose >= 1:
				print(noch)
		
	def löse(self,context=None):
		# context ist hier unbenutzt.
		if self.verbose >= 5:
			print('   ==> löse() mit self.unbekannt:',self.unbekannt)
		self.löseDirekt()
		while self.unbekannt > 0:
			time.sleep(self.bremse)
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
								time.sleep(self.bremse)
								self.rateTiefe += 1
								try:
									if self.verbose >= 2:
										print('   In Kästchen ',z+1,',',s+1
										     ,' probiere ich ',zahl,' . Ratetiefe:'
										     , self.rateTiefe-1,'-->',self.rateTiefe)
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
										print(self.unbekannt
										     ,' <-- Jetzt sind wieder mehr unbekannt.')
								if self.verbose >= 2:
									print('   Ratetiefe:',self.rateTiefe-1,'<--',self.rateTiefe)
								self.rateTiefe -= 1
							#endif Diese Zahl wäre noch erlaubt
						#endfor zahlIndex
						
						# Ich bin auf dem Aufstiegsweg aus der löse()-Rekursion.
							
						if self.unbekannt > 0:
							if self.verbose >= 2:
								print('   In Kästchen ',z+1,',',s+1,' alles durchprobiert')
							raise SudokuVerklemmt('jede Möglichkeit durchprobiert ',z+1,s+1
							                     ,self.rateTiefe)
					#endif Kasten leer
				#endfor s
			#endfor z
		#endwhile unbekannt
	
	def gebeUnbekannt(self):
		erg = self.unbekannt
		return erg
	
	def gebeAnzahlRaten(self):
		return self.anzahlRaten
	
	def gebeZahl(self,z,s):
		zahl = self.feld[z][s][0]
		if len(self.feld[z][s]) > 1+9:
			grund = self.feld[z][s][10]
		else:
			grund = ''
		return zahl,grund
	
	def gebeZahlOS(self,z,s): # OS wirkunglos in dieser Implementation
		zahl = self.feld[z][s][0]
		if len(self.feld[z][s]) > 1+9:
			grund = self.feld[z][s][10]
		else:
			grund = ''
		return zahl,grund
		
	def printZahlen(self):
		for z in range(9):
			for s in range(9):
				print( self.feld[z][s][0], end = '  ')
			print()
			
	def printZahlenSchön(self,leer='.'):
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
	
	def printZahlenSehrSchön(self,einVon=1,leer='.'):
		'''
		einVon : wieviel Sudokubilder sollen auf eine Bildschirmseite
		         bei Hochkantausgabe passen?
		         Sinnvolle (und erwartete) Werte: 1, 2 oder 3
		'''
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
	
	
	def gebeZahlenSehrSchön(self):
		r = Rahmen()
		f = self.gebeFeld1(leer=' ')
		return r.gebeS81a1SehrSchön(f)
		
	
	
	def gebeVergleichS81a1(self,r9x9,selbstLinks=True):
		r = Rahmen()
		l = self.gebeFeld1()
		if selbstLinks:
			rs = r.gebeS81a1PaarSehrSchön(l,r9x9)
		else:
			rs = r.gebeS81a1PaarSehrSchön(r9x9,l)
		return rs
		
	def printFeld(self):
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
	
	def printFeldDetails(self):
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
	
	def printUnbekannt(self):
		print( 'noch unbekannt: ', self.unbekannt )
	
	def printAbschlussbericht(self):
		if self.unbekannt == 0:
			print('Die Sudoku-Aufgabe ist gelöst.')
		else:
			print('Die Sudoku-Aufgabe ist noch nicht gelöst!')
			print('Es sind noch ',self.unbekannt,' Felder nicht besetzt.')
		
if __name__ == '__main__':
	print(modulname,'  --  Selbsttest')
		
	f = SudokuEinfach()
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
	
	
