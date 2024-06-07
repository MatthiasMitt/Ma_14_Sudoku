modulname = 'Ma_14_AlleLoesungen'
_c_ = '(c) 2020 copyright: Matthias Mittelstein , Hauptstraße 23, 23816 Neversdorf, Germany ,, Matthias@Mittelstein.name'

import copy
from Ma_14_SudokuEinfach import SudokuEinfach
from Ma_14_SudokuEinfach import SudokuVerklemmt
from Ma_14_Entscheidungsbaum import EntscheidungsKnoten
	
	
class SudokuAlleLösungen(SudokuEinfach):
	#super:
	# feld        = []
	# unbekannt   = 81
	# rateTiefe   = 0
	# verbose     = 9
	# rateHinweis =
	#hier:
	# erstesRaten    = None
	# anzahlLösungen = 0
	# anzahlRaten    = 0
	
	def __init__(self):
		super().__init__()
	
	def lösche(self):
		super().lösche()
		self.erstesRaten    = None
		self.anzahlLösungen = 0
		self.anzahlRaten    = 0
		
	#def setzeVerbose(self,plaudergrad):
	#def setzeFeld9(self,neunStrings):
	#def setzeFeld1(self,einString):
	#def gebeFeld1(self):
	#def löscheZahl(self,z,s):
	#def setzeZahl(self,z,s,zahl,grund=''):
	#def setzeRateKleinste(self):
	#def setzeRateGrößte(self):
	#def setzeRateZufällig(self):
	#def getZahlenVonZeile(self,z,s):
	#def getZahlenVonSpalte(self,z,s):
	#def getZahlenVonQuadrat(self,z,s):
	#def getVerboteneZahlen(self,z,s):
	#def verbieteZahlen(self,z,s):
	#def verbieteZahlenÜberall(self):
	#def löseDirekt(self):
	
		
	def löse(self,context=None):
		k = None
		if self.verbose >= 5:
			print('   ==> SudokuAlleLösungen.löse() mit self.unbekannt: '
			     ,self.unbekannt)
		self.löseDirekt()
		if self.unbekannt == 0:
			self.anzahlLösungen += 1
		#else
		while self.unbekannt > 0:
			if self.verbose >= 1:
				print('   Ich muss raten.'
				     ,'   Anzahl Lösungen:',self.anzahlLösungen
				     ,' offene Kästchen:',self.unbekannt
				     ,' Anzahl Raten',self.anzahlRaten)
				if self.verbose >= 4:
					self.printFeldDetails()
				
			for z in range(9):
				for s in range(9):
					if self.feld[z][s][0] == 0:
						# Hier ist das erste Kästchen, dass noch offen ist.
						
						# Ich sollte eine Sicherheitskopien anlegen. Aber daswerde ich
						# erst tun, wenn es überhaupt etwas zu probieren gibt.
						ersterVersuch      = True
						
						esGabMinEineLösung = False
						nochErlaubt        = self.feld[z][s][1:]
						#deb print(nochErlaubt)
						k = EntscheidungsKnoten(z,s,self.rateTiefe,nochErlaubt )
						#deb self.printZahlenSchön() #deb
						#deb k.druckeAst()           #deb
						if self.erstesRaten == None:
							# Diesmal ist der Entscheidungsknoten ˋkˋ die Wurzel des Baumes,
							# der noch entstehen soll. Planze sie in der Klasseninstanz ein.
							self.erstesRaten = k
						
						for zahlIndex in range(8,-1,-1): # range(9):
							if nochErlaubt[zahlIndex]: # Diese Zahl wäre noch erlaubt
								self.anzahlRaten += 1
								if ersterVersuch:
									nochHeilFeld      = copy.deepcopy(self.feld)
									nochHeilUnbekannt = self.unbekannt
								else:
									self.feld      = copy.deepcopy(nochHeilFeld)
									self.unbekannt = nochHeilUnbekannt
								zahl = zahlIndex + 1							
								self.setzeZahl(z,s,zahl,grund='geraten')
								self.rateTiefe += 1
								try:
									if self.verbose >= 2:
										print('   In Kästchen ',z+1,',',s+1
										     ,' probiere ich ',zahl,' . Ratetiefe:'
										     , self.rateTiefe-1,'-->',self.rateTiefe)
									erg = self.löse(context=k)
									if erg != None:
										k.setzeNachfolger(zahl,erg)
									else:
										k.setzeZifferGeht(zahl)
									esGabMinEineLösung  =  True
									
									letztesErfolgreichesSpiel = copy.deepcopy(self.feld),  self.unbekannt
									#if context != None:
									#	context.setzeNachfolger(zahl,k)
									if self.verbose >= 1:
										if self.rateTiefe <= 1:
											print('Zwischenergebnis auf Ratetiefe '
											     ,self.rateTiefe,':')
											self.printZahlenSchön() #deb
								except SudokuVerklemmt as err:
									if self.verbose >= 2:
										print('   Sackgasse: ',err.text,err.zeile,err.spalte
										     , ' .')
										if self.verbose >= 4:
											#self.printFeldDetails()
											print(self.gebeVergleichS81a1(nochHeilFeld)) #war vor 2023-06-29: (nochHeil81))
									k.setzeZifferGehtNicht(zahl)
									
									if self.verbose >= 1:
										print(self.unbekannt
										     ,' <-- Jetzt sind wieder mehr unbekannt.')
								if self.verbose >= 2:
									print('   Ratetiefe:',self.rateTiefe-1,'<--',self.rateTiefe)
								self.rateTiefe -= 1
								ersterVersuch = False
							#endif Zahl erlaubt
						#endfor zahlIndex
						
						# Ich bin auf dem Aufstiegsweg aus der löse()-Rekursion.
						
						if esGabMinEineLösung:
							self.feld , self.unbekannt = letztesErfolgreichesSpiel
						
						if self.unbekannt > 0:
							if self.verbose >= 2:
								print('   In Kästchen ',z+1,',',s+1,' alles durchprobiert')
								self.printFeld()
							k.druckeAst()
							raise SudokuVerklemmt('jede Möglichkeit durchprobiert ',z+1,s+1
							                     ,self.rateTiefe)
					#endif Kästchen noch offen
				#endfor s
			#endfor z
		#endwhile unbekannt
		if self.verbose >= 1:
			print('k= ',k)
		return k
					
	def gebeAnzahlLösungen(self):
		return self.anzahlLösungen
	
	#def gebeAnzahlRaten(self):
	#def gebeZahl(self,z,s):
	#def printZahlen(self):
	#def printZahlenSchön(self):
	#def printFeld(self):
	
	#def printFeldDetails(self):
	#def printUnbekannt(self):
		
	
	def printAbschlussbericht(self):
		super().printAbschlussbericht()
		if self.erstesRaten == None:
			print('Das ging ohne Raten.')
		else:
			self.erstesRaten.druckeAst()
		print('Es gibt ',self.anzahlLösungen,' Lösungen.')
		
if __name__ == '__main__':
	print(modulname,'  --  Selbsttest')
		
	f = SudokuAlleLösungen()
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
		f.printZahlenSchön()
		f.löseDirekt()
		f.printZahlenSchön()
		print(f.gebeZahl(3,4))
		f.printAbschlussbericht()
		print('Anzahl Lösungen: ',f.gebeAnzahlLösungen())
	elif test == 3:
		f.löse()
		f.printAbschlussbericht()
	
	
