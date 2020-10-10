# -*- coding: utf-8 -*-


"""
作业脚本列表
"""

Cert_Deploy_Job_Script = """#!/bin/bash

if [ $# -lt 4 ] ;then
    echo "Usage: $0 domain path crt key [script]"
    exit -1
fi

RETVAL=0

DOMAIN_NAME=`echo $1 |awk -F':' '{print $1}'`
CERT_PATH=$2
CERT_CRT=$3
CERT_KEY=$4
SCRIPT=$5

echo "检查并创建证书存放路径"
[ -d ${CERT_PATH} ] || mkdir -p ${CERT_PATH}

echo "写入证书${CERT_PATH}/${DOMAIN_NAME}.crt"
echo $CERT_CRT | base64 -d  >${CERT_PATH}/${DOMAIN_NAME}.crt

echo "写入证书秘钥${CERT_PATH}/${DOMAIN_NAME}.crt"
echo $CERT_KEY| base64 -d >${CERT_PATH}/${DOMAIN_NAME}.key

if [ $SCRIPT != "" ];then
  SCRIPT=`echo ${SCRIPT} | base64 -d`
  echo "执行服务管理脚本${SCRIPT}"
  $SCRIPT
  RETVAL=$?
fi
sleep 5
exit $RETVAL
"""