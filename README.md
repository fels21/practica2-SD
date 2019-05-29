Practica2 SD
==============================

### Com funciona
Funció Leader:
El programa executa una funció "leader" la qual rep l'identificador de cada funció "slave" una vegada rebuda tots els identificadors dóna permís a cada "slave" per a escriure el resultat.

Funció Slave:
Genera un nombre aleatori del 1 al 1000, si rep el permís per escriure guarda el seu número generat a la cola d'intercanvi, també guarda els resultats anteriors a la seva cola dels números, al trobar el missatge fi para de rebre els números.

# Index
1. [Requiriments](#requiriments)
2. [Com executar](#com-executar)
3. [Arxius de configuració](arxius-de-configuració)


## Requiriments
* [PyWren over IBM Cloud Functions](https://github.com/pywren/pywren-ibm-cloud).
* [Compte al IBM Cloud](https://www.ibm.com/cloud/)
* Alternativament [CloudAMQP](https://www.cloudamqp.com/) RabbitMQ
* Arxiu de configuració [.pywren_config](arxius-de-configuració) explicat al seu apartat
* Python 3.5, Python 3.6 or Python 3.7


## Com Executar

Per executar:

	py main.py #num_slaves

on #num_slaves el número d'esclaus que vol executar


### Arxius de configuració

L'arxiu `~/.pywren_config` al directori home de l'usuari:

```yaml
pywren: 
    storage_bucket: <BUCKET_NAME>

ibm_cf:
    endpoint    : <HOST>  # make sure to use https:// as prefix
    namespace   : <NAMESPACE>
    api_key     : <API_KEY>
   
ibm_cos:
    endpoint   : <REGION_ENDPOINT>  # make sure to use https:// as prefix
    api_key    : <API_KEY>

rabbitmq:
    amqp_url   : <amqp://>

```
