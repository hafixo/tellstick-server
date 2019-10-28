#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(
	name='RF433',
	version='0.1',
	packages=['rf433'],
	package_dir = {'':'src'},
	entry_points={ \
		'telldus.startup': ['c = rf433:RF433 [cREQ]'],
	},
	extras_require = dict(cREQ = 'Base>=0.1\nBoard>=0.1\nTelldus>=0.1\nTelldusLive>=0.1'),
	package_data={'rf433' : [
		'firmware/TellStickDuo.hex'
	]}
)
