#!/bin/sh

while getopts dlgs mode
do
case "${mode}" in
  d)
  echo "--> runserver"
  python manage.py runserver $2
  ;;
  l)
  echo "--> runserver with log"
  python manage.py runserver $2 > log-backend.txt 2>&1
  ;;
  g)
  echo "--> run gunicon start"
  ;;
  s)
  sleep 3s
  xdg-open http://localhost:8000/admin/
  ;;
esac
done
