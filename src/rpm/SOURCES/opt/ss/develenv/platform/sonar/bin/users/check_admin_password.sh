#!/bin/bash
netrc_file=/opt/ss/develenv/platform/sonar/conf/.admin_password
grep -qE " admin$" "${netrc_file:?}" && exit 1
curl --netrc-file "${netrc_file:?}" -fs "http://localhost/api/issues/tags"