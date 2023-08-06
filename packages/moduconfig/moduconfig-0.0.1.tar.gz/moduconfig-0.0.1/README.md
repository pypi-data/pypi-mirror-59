# moduconfig ⚙️

A declarative and powerful configuration API for application configuration and documentation. 

## Basic Usage 🤷‍♂️
Create a file that you can import across your application. This can be a python or JSON file. This example uses a python file called configuration.py within a 
config module in our source (src) module. If our entrypoint for our application is main.py, we will be able to import the configuration.py module and it's content 
like so ```from src.config.configuration import *``` anywhere in the application.

```
src/
    config/
        __init__.py
        configuration.py
        # file with production variables
        production.py
        # file with development variables
        development.py
    __init__.py
main.py
```

configuration.py will have our configuration definition. You can also choose to do this in a JSON file as stated above which moduconfig will load and use. 

Here for example we are configuring an application that will connect to a database

```py
# configuration.py

APP_CONFIGS = {
    # the name of your application, used to prefix the names of configuration variables for their environment variables 
    # {applicationName}_{variableName} 
    "applicationName": "MY_AWESOME_APP",

    # we define our modes for our application, usually production and development but can be anything you like
    # the key is the mode name and the value is the description of what the mode does 
    "modes": {
        "testing": "Mode for integration tests to ensure application is functioning correctly",
        "development": "Mode for developing the application, should only be used to develop locally and not to serve clients",
        "production": "Mode for running the application to serve clients" 
    }
    "variables":{
        "DATABASE_HOST":{
            # error will be thrown if a value cannot be obtained 
            "required": True,
            "default":{
                # default only in the selected modes 
                "development": "localhost",
                "testing": "localhost"
            },

            # NOTE: if this is a JSON file, simply wrap the type around qoutations
            "type": str,

            # An optional description to the variable 
            "description": "The host name of the database without the port"
        },
        "DATABASE_PORT": {
            "required": True,
            # default across all modes
            "default": 5432,

            # environment variables are always strings, moduconfig will attempt to cast the value to the specified type if it's not a str
            "type": int
        },

        "DATABASE_USER":{
            "required": True,

            "default":{
                "development": "postgres",
                "testing": "postgres"
            },

            # configuring where to load the variable from 
            "configOpts": {
                
                # Only allow loading from an environment variable, we might want to do this for security reasons for example 
                "environmentVariable": True
            },

            "type": str
        },

        "DATABASE_NAME":{
            "required": True,
            "default": "myawesomedb",
            "type": str
        },
        "DATABASE_PASSWORD":{
            "required": True,
            "default":{
                "development": "postgres",
                "testing": "postgres"
            },
            "configOpts": {
                "environmentVariable": True
            },
            "type" : str
        },

    
        "DATABASE_URI": {
            # downstream configuration variable built on defined variables 🔥
            "dependsOn": [
                "DATABASE_HOST",
                "DATABASE_NAME",
                "DATABASE_PORT",
                "DATABASE_PASSWORD",
                "DATABASE_USER"
            ]

            # build variable based upon depended on variables.
            "format":"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
        }
    }
}

```


Now we use moduconfig to load variables into a simple python dict based on our specifications.


```py
# main.py
import os
from moduconfig import load_configuration_variables
from src.config.configuration import APP_CONFIGS
from src.config import production, development

app_env = os.environ.get("APP_ENV") or "production"

variables = load_configuration_variables(
    spec = APP_CONFIGS,
    environment=app_env,

    # we have specified our production and development configuration files to be python modules however, this can be a python dictionary, a path to a JSON file, or a path to an .env file
    # if no file is defined for a specific mode then configuration variables will only be loaded from environment variables
    # you can also specify a single file to be used across all modes e.g.
    # configuration_modules=default
    # this can be a python module, python dictionary, path to JSON file or path to .env file
    configuration_modules={
        "development": development,
        "production": production
    }
)
```

Variables will be loaded into a python dict and returned from load_configuration_variables. Here are some configuration variables returned when our mode is development

```py
{
    "DATABASE_NAME": "mydatabase",
    "DATABASE_HOST": "localhost",
    "DATABASE_PORT": 5432,
    "DATABASE_USER": "postgres",
    "DATABASE_PASSWORD": "postgres"
    "DATABASE_URI": "postgresql+psycopg2://postgres:postgres@localhost:5432/mydatabase"
}
```

we have specified a value other than the default by specifying an environment variable

```sh 
$ export MY_AWESOME_APP_DATABASE_NAME="mydatabase"
```

if you look closely you can see this is a concatination of the ```applicationName``` setting and the variable name. This ensures environment variables are unique to this application and we don't load a value from another application with a conflicting environment variable name.

You can now use these values to configure your application.

It doesn't stop there however ! We can generate documentation for our configuration using the moduconfig CLI ! 

```sh
# make sure you activate your virtualenv if you installed moduconfig there 

$ ls
main.py src/
$ moduconfig -c src/config/configuration.py:APP_CONFIGS -o HOW_TO_CONFIGURE.md
```

we specify our configuration file using the -c argument. If it is a python module this will be the file path ( src/config/configuration.py in our case) followed by the variable to 
access ( APP_CONFIG ) seperated by a colon. If it is a JSON file this will just be the path to the JSON file

We specify the output by the -o argument. Here we define the filename and path to the markdown file we want to generate. In this case we want to generate a markdown file at the root 
of our project called HOW_TO_CONFIGURE.

As your application grows it's simple to add configuration variables, simply go back to configuration.py and add the variable definition to you variables dictionary. Then call the moduconfig cli 
to regenerate your documentation! No figuring out, where you need to modify repeated code, add more boilerplate or add to the documentation. 


