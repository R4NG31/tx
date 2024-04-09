# from conexion import conexion
# import pandas as pd
# from sqlalchemy import create_engine
# from django.conf import settings
# import numpy as np

# import pandas as pd
# from sqlalchemy import create_engine

# database_url = 'mysql+pymysql://root:secret@localhost:3306/transporte'

# engine = create_engine(database_url)

# querySitios ="SELECT * FROM tb1_sitiosTotales" 
# tb2_s =pd.read_sql(querySitios, con=engine)
# print(tb2_s)
# queryFO ="SELECT * FROM tb1_fibraoptica" 
# tb2_f =pd.read_sql(queryFO, con=engine)

# queryAGG ="SELECT * FROM tb1_agregadores" 
# tb2_a =pd.read_sql(queryAGG, con=engine)

# join = pd.merge(tb2_s,tb2_f,how="inner",left_on='ATT_ID', right_on='ID_ATT')
# import json

# ruta_archivo_json = r'C:\Users\HugodeJesúsMeloRange\Desktop\tutorialDajngo\prueba.json'
# datos = pd.read_json(ruta_archivo_json, orient='records')
# d = datos.to_dict("tight")
# print(d)