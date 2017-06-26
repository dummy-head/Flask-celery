# -*- coding: utf-8 -*-
"""Click commands."""
import os
from glob import glob
from subprocess import call

import click
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.exceptions import MethodNotAllowed, NotFound

from enferno.extensions import db
from flask_security.script import CreateUserCommand, AddRoleCommand
from flask.ext.security.utils import encrypt_password
from enferno.user.models import User
from flask import current_app
from flask.cli import with_appcontext



@click.command()
@with_appcontext
def install():
    """Install a default admin user and add an admin role to it.
    """
    #check if admin exists
    from enferno.user.models import Role
    a = Role.objects.filter(name ='admin').first()

    if a == None:
        r = Role(name='admin').save()
        u = click.prompt('Admin Email?',default='admin@enferno.io')
        p = click.prompt('Admin Password (min 6 characters)?',default='enferno')
        CreateUserCommand().run(email=u,password=p,active=1)
        AddRoleCommand().run(user_identifier=u,role_name='admin')
    else:
        print ('Seems like an Admin is already installed')


@click.command()
@click.option('-e', '--email', prompt=True, default=None)
@click.option('-p', '--password', prompt=True, default=None)
@with_appcontext
def create(email, password):
    """Creates a user using an email.
    """
    if User.objects(email = email).first() != None:
        print 'User already exists!'
    else:
        CreateUserCommand().run(email=email, password=password, active=1)
        # you can add default roles here

@click.command()
@click.option('-e', '--email', prompt=True, default=None)
@click.option('-r', '--role', prompt=True, default='admin')
@with_appcontext
def add_role(email, role):
    """Adds a role to the specified user.
    """
    from enferno.user.models import Role
    u = User.objects(email = email).first()
    if u == None:
        print 'Sorry, this user does not exist!'
        return
    r = Role.objects(name = role).first()
    if r == None:
        print 'Sorry, this role does not exist!'
        u = click.prompt('Would you like to create one? Y/N', default='N')
        if u.lower() == 'y':
            Role(name=role).save()
            print 'Role created successfully, you may add it now to the user'
    else:
        AddRoleCommand().run(user_identifier=email, role_name=role)

@click.command()
@click.option('-e', '--email', prompt=True, default=None)
@click.option('-p', '--password', prompt=True, default=None)
@with_appcontext
def reset(email, password):
    """Reset a user password
    """
    try:
        pwd = encrypt_password(password)
        u = User.objects(email= email).first()
        u.password = pwd
        u.save()
        print ('User password has been reset successfully.')
    except Exception as e:
        print ('Error resetting user password: %s' % e)


@click.command()
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory.
    Borrowed from Flask-Script, converted to use Click.
    """
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                click.echo('Removing {}'.format(full_pathname))
                os.remove(full_pathname)


