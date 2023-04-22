#!/bin/bash
curl -su admin:$(cat /opt/ss/develenv/platform/sonar/conf/.admin_password) -X GET "http://localhost/api/users/groups?login=sonar" | grep -v "Unknown user: sonar"
