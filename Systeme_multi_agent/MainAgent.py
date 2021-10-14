#MainAgents

from pade.misc.utility import display_message, start_loop, call_later
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from sys import argv
from pade.acl.filters import Filter
import pickle

from Agence import Agence
from hotel_1 import Hotel_1
from hotel_2 import Hotel_2
from hotel_3 import Hotel_3
from Client import Client

def addNewAgent (agents, Class, name_agent, port):
    agents.append(Class(AID(name=name_agent+'@localhost:{}'.format(port))))
    

if __name__ == '__main__':
    agents = list()
    port = int(argv[1])
    
    nameAgents = [[Hotel_1, "hotel_1"], [Hotel_2, "hotel_2"], [Hotel_3, "hotel_3"], [Agence, "agence"], [Client, "client"]]

    for agent in nameAgents:
        addNewAgent(agents, agent[0], agent[1], port)
        port += 1

    start_loop(agents)
