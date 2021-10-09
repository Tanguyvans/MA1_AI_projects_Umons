#Agence
from pade.misc.utility import display_message, start_loop, call_later
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from sys import argv
from pade.acl.filters import Filter
import pickle

from collections import Counter

class Agence(Agent):
    #message reçu du client
    clientMessage = {}
    nbrPers = 0 #variable qui va prendre le nombre de personnes demandé par le client
    QuntD = 0 #variable qui va prendre le nombre de nuits souhaitées par le client
    ville = "" #variable qui va prendre le nom de la ville souhaité par le client
    etoiles = 0 #variable qui va prendre le nombre d'étoile de l'hotel souhaité par le client
    prix = 0 
    
    
    decFinal=0 #variable qui va verifier si la demande du client correspond à l'un des meilleures offres de marchée
    nbrpro =0 #variable qui va compter le nombre d'article similaire (avec prix different)
    PrixFinal=0 # le toral du prix selon la quantité demandé, une réduction de 30% est appliqué sur le total, si quantité est > =3
    IdBestHotel=""
    contactTermine=0

    #contient les messages de reponses des hotels
    LesHotels = []

    countHotel = 0
    dictHotels = {}

    #Questions facultatives
    HistoriqueCommande = []

    nbCaracteristique = 4

    def contact_hot1(self):
        message = ACLMessage(ACLMessage.CFP)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_sender(AID('agence'))
        message.add_receiver(AID("hotel_1"))
        message.set_ontology("contactHot1")

        new_msg = pickle.dumps(self.clientMessage)
        message.set_content(new_msg)
        self.send(message)

    def contact_hot2(self):
        message = ACLMessage(ACLMessage.CFP)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_sender(AID('agence'))
        message.add_receiver(AID("hotel_2"))
        message.set_ontology("contactHot2")
        new_msg = pickle.dumps(self.clientMessage)
        message.set_content(new_msg)
        self.send(message)  

    def contact_hot3(self):

        message = ACLMessage(ACLMessage.CFP)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_sender(AID('agence'))
        message.add_receiver(AID("hotel_3"))
        message.set_ontology("contactHot3")

        new_msg = pickle.dumps(self.clientMessage)
        message.set_content(new_msg)
        self.send(message)

    def saveClientMessage(self, msg):
        self.clientMessage = pickle.loads(msg)
        self.nbrPers = self.clientMessage["personne"]
        self.QuntD = self.clientMessage["nuit"]
        self.ville =self.clientMessage["ville"]
        self.etoiles = self.clientMessage["etoiles"]
        self.prix = self.clientMessage['prix']

    def refus(self, hotel):
        message = ACLMessage(ACLMessage.REJECT_PROPOSAL)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_sender(AID('agence'))
        message.add_receiver(AID(hotel))
        message.set_ontology("reject-proposal")
        message.set_content("Vous ne correspondez a la demande du client")
        self.send(message)

    def accept(self, hotel):
        message = ACLMessage(ACLMessage.ACCEPT_PROPOSAL)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_sender(AID('agence'))
        message.add_receiver(AID(hotel))
        message.set_ontology("accept-proposal")
        message.set_content("Vous pouvez considérer la demande du client")
        self.send(message)
    
    def contact_Client_ChoixHotel(self):
        
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_sender(AID('agence'))
        message.add_receiver(AID("client"))

        message.set_ontology("decision")
        contactHotel = {"nameHotel": self.IdBestHotel, "prixHotel": self.PrixFinal}
        new_msg = pickle.dumps(contactHotel)
        message.set_content(new_msg)
        self.send(message)

    def contact_Client_Scoring(self, sorted_scoring):
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_sender(AID('agence'))
        message.add_receiver(AID("client"))
        message.set_ontology("decision")
        message.set_content(pickle.dumps(sorted_scoring))
        self.send(message)

    def __init__(self, aid):
        super(Agence, self).__init__(aid=aid, debug=False)

    def on_start(self):
        super(Agence, self).on_start()
        display_message(self.aid.localname, "Demarrage de l'agent Agence - reception des notes en cours ...")

    def react(self, message):
        ontocmd="cmdClient"
        perVend="propose"
        super(Agence, self).react(message)

        self.countHotel
        # Contacter les hotels dès qu'on recoit une commande de client
        if message.ontology  == "cmdClient":
            self.saveClientMessage(message.content)
            call_later(3.0, self.contact_hot1)
            call_later(3.0, self.contact_hot2)
            call_later(3.0, self.contact_hot3)

        # Enregistrement de la réponse des TROIS hotels
        if message.ontology  == "offrePropose" and self.countHotel <= 3:
            self.countHotel += 1
            proposition = pickle.loads(message.content)
            self.LesHotels.append(proposition)
            #print(F"{self.countHotel} hotel enregister")

        # Quand on a la réponse des TROIS hotels, on choisit le meilleur ou on propose un classment
        if self.countHotel == 3:
            self.countHotel = 0
            print(">>> Toutes les réponses sont reçues par l'agence")
            #print(">>> Voici le meilleur hotel")
            #self.choixHotel()
            print(">>> Voici le classement des hotels")
            classement = self.scoringAndSortingHotel()
            self.contact_Client_Scoring(classement)

        
    def scoringAndSortingHotel(self):
        scoring = {}
        doubleScore = []
        penalite = 0.1

        for hotel in self.LesHotels:
            scoring[hotel['nameHotel']]= self.score(hotel)
        
        counting = Counter(scoring.values())
        for key, val in counting.items():
            if val != 1:
                doubleScore.append(key)

        for key, val in scoring.items():
            if val in doubleScore:
                for hotel in self.LesHotels:
                    if hotel['nameHotel'] == key:
                        scoring[key] =  val - self.calculPrix(hotel)*penalite

        sorted_scoring = dict(sorted(scoring.items(), key=lambda item: item[1], reverse = True))  
        
        return sorted_scoring



    def score(self, hotel) -> float :
        return (100/self.nbCaracteristique) * self.critereSatisfait(hotel)

    def critereSatisfait(self, hotel) -> int:
        nbr_critereSatisfaits = 0

        if hotel["nbrMaxPersAccepte"] >= self.nbrPers: nbr_critereSatisfaits+=1
        if hotel['ville'] == self.ville: nbr_critereSatisfaits+=1
        if hotel["nbrEtoilesP"] >= self.etoiles: nbr_critereSatisfaits+=1
        if self.calculPrix(hotel) <= self.prix : nbr_critereSatisfaits+=1

        return nbr_critereSatisfaits

    def calculPrix(self, hotel) -> int:
        prix =  hotel["prix"] * self.QuntD
        if self.QuntD >= 3 : 
            prix *= (100 - hotel["avantage"]) * 0.01

        return prix


             







                














            