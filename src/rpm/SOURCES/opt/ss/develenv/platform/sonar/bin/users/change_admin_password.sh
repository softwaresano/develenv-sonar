#!/bin/bash -e
password=${1:-$(cat /opt/ss/develenv/platform/sonar/conf/.admin_password)}
if curl -fsu "admin:${password}" "http://localhost/api/issues/tags"; then
  echo "[ERROR] password not changed"
  exit 1
fi
old_password=$(cat /opt/ss/develenv/platform/sonar/conf/.admin_password)
curl -fsu "admin:${old_password:?}" -X POST \
"http://localhost/api/users/change_password?login=admin&password=${password:?}&previousPassword=${old_password:?}"
echo "${password:?}" > /opt/ss/develenv/platform/sonar/conf/.admin_password
echo "Password changed"
