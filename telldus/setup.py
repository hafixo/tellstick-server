#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
try:
	from setuptools import setup
	from setuptools.command.install import install
except ImportError:
	from distutils.core import setup
	from distutils.command.install import install

class Webpack(install):
	def run(self):
		print("generate webpack application")
		if os.system('npm install') != 0:
			raise Exception("Could not install npm packages")
		if os.system('npm run deploy') != 0:
			raise Exception("Could not build web application")
		install.run(self)

setup(
	name='Telldus',
	version='0.1',
	packages=['telldus', 'telldus.web'],
	package_dir={'':'src'},
	cmdclass={'install': Webpack},
	entry_points={ \
		'telldus.plugins': [
			'api = telldus.DeviceApiManager',
			'react = telldus.web.React'
		]
	},
	extras_require={
		'telldus': ['Base>=0.1\nEvent>=0.1'],
	},
	package_data={'telldus' : [
		'templates/*.html',
		'htdocs/img/*.png',
		'htdocs/img/*.ico',
		'htdocs/fonts/*.eot',
		'htdocs/fonts/*.ttf',
		'htdocs/fonts/*.woff',
		'htdocs/fonts/*.woff2',
		'htdocs/js/*.js',
	]}
)
