


import sqlite3
import csv




	
def tabla_principal():
    conexion = conectarse()
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Stock (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        descripcion TEXT,
                        marca TEXT,
                        stock INTEGER,
                        precio_Unitario INTEGER
                      )''')
    
                      
    conexion.commit()
    conexion.close()
    
    
    

def conectarse():
	conexion = sqlite3.connect("ESBA_Market.db")
	return conexion

def insertar_producto():
	descripcion = ""
	marca = "d"
	precio = 0
	stock = 0
	while descripcion == "" or marca == "" or precio <= 0 or stock <=0:
		descripcion=input("Ingrese nombre del producto: ")
		descripcion=descripcion.upper()
		marca=input(f"ingrese la marca de {descripcion}: ")
		marca=marca.upper()
		if marca.isnumeric() or descripcion.isnumeric():
			print("los valores de marca y descripción deben ser alfabéticos o alfanuméricos")
			marca=""
			descripcion=""
		else:
			precio=input(f"Ingrese precio de {descripcion}: ")
			stock=input(f"Ingrese stock disponible de {descripcion}: ")
			if precio.isnumeric() and stock.isnumeric():
				precio=int(precio)
				stock=int(stock)
			else:
				precio=0
				stock=0
				print("Los valores de stock y precio deben ser numéricos y mayores a 0 \n carga eliminada")
	conexion = conectarse()
	cursor = conexion.cursor()
	cursor.execute("INSERT INTO Stock (descripcion, marca, stock, precio_Unitario) VALUES (?, ?, ?, ?)",(descripcion, marca, stock, precio))
	conexion.commit()
	conexion.close()
	print(f"se agregó con éxito el nuevo producto \n nombre: {descripcion} \n marca: {marca} \n precio: ${precio} \n stock: {stock}")
			
			
def insertar_varios_productos():
	cantidad=0
	while cantidad<=0:
		cantidad=input("¿Cuántos Productos desea agregar? ")
		if cantidad.isnumeric():
			cantidad = int(cantidad)
		else:
			cantidad=0
	for i in range (cantidad):
		insertar_producto()
	print(f"SE HAN INSERTADO {cantidad} PRODUCTOS\n\n")

def obtener_productos():
	conexion = conectarse()
	cursor = conexion.cursor()
	cursor.execute("SELECT * FROM Stock")
	productos = cursor.fetchall()
	conexion.close
	return productos
	
def modificar_producto():
	descripcion = ""
	marca = "d"
	precio = 0
	stock = 0
	
	while descripcion == "" or marca == "" or precio <= 0 or stock <=0:
		id = input("ingrese el Id del producto a modificar: ")
		if id.isnumeric():
			id = int(id)
			descripcion=input("Ingrese nombre del producto: ")
			marca=input(f"ingrese la marca de {descripcion}: ")
			if marca.isnumeric() or descripcion.isnumeric():
				print("los valores de marca y descripción deben ser alfanuméricos")
				marca=""
				descripcion=""
			else:
				precio=input(f"Ingrese precio de {descripcion}: ")
				stock=input(f"Ingrese stock disponible de {descripcion}: ")
				if precio.isnumeric() and stock.isnumeric():
					precio=int(precio)
					stock=int(stock)
				else:
					
					precio=0
					stock=0
					print("Los valores de stock y precio deben ser numéricos y mayores a 0 \n carga eliminada")
		else:
			print("Id debe ser numérico")
			
		
	conexion = conectarse()
	cursor = conexion.cursor()
	
	cursor.execute("UPDATE Stock SET descripcion=?, marca=?, stock=?, precio_Unitario=? WHERE id=?", (descripcion.upper(), marca.upper(), stock, precio, id))
	conexion.commit()
	conexion.close()
	print("Modificación realizada\n\n")

   

def eliminar_producto():
	opcion=0
	while opcion!=1 and opcion!=2 and opcion!=3:
		try:
			opcion = int(input("Ingrese una opción \n 1: Eliminar según Id \n 2: Eliminar según nombre \n 3: Eliminar según marca \n"))
		except ValueError:
			opcion=0
	match opcion:
		case 1:
			try:
				valor= int(input("Ingrese el Id \n"))
				eleccion = "id"
			except ValueError:
				print("Id inexistente")
				valor=-1
				
				
		case 2:
			valor = input("ingrese el nombre \n")
			eleccion = "descripcion"
		case 3:
			valor = input ("ingrese la marca \n")
			eleccion = "marca"
	conexion = conectarse()
	cursor = conexion.cursor()
	if opcion==1:
		if valor>=0:
			cursor.execute(f"DELETE FROM Stock WHERE {eleccion}=?",(valor,))
			ver_stock()
	else:
		cursor.execute(f"DELETE FROM Stock WHERE {eleccion}=?",(valor,))
		
		
	
	conexion.commit()
	conexion.close()
			
			
def ver_stock():
	mistock=obtener_productos()
	print("STOCK\n ID PRODUCTO   MARCA   PRECIO  STOCK\n")
	for stock in mistock:
		print(stock)
		
def obtener_stock():
	conexion = conectarse()
	cursor = conexion.cursor()
	cursor.execute("SELECT * FROM Stock")
	mistock = cursor.fetchall()
	conexion.close()
	return mistock

def exportar_csv():
	
	stock = obtener_stock()
	with open("Stock.csv","w") as doc:
		doc.write("Id,Nombre,Marca,Stock,Precio\n")
		for producto in stock:
			doc.write(f"{producto[0]},{producto[1]},{producto[2]},{producto[3]},{producto[4]}\n")
	print("Se exportaron los datos a Stock.csv")
		
def importar_csv():
    diccionario = {}
    with open("Stock.csv", "r") as doc:
        lector = csv.reader(doc)
        i = 0
        
        for fila in lector:
            contenido = {fila[0]: (fila[1], fila[2], fila[3])}
            if i == 1:
                diccionario = contenido
                marcas = [fila[2],]
              
            elif i>1:
                diccionario.update(contenido)
                marcas.append(fila[2])
        
                
            i += 1
        marcas = set(marcas)
    print(f"\t\t\t\t\t\t LISTADO\n\n\n{diccionario}\n\n\n Cantidad de productos en el archivo: {i-1}\n\n\n Cantidad de marcas registradas en el archivo: {len(marcas)}\n\n\n Listado de marcas: {marcas}\n\n\n ")


def buscar_por_criterio():
	respuesta="F"
	while respuesta!="A" and respuesta!="B" and respuesta!="C" and respuesta!="D":
		respuesta=(input(f"Ingrese letra correspondiente al criterio de la búsqueda:\n NOMBRE DE PRODUCTO --> 'A'\n MARCA --> 'B'\n STOCK --> 'C'\n PRECIO --> 'D'\n")).upper()
	valor = input("ingrese el valor a buscar según el criterio elegido: ")
	match respuesta:
		case "A":
			while valor.isnumeric():
				valor=input("No se aceptan valores numéricos, agregue otro valor: ")
			tipo="descripcion"
			valor=valor.upper()
		case "B":
			while valor.isnumeric():
				valor=input("No se aceptan valores numéricos, agregue otro valor: ")
			tipo="marca"
			valor=valor.upper()
		case "C":
			while not valor.isnumeric():
				valor=input("El valor debe ser numérico, agregue otro valor: ")
			tipo="stock"
		case "D":
			while not valor.isnumeric():
				valor=input("El valor debe ser numérico, agregue otro valor: ")
			tipo="precio_Unitario"
	conexion = conectarse()
	cursor=conexion.cursor()
	cursor.execute(f"SELECT * FROM Stock WHERE {tipo}=?", (valor, ))
	stock=cursor.fetchall()
	conexion.close()
	print(f"Registros de {tipo} encontrados mediante el valor {valor}:\n ID  PRODUCTO     MARCA    PRECIO    STOCK\n")
	
	for producto in stock:
		print(producto)


def consultar_rango_de_precio():
    minimo = input(f"ingrese el valor mínimo de precio: ")
    maximo = input(f"ingrese el valor máximo de precio: ")
    
    while not minimo.isnumeric() or not maximo.isnumeric():
        minimo = input(f"INGRESE VALORES NUMÉRICOS\n ingrese el valor mínimo de precio: ")
        maximo = input(f"ingrese el valor máximo de precio: ")
    maximo=int(maximo)
    minimo=int(minimo)
    if minimo > maximo:
        minimo, maximo = maximo, minimo
       
    print(f"productos entre ${minimo} y ${maximo}")
    conexion=conectarse()
    cursor=conexion.cursor()
    cursor.execute(f"SELECT * FROM Stock WHERE precio_Unitario BETWEEN ? AND ?",(minimo,maximo))
    stock=cursor.fetchall()
    conexion.close()
    i=0
    j=0
    listado=[]
    for producto in stock:
     print(producto)
     
def menu_principal():
	salir=True
	opcion=""
	while opcion!="0":
		opcion=input("\t\t\t\tBIENVENIDO AL MENÚ DE STOCK DE ESBA MARKET\n presione:\n 0 = Salir\n 1 = Insertar un producto\n 2 = Insertar varios productos\n 3"
		 "= Ver el stock completo\n 4 = Ver stock según rango de precios\n 5 = Modificar un producto\n 6 = Eliminar un producto\n 7 = Exportar archivo 'Stock.csv'\n 8"
		 " = Importar y analizar archivo 'Stock.csv'\n 9 = Buscar en el stock según criterio\n ")
		match opcion:
			case "0":
				opcion=input("¿Seguro desea salir?, indique 'SI' para continuar, o cualquier otra opción para cancelar y seguir en el menú: ").upper()
				if opcion == "SI":
					opcion = "0"
					print("¡HASTA LUEGO!")
			case "1":
				insertar_producto()
			case "2":
				insertar_varios_productos()
			case "3":
				ver_stock()
			case "4":
				consultar_rango_de_precio()
			case "5":
				modificar_producto()
			case "6":
				eliminar_producto()
			case "7":
				exportar_csv()
			case "8":
				importar_csv()
			case "9":
				buscar_por_criterio()
			case _:
				print("Opción incorrecta\n")
				
	

print("\n\t\t\t\t\tTP FINAL H. DE PROGRAMACIÓN\n\n\nINTEGRANTES:\n\n-Pablo Vargas\n-Gaston Bustamante\n-Juan Ignacio Skreka Ivanesevic\n")
tabla_principal()
menu_principal()

