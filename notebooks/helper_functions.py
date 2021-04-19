# helper functions

def str_rem_empty(char):
    '''Funcion para limpiar ultimo espacio vacio en strings'''
    if str(char)[-1] == ' ':
        newchar = str(char)[:-1]
    else:
        newchar = str(char)
    return newchar


def info_evento(sheetname):
    '''Esta funcion levanta la informacion de las solapas que se pasan como input del excel de eventos'''
    df_eve = pd.read_excel(RAW/'eventos.xlsx', engine='openpyxl', sheet_name=sheetname)
    dic_eve = {
        "evento": df_eve['Evento'][0], 
        "fecha": df_eve['Fecha'][0],
        "socios": df_eve.loc[df_eve['Tipo'] == 'Socio']['Numero'].unique(),
        "publico": len(set([str(x) for x in df_eve[['Tipo', 'Numero']].values]))
        }
    return dic_eve      
    
    
    
