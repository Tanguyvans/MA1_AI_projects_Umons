#Client
from pade.misc.utility import display_message, start_loop, call_later
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from sys import argv
from pade.acl.filters import Filter
import pickle

class Client(Agent):
    def __init__(self, aid):
        super(Client, self).__init__(aid=aid, debug=False)
    def on_start(self):
        super(Client, self).on_start()
        display_message(self.aid.localname, "Demarrage de l'agent Client : Envoie de la demande en cours ...")
        call_later(8.0, self.sending_cmd)

    def sending_cmd(self):
        message = ACLMessage(ACLMessage.REQUEST)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_sender(AID('client'))
        message.add_receiver(AID('agence'))
        message.set_ontology("cmdClient")
        RESERVATION = {"personne": 2, "nuit": 3, "ville": 'Mons', "etoiles": 3, 'prix' : 220} 
        RESERVATION_encp = pickle.dumps(RESERVATION)
        message.set_content(RESERVATION_encp)
        self.send(message)
        print('>>> Demande du client envoyée')
        
    def react(self, message):
        onto="decision"
        perOK="agree"
        perNotOK="reject-proposal"
        super(Client, self).react(message)

        if message.ontology  == onto:
            proposition = pickle.loads(message.content)
            #print(" l'hotel qu'on me propose est de : "+ proposition["nameHotel"]+ " le prix par personne est de : " + str(proposition["prixHotel"]))
            for key, val in proposition.items():
                print(key, val+'%')

