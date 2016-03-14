# -*- coding: utf-8 -*-

import imaplib
import email
from email.header import decode_header
import time
import re
import mimetypes

import chardet

try:
    unicode('')
except NameError:
    # for python3 compatibility.
    unicode = str


class MailObj(object):
    def __init__(self, message, uid=-1, raw=''):
        self._message = message
        self._uid = uid if uid > -1 else None
        self._raw = raw if raw else None

    @property
    def uid(self):
        return self._uid

    @property
    def title(self):
        return _decode_header(self._message.get('Subject'))

    @property
    def to(self):
        return _decode_header(self._message.get('To'))

    @property
    def from_addr(self):
        """Method name includes _addr so it does not conflict with the `from`
        keyword in Python."""
        return _decode_header(self._message.get('From'))

    @property
    def sender(self):
        return _decode_header(self._message.get('Sender'))

    @property
    def cc(self):
        return _decode_header(self._message.get('CC'))

    @property
    def delivered_to(self):
        return _decode_header(self._message.get('Delivered-To'))

    @property
    def content_type(self):
        return _decode_header(self._message.get('Content-Type'))

    @property
    def content_transfer_encoding(self):
        return _decode_header(self._message.get('Content-Transfer-Encoding'))

    @property
    def references(self):
        return _decode_header(self._message.get('References'))

    @property
    def in_reply_to(self):
        return _decode_header(self._message.get('In-Reply-To'))

    @property
    def reply_to(self):
        return _decode_header(self._message.get('Reply-To'))

    @property
    def return_path(self):
        return _decode_header(self._message.get('Return-Path'))

    @property
    def mime_version(self):
        return _decode_header(self._message.get('MIME-Version'))

    @property
    def message_id(self):
        return _decode_header(self._message.get('Message-ID'))

    @property
    def date(self):
        return _decode_header(self._message.get('Date'))

    @property
    def raw(self):
        return self._raw

    @property
    def body(self):
        for part in self._message.walk():
            maintype = part.get_content_maintype()
            if maintype != 'multipart' and not part.get_filename():
                return _decode_body(part)
            if maintype == 'multipart':
                for p in part.get_payload():
                    if p.get_content_maintype() == 'text':
                        return _decode_body(p)
        raise Exception("orz... something... something happened.")

    @property
    def attachments(self):
        counter = 1
        attachments = []
        for part in self._message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get_filename():
                filename = part.get_filename()
                if not filename:
                    ext = mimetypes.guess_extension(part.get_content_type())
                    if not ext:
                        # Use a generic bag-of-bits extension
                        ext = '.bin'
                    filename = 'part-%03d%s' % (counter, ext)
                counter += 1

                data = part.get_payload(decode=True)
                content_type = part.get_content_type()
                if not data:
                    continue
                attachments.append((filename, data, content_type))
        return attachments

    def __str__(self):
        template = "{date}", "{sender}", "{title}"
        represent = " || ".join(template).format(
            date=self.date,
            sender=self.sender,
            title=self.title.encode("utf8")
        )
        return represent


class Imapper(object):
    def __init__(self, host, user, password, mailbox, timeout, ssl, port, **kwargs):
        self._fetch_message_parts = kwargs.get("fetch_message_parts", "(UID RFC822)")
        self._read_only = kwargs.get("read_only", False)
        self._mailer = self._get_mailer(host, user, password, mailbox, timeout, ssl, port)

    def _get_mailer(self, host, user, password, mailbox, timeout, ssl, port):
        timeout = time.time() + timeout
        if ssl:
            mailer = imaplib.IMAP4_SSL(host=host, port=port)
        else:
            mailer = imaplib.IMAP4(host=host, port=port)
        mailer.login(user, password)
        while True:
            status, msgs = mailer.select(mailbox, self._read_only)
            if status == 'OK':
                break
            if time.time() > timeout:
                raise Exception("Timeout.")
        return mailer

    def quit(self):
        """close and logout"""
        self._mailer.close()
        self._mailer.logout()

    def change_mailbox(self, mailbox):
        status, msgs = self._mailer.select(mailbox, self._read_only)
        if status == 'OK':
            return True
        return False

    def unseen(self, limit=10):
        return self.listup(limit, 'UNSEEN')

    def listids(self, limit=10, criterion=None):
        criterion = criterion or 'ALL'
        status, msgs = self._mailer.uid('search', None, criterion)
        if status == 'OK':
            email_ids = msgs[0].split()
            start = min(len(email_ids), limit)
            return email_ids[-1:-(start + 1):-1]
        else:
            raise Exception("Could not get ALL")

    def listup(self, limit=10, criterion=None, include_raw=False):
        email_ids = self.listids(limit, criterion)
        result = []
        for i in email_ids:
            typ, content = self._mailer.uid('fetch', i, self._fetch_message_parts)
            if typ == 'OK':
                mail = _parse_email(content, include_raw=include_raw)
                result.append(mail)
        return result

    def mail(self, uid, include_raw=False):
        """returns MailObj by specified id"""
        typ, content = self._mailer.uid('fetch', uid, self._fetch_message_parts)
        if typ == 'OK':
            mail = _parse_email(content, include_raw=include_raw)
            return mail
        else:
            raise Exception("Could not get email.")


def connect(host, user, password, mailbox='INBOX', timeout=15, ssl=True, port=993, **kwargs):
    return Imapper(host, user, password, mailbox, timeout, ssl, port, **kwargs)


def _decode_header(data):
    if data is None:
        return
    decoded_headers = decode_header(data)
    headers = []
    for decoded_str, charset in decoded_headers:
        if isinstance(decoded_str, unicode):
            headers.append(decoded_str)
        elif charset:
            headers.append(unicode(decoded_str, charset))
        else:
            encoding = chardet.detect(decoded_str)
            if encoding.get('encoding'):
                headers.append(unicode(decoded_str, encoding['encoding']))
            else:
                headers.append(decoded_str)
    return "".join(headers)


def _decode_body(part):
    charset = str(part.get_content_charset())
    payload = part.get_payload(decode=True)
    try:
        body = unicode(payload, charset) if charset else part.get_payload()
    except:
        encoding = chardet.detect(payload)
        if encoding.get('encoding'):
            body = unicode(payload, encoding['encoding'])
        else:
            body = payload
    return body


def _parse_email(data, include_raw=False):
    string_or_bytes_message = data[0][1]
    string_or_bytes_uid = data[0][0]
    if not isinstance(string_or_bytes_message, str):
        encoding = chardet.detect(string_or_bytes_message)
        string_or_bytes_message = string_or_bytes_message.decode(encoding.get('encoding'))
    if not isinstance(string_or_bytes_uid, str):
        encoding = chardet.detect(string_or_bytes_uid)
        string_or_bytes_uid = string_or_bytes_uid.decode(encoding.get('encoding'))
    message = email.message_from_string(string_or_bytes_message)
    uid = re.findall('[UID ](\d+)', string_or_bytes_uid)
    args = {}
    if uid:
        args['uid'] = int(uid[0])
    if include_raw:
        args['raw'] = data[0][1]

    return MailObj(message, **args)
