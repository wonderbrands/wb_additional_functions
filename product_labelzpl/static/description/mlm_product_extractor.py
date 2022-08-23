archivo = open( 'mlm_product.csv')
before=''
for linea in archivo:
	#print (linea[:-1])
	record= linea[:-1].split(',')
	#print (record)
	if 'MLM' in record[1]:
		print ( str(record[0])+',MERCADOLIBRE'+','+str(record[1])+',SOMOS REYES OFICIALES' )
		if 'MLM' in record[2]:
			print ( str(record[0])+',MERCADOLIBRE'+','+ str(record[2])+',SOMOS REYES VENTAS'  )
			if 'MLM' in record[3]:
				print ( str(record[0])+',MERCADOLIBRE'+','+ str(record[3])+',SOMOS REYES PEKES'  )

	elif 'MLM' not in record[1]:
		if 'MLM' in record[2]:
			print ( str(record[0])+',MERCADOLIBRE'+','+ str(record[2])+',SOMOS REYES VENTAS'  )
			if 'MLM' in record[3]:
				print ( str(record[0])+',MERCADOLIBRE'+','+ str(record[3])+',SOMOS REYES PEKES'  )





	




