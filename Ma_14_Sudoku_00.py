modulname = 'Ma_14_Sudoku_00'
_c_ = '(c) 2020 copyright: Matthias Mittelstein , Hauptstraße 23, 23816 Neversdorf, Germany ,, Matthias@Mittelstein.name'
'''
Was kommt heraus, wenn bei Sudoku mit einem
gänzlich leeren Blatt startet?
'''


from Ma_14_SudokuEinfach import SudokuEinfach
from Ma_14_AlleLoesungen import SudokuAlleLösungen

if __name__ == '__main__':
		
	f = SudokuEinfach()
	#f = SudokuAlleLösungen()
	f.setzeFeld9(['...   ...'
	             ,'...   ...'
	             ,'...   ...'
	             ,'   ...   '
	             ,'   ...   '
	             ,'   ...   '
	             ,'...   ...'
	             ,'...   ...'
	             ,'...   ...'])
	f.setzeVerbose(1)
	f.setzeRateZufällig()
	
	f.printZahlenSchön()
	f.löse()
	f.printZahlenSchön()
	f.printAbschlussbericht()
