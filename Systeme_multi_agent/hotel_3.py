#Hotel_3
from pade.misc.utility import display_message, start_loop, call_later
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from sys import argv
from pade.acl.filters import Filter
import pickle

class Hotel_3(Agent):
    #definir les paramètre de l'hotel N° 1 : 
    nbrMaxPersAccepte = 2 #parametre qui definie le nombre de maximum de personnes accepté par chambre
    prix = 80 # prix par personne
    ville ="Mons"
    stock = 4 # chambre disponibles
    nbrEtoiles = 3 # nombre d'etoiles proposées
    reduction = 35 # en cas de demande de 3 nuits ou plus, un pourcentage de réduction peut être appliqué au niveau de l'agence

    def __init__(self, aid):
        super(Hotel_3, self).__init__(aid=aid, debug=False)
    def on_start(self):
        super(Hotel_3, self).on_start()
        display_message(self.aid.localname, "Demarrage de l'agent Hotel_3 - reception des demandes en cours ...")

    def react(self, message):
        super(Hotel_3, self).react(message)
        perCFP="cfp"
        ontoCFP="contactHot3"
        perAccept="accept-proposal"
        perReject="reject-proposal"
        super(Hotel_3, self).react(message)
        if message.performative==perCFP and message.ontology==ontoCFP:
            print("Hotel_3 : Commande recu Tentative de reservation cours ...")
            Offre = ACLMessage(ACLMessage.PROPOSE)
            Offre.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
            Offre.add_receiver(AID('agence'))
            Offre.set_ontology("offrePropose")
            offreP={'nameHotel' : 'hotel_3', 'nbrMaxPersAccepte' : Hotel_3.nbrMaxPersAccepte, 'prix' : Hotel_3.prix, 'ville' : Hotel_3.ville, 'avantage' : Hotel_3.reduction, 'nbrEtoilesP' : Hotel_3.nbrEtoiles}
            ob=pickle.dumps(offreP)
            Offre.set_content(ob)
            self.send(Offre)

        if message.performative==perReject:
            print("Hotel_3 : Tentative de reservation refusée par l'agence")

        if message.performative==perAccept:
            print("Hotel_3 : Reservation confirmée")
            Hotel_3.stock-=1
            #print("Le nombre de disponibilité restantes est de : ", Hotel_3.stock)
