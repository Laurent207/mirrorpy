#! /bin/sh
### BEGIN INIT INFO
# Provides:          mirrorpy
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Démarrage du script pour le mirror
# Description:       Script qui lit les données du mir:ror et appel des requêtes http en fonction de ce qui est dé$
### END INIT INFO

#chemin où se trouve le script python
DIR="/home/pi/mirrorpy"
#nom du fichier qui contient le script python
DAEMON=$DIR/mirror.py
#argument à utiliser par le programme
DEAMON_OPT=""
#nom du service
DEAMON_NAME="mirrorpy"
#utilisateur du programme
DAEMON_USER="root"

# The process ID of the script when it runs is stored here:
PIDFILE=/var/run/$DAEMON_NAME.pid

. /lib/lsb/init-functions

do_start () {
  log_daemon_msg "Démarrage du service $DEAMON_NAME"
  start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER --exec $DAEMON
  log_end_msg $?
}
do_stop () {
  log_daemon_msg "Arrêt du service $DEAMON_NAME"
  start-stop-daemon --stop --pidfile $PIDFILE --retry 10
  log_end_msg $?
}

case "$1" in
  start|stop)
    do_${1}
    ;;

  restart|reload|force-reload)
    do_stop
    do_start
    ;;

  force-stop)
    do_stop
    killall -q $DEAMON_NAME || true
    sleep 2
    killall -q -9 $DEAMON_NAME || true
    ;;

  status)
    status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
    ;;

  *)
    echo "Utilisation : /etc/init.d/$DEAMON_NAME {start|stop|force-stop|restart|reload|force-reload|status}"
    exit 1
    ;;

esac
exit 0
