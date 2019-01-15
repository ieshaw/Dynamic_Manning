# Code for Dynamic Manning

This is the directory where all the code for prototyping the concepts of Dyanmic Manning are held.

## Virtual Enviroment

### Setup

In order to setup the virtual enviroment. Ensure that Python 3.7 is installed on your current computer.

Then make sure in that python distrubution you have the package to support virtual enviroments.

```
pip install virtualenv
```

Now setup the Dynamic Manning Enviroment, let's call it `dm`

```
virtualenv dm
```

### Use

In order to start the virtual enviroment anytime you code, you want to activate it with the command

```
source dm/bin/activate
```

Also want to make sure you are up to date on the required packages

```
pip install -r requirements.txt
```

When you finish your coding session, close out your virtual enviroment

```
deactivate
```

## Using the Jupyter Notebooks

In order to access the jupyter notebooks, just run the command below and a browser screen will open by which you can access the notebook.

```
jupyter notebook
```
