mailwrapper
===========

a wrapper for mail sent through the php mail function. Suitable for hosters and VPS users.

Very simple script that is used to wrap the mail() function of php. But why? Because in this way you can control how many emails are sent from the web by each user (using php mail() function). Infact in most of cases, a form or a site can be abused from an attacker and used to send spam email. This obviously can lead to the server IP to be blacklisted. Instead, with this wrapper you can put a limit on the outbound emails that goes out from each php site. Above this limit, the exceeding emails are blocked, and an alert message is sent to supervisor. Using the path returned from the alert email, you can also understand which script of the site has been used to send the violating emails.

How to install
==============

be sure to have python 2.x

copy the script to /etc/rc.d or wherever else you prefer. Give execute permission to the script (the user that runs apache must have permission to execute it)

customize values of constants inside the script and the path of python interpreter

mkdir /var/log/phpmailer

chown -R apache.apache /var/log/phpmailer  (or the user that runs apache)

set the  php_admin_value sendmail_path "/etc/rc.d/wrapper.py 500" inside the php.ini . Where 500 is, for example, the maximum number you allow for web-based outbound emails.

set the following cron job, to clean the counter once a day
00 00 * * * rm -f /var/log/phpmailer/*.cnt
