import pandas as pd
import numpy as np
import openpyxl
import xlrd
ruta = r"C:\Users\HugodeJesúsMeloRange\Desktop\tutorialDajngo\corte_p2p_mixto_231020-Efi Tec.xlsx"
data = pd.read_excel(ruta)
#convertir = data.to_excel('data.xlsx')
df = pd.DataFrame(data, columns = ['VENDOR','IP_ADDRESS','PREFIX_LENGTH','INTERFACE_NAME','ID_SITE_DEVICE_NAME','DEVICE_NAME',
                                  'SITE_ID','LAGPORT','WORK_IP','WORK_IP2','WORK_IP3','LAG_CONFIGURATED_SPEED','LAG_CLASS','WORK_SPEED',
                                  'TO','IP_ADDRESS_P2P','PREFIX_LENGTH_P2P','SITE_ID_P2P','ID_SITE_NAME_P2P','SITE_NAME_P2P',
                                   'INTERFACE_NAME_P2P','LAGPORT_P2P','CONFIGURATED_SPEED_P2P','LAGG_CLASS_P2P','OPERATIONAL_SPEED_KBPS_P2P','VENDOR_P2P'])


filtro_com = df[df['DEVICE_NAME'].str.endswith("com")]
filtro_com = filtro_com["DEVICE_NAME"].str.slice(2,12)
filtro_mx = df[df["DEVICE_NAME"].str.endswith("mx")]
filtro_mx = filtro_mx["DEVICE_NAME"].str.slice(2,8)

filtro2_com =df[df["SITE_NAME_P2P"].str.endswith("com")]
filtro2_com= filtro2_com["SITE_NAME_P2P"].str.slice(2,12)
filtro2_mx =df[df["SITE_NAME_P2P"].str.endswith("mx")]
filtro2_mx =filtro2_mx["SITE_NAME_P2P"].str.slice(2,8)

for i,v in enumerate(df.columns):
    if v =='ID_SITE_DEVICE_NAME':
      df['ID_SITE_1'] = filtro_com
      df['ID_SITE_2'] = filtro_mx
      df['ID_SITE_DEVICE_NAME'] = df[['ID_SITE_1','ID_SITE_2']].apply(lambda x: ''.join(x.astype('str')), axis=1)
      df['ID_SITE_DEVICE_NAME'] = df['ID_SITE_DEVICE_NAME'].str.replace('nan',' ')

for i,v in enumerate(df.columns):
    if v == 'ID_SITE_NAME_P2P':
      df['ID_SITE_3'] = filtro2_com
      df['ID_SITE_4'] = filtro2_mx
      df['ID_SITE_NAME_P2P'] = df[['ID_SITE_3','ID_SITE_4']].apply(lambda x: ''.join(x.astype('str')), axis=1)
      df['ID_SITE_NAME_P2P'] = df['ID_SITE_NAME_P2P'].str.replace('nan',' ')

df = df.drop(['ID_SITE_1','ID_SITE_2','ID_SITE_3','ID_SITE_4'],axis=1)
df.to_excel('salida2.xlsx',index=False)
