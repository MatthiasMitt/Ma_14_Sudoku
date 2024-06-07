modulname = 'Ma_14_Entscheidungsbaum'
_c_ = '(c) 2020 copyright: Matthias Mittelstein , Hauptstraße 23, 23816 Neversdorf, Germany ,, Matthias@Mittelstein.name'
'''
Ein Speicher für alle Entscheidungen, wenn beim Löse einer Sudoku-Aufgabe
gefordert wurde, sämtliche Lösungen zu finden.
'''

class SudokuInternerFehler(Exception):
	
	def __init__(self,text,zeile,spalte,rateTiefe):
		self.text      = text
		self.zeile     = zeile
		self.spalte    = spalte
		self.rateTiefe = rateTiefe


class EntscheidungsKnoten:
	
	# Konstanten
	SOWIESO_NICHT_ERLAUBT = 0
	ZU_ANFANG_ERLAUBT     = 1
	ERLAUBT_OHNE_RATEN    = 2
	ERLAUBT_MIT_RATEN     = 3
	DOCH_NICHT_ERLAUBT    = 4
	
	def __init__(self,zeile,spalte,rateTiefe,nochErlaubt): # erl1,erl2,erl3,erl4,erl5,erl6,erl7,erl8,erl9):
		möglichkeiten = 0
		ziffern = []
		for ix in range(9):
			if nochErlaubt[ix]:
				ziffern.append(self.ZU_ANFANG_ERLAUBT)
				möglichkeiten += 1
			else:
				ziffern.append(self.SOWIESO_NICHT_ERLAUBT)
		if möglichkeiten < 2:
			raise SudokuInternerFehler('Es sind gar nicht mehr mehrere Zahlen verfügbar',zeile,spalte,rateTiefe)
		self.ziffern       = ziffern
		self.möglichkeiten = möglichkeiten
		self.zeile         = zeile
		self.spalte        = spalte
		self.rateTiefe     = rateTiefe
		self.nachfolger    = [None,None,None,None,None,None,None,None,None]
	
	def __str__(self):
		return self.__repr__()
	
	def __repr__(self):
		s = 'Entscheidungsknoten('
		s += str(self.zeile) + ',' + str(self.spalte)
		s += ' : ['
		for ix in range(9):
			if   self.ziffern[ix] == self.SOWIESO_NICHT_ERLAUBT:
				s += '_'
			elif self.ziffern[ix] == self.ZU_ANFANG_ERLAUBT:
				s += '?'
			elif self.ziffern[ix] == self.ERLAUBT_OHNE_RATEN:
				s += '*'
			elif self.ziffern[ix] == self.ERLAUBT_MIT_RATEN:
				s += '+'
			elif self.ziffern[ix] == self.DOCH_NICHT_ERLAUBT:
				s += '.'
			else:
				s += str(self.ziffern[ix])
		s += ']'
		s += ')'
		return s

	def setzeNachfolger(self,ziffer,nachfolger):
		if 1 > ziffer or ziffer > 9:
			raise SudokuInternerFehler('nur 1..9 als Ziffern'
			                          ,self.zeile,self.spalte,self.rateTiefe)
		if self.rateTiefe + 1 != nachfolger.rateTiefe:
			raise SudokuInternerFehler('im Baum muss Ratetiefe je um 1 zunehmen'
			                          ,self.zeile,self.spalte,self.rateTiefe)
		ix = ziffer - 1
		self.ziffern[ix]    = self.ERLAUBT_MIT_RATEN
		self.nachfolger[ix] = nachfolger
	
	def setzeZifferGehtNicht(self,ziffer):
		if 1 > ziffer or ziffer > 9:
			raise SudokuInternerFehler('nur 1..9 als Ziffern'
			                          ,self.zeile,self.spalte,self.rateTiefe)
		ix = ziffer - 1
		self.ziffern[ix] = self.DOCH_NICHT_ERLAUBT
		
	def setzeZifferGeht(self,ziffer):
		if 1 > ziffer or ziffer > 9:
			raise SudokuInternerFehler('nur 1..9 als Ziffern'
			                          ,self.zeile,self.spalte,self.rateTiefe)
		ix = ziffer - 1
		self.ziffern[ix] = self.ERLAUBT_OHNE_RATEN
	
	def nenneAnfänglicheMöglichkeitenHier(self):
		anz = 0
		for ix in range(9):
			if self.ziffern[ix] == self.ZU_ANFANG_ERLAUBT or self.ziffern[ix] == self.ERLAUBT_OHNE_RATEN or self.ziffern[ix] == self.ERLAUBT_MIT_RATEN or self.ziffern[ix] == self.DOCH_NICHT_ERLAUBT:
				anz += 1
		if anz != self.möglichkeiten:
			raise SudokuInternerFehler('bei Möglichkeiten verzählt',self.zeile,self.spalte,self.rateTiefe)
		return anz
	
	def nenneAnfänglicheMöglichkeitenImAst(self):
		anz = self.nenneAnfänglicheMöglichkeitenHier()
		for nachfolger in self.nenneAlleNachfolger():
			if nachfolger != None:
				anz += nachfolger.nenneAnfänglicheMöglichkeitenImAst()
		return anz
	
	def nenneMöglichkeitenHier(self):
		anz = 0
		for ix in range(9):
			if self.ziffern[ix] == self.ZU_ANFANG_ERLAUBT or self.ziffern[ix] == self.ERLAUBT_OHNE_RATEN or self.ziffern[ix] == self.ERLAUBT_MIT_RATEN :
				anz += 1
		return anz
	
	def nenneMöglichkeitenImAst(self):
		anz = self.nenneMöglichkeitenHier()
		for nachfolger in self.nenneAlleNachfolger():
			if nachfolger != None:
				anz += nachfolger.nenneMöglichkeitenImAst()
		return anz
	
	def nenneNachfolger(self,ziffer):
		if 1 > ziffer or ziffer > 9:
			raise SudokuInternerFehler('nur 1..9 als Ziffern'
			                          ,zeile,spalte,rateTiefe)
		ix = ziffer - 1
		return self.nachfolger[ix]
		
	def nenneAlleNachfolger(self):
		liste = []
		for ix in range(9):
			if self.ziffern[ix] > 0:
				liste.append(self.nachfolger[ix])
		return liste
	
	def druckeAst(self):
		indent ='.'
		for z in range(self.rateTiefe):
			indent += '  '
		print(indent,self)
		for nachfolger in self.nenneAlleNachfolger():
			if nachfolger != None:
				nachfolger.druckeAst()
		
		
if __name__ == '__main__':
	
	print(modulname)
	
	k1 = EntscheidungsKnoten(2,3,4,[False,False,False,True,True,True,False,False,False])
	
	k2 = EntscheidungsKnoten(2,5,5,[True,False,False,True,True,True,False,False,False])
	k3 = EntscheidungsKnoten(2,6,5,[False,False,False,True,True,True,False,True,True])
	k1.setzeZifferGehtNicht(4)
	k1.setzeNachfolger(5,k2)
	k1.setzeNachfolger(6,k3)
	print('k1     :',k1,'-->',k1.nenneAnfänglicheMöglichkeitenHier()
	     ,'  (',k1.nenneAnfänglicheMöglichkeitenImAst(),')')
	print('k1     :',k1,'-->',k1.nenneMöglichkeitenHier()
	     ,'  (',k1.nenneMöglichkeitenImAst(),')')
	print('k1.[5] :',k1.nenneNachfolger(5))
	print()
	print('Drucke Ast "k1"')
	k1.druckeAst()

