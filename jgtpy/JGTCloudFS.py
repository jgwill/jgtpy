
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import JGTConfig as jgtc
import dropbox
import pathlib
from dropbox.exceptions import AuthError
import pandas as pd
#@title Functions DROPBOX Api

import JGTCore as jko

from pathlib import Path
import pathlib


_DROPBOX_ACCESS_TOKEN=jgtc._DROPBOX_ACCESS_TOKEN
def mkdir_existok(tpath):
    pathlib.Path(tpath).mkdir(parents=True, exist_ok=True)
     
def etc_dl_json_as_dict(fn,subdir='.'):
    tmpdir = 'tmp'
    etc_dl(fn,tmpdir,subdir)
    tfile = os.path.join(tmpdir,fn)
    print(tfile)
    dictio= jko.jsonfile2prop(tfile)
    os.remove(tfile)
    return dictio
               
def etc_dl(fn,local_tdir='.',etcsubdir='.'):
    mkdir_existok(local_tdir)
    local_file_path =  local_tdir + '/'+ fn
    #os.path.join(local_tdir,fn)
    print('Local file: ' + local_file_path)
    etcpath = jgtc.DROPBOX_ETC_PATH
    if etcsubdir != '.':
        etcpath = etcpath + '/' + etcsubdir
    etcpath=etcpath.replace('//','/')
    print('etc path:' + etcpath)
    fnpath= etcpath +'/'+ fn
    fnpath= fnpath.replace('//','/')
    print('fnpath: ' + fnpath)
    meta=dropbox_download_file(fnpath,local_file_path)
    print(meta)




def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox(_DROPBOX_ACCESS_TOKEN)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx
    

def dxls(path='/'):
	"""Return List dropbox files as dataframe
	alias of dropbox_list_file
	"""
	return dropbox_list_files(path)


def dropbox_list_files(path):
    """Return a Pandas dataframe of files in a given Dropbox folder path in the Apps directory.
    """

    dbx = dropbox_connect()

    try:
        files = dbx.files_list_folder(path).entries
        files_list = []
        for file in files:
            if isinstance(file, dropbox.files.FileMetadata):
                metadata = {
                    'name': file.name,
                    'path_display': file.path_display,
                    'client_modified': file.client_modified,
                    'server_modified': file.server_modified
                }
                files_list.append(metadata)

        df = pd.DataFrame.from_records(files_list)
        return df.sort_values(by='server_modified', ascending=False)

    except Exception as e:
        print('Error getting list of files from Dropbox: ' + str(e))


def np_dropbox_download_csv(dropbox_file_path):
    """Download a file from Dropbox to the local machine."""

    try:
        dbx = dropbox_connect()

        
        metadata, result = dbx.files_download(path=dropbox_file_path)
        #print(metadata)
        return result.content
        #f.write(result.content)
    except Exception as e:
        print('Error downloading file from Dropbox: ' + str(e))
        
def jgt_dropbox_download_dic(dropbox_file_path):
    """Download a file from Dropbox to the local machine."""

    try:
        dbx = dropbox_connect()
        
        metadata, result = dbx.files_download(path=dropbox_file_path)
        #print(metadata)
        return jko.cnf_Decoder(result.content)
        #f.write(result.content)
    except Exception as e:
        print('Error downloading file from Dropbox: ' + str(e))
        
def dropbox_download_file(dropbox_file_path, local_file_path):
    """Download a file from Dropbox to the local machine."""

    try:
        dbx = dropbox_connect()

        with open(local_file_path, 'wb') as f:
            metadata, result = dbx.files_download(path=dropbox_file_path)
            f.write(result.content)
    except Exception as e:
        print('Error downloading file from Dropbox: ' + str(e))
        

def dxu(local_file,dxfilepath):
	local_path ='TODO'
	return dropbox_upload_file(local_path,local_file,dxfilepath)


def dropbox_upload_file(local_path, local_file, dropbox_file_path):
    """Upload a file from the local machine to a path in the Dropbox app directory.

    Args:
        local_path (str): The path to the local file.
        local_file (str): The name of the local file.
        dropbox_file_path (str): The path to the file in the Dropbox app directory.

    Example:
        dropbox_upload_file('.', 'test.csv', '/stuff/test.csv')

    Returns:
        meta: The Dropbox file metadata.
    """

    try:
        dbx = dropbox_connect()

        local_file_path = pathlib.Path(local_path) / local_file

        with local_file_path.open("rb") as f:
            meta = dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))

            return meta
    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))
        
        
        
        
def dropbox_get_link(dropbox_file_path):
    """Get a shared link for a Dropbox file path.

    Args:
        dropbox_file_path (str): The path to the file in the Dropbox app directory.

    Returns:
        link: The shared link.
    """

    try:
        dbx = dropbox_connect()
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_file_path)
        shared_link = shared_link_metadata.url
        return shared_link.replace('?dl=0', '?dl=1')
    except dropbox.exceptions.ApiError as exception:
        if exception.error.is_shared_link_already_exists():
            shared_link_metadata = dbx.sharing_get_shared_links(dropbox_file_path)
            shared_link = shared_link_metadata.links[0].url
            return shared_link.replace('?dl=0', '?dl=1')


