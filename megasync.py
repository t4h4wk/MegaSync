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

directorio_local = 'temp'

# Devuelve la url remota de los ficheros que le pasamos en hash
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

# Descarga todo el arbol de ficheros y directorios que hay en MegaClient
def download_all_files():
    result = True
    # Para cada fichero, obtiene su url remota, comprueba si existe la url local
    # y lo descarga 
    for file in files.items():
      if 'meta_mac' in file[1]:
	remote_filepath = getpath(files, file[1]['h'])
	local_filepath = directorio_local + remote_filepath
	# Descargamos el fichero si no existe en local
	if not os.path.exists(local_filepath):
	  verify_local_path(local_filepath)
	  print '[*] Descargando ' + remote_filepath
	  r = client.downloadfile(file[1], local_filepath)
	  if not r:
	    print '[ERROR] No se ha podido descargar ' + filepath
	    result = False
	else:
	  print '[*] No es necesario descargar el fichero ' + remote_filepath
	  
    if result:
      print '[*] Ficheros descargados correctamente'
    else:
      print '[ERROR] Ha ocurrido algun error al descargar los ficheros'
    return result
    
# Sube todo el arbol de ficheros locales a Mega. De momento los directorios deben existir
def upload_all_files():
    result = True
    
    # Lo primero que habria que hacer es recorrer el arbol de directorios locales
    # y comprobar si existen en remoto para crear los que no existan.
    
    
    # Recorremos el arbol de directorios locales
    for path, dir, name in os.walk(directorio_local):
      for n in name:
	# Guardamos en variables los diferentes path's y nombres de fichero
	local_filepath = path + '/' + n
	remote_filename = n
	remote_filepath = path.replace(directorio_local, '')
	# Para subir un fichero necesitamos saber el hash del directorio remoto donde se subira
	hash_path = path2hash(remote_filepath)
	# Si no existe el directorio en Mega hay que crearlo. POR HACER
	if hash_path == 'null':
	  print 'ERROR: No existe el directorio ' + remote_filepath + ' en Mega'
	  return False
	# Subimos el fichero
	print '[*] Subiendo ' + local_filepath
	client.uploadfile(local_filepath, files[hash_path]['h'], remote_filename)
	
    return result

# Verifica si un directorio existe en local y si no existe lo crea
def verify_local_path(path):
  import os.path
  
  acum_path = ''
  # Divide el path para comprobar si existe cada directorio por separado
  subpath = path.split('/')
  subpath = subpath[:-1]
  # Si alguno de los path's no exite lo creamos
  for i in subpath:
    acum_path = acum_path + i + '/'
    if not os.path.exists(acum_path):
      print '\tCreando directorio ' + acum_path
      os.mkdir(acum_path)

# Muestra el listado de directorios locales
def show_folders(path):
  print '[*] Directorios locales'
  for path, dir, name in os.walk(path):
    print '\t' + path

# Muestra el listado de ficheros locales    
def show_files(path):
  print '[*] Ficheros locales'
  for path, dir, name in os.walk(path):
    for n in name:
      print '\t' + path + '/' + n

# Funcion que devuelve el path de un hash
def path2hash(path):
    hash = 'null'
    for f in files.items():
      if getpath(files, f[0]) == path:
	hash = f[0]
	
    return hash

# Main. Pide el email y el password del usuario de Mega      
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
    #download_all_files()
    upload_all_files()
    

