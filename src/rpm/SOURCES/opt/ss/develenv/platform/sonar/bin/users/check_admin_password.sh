#!/bin/bash
netrc_file=/opt/ss/develenv/platform/sonar/conf/.admin_password
grep -qE " admin$" "${netrc_file:?}" && echo "[ERROR] admin is de default password. Change the password" && exit 1
curl --netrc-file "${netrc_file:?}" -fs "http://localhost/api/issues/tags"
