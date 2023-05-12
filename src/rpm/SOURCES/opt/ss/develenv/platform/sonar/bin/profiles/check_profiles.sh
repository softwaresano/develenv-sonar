#!/bin/bash
netrc_file=/opt/ss/develenv/platform/sonar/conf/.admin_password
curl -s --netrc-file "${netrc_file:?}" -X GET "http://localhost/api/qualityprofiles/search" | grep -q '"name":"CDN"'
