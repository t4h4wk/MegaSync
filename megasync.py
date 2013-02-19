#
#
# MEGAFS
# https://github.com/CyberjujuM/MegaFS
#
# PYCRYPTO
# https://github.com/dlitz/pycrypto

from megaclient import MegaClient
import errno
import getpass
import os
import stat
import tempfile
import time

def getpath(files, hash):
	hash2path = {}
	
        if not hash:
            return ""
        elif not hash in hash2path:
            path = getpath(files, files[hash]['p']) + "/" + files[hash]['a']['n']

            i = 1
            filename, fileext = os.path.splitext(path)
            while path in hash2path.values():
                path = filename + ' (%d)' % i + fileext
                i += 1

            hash2path[hash] = path.encode()
        return hash2path[hash]
        
def download_all_files():
    result = True
    for file in files.items():
      if 'meta_mac' in file[1]:
	remote_filepath = getpath(files, file[1]['h'])
	local_filepath = 'temp' + remote_filepath
	verify_local_path(local_filepath)
	print '[*] Descargando ' + remote_filepath
	r = client.downloadfile(file[1], local_filepath)
	if not r:
	  print '[ERROR] No se ha podido descargar ' + filepath
	  result = False
    if result:
      print '[*] Ficheros descargados correctamente'
    else:
      print '[ERROR] Ha ocurrido algun error al descargar los ficheros'
    return result
	
def verify_local_path(path):
  import os.path
  
  acum_path = ''
  
  subpath = path.split('/')
  subpath = subpath[:-1]
  for i in subpath:
    acum_path = acum_path + i + '/'
    if not os.path.exists(acum_path):
      print '\tCreando directorio ' + acum_path
      os.mkdir(acum_path)
  
if __name__ == '__main__':
    email = raw_input("Email [%s]: " % getpass.getuser())
    if not email:
        email = getpass.getuser()
    password = getpass.getpass()
    client = MegaClient(email, password)
    client.login()
    files = client.getfiles()
    
    print files
    print
    print
    download_all_files()
