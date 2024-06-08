modulname = 'Ma_14_Rahmen'
_c_ = '(c) 2020 copyright: Matthias Mittelstein , Hauptstraße 23, 23816 Neversdorf, Germany ,, Matthias@Mittelstein.name'

# iPad and iPhone only: import console



import sys
import os
b2 = os.path.realpath(__file__).split("/")
b4 = "/".join(b2[0:-2]) 
b5 = "/".join(b2[0:-1])
# 'import' soll auch in dem Ordner suchen, in dem dises Programm gespeichet ist.
sys.path.insert(1,b5)
# 'import' soll auch in dem umfassenden Ordner suchen, wo es hoffentlich das
# Hilfspaket 'Ma_Util' gibt. Unabhänge davon, wie und von wo aus gestartet wurde.
sys.path.insert(1,b4)

from   Ma_Util.Ma_Print                             import print_dict, print_list, print_list_of_dicts
from   Ma_Util.Ma_Console                           import Ma_Console
from   Ma_Util.Ma_Plattform                         import Ma_Plattform
Ma14RPlattform = Ma_Plattform()


class Rahmen():
	
	nl   = '\n'
	
	_ES_ = '\u250F'
	_E_W = '\u2501'
	_EsW = '\u252F'
	_ESW = '\u2533'
	_SW_ = '\u2513' # Ein Doppel-_ würde Aktionen auslösen. Darum anders.
	
	N_S_ = '\u2503'
	____ = '\u0020'
	n_s_ = '\u2502'
	
	NeS_ = '\u2520'
	_e_w = '\u2500'
	nesw = '\u253C'
	NeSw = '\u2542'
	N_Sw = '\u2528'
	
	NES_ = '\u2523'
	_E_W = '\u2501'
	nEsW = '\u253F'
	NESW = '\u254B'
	N_SW = '\u252B'
	
	NE__ = '\u2517'
	nE_W = '\u2537'
	NE_W = '\u253B'
	N__W = '\u251B'
	
	systemFont = 'Menlo-Regular'
	
	def setzeSchriftgröße(self,points=30):
		if Ma14RPlattform.plattform.auf_iPhone_o_iPad():
			console.set_font('Menlo-Regular',points)
	
	def setzeNormaleSchrift(self):
		if Ma14RPlattform.plattform.auf_iPhone_o_iPad():
			console.set_font()
	
	def testBoxWithNames(self):
		r = self
		print('')
		print( r._ES_ , r._E_W , r._EsW , r._ESW , r._SW_ , sep='' )
		print( r.N_S_ , r.____ , r.n_s_ , r.N_S_ , r.N_S_ , sep='' )
		print( r.NeS_ , r._e_w , r.nesw , r.NeSw , r.N_Sw , sep='' )
		print( r.NES_ , r._E_W , r.nEsW , r.NESW , r.N_SW , sep='' )
		print( r.NE__ , r._E_W , r.nE_W , r.NE_W , r.N__W , sep='' )
		print('')

	def gebeS81a1SehrSchön(self,s1_9x9):
		s3 = ''
		for ix in range(9*9):
			s3 += ' ' + s1_9x9[ix] + ' '
		return self.gebeS81a3SehrSchön(s3)
		
	def gebeS81a3SehrSchön(self,s3_9x9):
		# s3_9x9 ist eine sehr lange Zeichenkette, die
		# mit Rahmen versehen wie ein 9*9 Feld aussehen
		# soll. Pro Feld werden 3 Zeichen übergeben.
		# Ergebnis ist eine noch längere Zeichenkette,
		# in die Rahmenzeichen Unicode U+25xx und NewLines
		# eingemischt sind.
		fs = ''
		r = self # kürzer Schreibweise
		#linie       = '|---|---|---H---|---|---H---|---|---|'
		#doppellinie = '|===|===|===H===|===|===H===|===|===|'
		dünneLinie = r.NeS_ + 3*r._e_w + r.nesw + 3*r._e_w + r.nesw + 3*r._e_w + r.NeSw + + 3*r._e_w + r.nesw + 3*r._e_w + r.nesw + 3*r._e_w + r.NeSw +  3*r._e_w + r.nesw + 3*r._e_w + r.nesw + 3*r._e_w +r.N_Sw 
		dickeLinie = r.NES_ + 3*r._E_W + r.nEsW + 3*r._E_W + r.nEsW + 3*r._E_W + r.NESW + 3*r._E_W + r.nEsW + 3*r._E_W + r.nEsW + 3*r._E_W + r.NESW +3*r._E_W + r.nEsW + 3*r._E_W + r.nEsW + 3*r._E_W + r.N_SW 
		kopfLinie  = r._ES_ + 3*r._E_W + r._EsW + 3*r._E_W + r._EsW + 3*r._E_W + r._ESW + 3*r._E_W + r._EsW + 3*r._E_W + r._EsW + 3*r._E_W + r._ESW +3*r._E_W + r._EsW + 3*r._E_W + r._EsW + 3*r._E_W + r._SW_ 
		fussLinie  = r.NE__ + 3*r._E_W + r.nE_W + 3*r._E_W + r.nE_W + 3*r._E_W + r.NE_W + 3*r._E_W + r.nE_W + 3*r._E_W + r.nE_W + 3*r._E_W + r.NE_W +3*r._E_W + r.nE_W + 3*r._E_W + r.nE_W + 3*r._E_W + r.N__W 
		fs += kopfLinie + self.nl
		for z in range(9):
			fs += r.N_S_
			for s in range(9):
				ix = (z*9+s)*3
				fs += s3_9x9[ix:ix+3]
				if s == 2 or s == 5 or s == 8:
					fs += r.N_S_
				else:
					fs += r.n_s_
			fs += self.nl
			if z == 2 or z == 5:
				fs += dickeLinie + self.nl
			elif z == 8:
				fs += fussLinie + self.nl
			else:
				fs += dünneLinie + self.nl
		return fs
	
	def gebeS81a1PaarSehrSchön(self,l9x9,r9x9):
		# l9x9 und r9x9 sind zwei sehr lange Zeichenkette, 
		# die jeweils ein Zeichen für ein 9*9-Feld enthalten.
		# Die Werte werden verglichen und dann pro Kästchen
		# links (l) und rechts (r) dargestellt. Sind im einem
		# Kästchen die Werte gleich, wird das Zeichen mittig
		# und nur einmal gezeigt.
		# Das Ergebnis ist nur ein 9*9-Feld.
		# Ergebnis ist eine lange Zeichenkette,
		# in die zusätzlich Rahmenzeichen Unicode U+25xx
		# und NewLines eingemischt sind.
		s3_9x9 = ''
		for ix in range(9*9):
			l = l9x9[ix]
			r = r9x9[ix]
			if l == r:
				s3_9x9 += ' ' + l + ' '
			else:
				s3_9x9 += l + ' ' + r
		return self.gebeS81a3SehrSchön(s3_9x9)

if __name__ == '__main__':
	print(modulname,'  --  Selbsttest')

	def testBoxDirect():
		print('')
		print('Unicode \u250F\u2501\u252F\u2533\u2513 ?')
		print('Unicode \u2503\u0020\u2502\u2503\u2503 ?')
		print('Unicode \u2520\u2500\u253C\u2542\u2528 ?')
		print('Unicode \u2523\u2501\u253F\u254B\u252B ?')
		print('Unicode \u2517\u2501\u2537\u253B\u251B ?')
		print('')
	
	def test3(rah,fn,siz):
		if Ma14RPlattform.auf_iPhone_o_iPad():
			if fn == '' or fn == None:
				print('             font zurücksetzen.')
				console.set_font() # reset
			else:
				console.set_font(fn,siz)
				print('             font : ',fn,siz)
		rah.testBoxWithNames()
	
	testBoxDirect()
	
	r = Rahmen()
	#r.testBoxWithNames()
	
	test3(r,'Courier',30)
	test3(r,'CourierNewPS-BoldMT',40)
	test3(r,'Arial',25) # 'Arial' is proportional
	test3(r,'Menlo-Regular',30)
	test3(r,'Menlo-Regular',8)
	
	if Ma14RPlattform.auf_iPhone_o_iPad():
		console.set_font() # reset

