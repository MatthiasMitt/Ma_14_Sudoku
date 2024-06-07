modulname = 'Ma_14_AufgabeSuchenSg2'
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
from   Ma_14_AufgabeSuchen import SudokuAufgabeSuchen

class SudokuAufgabeSuchenSg2(SudokuAufgabeSuchen):
	
	def __init__(self):
		super().__init__()
		#.lösungFeld    = ''
		#.lösungSudoku  = SudokuEinfach()
		#.aufgabeFeld   = ''
		#.aufgabeSudoku = SudokuAlleLösungen()
		#.einmalLeichter = ('',0,0)
		#.verbose = 9
		#.anzLösungen   = 0
		#.anzRaten      = 0
	
	def gebeSchwierigkeitsgrad(self):
		return 2 
		
	# setzeVerbose(self,plaudergrad):
	# gebeLösung1(self):
	# gebeAufgabe1(self):
	# findeLösung(self):
	# prüfeAufgabe(self):
	# erschwereAufgabe(self):
	
	
	def zuLeicht(self):
		if self.anzLösungen <= 2 and self.anzRaten < 10:
			zl = True
		else:
			zl = False
		return zl
	
	def zuSchwer(self):
		if self.anzLösungen > 3 or self.anzRaten >= 15:
			zs = True
		else:
			zs = False
		return zs
	
	# findeSchwereAufgabe(self):
	# druckeAufgabeSchön(self):
	# druckeAufgabeSehrSchön(self,einVon=1):
	# gebeAufgabeSehrSchön(self):
	
		
		
if __name__ == '__main__':
	print(modulname,'  --  Selbsttest')
	
	sa = SudokuAufgabeSuchenSg2()
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
	
	print('Schweregrad:  ',sa.gebeSchwierigkeitsgrad())
	print(modulname,'  --  Ende vom Selbsttest')
