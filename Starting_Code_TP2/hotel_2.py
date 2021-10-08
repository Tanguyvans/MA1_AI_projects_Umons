#Hotel_2
from pade.misc.utility import display_message, start_loop, call_later
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from sys import argv
from pade.acl.filters import Filter
import pickle

class Hotel_2(Agent):
    #definir les paramètre de l'hotel N° 1 : 
    nbrMaxPersAccepte = 2 #parametre qui definie le nombre de maximum de personnes accepté par chambre
    prix = 129.99 # prix par personne
    ville ="Paris"
    stock =20 # chambre disponibles
    nbrEtoiles=4 # nombre d'etoiles proposées
    reduction =35 # en cas de demande de 3 nuits ou plus, un pourcentage de réduction peut être appliqué au niveau de l'agence

    def __init__(self, aid):
        super(Hotel_2, self).__init__(aid=aid, debug=False)
    def on_start(self):
        super(Hotel_2, self).on_start()
        display_message(self.aid.localname, "Demarrage de l'agent Hotel_2 - reception des demandes en cours ...")

    def react(self, message):
        super(Hotel_2, self).react(message)
        perCFP="cfp"
        ontoCFP="contactHot2"
        perAccept="accept-proposal"
        perReject="reject-proposal"
        super(Hotel_2, self).react(message)
        if message.performative==perCFP and message.ontology==ontoCFP:
            print("Hotel_2 : Commande recu Tentative de reservation cours ...")
            Offre = ACLMessage(ACLMessage.PROPOSE)
            Offre.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
            Offre.add_receiver(AID('agence'))
            Offre.set_ontology("offrePropose")
            offreP={'nameHotel' : 'hotel_2','nbrMaxPersAccepte' : Hotel_2.nbrMaxPersAccepte, 'prix' : Hotel_2.prix, 'ville' : Hotel_2.ville, 'avantage' : Hotel_2.reduction, 'nbrEtoilesP' : Hotel_2.nbrEtoiles}
            ob=pickle.dumps(offreP)
            Offre.set_content(ob)
            self.send(Offre)

        if message.performative==perReject:
            print("Hotel_2 : Tentative de reservation refusée par l'agence - peut être une autre fois\n")

        if message.performative==perAccept:
            print("Hotel_2 : Reservation confirmé - contact avec le client établie")
            Hotel_2.stock-=1
            print("Le nombre de disponibilité restantes est de : ", Hotel_2.stock)

