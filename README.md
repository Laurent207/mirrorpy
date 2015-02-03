# mirrorpy
Pré-requis :
- un mir:ror.
- au moins une puce RFID (le mir:ror peux lire les nanoztag, les zstamps, les puces de Disney infinity 1&2 ou Skylanders).
- un raspberry pi (ou un pc sous linux).
- python 2.x

1. Télécharger et copiez mirror.py et mirror.xml sur le rpi.
2. Modifier le fichier mirror.xml comme vous le souhaitez pour ajouter vos puces . Pour l'instant il n'y a aucun contrôle sur l'intégrité du fichier xml, donc soyez attentif à vos modifications.
3. Pour exécuter le script, tapez :
    sudo python /home/pi/mirror.py
ps : script écrit sous archlinux avec python 2.7 (tapez python -V dans une console pour connaître la version que vous utilisé par défaut).
