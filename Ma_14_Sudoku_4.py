modulname = 'Ma_14_Sudoku_4'
_c_ = '(c) 2020 copyright: Matthias Mittelstein , Hauptstraße 23, 23816 Neversdorf, Germany ,, Matthias@Mittelstein.name'
'''
Wenn ich aus einer Aufgabe noch etwas mehr Zahlen 
weglasse, gibt es schnell so viele Lösungen, das
es schwirig bis unmöglich wird, sie alle zu berechnen.
'''

from Ma_14_SudokuEinfach import SudokuEinfach
from Ma_14_SudokuEinfach import SudokuVerklemmt
from Ma_14_AlleLoesungen import SudokuAlleLösungen

if __name__ == '__main__':
		
	f1 = SudokuEinfach()
	f2 = SudokuAlleLösungen()
	
	f2.setzeFeld9(['.9.   8.3' 
	             ,'7149  ...' 
	             ,'... 12...'
	             ,'6 8...95 '
	             ,'45 6..   '
	             ,'   .45 7 '
	             ,'...49 ...'
	             ,'... 7 16.'
	             ,'2..3  ..7'])
	             
	f2.setzeFeld9(['.9.   8.3' 
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
	             ,'   ...9  '
	             ,'    ..   '
	             ,'   .     '
	             ,'...49 ...'
	             ,'... 7   .'
	             ,'2..3  .. '])
	
	f1.setzeFeld1('..32....8.7.3.5.6....49..1.1.4.59.728.....5.6....4813...2...6.551..6.32.78.5....1')
	f2.setzeFeld1('..32....8.7.3.5.6....49..1.1.4.59.728.....5.6....4813...2...6.551..6.32.78.5....1')
	             
	f1.setzeVerbose(0)
	f2.setzeVerbose(6)
	
	f2.printZahlenSchön()
	
	print('')
	print('SudokuEinfach')
	f1.löse()
	f1.printZahlenSchön()
	f1.printAbschlussbericht()
	
	print('')
	print('SudokuAlleLösungen')
	try:
		f2.löse()
	except SudokuVerklemmt as err:
		print('!!! SudokuVerklemmt ')
		print(f1.gebeVergleichS81a1(f2.gebeFeld1()))
	f2.printZahlenSchön()
	#deb f.printFeldDetails()
	f2.printAbschlussbericht()
	
	print(f1.gebeVergleichS81a1(f2.gebeFeld1()))
	
	
