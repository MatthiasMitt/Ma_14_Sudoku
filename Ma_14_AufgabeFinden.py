modulname = 'Ma_14_AufgabeFinden'
_c_ = '(c) 2020 copyright: Matthias Mittelstein , Hauptstraße 23, 23816 Neversdorf, Germany ,, Matthias@Mittelstein.name'
'''
Finde oder erfinde eine Sudoku-Aufgabe.

Lösungsanzatz:
1. Eine Sudoku-Lösung finden.
   Also ein vollständig gefülltes Feld.
2. Nach und nach Ziffern wegnehmen.
   Dadurch wird jeweils die Aufgabe schieriger.
3. Bis die Aufgabe den gewünschten Schwierigkeitgrad erreicht hat.
'''

import datetime
import console
import clipboard
#import random
#from  Ma_14_SudokuEinfach    import SudokuEinfach
#from  Ma_14_AlleLoesungen    import SudokuAlleLösungen
from   Ma_14_AufgabeSuchen    import SudokuAufgabeSuchen
from   Ma_14_AufgabeSuchenSg2 import SudokuAufgabeSuchenSg2
from   Ma_14_AufgabeSuchenSg3 import SudokuAufgabeSuchenSg3

'''
console.input_alert(title[, message, input, ok_button_title, hide_cancel_button=False])
Show a dialog with a single text field. The text field can be pre-filled with the input parameter. The text that was entered by the user is returned. The ‘Cancel’ button sends a KeyboardInterrupt.
'''


if __name__ == '__main__':
	print(modulname)
	asString = ''
	
	for geduld in range(10):
		print('')
		print('Bitte Schwierigkeitsgrad eingeben! 1=leicht .. 3=schwer : ')
		sg = console.input_alert('Schwierigkeitsgrad','1 bis 3','3','weiter')
		if sg == '1' or sg == '2' or sg == '3':
			break
		print(' ! nur eine Ziffer !')
	schwierigkeitsgrad = int(sg)
	
	for geduld in range(10):
		print('')
		print('Möchten Sie 1, 2 oder 3 Aufgaben bekommen?')
		sa = console.input_alert('Anzahl Aufgaben','1 , 2 oder 3','1','los !')
		if sa == '1' or sa == '2' or sa == '3':
			break
		print(' ! nur eine Ziffer !')
	anzahlAufgaben = int(sa)
	
	ts = datetime.datetime.now().timestamp()
	readable = datetime.datetime.fromtimestamp(ts).isoformat()
	
	if anzahlAufgaben == 1:
		asString += 'Und hier ist die gewünschte Sudoku-Aufgabe:\n\n'
		asString += 'Schwierigkeitsgrad: ' + str(schwierigkeitsgrad) + '\n'
		asString += 'Aufgabe gestellt  : ' + readable + '\n'
	else:
		asString += 'Und hier sind die gewünschte Sudoku-Aufgaben:\n\n'
		asString += 'Schwierigkeitsgrad: ' + str(schwierigkeitsgrad) + '\n'
		asString += 'Aufgaben gestellt : ' + readable + '\n'
	
	print(asString)
	
	for aa in range(anzahlAufgaben):
		if   schwierigkeitsgrad == 3:
			sa = SudokuAufgabeSuchenSg3()
		elif schwierigkeitsgrad == 2:
			sa = SudokuAufgabeSuchenSg2()
		else:
			sa = SudokuAufgabeSuchen()
		sa.setzeVerbose(0)
		sa.findeLösung()
		#print(sa.gebeLösung1())
		
		sa.findeSchwereAufgabe()
		
		
		sa.druckeAufgabeSehrSchön(einVon=anzahlAufgaben)
		asString += sa.gebeAufgabeSehrSchön()
	
	clipboard.set(asString)
	
	tsEnd = datetime.datetime.now().timestamp()
	print(datetime.datetime.fromtimestamp(tsEnd).isoformat())
