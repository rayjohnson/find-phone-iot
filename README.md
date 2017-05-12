
# IOT Button -> "Find my iPhone"

### AWS lambda function for iot button to call iCloud to find iPhone 


My wife miss places her phone on occasion.  She will often ask me to use the
"Find my iPhone" feature of iCloud to get that nice submarine ping going to find
her phone.  She has even been known to call me at work from the land-line to 
have me trigger it!  I've tried to teach her to do it herself - no luck...

So - enter the AWS IOT Button.  This project gives a little AWS lambda function
that can be configured to run for a button push.  It then calls iCloud and plays
the find my iPhone sound.  What could be more simple!

## What you need to build this:
You will need python with pip installed
You will need an AWS account, AWS IOT Button, the aws command line tool

The Makefile will build a python app and it's dependacies into a zip file
that can be loaded into AWS.

The Makefile can also load the code into AWS if you configured your aws command line tool.


## Set up of your lambda function

You will need to create the lambda function by hand initially.  You will
need to set the following options:

Runtime: Python 2.7
Handler: lambda_function.lambda_handler
You will need to set up a role, etc.

The following Environment variables also need to be defined:
APPLE_ID = your iCloud apple id for your phone
APPLE_PASSWORD = your password to iCloud
DEVICE_NAME = the devince name of your phone

In addition, you must encrypt the APPLE_PASSWORD variable with KMS.  You will need to
set up a key to use in KMS and then use the encryption helpers on the lambda config
to encrypt the value of the APPLE_PASSWORD field.