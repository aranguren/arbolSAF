import csv
import re
from unicodedata import normalize
import psycopg2
from datetime import datetime

now = datetime.now() # current date and time


from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir('.') if isfile(join('.', f))]
files_to_open = list(filter(lambda x: (x.endswith('CORREGIDO.csv')), onlyfiles))

date_time = now.strftime("%Y-%m-%d")


con = psycopg2.connect(database="arbolsaf", user="docker", password="docker", host="127.0.0.1", port="5432")

cur = con.cursor()

row_count_total = 0
procesadas_total= 0
insertados_total = 0
errores_total = 0

general = open('general.log', 'w')

for filename in files_to_open:


    with open(filename, mode='r',encoding='latin1') as csv_file:
        general.write("Cargando fichero {}\n".format(filename))
        print("Cargando fichero {}\n".format(filename))
        
        csv_reader = csv.reader(csv_file, delimiter=';')

        
        line_count = 0
        procesadas = 0
        insertados = 0
        errores= 0 
        f = open('registro-{}.log'.format(filename[:-4]), 'w')
        fallidos = open('fallidos-{}.log'.format(filename[:-4]), 'w')
        
        data = [tuple(row) for row in csv_reader]
        #data = list(csv_reader)
        row_count = len(data)
        persona = {}
        for i in range(row_count):

            if line_count == 0 or line_count == 1:
                line_count += 1
                continue
            else:
                f.write("---------------- procesando linea {} -------------\n".format(i+1))

                procesadas+=1
                print("FICHERO {} / PROCESANDO LINEA {}...".format(filename, i+1))
                cod_especie = data[i][2] if data[i][2] else ''
                cod_cita = data[i][5] if data[i][2] else ''
                f.write("cod_especie -> {}\n".format(cod_especie))
                f.write("cod_cita -> {}\n".format(cod_cita))

                query = " select id, nombre_comun from arbolsaf_species as2  where cod_esp='%s';" % cod_especie
                cur.execute(query)
                r = cur.fetchone()
                if r and r[0]:
                    id_especie = r[0]
                    f.write("id especie -> {}\n".format(id_especie))
                else:
                    f.write("linea {} / especie no encontrada, codigo {}\n".format(i+1 , cod_especie))
                    fallidos.write("linea {} / especie no encontrada, codigo {}\n".format(i+1 , cod_especie))
                    general.write("fichero {} / linea {} / especie no encontrada, codigo {}\n".format(filename, i+1 , cod_especie))
                    
                    errores +=1
                    continue

                query = "select id, fuente_final from arbolsaf_reference where cod_cita='%s';" % cod_cita
                cur.execute(query)
                r = cur.fetchone()
                if r and r[0]:
                    id_cita = r[0]
                    f.write("id cita -> {}\n".format(id_cita))
                else:
                    f.write("linea {} / cita no encontrada (insertanto de todas maneras), codigo {}\n".format(i+1 , id_cita))
                    

                for j in range(6, len(data[i])):
                    cod_variable = data[0][j] if data[0][j] else False
                    if cod_variable:
                        valor_variable = data[i][j] if data[i][j] else ''
                        f.write("cod_variable -> {}\n".format(cod_variable))
                        f.write("valor_variable -> {}\n".format(valor_variable))
            
                        query = "select id, variable from arbolsaf_variable_type avt where cod_var='%s';" % cod_variable
                        try:
                            cur.execute(query)
                            r = cur.fetchone()
                        except Exception as e:
                            print(e)
                        if r and r[0]:
                            id_tipo_variable = r[0]
                            nombre_variable = r[1]
                            f.write("id id_tipo_variable -> {}\n".format(id_tipo_variable))
                            if valor_variable and valor_variable not in ['','na','n/a', 'NA','N/A']:
                                query = """INSERT INTO arbolsaf_variable  (created, modified, especie_id, referencia_id, tipo_variable_id, valor_general, chequeo)
                                        VALUES ('{}','{}', {}, {}, {}, '{}', false);""".format(
                                             date_time, date_time, int(id_especie), int(id_cita) or None, int(id_tipo_variable), str(valor_variable) 
                                        )
                                try:
                                    cur.execute(query)
                                    con.commit()

                                except Exception as e:
                                    fallidos.write("linea {} / error al insertar \n{}\n".format(i+1 , e))
                                    general.write("fichero {} / linea {} / error al insertar \n{}\n".format(filename, i+1 , e))
                                    
                                    errores +=1
                                else:
                                    f.write("linea {} / insertando valores \n{}\n".format(i+1 , query))
                                    insertados+=1

                            else:
                                f.write("linea {} / variable {} sin valor \n".format(i+1 , cod_variable))


                        else:
                            f.write("linea {} / id_tipo_variable no encontrado, codigo {}\n".format(i+1 , cod_variable))
                            fallidos.write("linea {} / id_tipo_variable no encontrado, codigo {}\n".format(i+1 , cod_variable))
                            general.write("fichero {} / linea {} / id_tipo_variable no encontrado, codigo {}\n".format(filename, i+1 , cod_variable))
                            
                            errores +=1
                            continue

                
            line_count += 1
        f.write("Fichero procesado\nLineas: {}\nProcesadas {}\nVariables Insertadas: {}\nErrores: {}".format(row_count, procesadas, insertados, errores))
        row_count_total +=row_count
        procesadas_total += procesadas
        insertados_total += insertados
        errores_total+=errores
        

        f.close()
        fallidos.close()

general.write("Ficheros procesado\nLineas: {}\nProcesadas {}\nVariables Insertadas: {}\nErrores: {}".format(row_count_total, procesadas_total, insertados_total, errores_total))
print("Fichero procesado\nLineas: {}\nProcesadas {}\nVariables Insertadas: {}\nErrores: {}".format(row_count_total, procesadas_total, insertados_total, errores_total))

general.close()
cur.close()
con.close()