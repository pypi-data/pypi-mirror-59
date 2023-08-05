import smtplib
import sys
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEBase import MIMEBase
# from email import Encoders
# from email.MIMEText import MIMEText

class EmailerBase( object ):

    def __init__( self, password, test=False ):
        if test:
            self.SMTPserver = 'mailtrap.io'
            self.PORT = 2525
            self.sender = 'adam.swenson@csun.edu'
            self.USERNAME = 'fc415c779e9d12'
            self.PASSWORD = password
            self.isTest = True
        else:
            self.SMTPserver = 'smtp.office365.com'
            self.sender = 'adam.swenson@csun.edu'
            self.USERNAME = "ars62917"
            self.PASSWORD = password
            self.isTest = False
            self.URL = "smtp.office365.com"
            self.PORT = 587
            self.EXCHANGE_USER = "adam.swenson@csun.edu"
            self.EXCHANGE_PASSWORD = password
            self.bcc_address = 'adamswenson@gmail.com'
            self.isTest = False

        # typical values for text_subtype are plain, html, xml
        self.text_subtype = 'html'
        if self.isTest:
            print( "TESTING MODE" )
        else:
            print( "LIVE MODE" )

    def _connect( self ):
        try:
            self.conn = smtplib.SMTP( self.URL, self.PORT )
            self.conn.set_debuglevel( False )
            self.conn.starttls()
            self.conn.login( self.EXCHANGE_USER, self.EXCHANGE_PASSWORD )
        except Exception as exc:
            sys.exit( "connection failed; %s" % str( exc ) )  # give a error message

    def sendMail( self, destination, message_content, subject, print_status=False ):
        """
        @param destination: should be an email address
        @type destination: C{str}
        """
        raise NotImplementedError

    def send_w_attachment( self, destination, message_content, subject, attachment ):
        """
        Sends an email with the specified attachment
        """
        raise NotImplementedError


class Emailer( EmailerBase ):
    """
    This is the base class for any emailing function
    """

    def __init__( self, test=False ):
        EmailerBase.__init__( self, test )

    def sendMail( self, destination, message_content, subject, print_status=False ):
        """
        @param destination: should be a list of email addresses
        @type destination: C{list}
        """
        # this invokes the secure SMTP protocol (port 465, uses SSL)
        # from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)

        self.destination = destination
        self.content = message_content
        self.subject = subject
        try:
            msg = MIMEText( self.content, self.text_subtype )
            msg[ 'To' ] = self.destination
            msg[ 'Subject' ] = self.subject
            msg[ 'From' ] = self.sender  # some SMTP servers will do this automatically, not all
            # msg['CC'] = self.sender

            conn = smtplib.SMTP( self.SMTPserver, self.PORT )
            conn.set_debuglevel( False )
            conn.starttls()
            conn.login( self.USERNAME, self.PASSWORD )
            try:
                conn.sendmail( self.sender, self.destination, msg.as_string() )
                if (print_status):
                    print( "Sent to: %s \n %s" % (self.destination, msg.as_string()) )
            finally:
                conn.close()
        except Exception as exc:
            sys.exit( "mail failed; %s" % str( exc ) )  # give a error message

    def send_w_attachment( self, destination, message_content, subject, attachment ):
        """
        Sends an email with the specified attachment
        """
        self.destination = destination
        self.content = message_content
        self.subject = subject
        try:
            msg = MIMEMultipart()
            msg[ 'Subject' ] = self.subject
            msg[ 'From' ] = self.sender
            msg[ 'To' ] = self.destination
            # msg['To'] = ', '.join(self.destination)
            part = MIMEBase( 'application', "octet-stream" )
            part.set_payload( open( attachment, "rb" ).read() )
            Encoders.encode_base64( part )
            part.add_header( 'Content-Disposition', 'attachment; filename="%s"' % attachment )
            msg.attach( part )
            conn = self.connect()
            try:
                conn.sendmail( self.sender, self.destination, msg.as_string() )
            finally:
                conn.close()
        except Exception as exc:
            sys.exit( "mail failed; %s" % str( exc ) )  # give a error message


class ExchangeEmailer( EmailerBase ):
    """
    Base class for sending email via exchange
    """

    def __init__( self, password, test=False ):
        super().__init__( password, test )

    def sendMail( self, destination, message_content: str, subject: str, print_status=False ):
        """
        @param destination: an of email address
        @type destination: C{string}
        :param print_status: Whether to print status messages
        :param subject: The subject line
        :param message_content: The body of the message
        """

        self.destination = destination
        self.content = message_content
        self.subject = subject
        try:
            msg = MIMEText( self.content, self.text_subtype )
            msg[ 'To' ] = self.destination
            msg[ 'Subject' ] = self.subject
            msg[ 'From' ] = self.sender  # some SMTP servers will do this automatically, not all

            # msg['CC'] = self.sender

            self._connect()
            try:
                self.conn.sendmail( self.sender, self.destination, msg.as_string() )
                self.conn.sendmail( self.sender, self.bcc_address, msg.as_string() )
                if print_status:
                    print( "Sent to: %s \n %s" % (self.destination, msg.as_string()) )
            finally:
                self.conn.close()
        except Exception as exc:
            sys.exit( "mail failed; %s" % str( exc ) )  # give a error message

    def send_w_attachment( self, destination, message_content, subject, attachment ):
        """
        Sends an email with the specified attachment
        Unclear whether this works yet
        """
        self.destination = destination
        self.content = message_content
        self.subject = subject
        try:
            msg = MIMEMultipart()
            msg[ 'Subject' ] = self.subject
            msg[ 'From' ] = self.sender
            msg[ 'To' ] = self.destination
            # msg['To'] = ', '.join(self.destination)
            part = MIMEBase( 'application', "octet-stream" )
            part.set_payload( open( attachment, "rb" ).read() )
            Encoders.encode_base64( part )
            part.add_header( 'Content-Disposition', 'attachment; filename="%s"' % attachment )
            msg.attach( part )
            conn = self.connect()
            try:
                conn.sendmail( self.sender, self.destination, msg.as_string() )
            finally:
                conn.close()
        except Exception as exc:
            sys.exit( "mail failed; %s" % str( exc ) )  # give a error message
