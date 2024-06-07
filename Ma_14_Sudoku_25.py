modulname = 'Ma_14_Sudoku_25'
_c_ = '(c) 2020 copyright: Matthias Mittelstein , Hauptstraße 23, 23816 Neversdorf, Germany ,, Matthias@Mittelstein.name'
'''
Als ein Beispiel (zum Kopieren) löst diese Programm das Sudoku,
dass ich in einem Buch von Ulla auf Seite 25 gefunden hatte.
'''


from Ma_14_SudokuEinfach import SudokuEinfach
from Ma_14_AlleLoesungen import SudokuAlleLösungen

if __name__ == '__main__':
		
	#f = SudokuEinfach()
	f = SudokuAlleLösungen()
	
	f.setzeFeld9(['.9.   8.3' #.9.
	             ,'7149  ...' 
	             ,'... 12...' #12...
	             ,'6 8...95 '
	             ,'45 6..   '
	             ,'   .45 7 '
	             ,'...49 ...'
	             ,'... 7 16.'
	             ,'2..3  ..7']) #2..3
	f.setzeVerbose(2)
	
	f.printZahlenSchön()
	f.löse()
	f.printZahlenSchön()
	#deb f.printFeldDetails()
	f.printAbschlussbericht()
