Sublime Text Clientside Plugin
==============================

Copyright 2012 Trent Richardson

This file is part of Clientside Plugin.

Clientside Plugin is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

Clientside Plugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Clientside Plugin. If not, see <http://www.gnu.org/licenses/>.

ABOUT
-----
This plugin provides common tools for developing with clientside languages 
javascript and css. Tools for javascript include:

- [JS-Beautifier](http://jsbeautifier.org/) to format and "Unminify"
- [JSMin](http://www.crockford.com/javascript/jsmin.html) to minify
- [JSLint](http://www.jslint.com/) to look for syntax issues
- [CSSLint](http://csslint.net/) to look for syntax issues

Author: [Trent Richardson](http://trentrichardson.com)

PREREQUISITES
-------------
NodeJS: <http://nodejs.org/>

For Ubuntu use: 

	sudo apt-get install nodejs

For other linux distrobutions this may be a click away in your package manager. 
The plugin uses nodejs to execute serverside javascript (jslint and jsbeautify)


INSTALL
-------

- Copy or clone the repository from https://github.com/trentrichardson/Clientside into your packages folder
- Go to the Preferences -> Package Settings -> Clientside and set preferences and nodejs path

CONFIGURE
---------
Since this plugin uses NodeJS it needs to know how to call it.  Inside the configuration window there is a field for the command to call from a terminal.  
If you've installed nodejs manually, it is likely accessible through the command using "node".  However, though Ubuntu's package manager you will need to 
use "nodejs".  And, on some occasions, you may have to actually point to the binary file location (Mac might be /usr/local/bin/node).  If you need help you 
can try running in a terminal (unix or linux) the which tool: "which nodejs" or "which node".  This should print out a file path to the binary.

Further help is located in the comments of the preferences configuration files

USE
---

- With your js or css file the active document go to Tools -> Clientside -> desired tool