# -*- coding: utf-8 -*-

import imaplib
import email
import time
import re
import mimetypes

import chardet


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
        return self._decode_header(self._message.get('Subject'))

    @property
    def to(self):
        return self._decode_header(self._message.get('To'))

    @property
    def from_addr(self):
        """Method name includes _addr so it does not conflict with the `from`
        keyword in Python."""
        return self._decode_header(self._message.get('From'))

    @property
    def sender(self):
        return self._decode_header(self._message.get('Sender'))

    @property
    def cc(self):
        return self._decode_header(self._message.get('CC'))

    @property
    def deliveredto(self):
        return self._decode_header(self._message.get('Delivered-To'))

    @property
    def contenttype(self):
        return self._decode_header(self._message.get('Content-Type'))

    @property
    def contenttransferencoding(self):
        return self._decode_header(self._message.get('Content-Transfer-Encoding'))

    @property
    def references(self):
        return self._decode_header(self._message.get('References'))

    @property
    def inreplyto(self):
        return self._decode_header(self._message.get('In-Reply-To'))

    @property
    def replyto(self):
        return self._decode_header(self._message.get('Reply-To'))

    @property
    def returnpath(self):
        return self._decode_header(self._message.get('Return-Path'))

    @property
    def mimeversion(self):
        return self._decode_header(self._message.get('MIME-Version'))

    @property
    def messageid(self):
        return self._decode_header(self._message.get('Message-ID'))

    @property
    def date(self):
        return self._decode_header(self._message.get('Date'))

    @property
    def raw(self):
        return self._raw

    @property
    def body(self):
        for part in self._message.walk():
            maintype = part.get_content_maintype()
            if maintype != 'multipart' and not part.get_filename():
                return self._decode_body(part)
            if maintype == 'multipart':
                for p in part.get_payload():
                    if p.get_content_maintype() == 'text':
                        return self._decode_body(p)
        raise Exception("orz... something... something happened.")

    @property
    def attachments(self):
        counter = 1
        attachments = []
        for part in self._message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
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

    def _decode_header(self, data):
        if data is None:
            return
        decoded_headers = email.Header.decode_header(data)
        headers = []
        for decoded_str, charset in decoded_headers:
            if charset:
                headers.append(unicode(decoded_str, charset))
            else:
                headers.append(unicode(decoded_str))
        return "".join(headers)

    def _decode_body(self, part):
        charset = str(part.get_content_charset())
        payload = part.get_payload(decode=True)
        try:
            body = unicode(payload, charset) if charset else part.get_payload()
        except:
            encoding = chardet.detect(payload)
            body = unicode(payload, encoding.get('encoding'))
        return body


class Imapper(object):
    def __init__(self, host, user, password, mailbox, timeout, **kwargs):
        self._fetch_message_parts = kwargs.get("fetch_message_parts", "(UID RFC822)")
        self._read_only = kwargs.get("read_only", False)
        self._mailer = self._get_mailer(host, user, password, mailbox, timeout)

    def _get_mailer(self, host, user, password, mailbox, timeout):
        timeout = time.time() + timeout
        M = imaplib.IMAP4_SSL(host=host)
        M.login(user, password)
        while True:
            status, msgs = M.select(mailbox, self._read_only)
            if status == 'OK':
                break
            if time.time() > timeout:
                raise Exception("Timeout.")
        return M

    def _parse_email(self, data, include_raw=False):
        message = email.message_from_string(data[0][1])
        uid = re.findall('[UID ](\d+)', data[0][0])
        args = {}
        if uid:
            args['uid'] = int(uid[0])
        if include_raw:
            args['raw'] = data[0][1]

        mailobj = MailObj(message, **args)
        return mailobj

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

    def listids(self, limit=10, *criterion):
        criterion = criterion or ['ALL']
        status, msgs = self._mailer.uid('search', None, *criterion)
        if status == 'OK':
            emailids = msgs[0].split()
            start = min(len(emailids), limit)
            return emailids[-1:-(start + 1):-1]
        else:
            raise Exception("Could not get ALL")

    def listup(self, limit=10, include_raw=False, *criterion):
        emailids = self.listids(limit, criterion)
        result = []
        for num in emailids:
            typ, content = self._mailer.fetch(num, self._fetch_message_parts)
            if typ == 'OK':
                mail = self._parse_email(content, include_raw=include_raw)
                result.append((int(num), mail))
        return result

    def mail(self, id, include_raw=False):
        """returns MailObj by specified id"""
        typ, content = self._mailer.fetch(id, self._fetch_message_parts)
        if typ == 'OK':
            mail = self._parse_email(content, include_raw=include_raw)
            return mail
        else:
            raise Exception("Could not get email.")


def connect(host, user, password, mailbox='INBOX', timeout=15, **kwargs):
    return Imapper(host, user, password, mailbox, timeout, **kwargs)
