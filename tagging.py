#############################################################################################
#
#   Desafío legalbot.cl
#   Ricardo Castro Vidal
#   Abril de 2019
#   Archivo Fuente (1/2) : tagging.py
#
#############################################################################################


import pickle
from gensim.models.ldamodel import LdaModel
import pandas as pd

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 10000)



def asignar_doc2cluster(local_model, local_corpus, documentos, print_palabras_caracteristicas=False):

    df_clusters = pd.DataFrame()
    local_corpus_info = local_model[local_corpus]
    cluster_words_dict = {}


    for i, row in enumerate(local_corpus_info):

        #ordenar las asignaciones para obtener el mas relevante
        row = sorted(row[0], key=lambda x: (x[1]), reverse=True)

        # solo interesa el valor de la primera tupla para conocer la asignacion
        # se pueden agregar la informacion de mas cluster si asi se desea
        (cluster_number, prop_topic) = row[0]

        # palabras que caracterizan al cluster asignado
        if cluster_number not in cluster_words_dict.keys():
            word_proportion = local_model.show_topic(cluster_number)
            cluster_keywords = ", ".join([word for word, _ in word_proportion])
            cluster_words_dict[cluster_number] = cluster_keywords
        else:
            cluster_keywords = cluster_words_dict[cluster_number]

        # agregar info al dataframe
        df_clusters = df_clusters.append(pd.Series([int(cluster_number), round(prop_topic,3), cluster_keywords]), ignore_index=True)


    df_clusters.columns = ['Cluster', 'Relevancia en %', 'Palabras Caracteristicas']

    if (print_palabras_caracteristicas):
            print ("Palabras caracteristicas de cada Cluster")
            for elem in cluster_words_dict:
                print ("cluster numero {} => {}".format(elem, cluster_words_dict[elem]))


    #agregar el documento final al dataframe
    documentos = pd.Series(documentos)
    return pd.concat([df_clusters, documentos], axis=1)



def cargar_modelos():
    my_model = LdaModel.load("models/5_clustermodel.m")
    corpus = pickle.load( open("objects/corpus.pkl", "rb"))
    df = pd.read_table('data/objetos_work.txt', header=None)
    df.columns = ["text"]

    documentos = df.text.values.tolist()
    return my_model, corpus, documentos



if __name__ == "__main__":
    my_model, corpus, documentos = cargar_modelos()

    #Asignar Documentos a Cluters a que Cluster pertenece cada documento
    df_asignaciones = asignar_doc2cluster(my_model, corpus, documentos, False)
    df_asignaciones = df_asignaciones.reset_index()
    df_asignaciones.columns = ['Nro_Doc', 'Cluster', 'Relevancia en %', 'Palabras Caracteristicas', 'Documento']

    print ((df_asignaciones.loc[df_asignaciones['Cluster'] == 0]).head())
    print("")
    print ((df_asignaciones.loc[df_asignaciones['Cluster'] == 1]).head())
    print("")
    print ((df_asignaciones.loc[df_asignaciones['Cluster'] == 2]).head())
    print("")
    print ((df_asignaciones.loc[df_asignaciones['Cluster'] == 3]).head())
    print("")
    print ((df_asignaciones.loc[df_asignaciones['Cluster'] == 4]).head())