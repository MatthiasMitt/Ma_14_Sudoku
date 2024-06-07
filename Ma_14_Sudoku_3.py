modulname = 'Ma_14_Sudoku_3'
_c_ = '(c) 2020 copyright: Matthias Mittelstein , Hauptstraße 23, 23816 Neversdorf, Germany ,, Matthias@Mittelstein.name'
'''
Wenn ich aus einer  aufgabe einige Ziffern weglasse,
gibt es schnell viele mögliche Lösungen.
'''

from Ma_14_AlleLoesungen import SudokuAlleLösungen

if __name__ == '__main__':
		
	#f = SudokuEinfach()
	f = SudokuAlleLösungen()
	f2 = SudokuAlleLösungen()
	
	f.setzeFeld9(['.9.   8.3' 
	             ,'7149  ...' 
	             ,'... 12...'
	             ,'6 8...95 '
	             ,'45 6..   '
	             ,'   .45 7 '
	             ,'...49 ...'
	             ,'... 7 16.'
	             ,'2..3  ..7'])
	             
	f.setzeFeld9(['.9.   8.3' 
	             ,'7149  ...' 
	             ,'... 12...'
	             ,'6 8...95 '
	             ,'45  ..   '
	             ,'   .45 7 '
	             ,'...49 ...'
	             ,'... 7 16.'
	             ,'2..3  ..7'])
	
	f2.setzeFeld9(['.9.   8.3' 
	             ,'7149  ...' 
	             ,'... 12...'
	             ,'6 8...95 '
	             ,'4   ..   '
	             ,'   .45 7 '
	             ,'...49 ...'
	             ,'... 7 16.'
	             ,'2..3  ..7'])
	
	             
	f.setzeVerbose(2)
	
	f.printZahlenSchön()
	f.löse()
	f.printZahlenSchön()
	#deb f.printFeldDetails()
	f.printAbschlussbericht()
