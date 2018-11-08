smtp-test.py
===========

Automated testing of SMTP servers for penetration testing:

* Runs nmap script scans against a target email server
* Runs Mxtoolbox.com smtp server checks against a target email server
* Tests ability to spoof emails to a target organization
    * external smtp server (spam filters should reject emails coming from outside
the email organization that appear to come from inside the organization)
    * target smtp server (smtp servers should require authentication)

--------------------------------------------------------------------------------
## Notes
External spoof test requires an SMTP server to relay through

Please feel free to submit PR for bugfixes or enhancements - any feedback,
input, or improvement is greatly appreciated!

Script tested on Kali Linux as well as OSX and should function on UNIX-based
systems with required dependencies.

--------------------------------------------------------------------------------
## Dependencies

### Python Module Dependencies:
* none at this time

### Binary Dependencies:
* cutycapt (installed on Kali Linux by default)

--------------------------------------------------------------------------------
## Todo

* add auth support for assessor-owned smtp server used for spoof testing

--------------------------------------------------------------------------------

Copyright 2015

Matthew C. Jones, CPA, CISA, OSCP

IS Audits & Consulting, LLC - <http://www.isaudits.com/>

TJS Deemer Dana LLP - <http://www.tjsdd.com/>

--------------------------------------------------------------------------------

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.