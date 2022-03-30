# Por Luis Mex, correo: bjt.mex@gmail.com

# Requisitos para correr la Aplicación:

# Crear un entorno virtual
"python -m virtualenv .{nombre_virtual_env}"

 # instalar la siguiente paqueteria que se encuentra en requirements.txt con el siguiente comando
"pip install -r requirements.txt

# correr el comando 
# asumiendo que se cuenta con la base de datos db.sqlite3
"python manage runserver "


# Los endpoints requeridos se encuentran en la carpeta : Equipments/urls

# En el folder common se ecnuentra una clase que herada de Pagination con custom response aplicado en los enpoints de Lista.