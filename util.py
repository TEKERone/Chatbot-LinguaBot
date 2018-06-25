import unicodedata

topicos = {
    
    'temas_de_la_primera_seccion': ["articulos", "preposiciones", "colores"],
    'tipos_de_articulos': ["definido", "indeterminado"],
    'articulo': ["el", "la", "los", "las"],
    'articulo_indeterminado': ["a", "an"],
    'tipos_de_preposicion': ["tiempo y lugar", "lugar y movimiento"],
    'preposicion': ["on", "in", "at"],
    'preposicion_de_lugar_y_movimiento': ["opposite", "on the corner", "between", "in front of", "near", "behind", "next to", "into", "out of"],
    'colores': ["colores"],
    'temas_de_la_segunda_seccion': ["pronombres personales", "números ordinales", "números cardinales", "sustantivos", "vocabulario"],
    'tipos_de_pronombres': ["sujeto", "adjetivo", "objeto", "posesivos", "reflexivos"],
    'pronombre': ["i", "you", "he", "she", "it", "we", "they"],
    'pronombre_de_adjetivo': ["my", "your", "his", "her", "its", "our", "you", "their"],
    'pronombre_de_objeto': ["me", "you", "him", "her", "it", "us", "you", "them"],
    'pronombre_posesivo': ["mine", "yours", "his", "hers", "its", "ours", "theirs"],
    'pronombre_reflexivo': ["myself", "yourself", "himself", "herself", "itself", "ourselves", "yourselves", "themselves", "each other"],
    'tipos_de_numeros': ["cardinales", "ordinales"],
    'numeros_cardinales': ["1 al 12", "13 al 19", "20 al 90", "formar decenas", "formar centenas", "centenas con docenas", "millares", "millones"],
    'numeros_ordinales': ["primero al tercero", "cuarto al decimoavo", "docenas millares millon", "formar decenas"],
    'tipos_de_sustantivos': ["plural", "singular"],
    'sustantivo': ["s", "es", "ies", "ves"],
    'sustantivo_singular': ["caso 1", "caso 2"],
    'tipos_de_vocabulario': ["presentaciones", "personas"],
    'tipo_de_presentaciones': ["saludos", "despedidas", "nuevas presentaciones"],
    'personas': ["personas"],
    'temas_de_la_tercera_seccion': ["verbos", "formas cortas", "vocabulario familiar"],
    'tipos_de_verbos': ["verbo to be", "verbo to have", "verbo to do"],
    'tipos_de_verbo_to_be': ["afirmativo","negativo","interrogativo"],
    'tipos_de_verbo_to_have': ["tener", "haber"],
    'tipos_de_verbo_to_do': ["presente simple", "pasado simple"],
    'verbo_to_be_afirmativo': ["i", "you", "he", "she", "it", "we", "they"],
    'verbo_to_be_negativo': ["i am", "you are", "he", "she is", "it is", "we are", "they are"],
    'verbo_to_be_interrogativo': ["am i", "are you", "is he", "is she", "is it", "are we", "are they"],
    'verbo_to_have_tener': ["i have","you", "he has", "she has", " we have","you have", "they have"],
    'verbo_to_have_haber': ["i had", "you", "he had", "she had", "we had", "you had", "they had"],
    'verbo_to_do_presente_simple': ["i do", "you", "he does", "she does","it does", "we do","you do", "they do"],
    'verbo_to_do_pasado_simple': ["i did", "you", "he did", "she did", "it did", "we did", "you did", "they did"],
    'tipo_de_vocabulario': ["vocabulario", "ejemplos"],
    'tipo_de_forma_corta': ["forma simple", "forma negativa"],
    'temas_de_la_cuarta_seccion': ["actidades"],
    'tipo_de_actividad': ["actividades"],
    
    
}

def elimina_tildes(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
