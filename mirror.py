#!/usr/bin/python
# -*- coding: utf-8 -*-
import binascii #pour convertir l'hexa en string
from urllib2 import Request, urlopen, URLError, HTTPError #pour pouvoir appeler une url
import socket #pour afficher gérer les sockets (utilisé ici que pour afficher une erreur de timeout)
from xml.dom.minidom import parse #pour pouvoir parser un fichier XML  avec minidom

#ouvre le fichier XML en utilisant le parser 'minidom'
DOMTree = parse("mirror.xml")
#construit l'arbre de la structure du fichier XML et le stock dans une variable
collection = DOMTree.documentElement
#récupére tous les éléments qui ont pour tag 'rfid' de l'arbre
puces = collection.getElementsByTagName("rfid")

#crée deux listes, une pour les puces posée et une pour les puces retirée
liste_puces_posee = []
liste_puces_retire = []

#on parcourt l'arbre qui contient toutes les puces et rempli les listes en fonction de l'action et de l'état indiqué dans le fichier XML
for puce in puces:
  id_puce = puce.getAttribute("id")
#  descriptif = puce.getElementsByTagName('descriptif')[0].childNodes[0].nodeValue
  etat = puce.getElementsByTagName('etat')[0].childNodes[0].nodeValue
  action = puce.getElementsByTagName('action')[0].childNodes[0].nodeValue
  url = puce.getElementsByTagName('url')[0].childNodes[0].nodeValue
#  commentaire = puce.getElementsByTagName('commentaire')[0].childNodes[0].nodeValue
  #detail_puce = [id_puce, [descriptif, url, commentaire]]
  detail_puce = [id_puce, url]

  if etat == 'actif':
    if action == 'pose':
      liste_puces_posee.append(detail_puce)
    if action == 'retire':
      liste_puces_retire.append(detail_puce)

#ouverture du port hidraw0 (port du mir:ror) en mode lecture octet par octet (rb)
mirror = open("/dev/hidraw0", "rb")

erreur_generale = False
while erreur_generale == False:
  #on lit les données envoyées par le mir:ror
  try:
    donnee = mirror.read(16)
  except Exception as e:
    print "Erreur inconnue (lecture du  mir:ror) : %s" % e
    erreur_generale = True

  #on test les données renvoyées par le mir:ror
  if donnee != '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
    try:
      rfid_id = binascii.hexlify(donnee)[4:]
    except Exception as e:
      print "Erreur inconnue (conversion binaire-string) : %s" % e

    #on test les 2 premiers octets pour savoir si une puce RFID est posée ou retirée
    if donnee[0:2] == '\x02\x01': #puce posée
      #liste des puces qui doivent faire une action quand la pose sur le mir:ror

      puce_definie_dans_xml = False
      #'puces_posee' va prendre les valeurs successives des éléments de 'liste_puces_posee'
      for i, puces_posee in liste_puces_posee:
        if rfid_id == format(i):
          requete = Request(format(puces_posee))
          try:
            #on essaye d'appeler la requête
            url = urlopen(requete, timeout = 1)
          except HTTPError as e:
            print 'Le serveur n''a pas pu répondre à la demande.'
            print 'Error code: ', e.code
          except URLError as e:
            try:
              if e.reason.errno == 111:
                print "Connexion refusée."
              if isinstance(e.reason, socket.timeout):
                print "Temps de connexion dépassé."
            except:
              print "Erreur  : %s" % e.reason

          puce_definie_dans_xml = True

      if puce_definie_dans_xml == False:
        print "Puce %s posée." % rfid_id

    elif donnee[0:2] == '\x02\x02': #puce retirée
      #liste des puces qui doivent faire une action quand la retire sur le mir:ror

      puce_definie_dans_xml = False
      #'puces_retire' va prendre les valeurs successives des éléments de 'liste_puces_retire'
      for i, puces_retire in liste_puces_retire:
        if rfid_id == format(i):
          requete = Request(format(puces_retire))
          try:
            #on essaye d'appeler la requête
            url = urlopen(requete, timeout = 1)
          except HTTPError as e:
            print 'Le serveur n''a pas pu répondre à la demande.'
            print 'Error code: ', e.code
          except URLError as e:
            try:
              if e.reason.errno == 111:
                print "Connexion refusée."
              if isinstance(e.reason, socket.timeout):
                print "Temps de connexion dépassé."
            except:
              print "Erreur  : %s" % e.reason

          puce_definie_dans_xml = True

      if puce_definie_dans_xml == False:
        print "Puce %s retirée." % rfid_id

    #on test le ler octet, s'il vaut 1, alors une action à été faite sur le mir:ror
    if donnee[0] == '\x01':

      if donnee[1] == '\x04':
        print "Le mir:ror est retourné face vers le haut"
      if donnee[1] == '\x05':
        print "Le mir:ror est retourné face vers le bas"
