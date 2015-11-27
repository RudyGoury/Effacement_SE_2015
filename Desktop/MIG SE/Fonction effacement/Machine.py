class Machine :
        
	def __init__(self, nom, consoMax, etatActuel, geneMaxTolere, etatContinu, etatRef, gene) :
		self.__nom = nom

		if(consoMax >= 0) :
			self.__consoMax = consoMax
		else :
			print("ERROR ("+nom+") ==> consoMax mis a 0")
			self.__consoMax = 0



		if ( etatActuel > 1) :
			etatActuel = 1
		elif ( etatActuel < 0):
			etatActuel = 0

		if (not etatContinu) :
			if(etatActuel > 0) :
				if(etatActuel !=1) :
					print("ERROR ("+nom+") ==> etatActuel mis a 1")
				etatActuel = 1
			elif(etatActuel < 0) : 
				if(etatActuel !=0) :
					print("ERROR ("+nom+") ==> etatActuel mis a 0")
				etatActuel = 0
		else : 
			if (etatActuel < 0) :
				print("ERROR ("+nom+") ==> etatActuel mis a 0")
				etatActuel = 0
			elif (etatActuel > 1) :
				print("ERROR ("+nom+") ==> etatActuel mis a 1")
				etatActuel = 1
		self.__etatActuel = etatActuel

# geneMaxTolere dans [0, 1]
		if(geneMaxTolere < 0 ) :
			print("ERROR ("+nom+") ==> geneMax mis a 0")
			geneMaxTolere = 0
		elif(geneMaxTolere > 1 ) :
			print("ERROR ("+nom+") ==> geneMax mis a 1")
			geneMaxTolere = 1

		self.__geneMaxTolere = geneMaxTolere
		
		self.__etatContinu = etatContinu
		
		if (etatRef < 0) :
			etatRef = 0
		elif (etatRef >1) :
			etatRef = 1
		
		self.__etatRef = etatRef
    
	def __str__(self) :
		s = "Machine : [nom="+str(self.__nom)
		s += ", consoMax="+str(self.__consoMax)
		s +=  ", etatActuel="+str(self.__etatActuel)
		s += ", geneMaxTolere="+str(self.__geneMaxTolere)
		s += ", etatContinu="+str(self.__etatContinu)
		s +=  ", etatRef="+str(self.__etatRef)+"]"
		s += ", etatRef="+str(self.__gene)+"]"
		return s


#||||||||||||||||||||||||  DONNES //  |||||||||||||||||||||||||||||||
	def renvoyerNom(self) :
		return self.__nom            
	def renvoyerConsoMax(self) :
		return self.__consoMax            
	def renvoyerEtatActuel(self) :
		return self.__etatActuel            
	def renvoyerGeneMaxTolere(self) :
		return self.__geneMaxTolere            
	def renvoyerEtatContinu(self) :
		return self.__etatContinu            
	def renvoyerEtatRef(self) :
		return self.__etatRef 
	def renvoyerGene():
		return self.__gene



#||||||||||||||||||||||||  MODIFIER  |||||||||||||||||||||||||||||
	def modifierEtatActuel(self, nouvelEtatActuel) :
		if(self.__etatContinu) :
			self.__etatActuel = nouvelEtatActuel
			return True
		elif (nouvelEtatActuel in [0,1]):
			self.__etatActuel = nouvelEtatActuel
			return True
		return False

	def modifierEtatRef(self, nouvelEtatRef) :
		self.__etatRef = nouvelEtatRef
	def modifierGeneMaxTolere(self, nouvelleGeneMaxTolere) :
		self.__geneMaxTolere = nouvelleGeneMaxTolere
	
	def modifierGene(self, nouvelleGene):
		self._gene = nouvelleGene
		


#||||||||||||||||||||||||  METHODES  |||||||||||||||||||||||||||||
	def consoMachine (self) :
		return self.__consoMax * self.__etatActuel
	                
	def geneMachine(self, temps, x) :
		return (self.__etatRef - self.__etatActuel)*self.__priorite * temps**2

	def effacementMax (self) :
		return self.__conso * (self.__etatActuel - etatEffacementMax())

	def etatEffacementMax (self) :
		etatEffacementMax=1
		for i in arange(21) :
			etatEffacement = 1 - i*(5/100);
		if( self.__geneMaxTolere < geneMachine(etatEffacement)) :
			return etatEffacement+i*(5/100)
		return 1
