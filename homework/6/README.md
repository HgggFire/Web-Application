To turn in homework 6, create files (and subdirectories if needed) in
this directory, add and commit those files to your cloned repository,
and push your commit to your bare repository on GitHub.

Add any general notes or instructions for the TAs to this README file.
The TAs will read this file before evaluating your work.

My Deployment URL:
ec2-54-159-74-108.compute-1.amazonaws.com 
(Please contact me at soap.cmu@gmail.com if you find this instance is not running, the AWS might be down)

Notes:
I configured /etc/apache2/sites-enabled/000-default.conf

I’m sending real Emails for registration (or the TAs won’t be able to test). Make sure you  use an real email address and confirm the link in the email sent to you.
In settings.py, I changed my real andrewID and password in to “my_andrewid” and “my_andrew_password” for submission, but on the VM I’m using the real ones.

I used postgres as the DB, with a password “123” for the DB user “chico” (as is in settings.py),  which should not matter because the password doesn’t mean anything.



External Resources Used:
https://www.sitepoint.com/deploying-a-django-app-with-mod_wsgi-on-ubuntu-14-04/
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/modwsgi/
http://stackoverflow.com/questions/7670289/sqlite3-operationalerror-unable-to-open-database-file
https://recalll.co/app/?q=Forbidden%20You%20don%27t%20have%20permission%20to%20access%20/%20on%20this%20server.%20%5BApache/2.2.22%20(Debian)%5D
https://www.digitalocean.com/community/tutorials/how-to-run-django-with-mod_wsgi-and-apache-with-a-virtualenv-python-environment-on-a-debian-vps
https://d1b10bmlvqabco.cloudfront.net/attach/is6faxgyce74jc/h5jq6sx7nht6yf/iu8ldmut2kle/Postgresinstallationinstructions.pdf
