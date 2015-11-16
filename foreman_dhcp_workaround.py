#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Max Oberberger <max@oberbergers.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License 
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import psycopg2
import socket
import subprocess

def connectDB():
    """
    connect to foreman database

    returns:
        conn        database connection
    """
    db = 'foreman'
    dbuser = 'foreman'
    dbuserpwd = 'password'

    try:
        conn = psycopg2.connect("dbname='{0}' user='{1}' host='localhost' password='{2}'".format(db, dbuser, dbuserpwd))
    except Exception as e:
        sys.stderr.write("ERROR: Can't connect to database")
        raise

    return conn

def get_nics(cursor):
    """
    get name and ip from nics table

    params:
        cursor      database cursor

    returns:
        dict    { 'fqdn': 'ip', 'fqdn': 'ip'...
    """
    try:
        cursor.execute("""SELECT name, ip from nics""")
    except Exception as e:
        sys.stderr.write("ERROR: Can't connect to database")
        raise

    nics = cursor.fetchall()

    nic_dict = {}
    for nic in nics:
        if nic[0]: ## have to check if nic[0] contains something. otherwise we add ('', None)
            ## nic[0] == FQDN
            nic_dict[nic[0]] = nic[1]

    return nic_dict

def get_resolvIP(name):
    """
    resolv given name to get real IP

    params:
        name    string (hostname, !fqdn)

    returns:
        IP if exists. Otherwise: False
    """
    try:
        data = socket.gethostbyname_ex(name)
        ip = data[2]
        return ip[0]
    except Exception as e:
        return False

def replace_db_ip(conn, cursor, name, ip):
    """
    replace ip in database with real IP

    params:
        conn    database connection
        cursor  database cursor
        name    fqdn
        ip      real IP
    """
    try:
        cursor.execute("""UPDATE nics SET ip = '{0}' where name = '{1}'""".format(ip, name))
        conn.commit()
    except Exception as e:
	print '{0}'.format(e)
        sys.stderr.write("ERROR: Can't connect to database")
        raise

def cleanup_dhcpd_leases():
    """
    empty dhcpd.leases file
    """
    with open('/var/lib/dhcp/dhcpd.leases', "w"):
        pass

def restart_dhcpd():
    """
    restart dhcpd process
    """
    command = ['service', 'isc-dhcp-server', 'restart']
    subprocess.call(command, shell=False)

## connect to Database
conn = connectDB()

## get all nics from database
nics = get_nics(conn.cursor())

for nic in nics:
    real_ip = get_resolvIP(nic.split(".")[0])

    ## check if real_ip is the same with the database ip...
    ## if not, replace it
    if real_ip and real_ip != nics[nic]:
        replace_db_ip(conn, conn.cursor(), nic, real_ip)

## close database connection
conn.close()

## have to cleanup dhcpd leases and restart dhcpd service, otherwise foreman
## does not get informed about free dhcp IPs
cleanup_dhcpd_leases()
restart_dhcpd()
