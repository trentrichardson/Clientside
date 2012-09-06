import sublime, sublime_plugin

from StringIO import StringIO
from jsmin import JavascriptMinify
from cssmin import CSSMin
import jsbeautifier
import os
import re
import subprocess
import json

class ClientsideCommand(sublime_plugin.TextCommand):

	def __init__(self, view):
		self.view = view
		self.window = sublime.active_window()
		self.plugin_dir = os.path.join(sublime.packages_path(), 'Clientside') #os.path.split(os.path.abspath(__file__))[0]

	def run(self, edit, operation="minify"):
		self.settings = sublime.load_settings('Clientside.sublime-settings')
		self.user_settings = sublime.load_settings('Preferences.sublime-settings')

		current_file = self.view.file_name()
		if not current_file:
			current_file = "tmp.js"

		file_ext = current_file.split(".")[-1]
		syntax = self.view.settings().get('syntax')
		selections = self._get_selections()
		output = self.settings.get(file_ext+"_"+operation+"_output", "new")
		new_str = ""

		self.view.set_status('clientside', "Clientside "+file_ext +" "+ operation)

		for sel in selections:
			selbody = self.view.substr(sel).encode('utf-8')
			if operation == 'minify':
				if file_ext == 'css':
					new_str = self.get_css_minified(selbody)
				else:
					new_str = self.get_js_minified(selbody)
			elif operation == 'format':
				if file_ext == 'css': 
					new_str = self.get_css_formatted(selbody)
				else:
					new_str = self.get_js_formatted(selbody)
			elif operation == 'lint':
				if file_ext == 'css': 
					new_str = self.get_css_lint(selbody)
				else:
					new_str = self.get_js_lint(selbody)

			new_str = new_str.decode('utf-8')
			
			if output == "replace":
				self.view.replace(edit, sel, new_str)
			elif output == "new":
				new_view = self.window.new_file()
				new_edit = new_view.begin_edit()
				if operation == "lint":
					syntax = "Packages/JavaScript/JavaScript.tmLanguage"
				new_view.set_syntax_file(syntax)
				new_view.insert(new_edit, 0, new_str)
				new_view.end_edit(new_edit)
			elif output == "clipboard":
				sublime.set_clipboard(new_str)
				self.view.set_status("clientside", "Code is copied to your clipboard")
			else:
				print new_str
				self.view.set_status("clientside", "Code is in the console")
		
		selections.clear()
		sublime.set_timeout(self.clear_status,5000)

	# CSS Helpers =========================================================
	def get_css_minified(self, codestr):
		return CSSMin().minify(codestr)


	def get_css_formatted(self, codestr, bracket_newline=False):
		opts = self.settings.get('cssformat', { 'bracket_newline': False, 'compact': False })
		use_tab = self.user_settings.get('translate_tabs_to_spaces',False)
		if use_tab:
			tab = "\t"
		else:
			tab = " " * int(self.user_settings.get('tab_size',False))
		
		return CSSMin().format(codestr, opts['bracket_newline'], tab, opts['compact']) 


	def get_css_lint(self, codestr):
		opts = json.dumps(self.settings.get('csslint', {}))
		if opts == '{}':
			opts = ''
		else:
			opts = ',' + opts

		csslint_path = os.path.join(self.plugin_dir, "csslint", "csslint")
		tmpfile_path = os.path.join(self.plugin_dir, "csslint", "tmp_csslint.js")
		tmpcode_path = os.path.join(self.plugin_dir, "csslint", "tmp_csslint_code.js")
		
		tmpfile = open(tmpfile_path,"w")
		tmpfile.writelines("var sys = require('sys');")
		tmpfile.writelines("var fs = require('fs');")
		tmpfile.writelines("var CSSLint = require('" + csslint_path.replace("\\", "\\\\") + "').CSSLint;")
		tmpfile.writelines("var body = fs.readFileSync('" + tmpcode_path.replace("\\", "\\\\") + "');")
		tmpfile.write('''
			body = body.toString("utf8");
			var result = CSSLint.verify(body'''+ opts +''');
			var msgs = result.messages;
			var out = 'Line      Char      Reason\\n';
			
			if(msgs){
				for(var i=0, len=msgs.length; i<len; i++){
					out += (msgs[i].line+"          ").substr(0,10) + (msgs[i].col +"          ").substr(0,10) +'"'+ msgs[i].type +': '+ msgs[i].message.toString().replace('"','\"') +'"\\n';
				}
			}
			
			process.stdout.write(out);
		''')
		tmpfile.close()
		
		# store in tmp file
		tmpcode = open(tmpcode_path,"w")
		tmpcode.write(codestr)
		tmpcode.close()
		
		# run validation
		result = self._get_cmd_output(self.settings.get('nodejs', 'nodejs') +' "' + tmpfile_path +'"')
		
		#clean up
		os.remove(tmpcode_path)
		os.remove(tmpfile_path)
		
		return result

	# JS Helpers =========================================================
	def get_js_minified(self, codestr):
		ins = StringIO(codestr)
		outs = StringIO()				
		JavascriptMinify().minify(ins, outs)	
		min_js = outs.getvalue()				
		if len(min_js) > 0 and min_js[0] == '\n':
			min_js = min_js[1:]				
		return re.sub(r'(\n|\r)+','', min_js)


	def get_js_formatted(self, codestr):
		opts = jsbeautifier.default_options()
		opts.eval_code = False

		# pull indentation from user prefs
		use_tab = self.user_settings.get('translate_tabs_to_spaces',False)
		if use_tab:
			opts.indent_with_tabs = True
		else:
			opts.indent_char = " "
			opts.indent_size = int(self.user_settings.get('tab_size',False))
		
		# pull the rest of settings from our config
		for k,v in self.settings.get('jsformat', {}).iteritems():
			setattr(opts, k, v)
				
		return jsbeautifier.beautify(codestr, opts)


	def get_js_lint(self, codestr):
		opts = json.dumps(self.settings.get('jslint', {}))

		jslint_path = os.path.join(self.plugin_dir,  "jslint", "jslint")
		tmpfile_path = os.path.join(self.plugin_dir, "jslint", "tmp_jslint.js")
		tmpcode_path = os.path.join(self.plugin_dir, "jslint", "tmp_jslint_code.js")
		
		tmpfile = open(tmpfile_path,"w")
		tmpfile.writelines("var sys = require('sys');")
		tmpfile.writelines("var fs = require('fs');")
		tmpfile.writelines("var JSLINT = require('" + jslint_path.replace("\\", "\\\\") + "').JSLINT;")
		tmpfile.writelines("var body = fs.readFileSync('" + tmpcode_path.replace("\\", "\\\\") + "');")
		tmpfile.write('''
			body = body.toString("utf8");
			var result = JSLINT(body, '''+ opts +''');
			var out = 'Line      Char      Reason\\n';
			
			if(JSLINT.errors){
				for(var i=0; i<JSLINT.errors.length; i++){
					if(JSLINT.errors[i]){
						out += (JSLINT.errors[i].line+"          ").substr(0,10) + (JSLINT.errors[i].character+"          ").substr(0,10) +'"'+ JSLINT.errors[i].reason.toString().replace('"','\"') +'"\\n';
					}
				}
			}
			
			process.stdout.write(out);
		''')
		tmpfile.close()
		
		# store in tmp file
		tmpcode = open(tmpcode_path,"w")
		tmpcode.write(codestr)
		tmpcode.close()
		
		# run validation
		result = self._get_cmd_output(self.settings.get('nodejs', 'nodejs') +' "' + tmpfile_path +'"')
		
		#clean up
		os.remove(tmpcode_path)
		os.remove(tmpfile_path)
		
		return result

	# SB Helpers ========================================================
	def tmp_status(self, status):
		self.view.set_status('clientside', status)
		sublime.set_timeout(self.clear_status,10000)

	def clear_status(self):
		self.view.erase_status('clientside')

	def _get_selections(self):
		selections = self.view.sel()
		has_selections = False
		for sel in selections:
			if sel.empty() == False:
				has_selections = True

		# if not, add the entire file as a selection
		if not has_selections:
			full_region = sublime.Region(0, self.view.size())
			selections.add(full_region)

		return selections

	def _get_cmd_output(self,cmd):
		
		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		result, err = p.communicate()
		#p.wait()
		
		return result
