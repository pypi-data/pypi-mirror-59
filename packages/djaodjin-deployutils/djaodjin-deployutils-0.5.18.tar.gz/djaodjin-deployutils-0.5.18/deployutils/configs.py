# Copyright (c) 2018, DjaoDjin Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Function to load site and credentials config files
"""
from __future__ import absolute_import
from __future__ import unicode_literals

import logging, os, re, six, sys
#pylint:disable=import-error
from six.moves.urllib.parse import urlparse

from . import crypt

LOGGER = None

def configure_logging():
    # We don't want the message that loads the config files in settings.py
    # to be lost so we go the extra length to find a natural logger for them.
    global LOGGER #pylint:disable=global-statement
    if LOGGER is None:
        LOGGER = logging.getLogger(__name__)
    if not LOGGER.handlers:
        LOGGER = logging.getLogger('gunicorn.error')
    if not LOGGER.handlers:
        LOGGER = logging.getLogger()


def locate_config(confname, app_name,
                  location=None, prefix='etc', verbose=False):
    """
    Returns absolute path on the filesystem to a config file named *confname*.
    """
    candidates = []
    if location:
        candidate = os.path.normpath(os.path.join(location, confname))
        if os.path.isfile(candidate):
            candidates += [candidate]
    candidate = os.path.normpath(os.path.join(
        os.path.dirname(os.path.dirname(sys.executable)),
        prefix, app_name, confname))
    if os.path.isfile(candidate):
        candidates += [candidate]
    candidate = os.path.normpath('/%s/%s/%s' % (prefix, app_name, confname))
    if os.path.isfile(candidate):
        candidates += [candidate]
    candidate = os.path.normpath(os.path.join(os.getcwd(), confname))
    if os.path.isfile(candidate):
        candidates += [candidate]
    if candidates:
        if verbose:
            LOGGER.info("config loaded from '%s'", candidates[0])
        return candidates[0]
    else:
        LOGGER.warning("config '%s' was not found.", confname)
    return None


#pylint: disable=too-many-arguments,too-many-locals,too-many-statements
def load_config(app_name, *args, **kwargs):
    """
    Given a path to a file, parse its lines in ini-like format, and then
    set them in the current namespace.

    Quiet by default. Set verbose to True to see the absolute path to the config
    files printed on stderr.
    """
    configure_logging()

    # compatible with Python 2 and 3.
    prefix = kwargs.get('prefix', 'etc')
    verbose = kwargs.get('verbose', False)
    location = kwargs.get('location', None)
    passphrase = kwargs.get('passphrase',
        os.getenv("%s_SETTINGS_CRYPT_KEY" % app_name.upper(),
            os.getenv("SETTINGS_CRYPT_KEY", None)))
    confnames = args

    if not location:
        location = os.getenv("%s_SETTINGS_LOCATION" % app_name.upper(), None)
    if not location:
        location = os.getenv("SETTINGS_LOCATION", None)
        if location:
            location = "%s/%s" % (location, app_name)

    config = {}
    for confname in confnames:
        content = None
        if location and location.startswith('s3://'):
            try:
                import boto
                _, bucket_name, prefix = urlparse(location)[:3]
                try:
                    conn = boto.connect_s3()
                    bucket = conn.get_bucket(bucket_name)
                    key_name = '%s/%s' % (prefix, confname)
                    key = bucket.get_key(key_name)
                    content = key.get_contents_as_string()
                    if verbose:
                        LOGGER.info("config loaded from 's3://%s/%s'",
                            bucket_name, key_name)
                except (boto.exception.NoAuthHandlerFound,
                        boto.exception.S3ResponseError) as _:
                    pass
            except ImportError:
                pass

        # We cannot find a deployutils S3 bucket. Let's look on the filesystem.
        if not content:
            confpath = locate_config(
                confname, app_name, location=location,
                prefix=prefix, verbose=verbose)
            if confpath:
                with open(confpath, 'rb') as conffile:
                    content = conffile.read()

        if content:
            if passphrase:
                content = crypt.decrypt(content, passphrase)
            if hasattr(content, 'decode'):
                content = content.decode('utf-8')
            for line in content.split('\n'):
                if not line.startswith('#'):
                    look = re.match(r'(\w+)\s*=\s*(.*)', line)
                    if look:
                        try:
                            # We used to parse the file line by line.
                            # Once Django 1.5 introduced ALLOWED_HOSTS
                            # (a tuple that definitely belongs to the site.conf
                            # set), we had no choice other than resort
                            # to eval(value, {}, {}).
                            # We are not resorting to import conf module yet
                            # but that might be necessary once we use
                            # dictionary configs for some of the apps...
                            # TODO: consider using something like ConfigObj
                            # for this:
                            # http://www.voidspace.org.uk/python/configobj.html
                            #pylint:disable=eval-used
                            varname = look.group(1).upper()
                            varvalue = os.getenv(varname)
                            if varvalue is None:
                                # Environment variables override the config file
                                varvalue =  eval(look.group(2), {}, {})
                            config.update({varname: varvalue})
                        except Exception:
                            raise
            # Adds both, concat and split, versions of database URI.
            if 'DB_LOCATION' in config:
                parts = urlparse(config['DB_LOCATION'])
                config.update({
                    'DB_ENGINE': parts.scheme,
                    'DB_USER': parts.username,
                    'DB_PASSWORD': parts.password,
                    'DB_HOST': parts.hostname,
                    'DB_NAME': parts.path[1:] if parts.path else None,
                })
            elif ('DB_ENGINE' in config and 'DB_NAME' in config and
                  'DB_USER' in config and 'DB_PASSWORD' in config and
                  'DB_HOST' in config):
                config.update({'DB_LOCATION': "%s://%s:%s@%s/%s" % (
                    config['DB_ENGINE'],
                    config['DB_USER'], config['DB_PASSWORD'],
                    config['DB_HOST'], config['DB_NAME'])})
            elif 'DB_ENGINE' in config and 'DB_NAME' in config:
                config.update({'DB_LOCATION': "%s:///%s" % (
                    config['DB_ENGINE'], config['DB_NAME'])})
    return config


def update_settings(module, config):

    for key, value in six.iteritems(config):
        #pylint:disable=protected-access
        if isinstance(value, six.string_types) and 'LOCALSTATEDIR' in value:
            value = value % {'LOCALSTATEDIR': module.BASE_DIR + '/var'}
        setattr(module, key.upper(), value)

    if hasattr(module, 'LOG_FILE'):
        for pathname in [module.LOG_FILE]:
            try:
                if not os.path.exists(pathname):
                    if not os.path.exists(os.path.dirname(pathname)):
                        os.makedirs(os.path.dirname(pathname))
                    with open(pathname, 'w') as _:
                        pass    # touch file
                LOGGER.info("logging app messages in '%s'", pathname)
            except OSError:
                LOGGER.warning("permission denied on '%s'", pathname)
