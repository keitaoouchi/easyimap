# -*- coding: utf-8 -*-

import imaplib
import time
import email
import cStringIO

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
    def date(self):
        return self._decode_header(self._message.get('Date'))

    @property
    def body(self):
        for part in self._message.walk():
            if part.get_content_maintype() != 'multipart' and not part.get_filename():
                return self._decode_body(part)
        raise Exception("凸[-_-]")

    def __str__(self):
        date_format = ""
        template = "{date}", "{sender}", "{title}"
        return " || ".join(template).format(date=self.date, sender=self.sender, title=self.title)

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
        body = unicode(part.get_payload(), charset) if charset else part.get_payload()
        return body

class MailerGateway(object):

    def __init__(self, mailer, *criteria):
        self._mailer = mailer
        self._ids = mailer.search(None, criteria)[1][0].split()

    @property
    def ids(self):
        return self._ids

    def _parse_email(self, data):
        message = email.message_from_string(data)
        return MailObj(message)

    def listup_mails(self, limit=None):
        emailids = self.ids
        start = min(len(emailids), limit)
        result = []
        for num in emailids[-1:-(start + 1):-1]:
            typ, content = self._mailer.fetch(num, '(RFC822)')
            mail = self._parse_email(content[0][1])
            result.append((int(num), mail))
        return result

    def get_body(self, id):
        typ, content = self._mailer.fetch(id, '(RFC822)')
        mail = self._parse_email(content[0][1])
        return mail.body

    def quit(self):
        self._mailer.close()
        self._mailer.logout()

class MailerFacade(object):

    def __init__(self, host, user, password, mailbox):
        self._mailgw = MailerGateway(self._get_mailer(host, user, password, mailbox))

    def _get_mailer(self, host, user, password, mailbox='INBOX'):
        M = imaplib.IMAP4_SSL(host=host)
        M.login(user, password)
        M.select(mailbox)
        return M

    def quit(self):
        """close and logout"""
        self._mailgw.quit()

    def listup(self, limit=10):
        """return list of tuples(email_id, mail_object)"""
        return self._mailgw.listup_mails(limit)

    def body(self, id):
        """return string of email body"""
        return self._mailgw.get_body(id)

def create(host, user, password, mailbox):
    return MailerFacade(host, user, password, mailbox)
