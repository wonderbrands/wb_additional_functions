
#=====================
archivo = open( 'MASTER_MLMS.csv')
before=''
sku_mlms={}

for linea in archivo:
	#print (linea[:-1])
	record= linea[:-1].split(',')
	sku_mlms[record[0]]=[record[1],record[2], record[3]]
	
#print (sku_mlms)
archivo.close()

#====================

archivo_odoo = open('product_template_update_mlm.csv')

for linea in archivo_odoo:
	#print (linea[:-1])
	record_odoo= linea[:-1].split(',')
	sku_a_buscar=record_odoo[1].replace('"','')
	#print ('sku a buscar: ',sku_a_buscar)

	#Con el SKU busca en el diccionario
	MLMs=sku_mlms.get(sku_a_buscar)
	if MLMs :# si encontro el SKU crea los registros de importacion
	
		default_code = record_odoo[1].replace('"','')
		id = record_odoo[0].replace('"','')

		account_indentificator=''
		market_identificator=''

		record=MLMs
		#print ('Lista de MLMs: ',record)
		header=0
		# ['MLM668181334', 'N/D', 'MLM666376666'], ['MLM605339276', 'N/D', 'N/D'],['N/D', 'N/D', 'MLM754343228'], ['N/D', 'N/D', 'N/D']
		marketplace = 'Mercado Libre'

		if 'MLM' in record[0]:
			header+=1
			account_indentificator = 'SOMOS REYES OFICIALES' 
			market_identificator =record[0]
			if header ==1:
				print (id+','+account_indentificator+','+ market_identificator+','+ default_code)
			else:
				print (''+','+ account_indentificator+','+ market_identificator+','+default_code)

		if 'MLM' in record[1]:
			header+=1
			account_indentificator = 'SOMOS REYES PEKES' 
			market_identificator =record[1]
			if header ==1:
				print ( id+','+account_indentificator+','+ market_identificator+','+ default_code)
			else:
				print (''+','+ account_indentificator+','+ market_identificator+','+default_code)


		if 'MLM' in record[2]:
			header+=1
			account_indentificator = 'SOMOS REYES VENTAS' 
			market_identificator =record[2]
			if header ==1:
				print (id+','+account_indentificator+','+ market_identificator+','+ default_code)
			else:
				print ( ''+','+ account_indentificator+','+ market_identificator+','+default_code)


		elif 'MLM' not in record[0]:
			if 'MLM' in record[1]:
				header+=1
				account_indentificator = 'SOMOS REYES PEKES' 
				market_identificator =record[1]
				if header ==1:
					print (id+','+account_indentificator+','+ market_identificator+','+ default_code)
				else:
					print (''+','+ account_indentificator+','+ market_identificator+','+default_code)

			if 'MLM' in record[2]:
				header+=1
				account_indentificator = 'SOMOS REYES VENTAS' 
				market_identificator =record[2]
				if header ==1:
					print (id+','+account_indentificator+','+ market_identificator+','+ default_code)
				else:
					print (''+','+ account_indentificator+','+ market_identificator+','+default_code)
		

		

	else: # si no, nada.
		pass
	#break



archivo.close()




	

	