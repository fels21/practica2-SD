import pywren_ibm_cloud as pywren
import pika
import random,json,os,sys,time

def conexion():
    pw_config  = json.loads(os.environ.get('PYWREN_CONFIG', ''))
    amqp_url = pw_config['rabbitmq']['amqp_url']
    params = pika.URLParameters(amqp_url)
    conexion = pika.BlockingConnection(params)
    return conexion

def leader(n_s):
    global n_msg
    global id_list
    global num_slaves
    connection = conexion()
    channel = connection.channel()
    t_start=time.time()
    channel.queue_declare(queue='logs')
    channel.exchange_declare(exchange="practica2", exchange_type='fanout') 
    num_slaves=n_s
    n_msg=0
    id_list=[]
    
    #DEFINICIONS
    #GetIds rep tots els ids dels slaves 
    def getIds(ch, method, properties, body):
        global id_list
        global n_msg
        
        idm=body.decode()
        id_list.append(idm)
        n_msg=n_msg+1
        if n_msg>= num_slaves:
            ch.stop_consuming()
    #executa quin slave escriu en cada moment
    def writeResult(channel, method, properties, body):
        global num_slaves
        global id_list
        global n_msg
        msg=json.loads(body)
        print(msg)
        if 'ok' in msg:
            n_msg=n_msg+1
            if n_msg<num_slaves:
                channel.basic_publish(exchange='', routing_key=str(id_list[n_msg]), body=json.dumps({'permis':1}))
            else:
                channel.basic_publish(exchange="practica2", routing_key='', body=json.dumps({'fi':1}))
                channel.stop_consuming()
               
    
    
    channel.basic_consume(getIds, queue='logs', no_ack=True)
    channel.start_consuming()
    channel.queue_purge('logs')
    n_msg=0
    random.shuffle(id_list)
    
    channel.basic_publish(exchange='', routing_key=str(id_list[n_msg]), body=json.dumps({'permis':1}))
    channel.basic_consume(writeResult, queue='logs', no_ack=True)
    channel.start_consuming()
    channel.queue_delete(queue='logs')
    channel.close()
    t_final=float(time.time()-t_start)
    return ("Total " + str(num_slaves) + " slaves finished in : " + str(t_final) + " secodns")
    
def slaves(id):
    connection = conexion()
    channel = connection.channel()
    global results
    global id_slave
    id_slave=str(id)
    
    channel.queue_declare(queue=id_slave)
    channel.queue_bind(queue=id_slave, exchange="practica2")
    
    channel.publish(exchange='', routing_key='logs', body=id_slave)
    results= []
    def generarNum(channel, method, properties, body):
        global  results
        global  id_slave
        valor=random.randint(0, 1000)
        body=json.loads(body)
        if 'permis' in body and body['permis'] == 1:
            message=json.dumps({'result':valor})
            channel.publish(exchange="practica2", routing_key='', body=message)
            channel.publish(exchange='', routing_key='logs', body=json.dumps({'ok':id_slave}))
        elif ('result' in body):
            results.append(body['result'])
        elif body['fi'] == 1:
            channel.stop_consuming()
            channel.queue_delete(queue=id_slave)
            channel.close()
        
    channel.basic_consume(generarNum, queue=id_slave, no_ack=True)
    channel.start_consuming()
    return (id_slave+ " : " + " ".join(str(e) for e in results))

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        pw = pywren.ibm_cf_executor(rabbitmq_monitor=True)
        n_slaves = int(sys.argv[1])
        
        pw.call_async(leader, n_slaves)
        
        args=[]
        for i in range(n_slaves):
            args.append({'id':i})
        pw.map(slaves, args)
        result = pw.get_result()
        for x in result:
            print(x)
        
                
    else:
            print ("Ha de haver mes dun mapper")
else:
            print ("Sintaxis: main.py num_mappers")
            exit(0)