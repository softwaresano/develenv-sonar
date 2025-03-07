#!/bin/bash -e
netrc_file=/opt/ss/develenv/platform/sonar/conf/.admin_password
curl -s --netrc-file "${netrc_file:?}" -X POST "http://localhost/api/users/create?login=sonar&name=sonar&local=true&password=sonar"
curl -f -u sonar:sonar -X POST "http://localhost/api/user_tokens/generate" -d "name=global_analysis_token" -d "type=GLOBAL_ANALYSIS_TOKEN" -d "expirationDate=9999-12-31" > /opt/ss/develenv/platform/sonar/conf/.sonar_token
