# -*- coding: utf8 -*-

import os
import settings
import json
import sys
import sewer
import base64
from datetime import datetime
from OpenSSL import crypto

from OpenSSL import SSL
from socket import socket
from datetime import datetime


def register(domain):
    account_key = ''
    account_key_file = ''
    info = {}
    client = None
    mjjisangel_domains = ['.youngjoygame.com', '.mobilelegends.com', '.yuanzhangame.com', '.yuanzhangame.net',
                          '.wujinduijue.cn', '.wujinduijue.net', '.wujinduijue.com', '.yuanzhanapp.cn',
                          '.yuanzhanapp.net', '.yuanzhanapp.com', '.yuanzhangame.cn']

    domain_list = domain.split('.')
    domain_endswith = '.' + domain_list[-2] + '.' + domain_list[-1]

    if domain_endswith in mjjisangel_domains:
        account_key_file = os.path.join(settings.TMP_DIR, 'mjjisangel_account_key')
        key = 'LTAI4FkZrV2iwUcP9nSwN9nn'
        secret = 'kHyJhXgX79I7Xi640p1pdsgqTUWis1'
    else:
        account_key_file = os.path.join(settings.TMP_DIR, 'moonton_account_key')
        key = 'LTAIPlRemlCEClEO'
        secret = 'tyCTjcLqFoaRCJgxN08V5Rslc4qHMs'

    if os.path.exists(account_key_file):
        try:
            with open(account_key_file, 'r') as f:
                account_key = f.read()
        except:
            pass

    dns_class = sewer.AliyunDns(key=key, secret=secret)
    if account_key:
        try:
            client = sewer.Client(domain_name=domain, dns_class=dns_class, account_key=account_key)
        except:
            os.remove(account_key_file)
    else:
        client = sewer.Client(domain_name=domain, dns_class=dns_class)
        account_key = client.account_key
        with open(account_key_file, 'w') as f:
            f.write(account_key)

    domain_name = client.domain_name
    certificate = client.cert()
    certificate_key = client.certificate_key

    cert = crypto.load_certificate(crypto.FILETYPE_PEM, certificate)

    info["created"] = datetime.strptime(cert.get_notBefore().decode()[0:-1], '%Y%m%d%H%M%S').strftime(
        '%Y-%m-%d %H:%M:%S')
    info["expired"] = datetime.strptime(cert.get_notAfter().decode()[0:-1], '%Y%m%d%H%M%S').strftime(
        '%Y-%m-%d %H:%M:%S')

    info['domain'] = domain_name
    info['crt'] = certificate
    info['key'] = certificate_key

    return info


def callback(conn, cert, errno, depth, result):
    if depth == 0 and (errno == 9 or errno == 10):
        return False  # or raise Exception("Certificate not yet valid or expired")
    return True


def CertInfo(host_name, port=443, cdn_status=0):
    info = {"notbefore": None, "notafter": None}

    try:
        context = SSL.Context(SSL.TLSv1_2_METHOD)  # Use TLS Method
        context.set_options(SSL.OP_NO_SSLv2)  # Don't accept SSLv2
        context.set_verify(SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
                           callback)

        sock = socket()
        ssl_sock = SSL.Connection(context, sock)
        ssl_sock.set_tlsext_host_name(host_name.encode('utf-8'))
        ssl_sock.connect((host_name, port))
        ssl_sock.do_handshake()

        cert = ssl_sock.get_peer_certificate()

        subject = cert.get_subject().get_components()
        num = len(subject) - 1
        subject_domain = str(subject[num][1]).split("'")[1]

        if cdn_status == 0:
            if subject_domain == host_name or host_name.endswith(subject_domain.lstrip('*.')):
                info["notbefore"] = datetime.strptime(cert.get_notBefore().decode()[0:-1], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
                info["notafter"] = datetime.strptime(cert.get_notAfter().decode()[0:-1], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
        else:
            info["notbefore"] = datetime.strptime(cert.get_notBefore().decode()[0:-1], '%Y%m%d%H%M%S').strftime(
                '%Y-%m-%d %H:%M:%S')
            info["notafter"] = datetime.strptime(cert.get_notAfter().decode()[0:-1], '%Y%m%d%H%M%S').strftime(
                '%Y-%m-%d %H:%M:%S')

    except Exception as e:
        print(e)

    return info


if __name__ == '__main__':
    #print(CertInfo('accountmt.moonton.com',443,1))
    print(CertInfo('akmstatic.ml.youngjoygame.com',443,1))
    # print(CertInfo('job.moonton.com'))
