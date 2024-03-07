# -*- coding: utf-8 -*-

import logging

APPNAME = 'Unicode Input by Name'
APPNAME_SHORT = 'unicode-input-by-name'
VERSION = '1.0'
DESCRIPTION = 'Unicode input tool which allows searching for characters by their names'
URL = 'http://code.google.com/p/unicode-input-by-name/'
UPDATE_URL = ''
REPORT_URL = ''
HELP_URL = URL
AUTHOR = u'Conrado Porto Lopes Gouvea'
AUTHOR_EMAIL = 'conradoplg@gmail.com'
COPYRIGHT = u"Copyright (c) 2008, %s <%s>\nAll rights reserved." % (AUTHOR, AUTHOR_EMAIL)

DEBUG = False
LOG_LEVEL = logging.ERROR
MEMORY = False

MANIFEST = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
    <assemblyIdentity
        version="0.64.1.0"
        processorArchitecture="x86"
        name="Controls"
        type="win32"
    />
    <description>Unicode Input By Name</description>
    <dependency>
        <dependentAssembly>
            <assemblyIdentity
                type="win32"
                name="Microsoft.Windows.Common-Controls"
                version="6.0.0.0"
                processorArchitecture="X86"
                publicKeyToken="6595b64144ccf1df"
                language="*"
            />
        </dependentAssembly>
    </dependency>
    <dependency>
        <dependentAssembly>
            <assemblyIdentity 
                type='win32' 
                name='Microsoft.VC90.CRT' 
                version='9.0.21022.8' 
                processorArchitecture='*' 
                publicKeyToken='1fc8b3b9a1e18e3b' />
        </dependentAssembly>
    </dependency>
    <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
        <security>
            <requestedPrivileges>
                <requestedExecutionLevel level="asInvoker" uiAccess="false"/>
            </requestedPrivileges>
        </security>
    </trustInfo>
</assembly> 
"""
