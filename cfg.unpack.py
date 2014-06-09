#!/usr/bin/python
# -*- coding: UTF-8, tab-width: 4 -*-
# Python Coding Style: http://docs.python.org/tutorial/controlflow.html#intermezzo-coding-style
# Command Line Arguments Parser: http://docs.python.org/library/argparse.html


from __future__ import division

from sys import argv, stdout, stderr
from codecs import open as cfopen



def main(invocation, *cli_args):
    HEIDI_CHARSET = 'UTF-8'
    INI_CHARSET = 'UTF-8-sig'

    if len(cli_args) < 1:
        raise ValueError('not enough parameters. required: ConfigFileName')
    cfg_fn = cli_args[0]

    cfg_realms = {
        'app': {},
        'srv': {},
        }
    for cfg_ln in cfopen(cfg_fn, 'r', HEIDI_CHARSET):
        cfg_key, cfg_fmt, cfg_value = cfg_ln.rstrip().split('<|||>', 2)
        cfg_realm, cfg_sect, cfg_key = split_cfg_key(cfg_key)
        if (cfg_realm, cfg_key) == ('srv', 'Password'):
            cfg_value = decode_heidi_password(cfg_value)
        cfg_realm = cfg_realms[cfg_realm]
        sect_dict = cfg_realm.get(cfg_sect)
        if sect_dict is None:
            sect_dict = cfg_realm[cfg_sect] = {}
        sect_dict[cfg_key] = cfg_fmt + '|' + cfg_value

    ini_fn = 'heidisql.ini'
    write_ini(cfopen(ini_fn, 'w', INI_CHARSET), cfg_realms['app'])
    for cfg_sect, sect_dict in cfg_realms['srv'].items():
        ini_fn = sanitize_file_name(cfg_sect).lower() + '.ini'
        write_ini(cfopen(ini_fn, 'w', INI_CHARSET), { cfg_sect: sect_dict })


def write_ini(dest, ini):
    for sect_name in sorted(ini.keys()):
        sect_dict = ini[sect_name]
        dest.write('[' + sect_name + ']\n')
        for opt_name in sorted(sect_dict.keys()):
            opt_value = sect_dict[opt_name]
            dest.write(opt_name + '=' + opt_value + '\n')
        dest.write('\n')


def split_at_first_nonalpha(idstr, defaultPrefix=None):
    for pos, chr in enumerate(idstr):
        if not chr.isalpha():
            pos += 1
            return idstr[0:pos], idstr[pos:]
    return defaultPrefix, idstr


def split_cfg_key(key):
    if key.startswith('Servers\\'):
        sect, key = key.split('\\', 2)[1:]
        return 'srv', sect, key

    form_part = key.split('.', 1)
    if len(form_part) == 2:
        # [u'ColPositions_connform', u'ListSessions']
        if form_part[0].lower().endswith('form'):
            form_prop, form_part = form_part
            form_prop = form_prop.split('_')
            if len(form_prop) == 2:
                # [u'ColPositions', u'connform']
                form_prop, form_name = form_prop
                sect = form_name
                key = form_part + '.' + form_prop
                return 'app', sect, key

    return 'app', 'HeidiSQL', key


def decode_heidi_password(obfus):
    obfus, caesar_key = obfus[:-1], obfus[-1:]
    caesar_key = -int(caesar_key, 16)
    clean = ''
    while obfus != '':
        cnum, obfus = obfus[:2], obfus[2:]
        cnum = int(cnum, 16)
        cnum += caesar_key
        char = None
        if (31 < cnum) and (cnum < 127):
            char = chr(cnum)
            if char in ('\\', '"', "'"):
                char = None
        if char is None:
            char = '\\u00' + hex(cnum).replace('0x', '00')[-2:]
        # print cnum, hex(cnum), char
        clean += char
    return '"' + clean + '"'


def sanitize_file_name(wild):
    sane = ''
    for char in wild:
        # print repr(char),
        if char.isalnum() or (char in '@-'):
            if repr(char)[2:-1] != char:
                # this alnum might be too fancy for some file systems.
                continue
            sane += char
            continue
        # if char.isspace():
        char = '_'
        if not sane.endswith(char):
            sane += char
    # print repr(sane)
    return sane












if __name__ == '__main__':
    main(*argv)
