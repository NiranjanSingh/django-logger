# Logging #
***
> Logging is done to remember what your code does in case you forget it someday! 
Apart from finding bugs/ understanding behaviour/ documentation and better visualization.

> ~ Sarvadim (Chapter 0, Verse 010) 


# django_logger #
***

django_logger is a Python logging library with super powers. It leverages python 
[logging](https://docs.python.org/2/library/logging.html) to log anything and formats it as configured in django settings, 
which can be parsed via elastic search and visualized in kibana.

The default implementation uses `StreamHandler()` and sends all messages to `stdout`. Currently support for Django>=1.9.

With django_logger, you can:

* Setup your own logger format to log all logs in a specific format.
* Log a functions input/ output using just a decorator `@FunctionLogger()`.
* Specify in settings or in decorator, paramater values you wish to hide in logs `@FunctionLogger(secure_args=['password'])`. 
* Mail logger can be set up to send log mails to `ADMINS` configured in django settings file 
appart from logging to `stdout`.
* Set params in log format in settings which will always be logged in every log and 
set their values globally only once when they change .
* and much more...

## Change Log ##
***

### 0.1.0
 * Function logger exit log was breaking for response of object type - FIXED
 * Removed dependency on cRequestMiddleware library to keep global logs, 
 Now global log variables can be set anywhere. 
 * All global log variables can be set at once by passing as {key:value}.
 * Added support for Django 1.8
 * Solved a minor issue of uploading to pyPi repo.
 * Support for Django 1.9
 * Added support for python 2.7

## Installation ##
***

    pip install django-logger

## Quick start ##
***

1. Add `DJANGO_LOGGER` in django settings file.

        DJANGO_LOGGER = {
            "APP_NAME": "YOUR_APP_NAME",
            "LOGGER_NAME": "YOUR_LOGGER_NAME",
            "MAIL_LOGGER_NAME": "YOUR_MAIL_LOGGER_NAME",
            "NAMESPACE_KEY": "YOUR_APP_NAME_DATA", # optional, default: <APP_NAME>_DATA
            "SECURE_PARAMS": ('any_secure_param',), # optional, default: ()
            "LOGGING_FORMAT": {} # optional, default: {}
        }
        
2. Add these two lines in the end of `settings` file.
        
        import django_logger

        LOGGING = django_logger.LOGGING_FORMAT
        
3. Test - open shell `python manage.py shell`
        
        import logging
        logger = logging.getLogger('YOUR_LOGGER_NAME')
        mail_logger = logging.getLogger('YOUR_MAIL_LOGGER_NAME')
        
        logger.info('It worked..') # should print log in screen 
        mail_logger.info('It's working..') # print log and ADMINS defined in settings should get a mail too 
                                           # provided proper mail settings are in django
        
4. Happy logging. Dive deeper for better understanding.


## Configuration ##
***

Lets see each 'key' from our `DJANGO_LOGGER` configuration  below one by one:

    DJANGO_LOGGER = {
        "APP_NAME": "APP_EX",
        "LOGGER_NAME": "LOGGER_EX",
        "MAIL_LOGGER_NAME": "MAIL_LOGGER_EX",
        "NAMESPACE_KEY": "APP_DATA_EX",
        "SECURE_PARAMS": ('password_ex',),
        "LOGGING_FORMAT": {
            # TWO DIFFERENT KEYS WITH SAME NAME BUT DIFFERENT CASE CAN ALSO BE SET
            # AVOID DOING THAT FOR CONSISTENCY BUT YES YOU HAVE FREEDOM TO DO THAT
            # FOR EX. `C` IN BELOW FORMAT
            
            "INT_KEY": int,
            "FLOAT_KEY": float,
            "C": str,
            "f": {
                'a': str,
                'b': int,
                'c': {
                    'c': {},  # for storing dict, if you will give `dict`
                              # it will be assumed as <str>
                    'd': dict, # will be assumed as <str>
                }
            },
    
        }
    }

Now lets print this log:
    
    import logging
    logger = logging.getLogger('LOGGER_EX')
    logger.info("Just an example.")
    
And this will be printed on console as: 
    
    {"FUNCTION":"<module>","TRACE":"","LEVEL":"INFO","APP":"APP_EX","TIME":"2018-03-09T17:06:45.975+05:30","PATH":"<ipython-input-3-6017132af706>","LOGGER":"LOGGER_EX","LINE":1,"APP_DATA_EX":{"C":"","FLOAT_KEY":"0.00","INT_KEY":"0","MESSAGE":{"TEXT": "Just an example."},"f":{"a":"","c":{"c":"{}","d":""},"b":0}}}

- APP_NAME : Name of your application which will be used in logs - `APP_EX`
- LOGGER_NAME : Name of logger which we have used to get this logger config - `LOGGER_EX`
- MAIL_LOGGER_NAME : Name of mail logger.
- NAMESPACE_KEY : Key name to be used to throw all logs data. - `APP_DATA_EX`
- SECURE_PARAMS : This is used while using function decorator to log input output 
                  of a function and so to just hide (log '***" instead of actual value) the params given here in tuple. see [example]
- LOGGING_FORMAT : This defines the actual log format in which its going to be logged, in key <NAMESPACE_KEY> for ex. `APP_DATA_EX`

##### LOGGING_FORMAT #####
***

This needs to be a dict, and should contain keys which you want in all logs (format <key_name>: type) 
Let's consider a use case - 


You have an application service which takes a person's details, verifies it and sends it to another service to book a loan
and throws error if any validation fails. 

Now in your validation service you have many validator functions (Name, Aadhar, Cibil,
DOB, etc. ). You would want to log some unique detail of person in every log in order to filter logs based on request or if a 
validation fails then to find which validator failed. 

You can do this either logging 'pan_number' everytime and passing it in every function
or configure this in `DJANGO_LOGGER` settings in `LOGGING_FORMAT` as: 
        
        DJANGO_LOGGER = {
            "APP_NAME": "APP_EX",
            "LOGGER_NAME": "LOGGER_EX",
            "MAIL_LOGGER_NAME": "MAIL_LOGGER_EX",
            "NAMESPACE_KEY": "APP_DATA_EX",
            "SECURE_PARAMS": ('password_ex',),
            "LOGGING_FORMAT": {
                    "PAN": <str>
                }
        }

Now everytime to log anything you will have a key `PAN` with default to "" as this is a string.
    
    logger = logging.getLogger('LOGGER_EX')
    logger.info("Validating aadhar..")

it logs, check key `APP_DATA_EX`
    
    {"FUNCTION":"<module>","TRACE":"","LEVEL":"INFO","APP":"APP_EX","TIME":"2018-03-09T18:43:47.235+05:30","PATH":"<ipython-input-4-f0f6d8e36d79>","LOGGER":"LOGGER_EX","LINE":1,"APP_DATA_EX":{"MESSAGE":{"TEXT": "Validating aadhar.."},"PAN":""}}

**Note**: float, int, dict (to be given as {}) types will have default values as 0.0, 0 and {} respectively.

Now to set this `PAN` globally when it arrives so that by default whenever there is a log statement it will pick
up value of `PAN` which has been set globally. It can be set as:

    import django_logger
    django_logger.set_global_logs({'PAN':'default_pan'})
    
**Note**: While setting this global logs as these are stored under a current thread key, make sure to clean global log
before and after exit point of a request/ process as:
    
    import django_logger
    django_logger.clean_global_log()
    
    django_logger.set_global_logs({'PAN':'TYUPS7658K'})
    
    django_logger.clean_global_log()

So what it does is clean global log so that it doesn't pick up global log variables from previous process just to be safe.
It also helps in keeping global log clean. In case your entry points are celery tasks then you can write a pre and post
celery signals which cleans global log before and after executing any task. For ex:
    
    import django_logger
    from celery.signals import task_prerun, task_postrun
    
    @task_prerun.connect()
    def task_clean__global_log():
        django_logger.clean_global_log()
        
    @task_postrun.connect()
    def task_clean__global_log():
        django_logger.clean_global_log()
     
    
Now when you will log anything, after this has been set it will always log PAN.

    logger = logging.getLogger('LOGGER_EX')
    logger.info("Validating aadhar..")

it logs, check key `APP_DATA_EX`
    
    {"FUNCTION":"<module>","TRACE":"","LEVEL":"INFO","APP":"APP_EX","TIME":"2018-03-09T18:43:47.235+05:30","PATH":"<ipython-input-4-f0f6d8e36d79>","LOGGER":"LOGGER_EX","LINE":1,"APP_DATA_EX":{"MESSAGE":{"TEXT": "Validating aadhar.."},"PAN":"default_pan"}}
    
Simmilarly, there can be complex configurations set in `LOGGER_FORMAT` to log complex data. Normal text logs goes in `APP_DATA_EX['MESSAGE']['TEXT']` key.


##### Decorator #####
***

It is often the case when we want to know the behaviour of our code 
when it entered any function the parameters passed and what it returned.
To do exactly this just put decorator `@FunctionLogger()` above function.

**Note**: Put this decorator in the end among other decorators, for ex.

    @staticmethod
    @FunctionLogger()
    def some_static_method():
        # do some boring stuff
        pass
        
Now, you may not want to log values of some parameters such as password, username, api_key, third_party_key, oauth_key etc.
To do this either set parameter name in settings under `SECURE_PARAMS` in a tuple or 
pass parameter name in decorator as `@FunctionLogger(secure_args=['password'])` and that parameter value will be logged as "****"

for example:
        
    # configuration
    DJANGO_LOGGER = {
        "APP_NAME": "APP_EX",
        "LOGGER_NAME": "LOGGER_EX",
        "MAIL_LOGGER_NAME": "MAIL_LOGGER_EX",
        "NAMESPACE_KEY": "APP_DATA_EX",
        "SECURE_PARAMS": ('password_ex',),
        "LOGGING_FORMAT": {}
    }
    
    # sample function 
    from django_logger import FunctionLogger
    
    @FunctionLogger(secure_args=['username'])
    def func_args(text, username, password_ex): # name of parameter should be exactly same as in configuration
        return text + " Username - " + password_ex
        
    # call this function
    func_args("Hello",'testing','test123')
    
    # this will log
    {"FUNCTION":"func_args","TRACE":"","LEVEL":"INFO","APP":"APP_EX","TIME":"2018-03-12T12:26:38.122+05:30","PATH":"<ipython-input-4-fb5235935e60>","LOGGER":"LOGGER_EX","LINE":1,"APP_DATA_EX":{"MESSAGE":{"TEXT": "Entering func_args", "ARGS": "NamedArgs(text='Hello', username='*******', password_ex='*******')", "KWARGS": ""}}}
    {"FUNCTION":"func_args","TRACE":"","LEVEL":"INFO","APP":"APP_EX","TIME":"2018-03-12T12:26:38.122+05:30","PATH":"<ipython-input-4-fb5235935e60>","LOGGER":"LOGGER_EX","LINE":1,"APP_DATA_EX":{"MESSAGE":{"TEXT": "Exiting func_args", "ARGS": "Hello Username - test123", "KWARGS": ""}}}

    
    # Outputs
    'Hello Username - test123'
    
As you can see in logs, it logged `username` and `password` as "*****" but not `text`.


### Examples: ###
***

Configuration:
    
    # put this in django settings file
    DJANGO_LOGGER = {
        "APP_NAME": "APP_EX",
        "LOGGER_NAME": "LOGGER_EX",
        "MAIL_LOGGER_NAME": "MAIL_LOGGER_EX",
        "NAMESPACE_KEY": "APP_DATA_EX",
        "SECURE_PARAMS": ('password_ex',),
        "LOGGING_FORMAT": {
            # TWO DIFFERENT KEYS WITH SAME NAME BUT DIFFERENT CASE CAN ALSO BE SET
            # AVOID DOING THAT FOR CONSISTENCY BUT YES YOU HAVE FREEDOM TO DO THAT
            # FOR EX. `C` IN BELOW FORMAT
            
            "INT_KEY": int,
            "FLOAT_KEY": float,
            "C": str,
            "f": {
                'a': str,
                'b': int,
                'c': {
                    'c': {},  # for storing dict, if you will give `dict`
                              # it will be assumed as <str>
                    'd': dict, # will be assumed as <str>
                }
            },
    
        }
    }
    
    import django_logger
    LOGGING = django_logger.LOGGING_FORMAT
    
Executing all this in `python manage.py shell` :
    
    import logging
    logger = logging.getLogger('LOGGER_EX')
    
    
1. Log simple warning:
        
        logger.warning("Validation failed for loan {} .".format('loan_id'))
        {"FUNCTION":"<module>","TRACE":"","LEVEL":"WARNING","APP":"APP_EX","TIME":"2018-03-12T12:49:18.205+05:30","PATH":"<ipython-input-3-b18d0a456c9e>","LOGGER":"LOGGER_EX","LINE":1,"APP_DATA_EX":{"C":"","FLOAT_KEY":"0.00","INT_KEY":"0","MESSAGE":{"TEXT": "Validation failed for loan loan_id ."},"f":{"a":"","c":{"c":"{}","d":""},"b":0}}}
        
2. Log with some arguments:
        
    **Note**: key `MESSAGE` AND `KWARGS` must be there else they will not be logged.

        logger.info({
            "MESSAGE": "API request invoked by client {}.".format("some client"),
            
            # It's better to give same key names inside `kwargs` in all logs, as they can be used later to visualize too for ex. api request data as `DATA` and response as `RESPONSE`.
            # so all api logs will have same signature in `kwargs`
            "KWARGS": {
                "CLIENT_ID": "123",
                "DATA": {"name":"abc","loan_id":"1234"} # it can be request.data but if that is too much data then try to put only required information
                }
        })
        
        
        {"FUNCTION":"<module>","TRACE":"","LEVEL":"INFO","APP":"APP_EX","TIME":"2018-03-12T12:56:18.489+05:30","PATH":"<ipython-input-6-6cc8d5e6eaa6>","LOGGER":"LOGGER_EX","LINE":5,"APP_DATA_EX":{"C":"","FLOAT_KEY":"0.00","INT_KEY":"0","MESSAGE":{"TEXT": "API request invoked by client some client.", "ARGS": "", "KWARGS": "{'DATA': {'loan_id': '1234', 'name': 'abc'}, 'CLIENT_ID': '123'}"},"f":{"a":"","c":{"c":"{}","d":""},"b":0}}}
        
3. Log entry-exit for a function having args and kwargs.
        
        from django_logger import FunctionLogger
        @FunctionLogger()
        def my_func(a,b=2,c=0,d="hello"):
            return a,b,c,d
        
        print my_func(1,2,c=3,d="Namaste")
        
    **Note**: As argument `b` was not passed as kwargs so it will be treated as args only.
    
            {"FUNCTION":"my_func","TRACE":"","LEVEL":"INFO","APP":"APP_EX","TIME":"2018-03-12T13:05:38.638+05:30","PATH":"<ipython-input-9-33c4f49cceb9>","LOGGER":"LOGGER_EX","LINE":2,"APP_DATA_EX":{"C":"","FLOAT_KEY":"0.00","INT_KEY":"0","MESSAGE":{"TEXT": "Entering my_func", "ARGS": "NamedArgs(a=1, b=2)", "KWARGS": "{'c': 3, 'd': 'Namaste'}"},"f":{"a":"","c":{"c":"{}","d":""},"b":0}}}
            {"FUNCTION":"my_func","TRACE":"","LEVEL":"INFO","APP":"APP_EX","TIME":"2018-03-12T13:05:38.638+05:30","PATH":"<ipython-input-9-33c4f49cceb9>","LOGGER":"LOGGER_EX","LINE":2,"APP_DATA_EX":{"C":"","FLOAT_KEY":"0.00","INT_KEY":"0","MESSAGE":{"TEXT": "Exiting my_func", "ARGS": "(1, 2, 3, 'Namaste')", "KWARGS": ""},"f":{"a":"","c":{"c":"{}","d":""},"b":0}}}
            
            # output
            (1, 2, 3, 'Namaste')

### Contribution guidelines ###
***

* Writing tests - Always welcome to improve on this, at this time its greater than 90%.

* Other guidelines - Feel free to suggest any more feature or raise a pull request.

### Who do I talk to? 
***

* Author - Niranjan Singh

