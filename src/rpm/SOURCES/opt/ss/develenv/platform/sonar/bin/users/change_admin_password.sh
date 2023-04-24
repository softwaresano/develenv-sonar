#!/bin/bash -e
netrc_file=/opt/ss/develenv/platform/sonar/conf/.admin_password
old_password=$(grep -Po "(?<= password ).*" "${netrc_file:?}")
curl -fs curl --netrc-file "${netrc_file:?}" -X POST \
"http://localhost/api/users/change_password?login=admin&password=${password:?}&previousPassword=${old_password:?}"
echo "machine localhost login admin password ${password:?}" > /opt/ss/develenv/platform/sonar/conf/.admin_password
echo "Password changed"
