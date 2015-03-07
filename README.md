# mirrorpy
Pré-requis :
- un mir:ror.
- au moins une puce RFID (le mir:ror peux lire les nanoztag, les zstamps, les puces de Disney infinity 1&2 ou Skylanders).
- un raspberry pi (ou un pc sous linux).
- python 2.x

A faire que si vous n'éte pas déjà connecté  avec le compte utilisateur : pi
*su pi*

On se place dans le répertoire home de l'utilisateur pi
*cd /home/pi*

On récupère les sources depuis github
*git clone --depth=0 git://github.com/Laurent207/mirrorpy.git*

On donne les droits d'exécution au script
*chmod +x /home/pi/mirrorpy/mirror.py*

Pour vérifier que le script fonctionne bien. S'il y a une erreur, ne pas aller plus loin et contacter laurent207 sur http://nabaztag.forumactif.fr/t15046-script-python-pour-piloter-un-mirror-pour-raspberry-pi ou sur le github du projet.
*sudo ./mirror.py*

Copiez le fichier du service dans le répertoire
*sudo cp /home/pi/mirrorpy/mirror.sh /etc/init.d*

Editer le fichier du service pour vérifier que les chemins sont bon (la commande linux qui permet de connaitre le chemin complet ou l'on se situe est : pwd

Edition du fichier du service(daemon). Modifiez DIR, DAEMON, DEAMON_OPT, DEAMON_NAME et DAEMON_USER (ligne 13, 15, 17, 19 et 21), si nécessaire.
*sudo nano /etc/init.d/mirror.sh*

Si vous avez modifier le fichier, faire ALT+'x', puis 'o' pour oui ou 'y' pour yes (ça dépand de la langue de l'os du rpi, puis 'entrée'

On donne les droits d'exécution au service
*sudo chmod +x /etc/init.d/mirror.sh*

On test l'exécution du fichier du service
*sudo /etc/init.d/mirror.sh start*

Normalement, vous devez voir : [ ok ] Démarrage du service mirrorpy:.
S'il y a une erreur, ne pas aller plus loin et contacter laurent207 sur http://nabaztag.forumactif.fr/t15046-script-python-pour-piloter-un-mirror-pour-raspberry-pi ou sur le github du projet.

Voici la liste des commandes pour gérer le service :
*sudo /etc/init.d/mirror.sh start*
*sudo /etc/init.d/mirror.sh status*
*sudo /etc/init.d/mirror.sh stop*
*sudo /etc/init.d/mirror.sh force-stop*
*sudo /etc/init.d/mirror.sh restart*
*sudo /etc/init.d/mirror.sh reload*
*sudo /etc/init.d/mirror.sh force-reload*

- Enfin cette ligne sert à lancer automatiquement le service au démarrage du raspberry pi
*sudo update-rc.d mirror.sh defaults*

Modifier le fichier mirror.xml comme vous le souhaitez pour ajouter vos puces . Pour l'instant il n'y a aucun contrôle sur l'intégrité du fichier xml, donc soyez attentif à vos modifications.

ps : script écrit sous raspbian avec python 2.7 (tapez python -V dans une console pour connaître la version que vous utilisé par défaut).

# Reste à faire :
- Ajouter un système de log qui évite d'écrire sur la SD pour sauvegarder la durée de vie de la carte SD.
- Ajouter des paramètres supplémentaire dans l'xml pour permettre d'éteindre la lumière et de couper le son du mir:ror.
- Ajouter une mini interface web pour faciliter la modification du fichier xml.
