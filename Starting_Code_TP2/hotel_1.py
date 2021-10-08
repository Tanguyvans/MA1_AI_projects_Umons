#Hotel_1
from pade.misc.utility import display_message, start_loop, call_later
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from sys import argv
from pade.acl.filters import Filter
import pickle

class Hotel_1(Agent):
    #definir les paramètre de l'hotel N° 1 : 
    nbrMaxPersAccepte = 3 #parametre qui definie le nombre de maximum de personnes accepté par chambre
    prix = 96.98 # prix par personne
    ville ="Paris"
    stock =50 # chambre disponibles
    nbrEtoiles=4 # nombre d'etoiles proposées
    reduction =25 # en cas de demande de 3 nuits ou plus, un pourcentage de réduction peut être appliqué au niveau de l'agence
    def __init__(self, aid):
        super(Hotel_1, self).__init__(aid=aid, debug=False)
    def on_start(self):
        super(Hotel_1, self).on_start()
        display_message(self.aid.localname, "Demarrage de l'agent Hotel_1 - reception des demandes en cours ...")

    def react(self, message):

        super(Hotel_1, self).react(message)
        perCFP="cfp"
        ontoCFP="contactHot1"
        perAccept="accept-proposal"
        perReject="reject-proposal"
        super(Hotel_1, self).react(message)
        if message.performative==perCFP and message.ontology==ontoCFP:
            print("Hotel_1 : Commande recu Tentative de reservation cours ...")
            Offre = ACLMessage(ACLMessage.PROPOSE)
            Offre.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
            Offre.add_receiver(AID('agence'))
            Offre.set_ontology("offrePropose")
            offreP={'nameHotel' : 'hotel_1', 'nbrMaxPersAccepte' : Hotel_1.nbrMaxPersAccepte, 'prix' : Hotel_1.prix, 'ville' : Hotel_1.ville, 'avantage' : Hotel_1.reduction, 'nbrEtoilesP' : Hotel_1.nbrEtoiles}
            ob=pickle.dumps(offreP)
            Offre.set_content(ob)
            self.send(Offre)
            
        if message.performative==perReject:
            print("Hotel_1 : Tentative de reservation refusée par l'agence - peut être une autre fois\n")

        if message.performative==perAccept:
            print("Hotel_1 : Reservation confirmé - contact avec le client établie")
            Hotel_1.stock-=1
            print("Le nombre de disponibilité restantes est de : ", Hotel_1.stock)
