Sublime Text Clientside Plugin
==============================

LICENSE
-------

Sublime Text Clientside Plugin is licensed under the MIT license.

Copyright (c) 2012 Trent Richardson [http://trentrichardson.com]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
THE SOFTWARE.

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
The plugin uses nodejs to execute serverside javascript (jslint and csslint)


INSTALL
-------

- Copy or clone the repository from https://github.com/trentrichardson/Clientside into your packages folder ("Packages/Clientside")
- Go to the Preferences -> Package Settings -> Clientside and set preferences and nodejs path

CONFIGURE
---------
Since this plugin uses NodeJS it needs to know how to call it.  Inside the configuration window there is a field for the command to call from a terminal.  
If you've installed nodejs manually, it is likely accessible through the command using "node".  However, though Ubuntu's package manager you will need to 
use "nodejs".  And, on some occasions, you may have to actually point to the binary file location (Mac might be /usr/local/bin/node).  If you need help you 
can try running in a terminal (unix or linux) the which tool: "which nodejs" or "which node".  This should print out a file path to the binary.

Further help is located in the comments of the preferences configuration files. 

Each operation can handle results in the following ways (editable in the configuration): 
- "new" Places the results in a new unsaved file
- "replace" Replaces the current selection
- "clipboard" Copies the results to your clipboard
- "console" Prints the results to your console. You will need to open your console (Ctl+`)

USE
---

- With your js or css file the active document go to Tools -> Clientside -> desired tool