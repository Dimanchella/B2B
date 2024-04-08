#!/bin/sh
#"$@"
#exec "$SHELL"

show="cd /storage/www/web/1c/backend; ls -la; source venv/bin/activate; pwd; python3; fuser -vn tcp 8000"
backend="cd /storage/www/web/1c/backend; ls -la; source venv/bin/activate; pwd; python3 manage.py runserver"
frontend="cd /storage/www/web/1c/frontend; ls -la; pwd; npm run dev"

#gnome-terminal --tab --title="show" --command "bash -c '$show; $SHELL;'" \
gnome-terminal --tab --title="backend" --command "bash -c '$backend; $SHELL;'"
gnome-terminal --tab --title="frontend" --command "bash -c '$frontend; $SHELL;'"

sleep 10s
xdg-open http://localhost:8000/admin/
xdg-open http://localhost:3000/