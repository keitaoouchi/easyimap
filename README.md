# About this module

Simple imap wrapper.

[![Latest Version](https://img.shields.io/pypi/v/easyimap.svg)](https://pypi.python.org/pypi/easyimap/)

[![Supported Python versions](https://img.shields.io/pypi/pyversions/easyimap.svg)](https://pypi.python.org/pypi/easyimap/)

[![License](https://img.shields.io/pypi/l/easyimap.svg)](https://pypi.python.org/pypi/easyimap/)

# Example to use

_connect_ function create IMAP4_SSL instance by default

```python
import easyimap
host = "imap.gmail.com"
user = "me@example.com"
password = "hogehogehogehoge"
mailbox = "secret"
imapper = easyimap.connect(host, user, password, mailbox)
```

_connect_ function also create IMAP4 instance by passing _ssl_ argument

```python
import easyimap
host = "imap.gmail.com"
user = "me@example.com"
password = "hogehogehogehoge"
mailbox = "secret"
imapper = easyimap.connect(host, user, password, mailbox, ssl=False, port=143)
```

This imapper can list up latest n mail by _listup_ method.  
By default, This invoke fetch from IMAP4_SSL instance with **(UID RFC822)**.

```python
mail1, mail2 = imapper.listup(2)
mail1.uid #80
mail1 #<easyimap.easyimap.MailObj object at 0x...>
type(mail1.body) #<type 'unicode'>
type(mail1.title) #<type 'unicode'>
type(mail1.date) #<type 'unicode'>
type(mail1.sender) #<type 'unicode'>
```

You can check latest unseen mail by _unseen_ method:

```python
imapper.unseen(2)
# [(82, <easyimap.easyimap.MailObj object at 0x...>), (81, <easyimap.easyimap.MailObj object at 0x...)]
```

You can directly fetch email object with specific id:

```python
imapper.mail(80)
# <easyimap.easyimap.MailObj object at 0x...>
```

You can download attachments:

```python
imapper.mail(80)
(id, mail) = imapper.mail(80)
for attachment in mail.attachment:
  print attachment[0], attachment[1]
```

Finally, call _quit_ method:

```python
imapper.quit()
```

# Basic API

-   easyimap.connect(host, user, password, mailbox=**INBOX**, timeout=15, ssl=True, port=993, \*\*kwargs)

    Create IMAP4(\_SSL) wrapper.

        If you want to keep read/unread status,
        Please pass optional read_only=True argument.

## Imapper

-   listids(limit=10, criterion=None)

    Returns list of available email ids.

-   listup(limit=10, criterion=None, include_raw=False)

    Returns list of mail_object.

-   unseen(limit=10)

    Returns list of mail_object.

-   mail(uid, include_raw=False)

    Returns MailObj.

-   change_mailbox(mailbox)

    Change mailbox.

-   quit()

    Close and Logout.

## MailObject

-   uid

    Returns UID(type: int).

-   raw

    if you fetched email with include_raw option, this returns raw

        [(id1, mail1), (id2, mail2)] = imapper.listup(2, include_raw)
        data = mail1.raw


-   title

    Returns string of **Subject** header.

-   sender

    Returns string of **Sender** header.

-   from_addr

    Returns string of **From** header.

-   to

    Returns string of **To** header.

-   date

    Returns string of **Date** header.

-   body

    Returns string of Body.

-   content_type

    Returns string of **Content-Type** header.

-   content_transfer_encoding

    Returns string of **Content-Transfer-Encoding** header.

-   references

    Returns string of **References** header.

-   in_reply_to

    Returns string of **In-Reply-To** header.

-   reply_to

    Returns string of **Reply-To** header.

-   return_path

    Returns string of **Return-Path** header.

-   mime_version

    Returns string of **MIME-Version** header.

-   message_id

    Returns string of **Message-ID** header.

-   attachments

    Returns list of tuples(**attached file name**, MailObj).

### Recent Change

-   0.6.3

    -   Add support for python-3.5.
    -   Fixed a bug in decoding an attached plain text.

-   0.6.2

    -   Fixed a bug in header/body encoding

-   0.6.1

    -   Fixed a bug in *_decode_header* function

-   0.6.0
    -   Add support for Python-3.4.
    -   **Backward incompatible changes**
      +   Modify listup to return list of mailobj.
      +   Rename many properties to underbar separated format.
