# Created: 22.10.2017
# Vladimir Vons, VladVons@gmail.com

import subprocess
import smtplib
#
from LibCommon import TControl, _Required


class TMail(TControl):
    def LoadParam(self, aParam):
        # Param":{"MailTo":"VladVons@gmail.com", "Relay":"smtp.gmail.com", "Port":"465", "User":"ua0976646510@gmail.com", "Password":"19710819"}
        Pattern = {'MailTo':_Required, 'Subject':'TGMail', 'User':'', 'Password':'', 'Port':0, 'Relay':'localhost', 'SSL':True}
        self.LoadParamPattern(aParam, Pattern)

    def Set(self, aValue):
        self.Send('Caller Alias: ' + self.Parent.Alias)

    def Send(self, aBody):
        # http://www.raspberry-projects.com/pi/software_utilities/email/ssmtp-to-send-emails
        Msg = '\r\n'.join([
            'From: '    + self.User,
            'To: '      + self.MailTo,
            'Subject: ' + self.Subject,
            '',
            aBody
            ])
        try:
            #print('---1', self.Relay, self.Port, self.User, self.Password)
            if (self.SSL):
                Server = smtplib.SMTP_SSL(self.Relay, self.Port)
            else:
                Server = smtplib.SMTP(self.Relay, self.Port)

            Server.ehlo()
            if (self.User):
                Server.login(self.User, self.Password)

            Server.sendmail(self.User, self.MailTo, Msg)
            Server.close()
        except smtplib.SMTPAuthenticationError as E: 
            print('TSendMail->Set. Authentication Error', E)

    def _Check(self, aValue):
        self.Set(aValue)
        return True


class TShell(TControl):
    def LoadParam(self, aParam):
        Pattern = {'Command':_Required}
        self.LoadParamPattern(aParam, Pattern)

    def Set(self, aValue):
        Pipe = subprocess.Popen(self.Command, shell = True, stdout = subprocess.PIPE)
        return Pipe.communicate()[0]

    def _Check(self, aValue):
        self.Set(aValue)
        return True



class TStop(TControl):
    def Set(self, aValue):
        self.ParentRoot.Stop()

    def _Check(self, aValue):
        self.Set(aValue)
        return True
