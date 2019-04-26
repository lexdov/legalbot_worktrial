# Desafío Legalbot
Se requiere crear un algoritmo que categorice el texto de constitucion de empresas

# Descripcion del Problema
 Existe un archivo objetos.txt que contine 2863 líneas (cuerpo), en donde cada una representa el texto que describe la creación de una empresa. El idioma es español, y no existe una categorí asignada, simplemente el texto plano.

# Supuestos



# Datos

# Solucion Propuesta
La solucion propuesta es la utilizacion de un algoritmo de clustering llamado Latent Dirichlecht Allocation, en donde, dado un numero de clusters inicial, se construye una distribucion de probabilidad para cada una de las PALABRAS del cuerpo de texto(a que cluster representa dicha palabra), y luego, basada en esta distribucion, se calcula a cual de estos clusters pertenece cada DOCUMENTO (calculando el peso de cada palabra del documento para cada cluster).  Este enfoque permite que la asignacion de un documento a un Cluster sea tambien una distribucion de probabilidad.  Por ejemplo, el documento 1 pertenece al cluster 5 con un 80% de probabilidad, al cluster 3 con un 10%, y al cluster 1 con 10%; esto se conoce como Soft Assignment.   Esto permite que el usuario final pueda tener una mejor vision de que informacion se encuentra en cada documento, ya que en el clustering de documentos, es muy comun que un articulo se trate de varios temas (clusters),  medicina deportiva, o politica enconomica, por ejemplo.

## Alternativas
Otros enfoques de clusterizacion, como por ejemplo Gaussian Mixture Models, obligan a que cada documento debe pertenecer a un solo cluster, con lo cual se pierde informacion al momento de la asignación.  Por otra parte, si se quiere asignar a un solo cluster usando LDA, se puede hacer simplemente tomando el cluster con mayor probabilidad.  

## Evaluación
A diferencia de metodos supervisados, en donde se aplican metricas como F1-Score, Precission y Recall, en metodos no supervisados existen 2 metricas comunmente usadas para evaluar la clusterizacion: Coherencia y Perplexity.  
### Perplexity 
Mide que tan bien puedo predecir la siguiente palabra para un conjunto de palabras dadas https://en.wikipedia.org/wiki/Perplexity dado un Modelo de Lenguaje previamente Calculado

### Coherence
Mide que tan similares son los textos que se encuentran en un Cluster en especifico. http://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf.

Para el Desafío he elegido la metrica de Coherencia para determinar el numero óptimo de Clusters a usar.


# Decisiones de implementacion
## Uso de n-grams de segundo nivel
## eliminacion de stopwords
## No uso de TF-IDF como mecanismo de caracterizacion de documentos
## Lematizacion
## No uso de embeddings para visualizacion 
## Uso de Language Model en Español 
## Persistencia del Preprocesamiento

## Entrenamiento vs Tagging de Documentos

# Resultados
![alt text](https://drive.google.com/file/d/1NCK6bw6Lu9Ol22s9eAXCVZX6ut1eTa6h/view?usp=sharing)

# Conclusion

# Referencias


# Requirements.txt
