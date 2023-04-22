#!/bin/bash
curl -fsu admin:$(cat /opt/ss/develenv/platform/sonar/conf/.admin_password) -X POST "http://localhost/api/users/create?login=sonar&name=sonar&local=true&password=sonar"
