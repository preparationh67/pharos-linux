#!/usr/bin/python
# Script Name: uninstall-pharos.py
# Script Function:
#	This script will uninstall pharos remote printing from the system.
#	The following tasks will be performed:
#	1. Remove the pharos backend from cups backend directory
#	2. Remove the popup scripts from /usr/local/bin/pharospopup
#	3. Remove the config file from /usr/local/etc/
#	4. Remove the uninstall script from /usr/local/bin/
#	5. Remove the users desktop environment autorun settings for running pharospoup at login
#	6. Delete the print queues that use pharos backend
#	
# Usage: 
#	$sudo python uninstall-pharos
#		This will uninstall the pharos remote printing
#
# Author: Junaid Ali
# Version: 1.0

# Imports ===============================
import os
import sys
import logging
import subprocess
import re
import shutil
import ConfigParser

# Script Variables ======================
logFile = '/tmp/pharosuninstall.log'
pharosBackendFileName = 'pharos'

# Functions =============================
class PharosUninstall:
	"""
	Handles the uninstallation of the pharos remote printing package
	"""
	def __init__(self, log):
		self.logger = log
		
	def uninstallPharosPrinters(self):
		"""
		Uninstall Pharos Printers
		"""
		logger.info('Uninstalling all pharos printers')
		allLocalPrinters = printerUtility.getAllPrinters()
		pharosPrinter = []
		for printer in allLocalPrinters.keys():
			printerSettings = allLocalPrinters[printer]
			if printerSettings.has_key('device-uri'):
				self.logger.info('Checking if printer %s with device uri %s is a pharos printer' %(printer, printerSettings['device-uri']))
				if re.match('pharos:\/\/', printerSettings['device-uri']):
					self.logger.info('Printer %s is a pharos printer' %printer)
					pharosPrinter.append(printer)
				else:
					self.logger.info('Printer %s is not a pharos printer' %printer)				
			else:
				self.logger.warn('could not find device-uri in printer settings %s' %printerSettings)
		
		allPharosPrintersDeleted = True
		if len(pharosPrinter) > 0:
			self.logger.info('There are total %s pharos printers installed on the system.' %len(pharosPrinter))			
			for printer in pharosPrinter:
				self.logger.info('Trying to delete printer %s' %printer)
				if printerUtility.deletePrinter(printer):
					self.logger.info('Printer %s successfully deleted' %printer)
				else:
					self.logger.info('Could not delete printer %s' %printer)
					allPharosPrintersDeleted = False			
		else:
			self.logger.warn('There are no pharos printers installed on the system')
		return allPharosPrintersDeleted
		
	def uninstallBackend(self):
		"""
		Uninstall Pharos Backend
		"""
		logger.info('Uninstalling pharos backend')
		backendDIR = '/usr/lib/cups/backend'
		backendFile = os.path.join(backendDIR, pharosBackendFileName)
		if os.path.exists(backendFile):
			self.logger.info('Backend file %s exists. Trying to remove it' %backendFile)
			try:
				os.remove(backendFile)
				logger.info('Successfully removed backend file: %s' %(backendFile))
			except:
				self.logger.error('Could not remove backend file %s' %backendFile)
		
		if os.path.exists(backendFile):
			return False
		else:
			return True			
		
	def uninstallPharosPopupServer(self):
		"""
		Uninstall Pharos Popup Server
		"""
		logger.info('Uninstall Pharos Popup Server')
		
		
	def uninstallLogFiles(self):
		"""
		Remove log files used
		"""
		logger.info('Uninstall Log Files')

	def uninstall(self):
		""""
		The main function
		"""
		logger.info('Beginning pharos uninstallation')
		
		if (self.uninstallPharosPrinters()):
			self.logger.info('All pharos printers have been deleted. Can proceed with uninstalling the CUPS pharos backend')
			if self.uninstallBackend():
				self.logger.info('Successfully removed backend file')
			else:
				self.logger.error('Could not remove backend file')
		else:
			self.logger.warn('All pharos printers could not be deleted. Will not be removing the CUPS pharos backend')
		
		self.uninstallPharosPopupServer()
		
		self.uninstallLogFiles()
		
		# Quit
		sys.exit(0)

# Main Script ============================

# Create logger
logger = logging.getLogger('pharos-uninstaller')
logger.setLevel(logging.DEBUG)
# Create file handler
fh = logging.FileHandler(logFile)
fh.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add loggers
logger.addHandler(fh)
logger.addHandler(ch)

# import the uninstall-pharos file
sys.path.append(os.getcwd())
try:	
	from printerutils import PrinterUtility
except:
	logger.error('Cannot import module printerutil')

printerUtility = PrinterUtility(logger)
pharosUninstaller = PharosUninstall(logger)

if __name__ == "__main__":
	pharosUninstaller.uninstall()
