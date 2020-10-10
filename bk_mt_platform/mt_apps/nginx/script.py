# -*- coding: utf-8 -*-

CertPushScript="""
echo "检查并创建证书存放路径"
[ -d {CERT_PATH} ] || mkdir -p {CERT_PATH}

echo "写入证书{CERT_PATH}/{DOMAIN_NAME}.crt"
echo {CERT_CRT} | base64 -d  >{CERT_PATH}/{DOMAIN_NAME}.crt

echo "写入证书秘钥{CERT_PATH}/{DOMAIN_NAME}.crt"
echo {CERT_KEY}| base64 -d >{CERT_PATH}/{DOMAIN_NAME}.key
"""

NginxBasePushScript="""#!/bin/bash
echo "写入{CONF_DIR}/nginx.conf"
echo {NGINX_CONFIG} | base64 -d  >{CONF_DIR}/nginx.conf
"""

NginxVhostPushScript="""
echo "清理{VHOST_DIR}/*.conf"
rm -rf {VHOST_DIR}/*.conf
for host in `echo {NGINX_CONFIG} | base64 -d `
do
    name=`echo $host|awk -F'@' '{{print $1}}'`
    content=`echo $host|awk -F'@' '{{print $2}}'`
    echo "写入{VHOST_DIR}/$name.conf"
    echo $content | base64 -d  >{VHOST_DIR}/$name.conf
done
"""