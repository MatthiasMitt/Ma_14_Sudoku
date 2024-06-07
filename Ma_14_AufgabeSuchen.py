modulname = 'Ma_14_AufgabeSuchen'
_c_ = '(c) 2020 copyright: Matthias Mittelstein , Hauptstraße 23, 23816 Neversdorf, Germany ,, Matthias@Mittelstein.name'
'''
Finde oder erfinde eine Sudoku-Aufgabe.

Lösungsanzatz:
1. Eine Sudoku-Lösung finden.
   Also ein vollständig gefülltes Feld.
2. Nach und nach Ziffern wegnehmen.
   Dadurch wird jeweils die Aufgabe schieriger.
3. Bis die Aufgabeden gewünschten Schwierigkeitgrad erreicht hat.
'''

import random
from   Ma_14_SudokuEinfach import SudokuEinfach
from   Ma_14_AlleLoesungen import SudokuAlleLösungen

class SudokuAufgabeSuchen():
	
	def __init__(self):
		self.lösungFeld    = ''
		self.lösungSudoku  = SudokuEinfach()
		self.aufgabeFeld   = ''
		self.aufgabeSudoku = SudokuAlleLösungen()
		self.einmalLeichter = ('',0,0)
		self.verbose = 9
		self.anzLösungen   = 0
		self.anzRaten      = 0
	
	def gebeSchwierigkeitsgrad(self):
		return 1
	
	def setzeVerbose(self,plaudergrad):
		if plaudergrad >= 0:
			self.verbose = plaudergrad
		else:
			self.verbose = 0
	
	def gebeLösung1(self):
		return self.lösungFeld
	
	def gebeAufgabe1(self):
		return self.aufgabeFeld
	
	
	def findeLösung(self):
		self.lösungSudoku.setzeVerbose(self.verbose-2)
		self.lösungSudoku.lösche()
		self.lösungSudoku.setzeRateZufällig()
		self.lösungSudoku.löse()
		self.lösungFeld = self.lösungSudoku.gebeFeld1()
		self.aufgabeFeld = self.lösungFeld
	
	def prüfeAufgabe(self):
		self.aufgabeSudoku.lösche()
		self.aufgabeSudoku.setzeVerbose(self.verbose-1)
		self.aufgabeSudoku.setzeFeld1(self.aufgabeFeld)
		self.aufgabeSudoku.löse()
		self.anzLösungen = self.aufgabeSudoku.gebeAnzahlLösungen()
		self.anzRaten    = self.aufgabeSudoku.gebeAnzahlRaten()
		return self.anzLösungen , self.anzRaten
	
	def erschwereAufgabe(self):
		self.einmalLeichter = self.aufgabeFeld, self.anzLösungen , self.anzRaten
		zahl = '.'
		while zahl == '.':
			ix = random.choice(range(9*9))
			zahl = self.aufgabeFeld[ix]
			#deb print('deb: ix,zahl: ',ix,zahl)
		z = int(ix/9)
		s = ix - 9 * z
		self.aufgabeSudoku.lösche()
		self.aufgabeSudoku.setzeFeld1(self.aufgabeFeld)
		self.aufgabeSudoku.löscheZahl(z,s)
		self.aufgabeFeld = self.aufgabeSudoku.gebeFeld1()
	
	def zuLeicht(self):
		if self.anzLösungen == 1 and self.anzRaten < 6:
			zl = True
		else:
			zl = False
		return zl
	
	def zuSchwer(self):
		if self.anzLösungen > 1 or self.anzRaten >= 6:
			zs = True
		else:
			zs = False
		return zs
	
	def findeSchwereAufgabe(self):
		zuLeicht = True
		while zuLeicht:
			self.erschwereAufgabe()
			self.prüfeAufgabe()
			if self.verbose >= 1:
				print('a: ',self.aufgabeFeld)
				if self.verbose >= 2:
					print() # Leerzeile
			zuLeicht = self.zuLeicht()
		if self.verbose >= 1:
				print('Es gibt ', self.anzLösungen ,' Lösungen nach '
				     ,self.anzRaten,' mal raten.')
		if self.zuSchwer():
			self.aufgabeFeld, self.anzLösungen , self.anzRaten = self.einmalLeichter
			self.aufgabeSudoku.lösche()
			self.aufgabeSudoku.setzeFeld1(self.aufgabeFeld)
			if self.verbose >= 1:
				print('Also lieber ',self.anzLösungen ,' Lösungen nach '
				     ,self.anzRaten,' mal raten.')
				print('A: ',self.aufgabeFeld)
	
	def druckeAufgabeSchön(self):
		self.aufgabeSudoku.lösche()
		self.aufgabeSudoku.setzeFeld1(self.aufgabeFeld)
		self.aufgabeSudoku.printZahlenSchön()
	
	def druckeAufgabeSehrSchön(self,einVon=1):
		self.aufgabeSudoku.lösche()
		self.aufgabeSudoku.setzeFeld1(self.aufgabeFeld)
		self.aufgabeSudoku.printZahlenSehrSchön(einVon=einVon,leer=' ')
	
	def gebeAufgabeSehrSchön(self):
		self.aufgabeSudoku.lösche()
		self.aufgabeSudoku.setzeFeld1(self.aufgabeFeld)
		return self.aufgabeSudoku.gebeZahlenSehrSchön()
		
		
if __name__ == '__main__':
	print(modulname,'  --  Selbsttest')
	
	sa = SudokuAufgabeSuchen()
	sa.findeLösung()
	print(sa.gebeLösung1())
	
	print(sa.gebeAufgabe1())
	print(sa.prüfeAufgabe())
	
	for i in range(4):
		print('')
		sa.erschwereAufgabe()
		print(sa.gebeAufgabe1())
		print(sa.prüfeAufgabe(),' <--prüfeAufgabe()')
		print(sa.zuLeicht(),' <--zuLeicht()')
	
	#sa.findeSchwereAufgabe()
	#print('')
	#print('')
	#print('Und hier ist die gewünschte Aufgabe:')
	#sa.druckeAufgabeSchön()
	##print(sa.prüfeAufgabe(),' <--prüfeAufgabe()')
	##print(sa.zuLeicht(),' <--zuLeicht()')
	
	print('Schweregrad:  ',sa.gebeSchwierigkeitsgrad())
	print(modulname,'  --  Ende vom Selbsttest')
