# LxpApi
Library and Command-Line Interface for the LxpApi (www.letterxpress.de)

The package consists of two building blocks:
- Python library LxpApi to integrate the interface into Python applications.
- Command line tool lxpservice, which is [explained here](https://github.com/Simsys/LxpApi/blob/master/lxpservice.md). 

Installing LxpApi
-----------------

As usual, LxpApi is installed with pip (or pip3). This will install both the library and the command line tool.
```
$pip install lxpservice
```
Using LxpApi
------------

First import the LxpAPi library and pprint for nice view on complex python types.
```python
>>> from LxpApi import LxpApi
>>> from pprint import pprint
```
Create an instance of LxpApi with the credentials
```python
>>> url = "https://sandbox.letterxpress.de/v1/"
>>> user = <User-Name>
>>> api_key = <Api-Key>
>>> lxp_api = LxpApi(url, user, api_key)
```
Now we can work with the API and execute various commands. The library always returns an answer from which it can be seen if the function could be executed successfully.

Let's first look at the current credit balance.
```python
>>> response = lxp_api.get_balance()
>>> pprint(response)
{'auth': {'id': '46', 'status': 'active', 'user': <User-Name>},
 'balance': {'currency': 'EUR', 'value': '91.59'},
 'message': 'OK',
 'status': 200}
```
Now we upload a PDF file to the server
```python
>>> response=lxp_api.set_job('one-page.pdf')
>>> pprint(response)
{'auth': {'id': '46', 'status': 'active', 'user': <User-Name>},
 'letter': {'job_id': '3422',
            'price': 0.74,
            'specification': {'color': 1,
                              'mode': 'simplex',
                              'page': 1,
                              'ship': 'national'},
            'status': 'queue'},
 'message': 'OK',
 'status': 200}
```
In response, we receive some information such as the price or other attributes of the order. These attributes can be influenced during upload. How todo this and other information can be found in the [library documentation](https://github.com/Simsys/LxpApi/blob/master/LxpApi/lxpapi.py). Alternatively they can be retrieved with help(LxpApi). All available methods and possible parameters are described here.

# Command line tool to manage LetterXpress print jobs.

With this tool credentials can be managed, print jobs can be activated, monitored and deleted.

Overview
--------
The lxpservice tool has four sub commands:
- credentials (Create and maintain credentials)
- status (check the status of the placed print jobs)
- send (Send PDF files to print service)
- delete (Delete job(s))

All commands are equipped with a help function
```
$ lxpservice --help
Usage: lxpservice [OPTIONS] COMMAND [ARGS]...

  Command line tool to manage LetterXpress print jobs.

  With this tool credentials can be managed, print jobs can be activated,
  monitored and deleted.

  See https://www.letterxpress.de

Options:
  --version      Show the version and exit.
  -v, --verbose  Be communicative.
  --help         Show this message and exit.

Commands:
  credentials  Create and maintain credentials.
  delete       Delete job(s).
  send         Send PDF files to print service.
  status       Check the status of the placed print jobs.
```

Managing Credentials
--------------------

```
$ lxpservice credentials --help
Usage: lxpservice credentials [OPTIONS] [USER] [URL] [APIKEY]

  Create and maintain credentials.

  The login data consists of user, url and api key. If all three parameters
  are specified, lxpapi stores them securely and uses  them in the future.
  If only user and url are specified, lxpapi loads the api key from the
  password repository of the operating  system. If only user is specified,
  lxapi changes the user, keeps the url and loads the api key from the
  password repository.

Options:
  -d, --delete  Deletes password (requires user and url).
  --help        Show this message and exit.
```

First, the credentials are passed to lxpservice. Lxpservice stores the user name and the url in the file ".lxpservice.ini" 
in the home directory of the current user. The necessary Api Key is stored safely in the password manager of the operating 
system.
```
$ lxpservice credentials <User_1> <Url> <Api_Key_1>
```
The login data no longer needs to be entered. Lxpservice can handle credentials for multiple users. All credentials are 
entered one after the other. You can now easily switch between users if the url remains the same by calling lxpservice 
with the username.
```
$ lxpservice credentials <User_2> <Url> <Api_Key_2>
$ lxpservice credentials <User_1>
$ lxpservice credentials <User_2>
```
Send PDF Files
--------------

```
$ lxpservice send --help
Usage: lxpservice send [OPTIONS] FILE_OR_DIRECTORY

  Send PDF files to print service.

  Either individual files or the PDF files of a directory can be
  transferred. Different options can be selected.

Options:
  -c, --color          Send colored Letters.
  -i, --international  Send letters to international destinations.
  -d, --duplex         Send double sided printed letters.
  --help               Show this message and exit.
```
PDF files are sent by specifying the path to the file. By adding optional arguments, you can influence the way the document 
is delivered. If you specify a path to a directory, lxpservice loads all PDF documents in that directory to the server. See 
also the help pages. 
```
$ lxpservice send -c one-page.pdf
User <User>
Url https://sandbox.letterxpress.de/v1/

Sending file(s) to print server...
  one-page.pdf

$ lxpservice send -d nine-pages.pdf
User <User>
Url https://sandbox.letterxpress.de/v1/

Sending file(s) to print server...
  nine-pages.pdf
```
Check Status of Print Jobs
--------------------------

```
$ lxpservice status --help
Usage: lxpservice status [OPTIONS]

  Check the status of the placed print jobs.

  A distinction is made between jobs covered by the credit balance and jobs
  not covered.

Options:
  --help  Show this message and exit.
```
With the sub command status you can easily check which files have been uploaded to the server.
```
lxpservice status
User <User>
Url https://sandbox.letterxpress.de/v1/

These letters will be sent soon:
Date                     Id Pgs Col Cost Filename                           
2019-01-27 21:03:47    3424   9   1 1.63 nine-pages.pdf                     
2019-01-27 21:03:33    3423   1   4 0.87 one-page.pdf
2019-01-27 20:11:42    3422   1   1 0.74 one-page.pdf
```
Delete Print jobs
-----------------

```
$ lxpservice delete --help
Usage: lxpservice delete [OPTIONS]

  Delete job(s).

  Delete a job identified by the id or delete all jobs of the print service.

Options:
  -i, --id INTEGER  Delete a single order.
  -a, --all         Delete all jobs.
  --help            Show this message and exit.
```  
Print jobs can be deleted with the delete command. A distinction is made between deleting a file 
(-i id) and all files (-a).
```
$ lxpservice delete -i 3424
User <User>
Url https://sandbox.letterxpress.de/v1/

Deleting order(s):
  nine-pages.pdf
  
$ lxpservice delete -a
User <User>
Url https://sandbox.letterxpress.de/v1/

Deleting order(s):
  one-page.pdf
  one-page.pdf
