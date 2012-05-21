About this module
-----------------
imap wrapper for me.

Example to use
--------------

*create* function helps me::

    >>> import easyimap
    >>> host = "imap.gmail.com"
    >>> user = "me@example.com"
    >>> password = "hogehogehogehoge"
    >>> mailbox = "secret"
    >>> mailer = easyimap.create(host, user, password, mailbox)

I can list up latest n mail by listup method::

    >>> mailer.listup(2)
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
    
And I can directly grub mail body by index::
    
    >>> body = mailer.body(80)
    >>> type(body)
    <type 'unicode'>

Finally, quit method helps me::

    >>> mailer.quit()

Basic API
---------
* easyimap.connect(host, user, password, mailbox)
    Create nice object.

MailerFacade
^^^^^^^^^^^^
* listup(limit=10)
    Returns list of tuples(email_id, mail_object).
* body(id)
    Returns string of email body.
* quit
    Close and logout.

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