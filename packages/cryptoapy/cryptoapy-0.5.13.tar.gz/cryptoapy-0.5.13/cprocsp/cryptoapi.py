#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from . import csp, PROV_GOST
from .certutils import Attributes, CertValidity, KeyUsage, EKU,\
    CertExtensions, SubjectAltName, CertificatePolicies, PKCS7Msg, \
    CertExtension, CertificateInfo, autopem, set_q_defaults

import platform
from binascii import hexlify, unhexlify
from .filetimes import filetime_from_dec
from datetime import datetime, timedelta
from binascii import b2a_qp, a2b_qp
import sys
import time
from functools import wraps
if sys.version_info >= (3,):
    unicode = str

    def ord(x):
        return x
else:
    unicode = unicode

PROV_KC1_GR3410_2001 = str("Crypto-Pro GOST R 34.10-2001 KC1 CSP")
PROV_KC2_GR3410_2001 = str("Crypto-Pro GOST R 34.10-2001 KC2 CSP")
PROV_KC1_GR3410_2012 = str("Crypto-Pro GOST R 34.10-2012 KC1 CSP")
PROV_KC2_GR3410_2012 = str("Crypto-Pro GOST R 34.10-2012 KC2 CSP")
PROV_HSM = str("Crypto-Pro HSM CSP")
PROV_GR3410_2001_HSM_LOCAL = str("Crypto-Pro GOST R 34.10-2001 HSM Local CSP")
PROV_GR3410_2012_HSM_LOCAL = str("Crypto-Pro GOST R 34.10-2012 HSM Local CSP")


# Обертка для функций, которые могут не сработать из-за длительного простоя
# туннеля, при работе с криптопровайдером внешнего хранилища. Максимальный
# таймаут = 0.25 + 0.5 + 1.0 = 1.75 секунд


def retry(f, timeout=0.25, num_tries=4):
    @wraps(f)
    def wrapper(*args, **nargs):
        sleep_time = timeout
        for tr in range(num_tries):
            try:
                return f(*args, **nargs)
            except Exception:
                if tr == num_tries - 1:
                    raise
                time.sleep(sleep_time)
                sleep_time *= 2

    return wrapper


def _to_hex(s):
    return unicode(b2a_qp(s), 'ascii').replace('=', '\\x')


def _from_hex(s):
    if isinstance(s, bytes):
        s = unicode(s, 'ascii')
    return a2b_qp(s.replace('\\x', '='))


def _mkcontext(cont, provider, flags=None):
    if cont is None:
        return None

    cont = _from_hex(cont)

    if flags is None:
        flags = csp.CRYPT_VERIFYCONTEXT

    if isinstance(provider, tuple):
        provider, provtype = provider
    elif provider == PROV_HSM:
        provtype = csp.PROV_GOST_2001_DH
    else:
        provtype = PROV_GOST

    return csp.Crypt(cont, provtype, flags, provider)


def gen_key(cont, local=True, silent=False, provider=None):
    '''
    Создание контейнера и двух пар ключей в нем

    :cont: Имя контейнера (строка)
    :local: Если True, контейнер создается в локальном хранилище по умолчанию
    :silent: Если True, включает режим без диалоговых окон. Без аппаратного датчика случайных
        чисел в таком режиме контейнер создать невозможно!
        По умолчанию silent=False
    :provider: По умолчанию None, в этом случае флаг local игнорируется и
        криптопровайдер выбирается принудительно.

        Если в качестве криптопровайдера передана строка, то она используется в
        качестве имени, тип берется из константы PROV_GOST.
        Если передан кортеж вида (тип, имя), то в создании контекста участвуют
        оба переданных параметра.
    :returns: True, если операция успешна

    '''
    silent_flag = csp.CRYPT_SILENT if silent else 0

    cont = _from_hex(cont)

    if provider is None and not local:
        provider = PROV_HSM
    try:
        ctx = _mkcontext(cont, provider, silent_flag)
    except (ValueError, SystemError):
        if platform.system() == 'Linux' and provider != PROV_HSM and not cont.startswith(b'\\\\'):
            cont = b'\\\\.\\HDIMAGE\\' + cont
        ctx = _mkcontext(cont, provider, csp.CRYPT_NEWKEYSET | silent_flag)

    ctx.set_password(str(''), csp.AT_KEYEXCHANGE)
    ctx.set_password(str(''), csp.AT_SIGNATURE)
    try:
        key = ctx.get_key()
    except ValueError:
        key = ctx.create_key(csp.CRYPT_EXPORTABLE, csp.AT_SIGNATURE)

    assert key, 'NULL signature key'

    try:
        ekey = ctx.get_key(csp.AT_KEYEXCHANGE)
    except ValueError:
        ekey = ctx.create_key(csp.CRYPT_EXPORTABLE, csp.AT_KEYEXCHANGE)

    assert ekey, 'NULL exchange key'
    return True


def remove_key(cont, local=True, provider=None):
    '''
    Удаление контейнера

    :cont: Имя контейнера
    :local: Если True, контейнер удаляется в локальном хранилище по умолчанию
    :provider: По умолчанию None, в этом случае флаг local игнорируется и
        криптопровайдер выбирается принудительно.

        Если в качестве криптопровайдера передана строка, то она используется в
        качестве имени, тип берется из константы PROV_GOST.
        Если передан кортеж вида (тип, имя), то в создании контекста участвуют
        оба переданных параметра.
    :returns: True, если операция успешна

    '''
    cont = _from_hex(cont)
    if provider is None and not local:
        provider = PROV_HSM
    if isinstance(provider, tuple):
        provider, provtype = provider
    else:
        provtype = PROV_GOST
    csp.Crypt.remove(cont, provtype, provider)
    return True


def create_request(cont, params, local=True, provider=None, insert_zeroes=False):
    """Создание запроса на сертификат

    :cont: Имя контейнера
    :params: Параметры запроса в виде словаря следующего вида:
        {
        'Attributes' : список пар [('OID', 'значение'), ...],
        'CertificatePolicies' : список вида [(OID, [(квалификатор, значение), ...]), ... ]
            OID - идент-р политики
            квалификатор - OID
            значение - произвольная байтовая строка
        'ValidFrom' : Дата начала действия (объект `datetime`),
        'ValidTo' : Дата окончания действия (объект `datetime`),
        'EKU' : список OIDов,
        'SubjectAltName' : список вида [(тип, значение), (тип, значение), ]
            где значение в зависимости от типа:
                'otherName' : ('OID', 'байтовая строка')
                'ediPartyName' : ('строка', 'строка') или 'строка'
                'x400Address' : 'байтовая строка'
                'directoryName' : [('OID', 'строка'), ...]
                'dNSName' : строка
                'uniformResourceIdentifier' : строка
                'iPAddress' : строка
                'registeredID' : строка
        'KeyUsage' : список строк ['digitalSignature', 'nonRepudiation', ...]
        'RawExtensions' : список троек [('OID', 'байтовая строка', bool(CriticalFlag)), ...]
            предназначен для добавления в запрос произвольных расширений,
            закодированных в DER-кодировку внешними средставми
        }
    :local: Если True, работа идет с локальным хранилищем
    :provider: По умолчанию None, в этом случае флаг local игнорируется и
        криптопровайдер выбирается принудительно.

        Если в качестве криптопровайдера передана строка, то она используется в
        качестве имени, тип берется из константы PROV_GOST.
        Если передан кортеж вида (тип, имя), то в создании контекста участвуют
        оба переданных параметра.
    :insert_zeroes: Если True, в запрос добавляются нулевые значения для ИНН, ОГРН
    :returns: байтовая строка с запросом в DER-кодировке

    """

    if provider is None and not local:
        provider = PROV_HSM
    ctx = _mkcontext(cont, provider, csp.CRYPT_SILENT)
    req = csp.CertRequest(ctx)
    set_q_defaults(params, insert_zeroes)
    req.set_subject(Attributes(params.get('Attributes', [])).encode())
    validFrom, validTo = params.get('ValidFrom'), params.get('ValidTo')
    if validFrom is None and validTo is None:
        validity = None
    else:
        validity = CertValidity(validFrom or datetime.now(),
                                validTo or datetime.now() + timedelta(days=365))
    eku = EKU(params.get('EKU', []))
    usage = KeyUsage(params.get('KeyUsage', []))
    all_exts = [usage, eku]
    altname = params.get('SubjectAltName', [])
    if len(altname):
        all_exts.append(SubjectAltName(altname))
    pols = params.get('CertificatePolicies', [])
    if len(pols):
        all_exts.append(CertificatePolicies(pols))
    for (oid, data, crit) in params.get('RawExtensions', []):
        all_exts.append(CertExtension(str(oid), data, bool(crit)))
    ext_attr = CertExtensions(all_exts)
    if validity is not None:
        validity.add_to(req)
    ext_attr.add_to(req)
    return req.get_data()


def bind_cert_to_key(cont, cert, local=True, provider=None, store=False):
    """Привязка сертификата к закрытому ключу в контейнере

    :cont: Имя контейнера
    :cert: Сертификат в байтовой строке
    :local: Если True, работа идет с локальным хранилищем
    :provider: По умолчанию None, в этом случае флаг local игнорируется и
        криптопровайдер выбирается принудительно.

        Если в качестве криптопровайдера передана строка, то она используется в
        качестве имени, тип берется из константы PROV_GOST.
        Если передан кортеж вида (тип, имя), то в создании контекста участвуют
        оба переданных параметра.
    :store: Сохранять сертификат в контейнере провайдера (по умолчанию -- False)
    :returns: отпечаток сертификата в виде строки

    """
    if provider is None and not local:
        provider = PROV_HSM
    ctx = _mkcontext(cont, provider, csp.CRYPT_SILENT)
    cert = autopem(cert)
    newc = csp.Cert(cert)
    newc.bind(ctx)
    if store:
        key = ctx.get_key()
        key.store_cert(newc)
    else:
        cs = csp.CertStore(ctx, b"MY")
        cs.add_cert(newc)
    return hexlify(newc.thumbprint())


def get_certificate(thumb=None, name=None, cont=None, provider=None):
    """Поиск сертификатов по отпечатку или имени

    :thumb: отпечаток, возвращенный функцией `bind_cert_to_key`
    :name: имя субъекта для поиска (передается вместо параметра :thumb:)
    :cont: контейнер для поиска сертификата (если указан, thumb и name игнорируются)
    :provider: По умолчанию None, в этом случае используется дефолтный для
        провайдера PROV_GOST.

        Если в качестве криптопровайдера передана строка, то она используется в
        качестве имени, тип берется из константы PROV_GOST.
        Если передан кортеж вида (тип, имя), то в создании контекста участвуют
        оба переданных параметра.
    :returns: сертификат в байтовой строке

    """
    ctx = _mkcontext(cont, provider, csp.CRYPT_SILENT)
    if cont is not None:
        key = ctx.get_key()
        return key.extract_cert()

    assert thumb or name and not (
        thumb and name), 'Only one thumb or name allowed'
    cs = csp.CertStore(ctx, b"MY")
    if thumb is not None:
        res = list(cs.find_by_thumb(unhexlify(thumb)))
    else:
        res = list(c for c in cs.find_by_name(bytes(name))
                   if csp.CertInfo(c).name() == b'CN=' + bytes(name))
    assert len(res), 'Cert not found'
    cert = res[0]
    return cert.extract()


def get_key(cont=None, provider=None):
    """Получение открытого ключа из контейнера

    :cont: контейнер для поиска сертификата (по умолчанию -- системный)
    :provider: провайдер для поиска сертификата (по умолчанию дефолтный для контейнера)
        Если в качестве криптопровайдера передана строка, то она используется в
        качестве имени, тип берется из константы PROV_GOST.
        Если передан кортеж вида (тип, имя), то в создании контекста участвуют
        оба переданных параметра.
    :returns: данные открытого ключа в байтовой строке

    """
    ctx = _mkcontext(cont, provider, csp.CRYPT_SILENT)
    return ctx.public_key()


@retry
def sign(thumb, data, include_data, cont=None, provider=None):
    """Подписывание данных сертификатом

    :thumb: отпечаток сертификата, которым будем подписывать
    :data: бинарные данные, байтовая строка
    :include_data: булев флаг, если True -- данные прицепляются вместе с подписью
    :cont: контейнер для поиска сертификата (если указан -- thumb игнорируется)
    :provider: провайдер для поиска сертификата (по умолчанию дефолтный для контейнера)
        Если в качестве криптопровайдера передана строка, то она используется в
        качестве имени, тип берется из константы PROV_GOST.
        Если передан кортеж вида (тип, имя), то в создании контекста участвуют
        оба переданных параметра.
    :returns: данные и/или подпись в виде байтовой строки

    """
    mess = csp.CryptMsg()
    if cont is None:
        ctx = _mkcontext(cont, provider)
        cs = csp.CertStore(ctx, b"MY")
        store_lst = list(cs.find_by_thumb(unhexlify(thumb)))
        assert len(store_lst), 'Unable to find signing cert in system store'
        signcert = store_lst[0]
    else:
        ctx = _mkcontext(cont, provider, csp.CRYPT_SILENT)
        key = ctx.get_key()
        signcert = csp.Cert(key.extract_cert())
        signcert.bind(ctx)
    sign_data = mess.sign_data(data, signcert, not(include_data))
    return sign_data


@retry
def sign_and_encrypt(thumb, certs, data, cont=None, provider=None):
    """Подписывание данных сертификатом

    :thumb: отпечаток сертификата, которым будем подписывать
    :certs: список сертификатов получателей
    :data: байтовая строка с данными
    :cont: контейнер для поиска сертификата (по умолчанию -- системный)
    :provider: провайдер для поиска сертификата (по умолчанию дефолтный для контейнера)
        Если в качестве криптопровайдера передана строка, то она используется в
        качестве имени, тип берется из константы PROV_GOST.
        Если передан кортеж вида (тип, имя), то в создании контекста участвуют
        оба переданных параметра.
    :returns: данные и подпись, зашифрованные и закодированные в байтовую строку

    """
    certs = [autopem(c) for c in certs]
    mess = csp.CryptMsg()
    for c in certs:
        cert = csp.Cert(c)
        mess.add_recipient(cert)
    if cont is None:
        ctx = _mkcontext(cont, provider)
        cs = csp.CertStore(ctx, b"MY")
        store_lst = list(cs.find_by_thumb(unhexlify(thumb)))
        assert len(store_lst), 'Unable to find signing cert in system store'
        signcert = store_lst[0]
    else:
        ctx = _mkcontext(cont, provider, csp.CRYPT_SILENT)
        key = ctx.get_key()
        signcert = csp.Cert(key.extract_cert())
        signcert.bind(ctx)
    sign_data = mess.sign_data(data, signcert)
    encrypted = mess.encrypt_data(sign_data)
    return encrypted


@retry
def check_signature(cert, sig, data, cont=None, provider=None):
    """Проверка подписи под данными

    :cert: сертификат в байтовой строке или `None`
    :data: бинарные данные в байтовой строке
    :sig: данные подписи в байтовой строке
    :cont: контейнер для поиска сертификата
    :provider: провайдер для поиска сертификата (по умолчанию дефолтный для контейнера)
        Если в качестве криптопровайдера передана строка, то она используется в
        качестве имени, тип берется из константы PROV_GOST.
        Если передан кортеж вида (тип, имя), то в создании контекста участвуют
        оба переданных параметра.
    :returns: True или False

    Если и :cert: и :cont: переданы как None, подпись считается верной, если хотя бы один
    из сертификатов в ней есть в системном хранилище и проходит проверку.

    """
    sign = csp.Signature(sig)
    if cert or cont:
        if cert:
            cert = autopem(cert)
        else:
            ctx = _mkcontext(cont, provider, csp.CRYPT_SILENT)
            key = ctx.get_key()
            cert = key.extract_cert()
        cs = csp.CertStore()
        cert = csp.Cert(cert)
        cs.add_cert(cert)
    else:
        cs = csp.CertStore(None, b"MY")

    for i in range(sign.num_signers()):
        isign = csp.CertInfo(sign, i)
        try:
            if not cs.get_cert_by_info(isign):
                continue
        except ValueError:
            continue
        return sign.verify_data(data, i)
    return False


@retry
def encrypt(certs, data):
    """Шифрование данных на сертификатах получателей

    :certs: список сертификатов в байтовых строках
    :data: данные в байтовой строке
    :returns: шифрованные данные в байтовой строке

    """
    certs = [autopem(c) for c in certs]
    msg = csp.CryptMsg()
    for c in certs:
        cert = csp.Cert(c)
        msg.add_recipient(cert)
    encrypted = msg.encrypt_data(data)
    return encrypted


@retry
def decrypt(data, thumb, cont=None, provider=None):
    """Дешифрование данных из сообщения

    :thumb: отпечаток сертификата для расшифровки.
        Если равен None, используется сертификат, сохраненный в контейнере.
    :data: данные в байтовой строке
    :cont: контейнер для поиска сертификата (по умолчанию -- системный)
    :provider: провайдер для поиска сертификата (по умолчанию дефолтный для контейнера)
        Если в качестве криптопровайдера передана строка, то она используется в
        качестве имени, тип берется из константы PROV_GOST.
        Если передан кортеж вида (тип, имя), то в создании контекста участвуют
        оба переданных параметра.
    :returns: шифрованные данные в байтовой строке

    """

    ctx = _mkcontext(cont, provider, csp.CRYPT_SILENT)
    if thumb is not None:
        cs = csp.CertStore(ctx, b"MY")
        certs = list(cs.find_by_thumb(unhexlify(thumb)))
        assert len(certs), 'Certificate for thumbprint not found'
        cert = certs[0]
    else:
        key = ctx.get_key()
        cert = csp.Cert(key.extract_cert())
        cert.bind(ctx)
    bin_data = data
    msg = csp.CryptMsg(bin_data)
    msg.decrypt_by_cert(cert)
    return msg.get_data()


@retry
def block_encrypt(cert, data):
    """Асимметричное шифрование данных на сертификатe получателя с генерацией эфемерной пары

    :certs: список сертификатов в байтовых строках
    :data: данные в байтовой строке
    :returns: кортеж вида (шифрованные данные, эфемерный ключ, сессионный ключ, инициализационный вектор)
    """
    cert = autopem(cert)
    cert = csp.Cert(cert)
    pkaid = csp.CertInfo(cert).public_key_algorithm()
    if pkaid == csp.szOID_CP_GOST_R3410_12_256:
        provtype, keyalg, keyexp = csp.PROV_GOST_2012_256, csp.CALG_DH_GR3410_12_256_EPHEM, csp.CALG_PRO12_EXPORT
    elif pkaid == csp.szOID_CP_GOST_R3410_12_512:
        provtype, keyalg, keyexp = csp.PROV_GOST_2012_512, csp.CALG_DH_GR3410_12_512_EPHEM, csp.CALG_PRO12_EXPORT
    else:
        provtype, keyalg, keyexp = csp.PROV_GOST_2001_DH, csp.CALG_DH_EL_EPHEM, csp.CALG_PRO_EXPORT
    ctx = csp.Crypt(b'', provtype, csp.CRYPT_VERIFYCONTEXT, None)
    pubKey = ctx.import_public_key_info(cert)
    keyData = pubKey.encode()
    ephemKey = ctx.create_key(csp.CRYPT_EXPORTABLE, keyalg)
    ephemData = ephemKey.encode()
    agreeKey = ctx.import_key(keyData, ephemKey)
    agreeKey.set_alg_id(keyexp)
    sessionKey = ctx.create_key(csp.CRYPT_EXPORTABLE, csp.CALG_G28147)
    ivData = sessionKey.get_iv()
    sessionKeyData = sessionKey.encode(agreeKey)
    sessionKey.set_mode(csp.CRYPT_MODE_CBCSTRICT)
    encryptedData = sessionKey.encrypt(data)
    return encryptedData, ephemData, sessionKeyData, ivData


@retry
def block_decrypt(cont, encryptedData, ephemData, sessionKeyData, ivData, provider=None):
    """Асимметричное дешифрование данных, полученных функцией block_encrypt

    :cont: Имя контейнера
    :encryptedData: шифрованные данные
    :ephemData: эфемерный ключ
    :sessionKeyData: сессионный ключ
    :ivData: инициализационный вектор
    :provider: по умолчанию None, в этом случае используется дефолтный для
        провайдера PROV_GOST.

        Если в качестве криптопровайдера передана строка, то она используется в
        качестве имени, тип берется из константы PROV_GOST.
        Если передан кортеж вида (тип, имя), то в создании контекста участвуют
        оба переданных параметра.
    :returns: дешифрованные данные (дополненные до размера, кратного блоку шифрования)
    """
    ctx = _mkcontext(cont, provider, 0)
    userKey = ctx.get_key(csp.AT_KEYEXCHANGE)
    algID = ctx.get_key().alg_id()
    if algID == csp.CALG_DH_EL_SF:
        keyexp = csp.CALG_PRO_EXPORT
    else:
        keyexp = csp.CALG_PRO12_EXPORT
    agreeKey = ctx.import_key(ephemData, userKey)
    agreeKey.set_alg_id(keyexp)
    sessionKey = ctx.import_key(sessionKeyData, agreeKey)
    sessionKey.set_mode(csp.CRYPT_MODE_CBCSTRICT)
    try:
        sessionKey.set_padding(csp.RANDOM_PADDING)
    except Exception:
        pass  # XXX возможная для VipNet CSP ошибка игнорируется
    sessionKey.set_iv(ivData)
    return sessionKey.decrypt(encryptedData)


def pkcs7_info(data):
    """Информация о сообщении в формате PKCS7

    :data: данные в байтовой строке
    :returns: словарь с информацией следующего вида:
    {
        'Content': '....', # байтовая строка
        'Certificates': [сертификат, сертификат, ...], # байтовые строки
        'SignerInfos': [ { 'SerialNumber': 'строка', 'Issuer': [(OID, 'строка'), ... ] }, ... ],
        'ContentType': 'signedData' # один из ('data', 'signedData',
                                    #   'envelopedData', 'signedAndEnvelopedData', 'digestedData',
                                    #   'encryptedData')
        'RecipientInfos': [ { 'SerialNumber': 'строка', 'Issuer': [(OID, строка), ...] }, ... ],
    }


    """
    msg = csp.CryptMsg(data)
    res = PKCS7Msg(data).abstract()
    res['Content'] = msg.get_data()
    res['Certificates'] = list(x.extract() for x in csp.CertStore(msg))
    return res


def provider_params(cont=None, provider=None):
    """Служебная информация о криптопровайдере

    :cont: Имя контейнера (строка)
    :provider: По умолчанию None, в этом случае используется дефолтный для
        провайдера PROV_GOST.

        Если в качестве криптопровайдера передана строка, то она используется в
        качестве имени, тип берется из константы PROV_GOST.
        Если передан кортеж вида (тип, имя), то в создании контекста участвуют
        оба переданных параметра.
    :returns: словарь с информацией следующего вида:
    {
        'Time': long,          # [> time_t <]
        'Version': int,        # [> версия структуры <]
        'FreeSpace': long,     # [> свободное место на /var в bytes <]
        'NumberUL': long,      # [> "\\local\\number_UL" --- количество выпущенных ключей УЛ <]
        'NumberSigns': long,   # [> "\\local\\number_signs" --- количество операций подписи <]
        'NumberChanges': long, # [> "\\local\\Kcard_changes" --- количество смен карт канала "К" <]
        'NumberKCards': long,  # [> "\\local\\number_Kcard_sessions" --- количество выпущенных в последний раз карт канала "К" <]
        'NumberKeys': long,    # [> "\\local\\number_keys" --- количество выпущенных  <]
        'KeysRemaining': long, # [> остаток ДСРФ <]
    }
    """
    ctx = _mkcontext(cont, provider, csp.CRYPT_SILENT)
    info = csp.CSPInfo(ctx)
    assert info
    return dict(
        Time=info.time(),
        Version=info.version(),
        FreeSpace=info.free_space(),
        NumberUL=info.number_ul(),
        NumberSigns=info.number_signs(),
        NumberChanges=info.number_changes(),
        NumberKCards=info.number_kcards(),
        NumberKeys=info.number_keys(),
        KeysRemaining=info.keys_remaining(),
    )


def cert_subject_id(cert):
    """Функция получения Subject Key Id сертификата.

    :cert: сертификат в base64, или в бинарнике
    :returns: Строку из шестнадцатиричных цифр.

    """
    cert = autopem(cert)
    cert = csp.Cert(cert)
    return hexlify(cert.subject_id())


def cert_info(cert):
    """Информация о сертификате

    :cert: сертификат в base64
    :returns: словарь с информацией следующего вида:
    {
        'Version' : целое число,
        'ValidFrom' : ДатаНачала (тип datetime),
        'ValidTo' : ДатаОкончания (тип datetime),
        'Issuer': [(OID, строка), ...],
        'UseToSign': булев флаг,
        'UseToEncrypt' : булев флаг,
        'Thumbprint': строка,
        'SerialNumber': СерийныйНомер,
        'Subject': [(OID, строка), ...],
        'Extensions': [OID, OID, ...]
    }

    """
    cert = autopem(cert)
    infoasn = CertificateInfo(cert)
    cert = csp.Cert(cert)
    info = csp.CertInfo(cert)
    res = dict(
        Version=info.version(),
        ValidFrom=filetime_from_dec(info.not_before()),
        ValidTo=filetime_from_dec(info.not_after()),
        Issuer=Attributes.load(info.issuer(False)).decode(),
        Thumbprint=hexlify(cert.thumbprint()),
        UseToSign=bool(info.usage() & csp.CERT_DIGITAL_SIGNATURE_KEY_USAGE),
        UseToEncrypt=bool(info.usage() & csp.CERT_DATA_ENCIPHERMENT_KEY_USAGE),
        SerialNumber=':'.join(hex(ord(x))[2:]
                              for x in reversed(info.serial())),
        Subject=Attributes.load(info.name(False)).decode(),
        SignatureAlgorithm=info.sign_algorithm(),
        PublicKeyAlgorithm=info.public_key_algorithm(),
        Extensions=infoasn.EKU(),
    )
    return res


class Hash(object):

    """Хэш по ГОСТ 3411, имитирующий интерфейс дайджестов из `hashlib`.

    ВАЖНО: после первого вызова digest() или hexdigest(), к хэшу больше нельзя
    добавлять данные (ограничения CryptoAPI 2.0)

    Пример использования:
    > data = os.urandom(10000)
    > h = GOSTR3411(data)
    > print(h.DIGEST_URI)
    > print(h.hexdigest())

    """

    DIGEST_URI = "http://www.w3.org/2001/04/xmldsig-more#gostr3411"

    def _init_hash(self, data, key=None, length=0):
        if key is None:
            self._hash = (csp.Hash(self._ctx, data, length)
                          if data else csp.Hash(self._ctx, length))
            return
        self._hash = (csp.Hash(self._ctx, data, key, length)
                      if data else csp.Hash(self._ctx, key, length))

    def __init__(self, data=None, key=None, length=0, provider=None):
        '''
        Инициализация хэша. Если присутствует параметр `data`, в него
        подгружаются начальные данные.

        '''
        self._ctx = _mkcontext('', provider)
        self._init_hash(data, key, length)

    def update(self, data):
        '''
        Добавление данных в хэш.

        '''
        self._hash.update(data)

    def digest(self):
        '''
        Возвращает дайджест данных и закрывает хэш от дальнейших обновлений.

        '''
        return self._hash.digest()

    def _derive_key(self):
        '''
        Возвращает ключевой объект для использования в HMAC

        '''
        return self._hash.derive_key()

    def hexdigest(self):
        '''
        Возвращает шестнадцатиричное представление хэша.

        '''
        return hexlify(self.digest())

    def verify(self, cert, signature):
        '''
        Проверка подписи, полученной из экземпляра класса `SignedHash`.

        :cert: Сертификат с открытым ключом подписанта в PEM или DER
        :signature: Бинарные данные подписи
        :returns: True или False

        '''
        cert = csp.Cert(autopem(cert))
        return self._hash.verify(cert, signature)

    def verify_pubkey(self, key, signature):
        '''
        Проверка подписи, полученной из экземпляра класса `SignedHash`.

        :key: BLOB с открытым ключом подписанта
        :signature: Бинарные данные подписи
        :returns: True или False

        '''
        key = self._ctx.import_key(key)
        return self._hash.verify(key, signature)


class HMAC(Hash):

    '''
    Вычисление HMAC в соответствии с ГОСТ 3411-94

    Пример использования:
    > data = os.urandom(10000)
    > key = b'some secret password'
    > mac = HMAC(key, data)
    или
    > mac = HMAC(key)
    > mac.update(data)

    > print(mac.hexdigest())

    '''

    def __init__(self, key, data=None, length=0):
        '''
        Инициализация HMAC-а. Помимо параметров базового класса, получает `key`
        -- байтовую строку с секретом

        '''
        _keyhash = Hash(data, length=length)
        _key = _keyhash._derive_key()

        self._ctx = _keyhash._ctx
        self._init_hash(data, _key, length)


class SignedHash(Hash):

    '''
    Хэш ГОСТ 3411 с возможностью подписывания. Требует наличия в хранилище
    сертификата, привязанного к контейнеру закрытого ключа.

    Пример использования:
    > data = os.urandom(10000)
    > digest = SignedHash('0123456789ABCDEF123456789ABCD')
    > print(digest.SIGNATURE_URI)
    > digest.update(data)
    > sig = digest.sign()
    > print(sig.encode('base64').rstrip())

    Для проверки подписи не требуется закрытый ключ, поэтому может
    использоваться базовый класс:
    > new_digest = Hash(data)

    > cert = open('cert.pem').read()
    или
    > cert = get_certificate('0123456789ABCDEF123456789ABCD')

    > res = new_digest.verify(cert, sig)
    > print(res)

    '''

    SIGNATURE_URI = "http://www.w3.org/2001/04/xmldsig-more#gostr34102001-gostr3411"

    def __init__(self, thumb, data=None, cont=None, provider=None, length=0):
        '''
        Инициализация хэша. Помимо параметров базового класса, получает `thumb`
        -- отпечаток сертификата для проверки подписи. Если None -- сертификат берется из контейнера.

        :cont: контейнер для поиска сертификата (по умолчанию -- системный)
        :provider: провайдер для поиска сертификата (по умолчанию дефолтный для контейнера)
            Если в качестве криптопровайдера передана строка, то она используется в
            качестве имени, тип берется из константы PROV_GOST.
            Если передан кортеж вида (тип, имя), то в создании контекста участвуют
            оба переданных параметра.

        '''
        ctx = _mkcontext(cont, provider, csp.CRYPT_SILENT)
        if thumb is not None:
            cs = csp.CertStore(ctx, b"MY")
            store_lst = list(cs.find_by_thumb(unhexlify(thumb)))
            assert len(store_lst), 'Unable to find signing cert in system store'
            self._ctx = csp.Crypt(store_lst[0])
        else:
            self._ctx = ctx
        if length == 0:
            # XXX: для подписываемого хэша можно вычислить длину по алгоритму закрытого
            # ключа в контейнере
            algID = self._ctx.get_key().alg_id()
            if algID == csp.CALG_DH_GR3410_12_256_SF:
                length = 256
            elif algID == csp.CALG_DH_GR3410_12_512_SF:
                length = 512
            elif algID == csp.CALG_DH_EL_SF:
                length = 2001
        self._init_hash(data, length=length)

    def sign(self):
        '''
        Возвращает подпись хэша данных и закрывает хэш от дальнейших обновлений.

        '''
        return self._hash.sign()
