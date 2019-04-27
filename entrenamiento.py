#############################################################################################
#
#   Desafío legalbot.cl
#   Ricardo Castro Vidal
#   Abril de 2019
#   Archivo Fuente (1/2) : entrenamiento.py
#
#############################################################################################

import pandas as pd
import pickle
import gensim.corpora as corpora
import gensim
import spacy

import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.models import Phrases
from gensim.models.phrases import Phraser

# Inicializar Idioma Español
nlp_espanol = spacy.load('es')
stopwords = stopwords.words("spanish")

def build_n_grams(lines):
    return Phraser(Phrases(lines, min_count=5, threshold=100))

def construir_bigramas(objetos, n2_gram):
    return [n2_gram[obj] for obj in objetos]

def eliminar_stopwords(lineas):
    return [[palabra for palabra in simple_preprocess(str(obj)) if palabra not in stopwords] for obj in lineas]

def lemmatization(lineas, entiquetas_de_interes):
    """
    lemmatiza solo aquellas partes de la oracion que entregan informacion relevante
    sustantivos, adjetivos, verbos y adverbios
    :param lineas:
    :param entiquetas_de_interes:
    :return:
    """

    lemmas = []
    for linea in lineas:
        doc_linea = nlp_espanol(" ".join(linea))
        lemmas.append([token.lemma_ for token in doc_linea if token.pos_ in entiquetas_de_interes])
    return lemmas


def generate_corpus(objetos):
    """
    Realiza el preprocesamiento de los documentos necesario para la Clusterizacion
    :param objetos:
    :return:
    """

    print("\nConstruyendo N-gramas.............")
    n2_gram = build_n_grams(objetos)

    print("\nEliminando stopwords.............")
    objetos = eliminar_stopwords(objetos)

    print("\nConstruyendo 2-grams para todos los lineas.............")
    objetos_2_grams = construir_bigramas(objetos, n2_gram)

    print("\nLematizando de palabras de interés ....................")
    objetos_lematizados = lemmatization(objetos_2_grams, entiquetas_de_interes=['NOUN', 'ADJ', 'VERB', 'ADV'])

    print("\nConstruyendo diccionario de palabras/indices....................")
    id2word = corpora.Dictionary(objetos_lematizados)

    return id2word, objetos_lematizados


def generar_modelos(n_clusters, corpus, id2word, objetos_lematizados):

    """
    Genera un Modelo de con n_clusters, usando documentos preprocesados (corpus, objetos_lematizados)
    :param n_clusters:
    :param corpus:
    :param id2word:
    :param objetos_lematizados:
    :return: lda_model, perplexity, coherence_lda
    """

    print (50*"=")
    print ("Entrenando modelo con {} Clusters".format(n_clusters))
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=n_clusters,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)


    # calcular Coherencia del modelo
    coherence_model_lda = CoherenceModel(model=lda_model, texts=objetos_lematizados, dictionary=id2word, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()

    # calcular Perplexity del modelo
    perplexity = lda_model.log_perplexity(corpus)

    print("Perplexity del Modelo => ", perplexity)
    print('Coherencia del Modelo => : ', coherence_lda)

    return lda_model, perplexity, coherence_lda


def inicializar_clustering(lineas, read_objects_from_file=False):
    """
    Construye los objetos que necesita el algoritmo de clustering para generar su salida.
    Si ya estan construidos (read_objects_from_file=True) entonces solo se cargan
    :param lineas:
    :param read_objects_from_file:
    :return: corpus, id2word, objetos_lematizados
    """

    if read_objects_from_file:
        corpus = pickle.load(open("objects/corpus.pkl", "rb"))
        id2word = pickle.load(open("objects/id2word.pkl", "rb"))
        objetos_lematizados = pickle.load(open("objects/objetos_lematizados.pkl", "rb"))
    else:
        id2word, objetos_lematizados = generate_corpus(lineas)
        corpus = [id2word.doc2bow(objeto) for objeto in objetos_lematizados]

        pickle.dump(corpus, open("objects/corpus.pkl", "wb"))
        pickle.dump(id2word, open("objects/id2word.pkl", "wb"))
        pickle.dump(objetos_lematizados, open("objects/objetos_lematizados.pkl", "wb"))

    return corpus, id2word, objetos_lematizados



if __name__ == "__main__":
    """
    Este archivo esta configurado para correr 3 clustering y graficar cual es 
    el que entrega mejor coherencia.
    También genera todos los archivos de preprocesamiento intermedio.
    
    Se pueden cambiar este comportamiento modificando los parametros de la sección #Configuración
    """

    #Configuracion
    limit = 7;
    start = 4;
    step = 1;
    read_objects_from_file = False


    # leer datos a clusterizar
    df = pd.read_table('data/objetos_work.txt', header=None)
    df.columns = ["text"]

    lineas = df.text.values.tolist()
    lineas = [simple_preprocess(str(obj), deacc=True) for obj in lineas]

    crps, id2wrd, objs_lemm = inicializar_clustering(lineas, read_objects_from_file)

    model_list =[]
    perplexity_list =[]
    coherence_list =[]

    for i in range(start,limit,step):
        print ("\nGenerando modelo número {} de {}".format(i, limit-1))
        model, perplexity, coherence = generar_modelos(i, crps, id2wrd, objs_lemm)
        model.save("models/" + str(i) + "_clustermodel.m")

        model_list.append(model)
        perplexity_list.append(perplexity)
        coherence_list.append(coherence)

    x = range(start, limit, step)
    plt.plot(x, coherence_list)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.show()
