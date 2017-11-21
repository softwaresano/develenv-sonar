#!/bin/bash
mkdir -p  src/rpm/SOURCES/opt/ss/develenv/platform/sonar/
rsync --delete -avr /home/develenv/SONAR/* \
  src/rpm/SOURCES/opt/ss/develenv/platform/sonar/

dp_package.sh