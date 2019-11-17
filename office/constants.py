"""Attributes for office module"""
import os

USERPROFILE = os.environ['USERPROFILE']
DESKTOP = f'{USERPROFILE}\\Desktop'
PROJECT = f'{DESKTOP}\\Projects'
DESKTOP_FILES = f'{PROJECT}\\DesktopFiles.txt'
ALIAS = f'{PROJECT}\\alias.bat'
APPMENU = f'{PROJECT}\\files.txt'
START = f'{PROJECT}\\start.txt'
MINUTES = f'{DESKTOP}\\Minutes'
PDFDIR = f'{DESKTOP}\\pdf'
ANNUALS = f'{PDFDIR}\\annuals'
MERGE = f'{PDFDIR}\\merge'
IMAGEPDF = [f'{PDFDIR}\\images\\images', f'{PDFDIR}\\images\\pdf']
PDFTABLES = f'{PDFDIR}\\tables'
DOWNLOADS = f'{DESKTOP}\\Downloads'