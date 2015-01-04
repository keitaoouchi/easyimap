About this module
-----------------
Simple imap wrapper.

.. image:: https://pypip.in/download/easyimap/badge.svg?period=month
    :target: https://pypi.python.org/pypi//easyimap/
    :alt: Downloads
.. image:: https://pypip.in/version/easyimap/badge.svg?text=version
    :target: https://pypi.python.org/pypi/easyimap/
    :alt: Latest Version
.. image:: https://pypip.in/py_versions/easyimap/badge.svg
    :target: https://pypi.python.org/pypi/easyimap/
    :alt: Supported Python versions
.. image:: https://pypip.in/status/easyimap/badge.svg
    :target: https://pypi.python.org/pypi/easyimap/
    :alt: Development Status

Example to use
--------------

*connect* function create IMAP4_SSL instance by default::

    >>> import easyimap
    >>> host = "imap.gmail.com"
    >>> user = "me@example.com"
    >>> password = "hogehogehogehoge"
    >>> mailbox = "secret"
    >>> imapper = easyimap.connect(host, user, password, mailbox)

*connect* function also create IMAP4 instance by passing *ssl* argument::

    >>> import easyimap
    >>> host = "imap.gmail.com"
    >>> user = "me@example.com"
    >>> password = "hogehogehogehoge"
    >>> mailbox = "secret"
    >>> imapper = easyimap.connect(host, user, password, mailbox, ssl=False, port=143)

| This imapper can list up latest n mail by *listup* method.
| By default, This invoke `fetch` from IMAP4_SSL instance with '(UID RFC822)'.::

    >>> mail1, mail2 = imapper.listup(2)
    >>> mail1.uid
    80
    >>> mail1
    <easyimap.easyimap.MailObj object at 0x...>
    >>> type(mail1.body)
    <type 'unicode'>
    >>> type(mail1.title)
    <type 'unicode'>
    >>> type(mail1.date)
    <type 'unicode'>
    >>> type(mail1.sender)
    <type 'unicode'>

You can check latest unseen mail by *unseen* method::

    >>> imapper.unseen(2)
    [(82, <easyimap.easyimap.MailObj object at 0x...>), (81, <easyimap.easyimap.MailObj object at 0x...)]

You can directly fetch email object with specific id::

    >>> imapper.mail(80)
    <easyimap.easyimap.MailObj object at 0x...>

You can download attachments::

    >>> imapper.mail(80)
    >>> (id, mail) = imapper.mail(80)
    >>> for attachment in mail.attachment:
    >>>     print attachment[0], attachment[1]

Finally, call *quit* method::

    >>> imapper.quit()

Basic API
---------
* easyimap.connect(host, user, password, mailbox='INBOX', timeout=15, ssl=True, port=993, \*\*kwargs)
    | Create IMAP4(_SSL) wrapper.
    | If you want to keep read/unread status, Please pass optional `read_only=True` argument.
    | kwargs are read from Imapper's constructor. Plz read source code.

Imapper
^^^^^^^
* listids(limit=10, criterion=None)
    Returns list of available email ids.
* listup(limit=10, criterion=None, include_raw=False)
    Returns list of mail_object.
* unseen(limit=10)
    Returns list of mail_object.
* mail(uid, include_raw=False)
    Returns MailObj.
* change_mailbox(mailbox)
    Change mailbox.
* quit()
    Close and Logout.

MailObject
^^^^^^^^^^
* uid
    Returns UID(type: int).
* raw
    if you fetched email with include_raw option, this returns raw Data::

        >>> [(id1, mail1), (id2, mail2)] = imapper.listup(2, include_raw)
        >>> data = mail1.raw

* title
    Returns string of 'Subject' header.
* sender
    Returns string of 'Sender' header.
* from_addr
    Returns string of 'From' header.
* to
    Returns string of 'To' header.
* date
    Returns string of 'Date' header.
* body
    Returns string of Body.
* content_type
    Returns string of 'Content-Type' header.
* content_transfer_encoding
    Returns string of 'Content-Transfer-Encoding' header.
* references
    Returns string of 'References' header.
* in_reply_to
    Returns string of 'In-Reply-To' header.
* reply_to
    Returns string of 'Reply-To' header.
* return_path
    Returns string of 'Return-Path' header.
* mime_version
    Returns string of 'MIME-Version' header.
* message_id
    Returns string of 'Message-ID' header.
* attachments
    Returns list of tuples('attached file name', MailObj).

Recent Change
~~~~~~~~~~~~~

- 0.6.1
    + Fixed a bug in _decode_header function

- 0.6.0
    + Add support for Python-3.4.
    + **Backward incompatible changes**
        * Modify `listup` to return list of mailobj.
        * Rename many properties to underbar separated format.
