About this module
-----------------
Simple imap wrapper.

Example to use
--------------

*connect* function create IMAP4_SSL instance::

    >>> import easyimap
    >>> host = "imap.gmail.com"
    >>> user = "me@example.com"
    >>> password = "hogehogehogehoge"
    >>> mailbox = "secret"
    >>> imapper = easyimap.connect(host, user, password, mailbox)

This imapper can list up latest n mail by *listup* method.
By default, This invoke `fetch` from IMAP4_SSL instance with '(UID RFC822)'.::

    >>> imapper.listup(2)
    [(80, <easyimap.easyimap.MailObj object at 0x...>), (79, <easyimap.easyimap.MailObj object at 0x...)]
    >>> [(id1, mail1), (id2, mail2)] = imapper.listup(2)
    >>> id1
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
* easyimap.connect(host, user, password, mailbox='INBOX', timeout=15)
    Create IMAP4_SSL wrapper.
    If you want to keep read/unread status, Please pass optional `read_only=True` argument.

Imapper
^^^^^^^
* listids(limit=10)
    Returns list of available email ids.
* listup(limit=10)
    Returns list of tuples(email_id, mail_object).
* unseen(limit=10)
    Returns list of typles(email_id, mail_object).
* mail(id)
    Returns MailObj.
* change_mailbox(mailbox)
    Change mailbox.
* quit
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
    Returns string of 'From' header.
* date
    Returns string of 'Date' header.
* body
    Returns string of Body.
* contenttype
    Returns string of 'Content-Type' header.
* contenttransferencoding
    Returns string of 'Content-Transfer-Encoding' header.
* references
    Returns string of 'References' header.
* inreplyto
    Returns string of 'In-Reply-To' header.
* replyto
    Returns string of 'Reply-To' header.
* returnpath
    Returns string of 'Return-Path' header.
* mimeversion
    Returns string of 'MIME-Version' header.
* messageid
    Returns string of 'Message-ID' header.
* attachments
    Returns list of tuples('attached file name', MailObj).
