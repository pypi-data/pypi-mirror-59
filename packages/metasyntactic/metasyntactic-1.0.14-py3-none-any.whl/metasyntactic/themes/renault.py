# -*- coding: utf-8 -*-
'''

############################
Acme::MetaSyntactic::renault
############################

****
NAME
****


Acme::MetaSyntactic::renault - Renault cars


***********
DESCRIPTION
***********


Car types from the French car manufacturer \ *Renault*\ .


***********
CONTRIBUTOR
***********


Abigail


*******
CHANGES
*******



- \*
 
 2012-11-05 - v1.000
 
 Published in Acme-MetaSyntactic-Themes version 1.026.
 


- \*
 
 2012-10-24
 
 Made into a multilist, and updated with the models listed on the French
 Wikipedia page `https://fr.wikipedia.org/wiki/V%C3%A9hicules_Renault <https://fr.wikipedia.org/wiki/V%C3%A9hicules_Renault>`_.
 


- \*
 
 2005-10-27
 
 Submitted by Abigail.
 



********
SEE ALSO
********


`Acme::MetaSyntactic <http://search.cpan.org/search?query=Acme%3a%3aMetaSyntactic&mode=module>`_, `Acme::MetaSyntactic::MultiList <http://search.cpan.org/search?query=Acme%3a%3aMetaSyntactic%3a%3aMultiList&mode=module>`_.
'''

name = 'renault'
DATA = '''\
# names models
Renault_40CV
Renault_KJ
Renault_MT
Renault_KZ
Renault_NN
Renault_Monasix
Renault_Vivasix
Renault_Monastella
Renault_Vivastella
Renault_Reinastella
Renault_Nervastella
Renault_Monaquatre
Renault_Primaquatre
Renault_Vivaquatre
Renault_Primastella
Renault_Celtaquatre
Renault_Viva_Grand_Sport
Renault_Reinasport
Renault_Nerva_Grand_Sport
Renault_Juvaquatre
Renault_Novaquatre
Renault_Suprastella
Renault_4CV
Renault_Colorale
Renault_Fregate
Renault_Dauphine
Renault_Dauphinoise
Renault_Caravelle
Renault_Floride
Renault_Estafette
Renault_4
Renault_4_Fourgonnette
Renault_8_et_10
Renault_Rambler
Renault_16
Renault_6
Renault_12
Renault_15
Renault_17
Renault_5
Renault_30
Renault_14
Renault_20
Renault_18
Renault_Fuego
Renault_Master
Renault_9
Renault_11
Renault_Trafic
Renault_Supercinq
Renault_25
Renault_Espace
Renault_Express
Renault_21
Renault_19
Renault_Clio
Renault_Espace_II
Renault_Safrane
Renault_Twingo
Renault_Laguna
Renault_Megane
Renault_Scenic
Renault_Espace_III
Renault_Spider
Renault_Kangoo
Renault_Master
Renault_Clio_II
Renault_Laguna_II
Renault_Espace_IV
Renault_Avantime
Renault_Trafic_II
Renault_Megane_II
Renault_Vel_Satis
Renault_Scenic_II
Renault_Modus
Renault_Clio_III
Renault_Twingo_II
Renault_Laguna_III
Renault_Megane_III
Renault_Koleos
Renault_Kangoo_II
Renault_Fluence
Renault_Scenic_III
Renault_Latitude
Renault_Wind
Renault_Master
Renault_Twizy
Renault_Clio_IV
Renault_Zoe
# names alpine
Alpine_A106
Alpine_A108
Alpine_A110
Alpine_A310
Alpine_GTA
Alpine_A610
# names usa
Renault_Le_Car
Renault_18i_Sportwagon
Renault_Alliance
Renault_Encore
Renault_Fuego_GTA
Renault_Alpine_GTA
Renault_Medallion
Renault_Premier
# names emerging_countries
Renault_Logan
Renault_Sandero
Renault_Symbol_II
Renault_Duster
Renault_Pulse
# names formula_1
Renault_RS01
Renault_RS10
Renault_RE20
Renault_RE30
Renault_RE40
Renault_RE50
Renault_RE60
Renault_R202
Renault_R23
Renault_R24
Renault_R25
Renault_R26
Renault_R27
Renault_R28
Renault_R29\
'''

from metasyntactic.base import parse_data
from random import choice, shuffle
from six import iteritems
data = parse_data(DATA)


def default():
    try:
        if 'default' in data:
            return data['default'][0]
    except (KeyError, IndexError):
        pass
    return 'en'


def all():
    acc = set()
    for category, names in iteritems(data['names']):
        if names:
            acc |= names
    return acc


def names(category=None):
    if not category:
        category = default()
    if category == ':all':
        return list(all())
    category = category.replace('/', ' ')
    return list(data['names'][category])


def random(n=1, category=None):
    got = names(category)
    if got:
        shuffle(got)
        if n == 1:
            return choice(got)
        return got[:n]

def categories():
    return set(data['names'])


