import psycopg2
import psycopg2.extras

con = psycopg2.connect(database="arbolsaf8", user="postgres", password="postgres", host="127.0.0.1", port="5432")

#cur = con.cursor()
cursor = con.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
errores  = open("errores.csv","w")
errores_cualitativos  = open("errores_cualitativos.csv","w")
cualitativos_repetidos  = open("cualitativos_repetidos.csv","w")
errores.write("ID VARIABLE;VALOR GENERAL;ID TIPO VARIABLE;COD VAR;NOMBRE VARIABLE;TIPO VARIABLE;COD ESP;NOMBRE ESPECIE;ERROR\n")
errores_cualitativos.write("ID VARIABLE;VALOR GENERAL;ID TIPO VARIABLE;COD VAR;NOMBRE VARIABLE;TIPO VARIABLE;COD ESP;NOMBRE ESPECIE;ERROR\n")
query = """select  avt.id as id_tipo_variable, 
avt.variable as nombre_variable, 
avt.cod_var as codigo_variable, 
avt.tipo_variables as tipo_variables, 
av.id as id_variable_valor,
av.valor_general, 
species.nombre_cientifico as nombre_especie,
species.cod_esp as codigo_especie 
from arbolsaf_variable av 
join arbolsaf_variable_type avt on (av.tipo_variable_id=avt.id)
join arbolsaf_species species on (species.id = av.especie_id)
order by id_tipo_variable"""
#where avt.tipo_variables <>'cualitativo'
cursor.execute(query)
results = cursor.fetchall()
for result in results:
    if result['valor_general'] and result['valor_general'] is not None and result['valor_general']!='':
        valor_general = result['valor_general']
        if result['tipo_variables'] =='rango' or result['tipo_variables'] =='numerico' :
            if ";" in valor_general:
                rangos = result['valor_general'].split(";")
            elif ":" in valor_general:
                rangos = result['valor_general'].split(":")
            else:
                rangos = result['valor_general'].split(":") 

            if len(rangos)==1:
                try:
                    rango_inferior = float(rangos[0])
                    query = f"""UPDATE arbolsaf_variable
                        SET rango_superior = {rangos[0]},
                            rango_inferior = {rangos[0]}
                        WHERE id={result['id_variable_valor']};"""
                    cursor.execute(query)
                    con.commit()
                    print(f"Procesada variable id->{result['id_variable_valor']}, cod_var->{result['codigo_variable']}, cod_esp->{result['codigo_especie']}, valor->{result['valor_general']}")
                except:
                     errores.write(f"""{result['id_variable_valor']};"{result['valor_general']}";{result['id_tipo_variable']};{result['codigo_variable']};{result['nombre_variable']};{result['tipo_variables']};{result['codigo_especie']};{result['nombre_especie']};el tipo de dato es incorrecto. no se puede asignar a un valor numerico un valor texto\n""")
     
            elif len(rangos)==2:
                try:
                    rango_inferior = float(rangos[0])
                    rango_superior = float(rangos[1])
                    query = f"""UPDATE arbolsaf_variable
                        SET rango_superior = {rango_superior},
                            rango_inferior = {rango_inferior}
                        WHERE id={result['id_variable_valor']};"""
                    cursor.execute(query)
                    con.commit()
                    print(f"Procesada variable id->{result['id_variable_valor']}, cod_var->{result['codigo_variable']}, cod_esp->{result['codigo_especie']}, valor->{result['valor_general']}")
                except:
                     errores.write(f"""{result['id_variable_valor']};"{result['valor_general']}";{result['id_tipo_variable']};{result['codigo_variable']};{result['nombre_variable']};{result['tipo_variables']};{result['codigo_especie']};{result['nombre_especie']};el tipo de dato es incorrecto. no se puede asignar a un valor numerico un valor texto\n""")
     
            else:
                errores.write(f"""{result['id_variable_valor']};"{result['valor_general']}";{result['id_tipo_variable']};{result['codigo_variable']};{result['nombre_variable']};{result['tipo_variables']};{result['codigo_especie']};{result['nombre_especie']};el valor general no existe o no esta correctamente formateado\n""")

        elif result['tipo_variables'] =='texto':
            try:
                valor_texto = str(result['valor_general'])
                query = f"""UPDATE arbolsaf_variable
                    SET valor_texto = '{valor_texto}'
                    WHERE id={result['id_variable_valor']};"""
                cursor.execute(query)
                con.commit()
            except Exception as e:
                errores.write(f"""{result['id_variable_valor']};"{result['valor_general']}";{result['id_tipo_variable']};{result['codigo_variable']};{result['nombre_variable']};{result['tipo_variables']};{result['codigo_especie']};{result['nombre_especie']};error inesperado al insertar un valor texto\n""")
               

            print(f"Procesada variable id->{result['id_variable_valor']}, cod_var->{result['codigo_variable']}, cod_esp->{result['codigo_especie']}, valor->{result['valor_general']}")
        
        elif result['tipo_variables'] =='boolean':

            valor_boolean = result['valor_general']
            if valor_boolean.lower() in ['si','verdadero','true']:
                query = f"""UPDATE arbolsaf_variable
                SET valor_boolean = true
                WHERE id={result['id_variable_valor']};"""
                cursor.execute(query)
                con.commit()
            elif valor_boolean.lower() in ['no','falso','false']:
                query = f"""UPDATE arbolsaf_variable
                SET valor_boolean = false
                WHERE id={result['id_variable_valor']};"""
                cursor.execute(query)
                con.commit()
            else:
                errores.write(f"""{result['id_variable_valor']};"{result['valor_general']}";{result['id_tipo_variable']};{result['codigo_variable']};{result['nombre_variable']};{result['tipo_variables']};{result['codigo_especie']};{result['nombre_especie']};valor incorrecto para variable booleana\n""")
                continue


               
            print(f"Procesada variable id->{result['id_variable_valor']}, cod_var->{result['codigo_variable']}, cod_esp->{result['codigo_especie']}, valor->{result['valor_general']}")

        elif result['tipo_variables'] =='cualitativo':
            valores_no_encontrados = []
            valores_cualitativos_str = valor_general.split(",")
            for valor_str in valores_cualitativos_str:
               
                query=f"""
                select id
                from arbolsaf_variable_type_option 
                where tipo_variable_id = {result['id_tipo_variable']} and nombre='{valor_str}'
                """
                cursor.execute(query)
                opcion = cursor.fetchone()
                if not opcion:
                    errores_cualitativos.write(f"""{result['id_variable_valor']};"{result['valor_general']}";{result['id_tipo_variable']};{result['codigo_variable']};{result['nombre_variable']};{result['tipo_variables']};{result['codigo_especie']};{result['nombre_especie']};el valor "{valor_str}" no se encuentra en las posibles opciones de la variable\n""")
                    valores_no_encontrados.append(valor_str)
                else:
                    query_opcion = f"""
                    select * from arbolsaf_variable_valores_cualitativos where variablemodel_id = {result['id_variable_valor']} and variabletypeoption_id = {opcion['id']}
                    """
                    cursor.execute(query_opcion)
                    opcion_asignada = cursor.fetchone()
                    if opcion_asignada:
                        cualitativos_repetidos.write(f"""{result['id_variable_valor']};"{result['valor_general']}";{result['id_tipo_variable']};{result['codigo_variable']};{result['nombre_variable']};{result['tipo_variables']};{result['codigo_especie']};{result['nombre_especie']};la opcion {valor_str} ya se encuentra asignada a la variable\n""")
                    else:
                        query_insertar_opciones = f"""
                        INSERT INTO arbolsaf_variable_valores_cualitativos (variablemodel_id, variabletypeoption_id)
                        VALUES ({result['id_variable_valor']}, {opcion['id']});
                        """
                        cursor.execute(query_insertar_opciones)
                        con.commit()
            if len(valores_no_encontrados)>0:
                general_values=",".join([str(i) for a,i in enumerate(valores_no_encontrados)])
                
                query_update_general_value=f"""
                    UPDATE arbolsaf_variable av
                    SET valor_general = '{general_values}'
                    where av.id = {result['id_variable_valor']};"""
            else:
                query_update_general_value=f"""
                    UPDATE arbolsaf_variable av
                    SET valor_general = ''
                    where av.id = {result['id_variable_valor']};"""
            cursor.execute(query_update_general_value)
            con.commit()




errores.close()
errores_cualitativos.close()
cualitativos_repetidos.close()