"""Office module functions"""

import csv
import datetime
import glob
import importlib
import os
import re
import subprocess
import sys
import textwrap
import time
import types
import urllib.parse
import urllib.request
import wave
from os import listdir, path, popen
from os.path import isdir, join
from time import gmtime, strftime

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageGrab
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

from office.constants import *

start_time = time.time()


def image():
    """Save Snips to Snip folder"""
    try:
        save_name = strftime('[%m-%d-%Y] %H.%M')
        myimage = ImageGrab.grabclipboard()
        x = 1
        save_path = f'{DESKTOP}\\Snips\\{save_name}[{x}].jpg'
        while os.path.exists(save_path):  # ensuring no duplicates
            save_path = f'{DESKTOP}\\Snips\\{save_name}[{x}].jpg'
            x += 1
        myimage.save(save_path)
        print(os.path.split(save_path)[1] +
              ' saved in Snips folder successfully')
    except:
        print('Clipboard not an image')


def append(index=None, text=None):
    """Appends new lines to files
    (0-aliases.bat/1-files.txt/2-DesktopFiles.txt)"""
    # For list of files
    filepath = [ALIAS, APPMENU, DESKTOP_FILES]
    with open(filepath[int(index)], 'a') as note:
        note.write(f'\n{text}')
        note.close()


def lines(textfile):
    """Returns a list of all lines in a text file"""
    return [w.strip('\n') for w in open(textfile, 'r').readlines()]


def info():
    """List all DOSKEY Commands"""
    alias = f'{PROJECT}\\aliases.bat'
    for w in open(alias, 'r').readlines():
        if not w.find('DOSKEY'):
            cmd = w.strip('\n').lstrip('DOSKEY')
            cmd = cmd.split('=')
            cmd[1] = textwrap.shorten(cmd[1], width=70, placeholder='...')
            print(f'> {cmd[0]:<10} {"-":>1} {cmd[1]:<5}')


def filename(path):
    """Returns a filename of a path"""
    path = os.path.basename(path)
    path = os.path.splitext(path)[0]
    return path


def pdftable():
    """Converting pdf to spreadsheets"""
    import tabula
    folder = fullpath(PDFTABLES)
    for files in folder:
        name = filename(files)
        tabula.convert_into(files, f'{DESKTOP}\\{name}.csv',
                            output_format='csv')
    print(runtime())


def allpath(directory):
    """Generates all absolute paths of files inside a directory"""
    paths = []
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            paths.append(os.path.abspath(os.path.join(dirpath, f)))
    return paths

def delete(index=None):
    """Deleting all pdfs on pdf folders [0-desktop/1-downloads/2-pdf]"""
    pdffiles = allpath(PDFDIR)
    downloads = fullpath(DOWNLOADS)
    desktop = fullpath(DESKTOP)
    selection = [desktop, downloads, pdffiles]
    listnames = ['Desktop','Downloads','PDF']
    protected_files = lines(DESKTOP_FILES)

    if not index:
        select(listnames)

    for files in selection[int(index)]:
        try:
            if os.path.basename(files) not in protected_files:
                os.remove(files)
                print(f'[{filename(files)}] deleted successfully')
        except:
            print(f'[{filename(files)}] Access Denied.')
            pass


def load(path):  # built in function
    subprocess.Popen(f'explorer /open, "{path}"', shell=True)


def client(query, year=None, action=None):
    """Improved Client Browser"""
    searchdic = {}
    parent_folder = fullpath('Z:\\Clients Files')
    workpapers = 'Annual Workpapers'
    final = 'Final Documents'

    if year:
        year = f'31 March {year}'
    else:
        return print('ERROR: Please indicate year')

    for items in parent_folder:
        if query.lower() in items.lower():
            searchdic[items] = os.path.split(items)[1]

    dic_count = searchdic.__len__()

    if dic_count > 1:
        for i, keys in enumerate(searchdic, start=1):
            print(f'[{i}] - {searchdic[keys]}')
        selection = int(input('Select company\n> '))
        company = list(searchdic.keys())[selection - 1]
    elif dic_count == 1:
        company = list(searchdic.keys())[0]
    else:
        return print('Client not found')

    clientname = os.path.split(company)[1]
    company = os.path.join(company, year, workpapers)

    if os.path.exists(company):
        if action == 'Y' or action == 'D':
            try:
                for files in fullpath(company):
                    if files.endswith('.xlsm'):
                        workpaper = files
                        break
                if action == 'Y':
                    load(workpaper)
                else:
                    uf = os.path.split(company)[0]
                    ffolder = fullpath(os.path.join(uf, final))
                    uf = [f for f in fullpath(uf) if f.endswith('pdf')]
                    signoff = uf + ffolder
                    signoff.append(workpaper)
                    for items in signoff:
                        print(items)
            except FileNotFoundError:
                print('File not found')
        elif action == 'M':
            output = os.path.join(DESKTOP, f'{clientname}.pdf')
            mrg = PdfFileMerger(strict=False)
            total = len(fullpath(company))
            tpages = 0
            for i, files in enumerate(fullpath(company)):
                try:
                    ProgressBar(i + 1, total)
                    if files.endswith('.pdf'):
                        reader = PdfFileReader(files)
                        pages = reader.getNumPages()
                        tpages += pages
                        mrg.append(files, pages=(0, pages))
                except:
                    print(f'Error reading [{os.path.split(files)[1]}]')
                    continue
            print(f'Total pages of all pdfs merged is [{tpages}]')
            mrg.write(output)
            mrg.close()
        else:
            load(company)
    else:
        print('Company directory for that year does not exist.')
    print(runtime())


def open_apps(index=None):
    """Open apps from a list"""
    apps = lines(APPMENU)
    if not index:
        for i, app in enumerate(apps, start=1):
            print(f'[{i}] - {filename(app)}')
        index = int(input('Select app\n> '))
        load(apps[index-1])
    else:
        load(apps[index])
    print(runtime())


def start():
    """Start all required apps"""
    for app in lines(START):
        load(app)
        print(f'[{filename(app)}] - has been initiated.')


def select(apps):
    """Function: file select prompt"""
    for i, app in enumerate(apps, start=1):
        print(f'[{i}] - {filename(app)}')
    index = int(input('Select from above\n> '))
    return apps[index-1]


def templates():
    """Open Templates"""
    folder = fullpath(r'Z:\Workpapers')
    template = select(folder)
    load(template)
    print(runtime())


def merge():
    """Merge all pdfs in the folder"""
    folder = fullpath(MERGE)
    output_path = os.path.join(DESKTOP, 'Merged.pdf')
    mrg = PdfFileMerger()

    for i, items in enumerate(folder):
        reader = PdfFileReader(items)
        page = reader.getNumPages()
        mrg.append(items, pages=(0, page))
        ProgressBar(i + 1, len(folder))
    mrg.write(output_path)
    mrg.close()
    print(runtime())


def prompt(q):
    """Function: Prompt loop for Y/N"""
    while True:
        reply = input('\n' + q + ' [Y/N]\n> ')
        if reply == 'Y':
            return True
        elif reply == 'N':
            return False
        else:
            print('Invalid Input.')


def detectfiles(dir):
    if not len(dir):
        print('No files detected')
        return False
    return True


def merge_fs():
    """Merge PDF files for clients' annuals"""
    # directories
    output = f'{DESKTOP}\\2019 - [CLIENT] - Financial Statements.pdf'

    # Instances, and variables
    mrg = PdfFileMerger(strict=False)
    dic, f = {}, ''

    # Check if there are files inside folder
    if not detectfiles(ANNUALS):
        return

    # get path of Financial Statements file
    fs = [x for x in fullpath(ANNUALS) if 'Statements.pdf' in x]

    # Check if FS file is available
    if not fs:
        print('No FS Found')
        return
    else:
        fs_end = PdfFileReader(fs[0]).getNumPages()

    # Confirmation
    if prompt('Are you merging a parent entity with its individuals?'):
        f = select(fullpath(ANNUALS))
        dic[f] = int(input(f'End page of {filename(f)}\n> '))

    # get end page tax summaries of tax returns
    for files in fullpath(ANNUALS):
        if files != fs[0] and files != f:
            dic[files] = int(input(f'End page of {filename(files)}\n> '))

    # merge pdf
    with open(output, 'wb'):
        mrg.append(fs[0], pages=(0, fs_end))
        if f:
            mrg.append(f, pages=(0, dic[f]))
        for keys in dic:
            if keys != fs[0] and keys != f:
                mrg.append(keys, pages=(0, int(dic[keys])))

    mrg.write(output)
    print(runtime())
    mrg.close()


def rename(find, replace=None):
    """Renaming files on desktop"""
    files = fullpath(DESKTOP)
    for f in files:
        name = os.path.basename(f)
        if name not in lines(DESKTOP_FILES):
            if find in name:
                replaced = name.replace(find, replace)
                os.rename(f, f.replace(name, replaced))
    print(runtime())


def myear(year):
    """Adding years on minuts names"""
    for items in fullpath(MINUTES):
        old = filename(items)
        new = f'{year} - {old}'
        os.rename(items, items.replace(old,new))
    print(runtime())


def csvfile(index=None):
    """Generate CSV templates [0-mjcsv/1-bankcsv]"""
    mj_csv = ['*Narration', '*Date', 'Description',
             '*AccountCode', '*TaxRate','*Amount',
             'TrackingName1', 'TrackingOption1',
             'TrackingName2', 'TrackingOption2']
    bank_csv = ['*Date', '*Amount', 'Payee',
                'Description', 'Reference',
                'Cheque Number']
    fields = [mj_csv, bank_csv]
    fields = ['Manual Journal', 'Bank Import']
    output = f'{DESKTOP}\\{fields[int(index)-1]}.csv'

    with open(output, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields[int(index)-1])
        writer.writeheader()
    print(f'\n{filename(output)} generated successfully')
    print(runtime())


def yt(query=None):
    """Download music from Youtube"""
    if not query:
        query = input('\nSearch for youtube videos\n> ')
    else:
        print('')

    query.replace(' ', '+')
    header = r'https://www.youtube.com/results?search_query='
    source = requests.get(header + query).text
    soup = BeautifulSoup(source, 'lxml')
    search_results = {}
    title = ''
    link = []
    for content in soup.find_all('div', class_="yt-lockup-content"):
        title = content.h3.a.text
        url = 'https://www.youtube.com' + content.h3.a['href']
        search_results[title] = url
        link.append(url)
    # print results
    for idx, titles in enumerate(search_results, start=1):
        print('[{}] - {}'.format(idx, titles))
        if idx == 10:
            break
    # selection
    selection = input('\nSelect the video to download music\n> ')

    subprocess.call(['youtube-dl', link[int(selection) - 1]])
    # print(link[int(selection)-1])
    print(runtime())


def fullpath(folder):
    """Function: Get full paths from files in folder"""
    return [os.path.join(folder, files) for files in os.listdir(folder)]


def imagepdf():
    """Convert images to pdf in folder"""
    pdf_path = IMAGEPDF[0]
    folder = fullpath(pdf_path)
    for files in folder:
        try:
            image = Image.open(files)
            pdf_name = os.path.split(os.path.splitext(files)[0])[1] + '.pdf'
            save_file = os.path.join(DESKTOP, pdf_name)
            image.save(save_file, "PDF", resolution=100.0, save_all=True)
            print(f'[{filename(files)}] Converted Successfully.')
        except OSError:
            print(f'[{filename(files)}] cannot be converted.')
            continue
    print(runtime())


def pdfimage():
    """Convert pdfs to image in folder"""
    import fitz
    pdfpath = IMAGEPDF[1]
    folder = fullpath(pdfpath)
    for files in folder:
        pdf = fitz.open(files)
        pdfname = filename(files)
        output = os.path.join(DESKTOP, pdfname)
        for i in range(len(pdf)):
            for idx, img in enumerate(pdf.getPageImageList(i), start=1):
                xref = img[0]
                pix = fitz.Pixmap(pdf, xref)
                outputs = f'{output}[{idx}].png'
                if pix.n < 5:
                    pix.writePNG(outputs)
                    print(f'{filename(outputs):<30} Converted Successfully.')
                else:
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.writePNG(outputs)
                    print(f'{filename(outputs):<30} Converted Successfully.')
    print(runtime())


def runtime():
    """Function: print run time of code executed"""
    t = round(time.time() - start_time, 2)
    return f'Task accomplished in {t} seconds'


def ProgressBar(iteration, total, prefix='Progress:',
                suffix='Complete',fill='█',length=28):
    """Progress bar for CMI"""
    decimal = round(100 * (iteration / total),1)
    percent = f'{decimal}%'
    filledLength = int(length * iteration / total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\rProgress: |{bar}| {percent} Complete', end='\r')
    # Print New Line on Completed
    if iteration == total:
        print()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        globals()[sys.argv[1]]()
    elif len(sys.argv) == 3:
        globals()[sys.argv[1]](sys.argv[2])
    elif len(sys.argv) == 4:
        globals()[sys.argv[1]](sys.argv[2],sys.argv[3])
    elif len(sys.argv) == 5:
        globals()[sys.argv[1]](sys.argv[2],sys.argv[3],sys.argv[4])
