#This file is part easyimap.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
# -*- coding: utf-8 -*-
import imaplib
import email
import time
import chardet

class MailObj(object):

    def __init__(self, message):
        self._message = message

    @property
    def title(self):
        return self._decode_header(self._message.get('Subject'))

    @property
    def sender(self):
        return self._decode_header(self._message.get('From'))

    @property
    def cc(self):
        return self._decode_header(self._message.get('CC'))

    @property
    def deliverdto(self):
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
    def inrepplyto(self):
        return self._decode_header(self._message.get('In-Reply-To'))

    @property
    def repplyto(self):
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
    def body(self):
        for part in self._message.walk():
            if part.get_content_maintype() != 'multipart' \
                and not part.get_filename():
                return self._decode_body(part)
            if part.get_content_maintype() == 'multipart':
                for p in part.get_payload():
                        if p.get_content_maintype() == 'text':
                            return self._decode_body(p)
        raise Exception("orz... something... something happened.")

    @property
    def attachments(self):
        attachments = []
        for part in self._message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            if part.get_filename():
                filename = part.get_filename() or 'none'
                data = part.get_payload(decode=True)
                if not data:
                    continue
                attachments.append((filename, data))
        return attachments
        raise Exception("orz... something... something happened.")

    def __str__(self):
        template = "{date}", "{sender}", "{title}"
        return " || ".join(template).format(
                date=self.date,
                sender=self.sender,
                title=self.title.encode("utf8")
                )

    def _decode_header(self, data):
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
        try:
            body = unicode(part.get_payload(decode=True), charset) \
                if charset else part.get_payload()
        except:
            encoding = chardet.detect(part.get_payload(decode=True))
            body = unicode(part.get_payload(decode=True), \
                encoding.get('encoding'))
        return body


class Imapper(object):

    def __init__(self, host, user, password, mailbox, timeout, **kwargs):
        self._mailer = self._get_mailer(host, user, password, mailbox, timeout)
        self._fetch_message_parts = kwargs.get("fetch_message_parts", "(RFC822)")

    def _get_mailer(self, host, user, password, mailbox, timeout):
        timeout = time.time() + timeout
        M = imaplib.IMAP4_SSL(host=host)
        M.login(user, password)
        while True:
            status, msgs = M.select(mailbox)
            if status == 'OK':
                break
            if time.time() > timeout:
                raise Exception("Timeout.")
        return M

    def _parse_email(self, data):
        message = email.message_from_string(data)
        return MailObj(message)

    def quit(self):
        """close and logout"""
        self._mailer.close()
        self._mailer.logout()

    def change_mailbox(self, mailbox):
        status, msgs = self._mailer.select(mailbox)
        if status == 'OK':
            return True
        return False

    def unseen(self, limit=10):
        return self.listup(limit, 'UNSEEN')

    def listup(self, limit=10, *criterion):
        criterion = criterion or ['ALL']
        status, msgs = self._mailer.search(None, *criterion)
        if status == 'OK':
            emailids = msgs[0].split()
            start = min(len(emailids), limit)
            result = []
            for num in emailids[-1:-(start + 1):-1]:
                typ, content = self._mailer.fetch(num, self._fetch_message_parts)
                if typ == 'OK':
                    mail = self._parse_email(content[0][1])
                    result.append((int(num), mail))
            return result
        else:
            raise Exception("Could not get ALL")

    def mail(self, id):
        """returns MailObj by specified id"""
        typ, content = self._mailer.fetch(id, self._fetch_message_parts)
        if typ == 'OK':
            mail = self._parse_email(content[0][1])
            return mail
        else:
            raise Exception("Could not get email.")


def connect(host, user, password, mailbox='INBOX', timeout=15, **kwargs):
    return Imapper(host, user, password, mailbox, timeout, **kwargs)
