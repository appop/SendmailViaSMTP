from exchangelib import ServiceAccount, Configuration, Account, DELEGATE 
from exchangelib import Message, Mailbox, FileAttachment 

from config import cfg # load your credentials 


def send_email(account, subject, body, recipients, attachments=None): 
    """ 
    Send an email. 

    Parameters 
    ---------- 
    account : Account object 
    subject : str 
    body : str 
    recipients : list of str 
     Each str is and email adress 
    attachments : list of tuples or None 
     (filename, binary contents) 

    Examples 
    -------- 
    >>> send_email(account, 'Subject line', 'Hello!', ['[email protected]']) 
    """ 
    to_recipients = [] 
    for recipient in recipients: 
     to_recipients.append(Mailbox(email_address=recipient)) 
    # Create message 
    m = Message(account=account, 
       folder=account.sent, 
       subject=subject, 
       body=body, 
       to_recipients=to_recipients) 

    # attach files 
    for attachment_name, attachment_content in attachments or []: 
     file = FileAttachment(name=attachment_name, content=attachment_content) 
     m.attach(file) 
    m.send_and_save() 


credentials = ServiceAccount(username=cfg['user'], 
          password=cfg['password']) 

config = Configuration(server=cfg['server'], credentials=credentials) 
account = Account(primary_smtp_address=cfg['smtp_address'], config=config, 
        autodiscover=False, access_type=DELEGATE) 

# Read attachment 
attachments = [] 
with open('filestorage/numbers-test-document.pdf', 'rb') as f: 
    content = f.read() 
attachments.append(('whatever.pdf', content)) 

# Send email 
send_email(account, 'Test 14:35', 'works', ['[email protected]'], 
      attachments=attachments) 
