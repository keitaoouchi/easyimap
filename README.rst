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

This imapper can list up latest n mail by *listup* method::

    >>> imapper.listup(2)
    [(80, <easyimap.easyimap.MailObj object at 0x...>), (79, <easyimap.easyimap.MailObj object at 0x...)]
    >>> [(id1, mail1), (id2, mail2)] = mailer.listup(2)
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

You can directly grub email object with specifiedd id::

    >>> imapper.mail(80)
    <easyimap.easyimap.MailObj object at 0x...>

Finally, call *quit* method::

    >>> mailer.quit()

Basic API
---------
* easyimap.connect(host, user, password, mailbox='INBOX', timeout=15)
    Create IMAP4_SSL wrapper.

Imapper
^^^^^^^
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
* title
    Returns string of 'Subject' header.
* sender
    Returns string of 'From' header.
* date
    Returns string of 'Date' header.
* body
    Returns string of Body.
