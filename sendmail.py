def send_order(listvar):
    import smtplib

    TO = 'bentref11@gmx.com'
    SUBJECT = 'New Sandwich order'
    #TEXT = 'Here is a message from python.'

    # Gmail Sign In
    gmail_sender = 'benjamin.trefry@lvschools.org'
    gmail_passwd = "it'smeandisohelpyourself"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', str(listvar)])
    print(BODY)

    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print ('email sent')
    except:
        print ('error sending mail')

    server.quit()
