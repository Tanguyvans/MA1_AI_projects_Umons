#Agence
from pade.misc.utility import display_message, start_loop, call_later
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from sys import argv
from pade.acl.filters import Filter
import pickle

class Agence(Agent):

    clientMessage = {}

    nbrPers = 0 #variable qui va prendre le nombre de personnes demandé par le client
    QuntD =0 #variable qui va prendre le nombre de nuits souhaitées par le client
    ville ="" #variable qui va prendre le nom de la ville souhaité par le client
    etoiles =0 #variable qui va prendre le nombre d'étoile de l'hotel souhaité par le client
    decFinal=0 #variable qui va verifier si la demande du client correspond à l'un des meilleures offres de marchée
    nbrpro =0 #variable qui va compter le nombre d'article similaire (avec prix different)
    PrixFinal=0 # le toral du prix selon la quantité demandé, une réduction de 30% est appliqué sur le total, si quantité est > =3
    IdBestHotel=""
    contactTermine=0
    LesHotels= []

    countHotel = 0
    dictHotels = {}

    listPrix = [] #cette liste va sotocker les prix totaux de chaque demande correspondant à la demande du client pour selectionner le prix totalt minimal


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
    
    def contact_Client(self):
        
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_sender(AID('agence'))
        message.add_receiver(AID("client"))

        message.set_ontology("decision")
        contactHotel = {"nameHotel": self.IdBestHotel, "prixHotel": self.PrixFinal}
        new_msg = pickle.dumps(contactHotel)
        message.set_content(new_msg)
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
        # Contacter les hotels
        if message.ontology  == "cmdClient":
            self.saveClientMessage(message.content)
            call_later(3.0, self.contact_hot1)
            call_later(3.0, self.contact_hot2)
            call_later(3.0, self.contact_hot3)

        # Enregistrement de la réponse des hotels
        if message.ontology  == "offrePropose" and self.countHotel <= 3:
            self.countHotel += 1
            proposition = pickle.loads(message.content)
            self.LesHotels.append(proposition)
            print(F"{self.countHotel} hotel enregister")

        # Quand on a la réponse des 3 hotels, on choisit le meilleur
        if self.countHotel == 3:
            self.countHotel = 0
            print("Toutes les réponses sont reçues")
            self.choixHotel()


    def choixHotel(self):
        print('Nous allons sélectionner le meilleur')
        lesHotels = self.LesHotels
        dictHotels =self.dictHotels
        nbrPers = self.nbrPers
        ville = self.ville
        nuit = self.QuntD
        etoiles = self.etoiles

        for count, hotel in enumerate(lesHotels): 
            #Les hotels qui répondent aux attentes du client
            if hotel["nbrMaxPersAccepte"] >= nbrPers and hotel["ville"] == ville and hotel["nbrEtoilesP"] >= etoiles:
                # Calcule du prix total
                prix = nbrPers * hotel["prix"] * nuit
                if nuit>=3 : 
                    prix *= 1/hotel["avantage"] 
                dictHotels[hotel["nameHotel"]] = prix
            #Les hotels qui ne match pas avec les demandes du client
            else:
                #print(hotel["nameHotel"] + 'Vous ne correspondez pas aux attentes du client')
                self.refus(hotel["nameHotel"])
                #lesHotels.remove(hotel)

        flag = True
        for key, val in dictHotels.items():
        
            if key == min(dictHotels, key=dictHotels.get) and flag:
                #print(key + "vous êtes le meilleur avec un prix de "+ str(val))
                self.accept(key)
                flag = False
                self.PrixFinal = val
                self.IdBestHotel = key
                self.contact_Client()



            else:
                #print(key + "vous n'etes pas le meilleur car votre prix est de "+ str(val))
                self.refus(key)




             







                














            