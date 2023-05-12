#!/bin/bash
netrc_file=/opt/ss/develenv/platform/sonar/conf/.admin_password
curl -s --netrc-file "${netrc_file:?}" -X POST "http://localhost/api/users/create?login=sonar&name=sonar&local=true&password=sonar"
