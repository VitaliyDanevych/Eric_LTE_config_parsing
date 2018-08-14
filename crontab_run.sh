#!/bin/sh

export ORACLE_HOME=/u01/app/oracle/product/11.2.0/client_1
export PATH=/usr/kerberos/bin:/usr/local/bin:/bin:/usr/bin:/home/optima/bin:/home/optima:/usr/bin/perl:/opt/optima:/u01/app/oracle/product/11.2.0/client_1/bin
WORK_DIR=/opt/optima/Interfaces/Configuration/loader

sqlldr GLOXXX@OPTXXX/GLOXXX control=$WORK_DIR/configuration_conf_cell_4G_Ericsson.ctl
sqlldr GLOXXX@OPTXXX/GLOXXX control=$WORK_DIR/configuration_conf_cell_4G_Ericsson_2.ctl
