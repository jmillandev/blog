---
title: "Una introducción a la asincronia en Python"
date: 2020-10-18
slug: "asyncronia-en-python"
description: ""
keywords: []
draft: false
tags: []
math: false
toc: false
---

##### NOTA: Puedes ver este mismo post desde [medium](https://medium.com/@jgmc3012/asyncronia-en-python-9d3542a728f5) o en formato markdown desde [github](https://gist.github.com/jgmc3012/df1d09b71a26fa2e6218e7021fb2781f)
![alter](https://1.bp.blogspot.com/-9DfiQYxVyHk/Vwi___XTRJI/AAAAAAAANnI/yqspgAHcBmUaf5cGycRDSp3cfs7vFBoEg/w1200-h630-p-k-no-nu/panoramica-cocina-sant-pau.jpg)
# Python en el cuerpo de un/a mesoner@
¿Te imaginas que el/la camarer@ de un restaurante pudiera tomar solo una orden a la vez? Es decir, que si alguien le pidiera unas papas fritas no pudiera atender a más nadie hasta que entregue esas papas fritas.

No se tu, pero a mi me parece que seria algo lento, creo que lo despedirian el primer día😓.

Bueno algo asi pasaria con python... al menos la mayoria de las veces. Ven, dejame explicarte mejor.

# Python es sincrono por default

## ¿Pero que significa eso?. 
Bueno basicamente que puede hacer una sola cosa a la vez y hasta que eso no este listo no puede hacer mas nada🤦.

## ¿Y cual es el problema en ser monotasking?
Bueno, si nuestro codigo esta haciendo un trabajo donde tenemos nuestra CPU a tope, realmente no hay problema con esto.

Pero... ¿que pasa cuando nuestro codigo esta haciendo uso de mucha entrada y salida (I/O)? 

Bueno, no nos queda mas remedio sino que esperar a que enviemos o recibamos dicho recurso. Y es aqui donde viene el problema.

Esto supone un error cuando queremos hacer cosas a gran escala. Imaginemos por un momento que queremos hacer un scraper. Vaya, que esperar un segundo por una request no es muy importante si solo haremos 2 o 3 peticiones. ¿Pero que pasa cuando queremos hacer 100, 200, o incluso miles por hora? Esto se vuelve un gran problema.

Porque la mayoria del tiempo nuestro CPU esta muerto de risa esperando que le mandemos informacion para trabajar. Es decir, no estamos aprovechando todos nuestros recursos. 

## Latencias

Antes de entrar a ver las posibles soluciones para este problema, veamos la siguiente tabla de un repo de [github](https://gist.github.com/hellerbarde/2843375) para tener un mejor contexto, sobre el tiempo aproximado que tardamos en buscar/enviar una informacion a los diferentes recursos de un sistema informatico.

|Recurso | Tiempo |
| --- | --- |
|Referencia de la caché L1 | 0.5 ns |
|Predicción errónea de rama | 5 ns |
|Referencia de la caché L2 | 7 ns |
|Bloqueo/Desbloqueo del [Mutex](https://en.wikipedia.org/wiki/Mutual_exclusion) | 25 ns |
|Referencia a la memoria principal | 100 ns |
|Comprimir 1K bytes con [Zippy](https://en.wikipedia.org/wiki/Snappy_(compression)) | 3,000 ns  =   3 µs |
|Enviar 2K bytes en una red de 1 Gbps | 20,000 ns  =  20 µs |
|Lectura aleatoria de un SSD | 150,000 ns  = 150 µs |
|Leer 1 MB secuencialmente de la memoria | 250,000 ns  = 250 µs |
|Viaje de ida y vuelta dentro del mismo centro de datos | 500,000 ns  = 0.5 ms |
|Leer 1 MB secuencialmente desde un SSD | 1,000,000 ns  =   1 ms |
|Busqueda de disco | 10,000,000 ns  =  10 ms |
|Leer 1MB secuencialmente desde un disco | 20,000,000 ns  =  20 ms |
|Enviar paquete CA-> Holanda-> CA | 150,000,000 ns  = 150 ms |
| --- | --- |

Puedes pensar. ¿Aja, y que con todo esto?. Bueno a priori no se ve muy importante si pensamos que son milesimas, cetesimas o inclusio nano segundos.
Aclaremos un poco mas el asunto, llevemos esto a unidades mas grandes(X1.000.000.000) y faciles de leer para nosotros(los humanos), ahora podemos ver los datos así:

### Menos de un Minuto:

| Proceso | tiempo | ¿que puede suceder? |
| --- | --- | --- |
| Referencia de la caché L1    | 0.5 s |  Un latido del corazon (0.5 s) |
| Predicción errónea de rama     | 5 s   |  Bostezo |
| Referencia de la caché L2    | 7 s   |  Bostezo  Largo |
| Bloqueo/Desbloqueo del [Mutex](https://en.wikipedia.org/wiki/Mutual_exclusion)     | 25 s  |  Hacer un café |
| Referencia a la memoria principal | 100 s   | Cepillarse los dientes |

### Minutos o Horas:
| Proceso | tiempo | ¿que puede suceder? |
| --- | --- | --- |
| Comprimir 1K bytes con [Zippy](https://en.wikipedia.org/wiki/Snappy_(compression))  | 50 min  | Un episodio de [Mr Robot](https://en.wikipedia.org/wiki/Mr._Robot) |
| Enviar 2K bytes en una red de 1 Gbps  | 5.5 hr  | Un curso corto de [Platzi](https://platzi.com/)(algo de practica incluida) |

### Dias:
| Proceso | tiempo | ¿que puede suceder? |
| --- | --- | --- |
| Lectura aleatoria de un SSD                    |  1.7 days | Un fin de semana |
| Leer 1 MB secuencialmente de la memoria |  2.9 days | Un fin de semana largo |
| Viaje de ida y vuelta dentro del mismo centro de datos  |  5.8 days | Una vacaciones promedio |
| Leer 1 MB secuencialmente desde un SSD    | 11.6 days | Gestación promedio de una [zarigüeyas](https://ast.wikipedia.org/wiki/Didelphimorphia) |

### Meses:
| Proceso | tiempo | ¿que puede suceder? |
| --- | --- | --- |
| Busqueda de disco                        | 16.5 weeks | Un semetre en la universidad |
| Leer 1MB secuencialmente desde un disco | 7.8 months | Un bebe(prematuro) pudo haber nacido |


### Años:
| Proceso | tiempo | ¿que puede suceder? |
| --- | --- | --- |
| Enviar paquete CA-> Holanda -> CA | 4.8 years | Completar el bachillerato/colegio/high school |


## Conclusiones
Usando estas medidas exorbitantes podemos tener una idea de que miestras nosotros enviamos 200Kb por una red de 1 Gbps pasarian **semanas**. Y realizar un proceso "*costoso*" para nuestra CPU como el de comprimir una imagen, se haria en solo **horas**. Y en todas esas semanas nuestra CPU no podria hacer nada, solo esperar.


# Algunos conceptos basicos(explicados de una forma sencilla)

## Instrucción o sentencia "bloqueante"
Es una instrucción que tiene el "**control**" del programa y no lo sede hasta culminar su tarea.
Ejemplo:

Un mesonero necesita servir/entregar una comida pero los platos no estan a su alcance. Asi que le pide a un cocinero que se los entregue.

Esos segundo que el cocinero espera que le entreguen los platos, es una acción bloqueante. Debido a que el no pudo hacer mas nada en este tiempo, tan solo esperar.

## Instrucción o sentencia "no bloqueante"
Es una instrucción que "**suelta el control**" del programa mientras ella no lo necesite. Podriamos decir que es una tarea que se esta ejecutando en background o en 2do plano.
Ejemplo:

Un mesonero recibe una orden de un cliente y la entrega al chef para que la prepare. El chef le indica que puede ir a atender a otros clientes mientras el prepara esa orden.

Esto es una tarea no bloqueante, debido a que el camarero no se queda allí esperando sin hacer nada. Digamos que "aprovecho" el tiempo y adenlanto otras tareas pendientes.

## Concurrencia
La concurrencia segun lo que la [wikipedia](https://es.wikipedia.org/wiki/Concurrencia_(inform%C3%A1tica)) nos habla es:

> se refiere a la habilidad de distintas partes de un programa, algoritmo, o problema de ser ejecutado en desorden o en orden parcial, sin afectar el resultado final.

Pensemos en la concurrencia en esa capacidad hacer varias cosas a la vez, pero de una forma intercalada. veamos un ejemplo para entenderlo mejor:


Vayamos al pasado, a los 2000 donde solo existian computadoras con un solo nucleo en su CPU. Un nucleo solo puede realizar una sentencia a la vez, sin embargo nuestras PCs mononúcleo eran capaces de reproducir musica, mientras se abria el navegador de Explorer, mientras dibujabamos algo en  Paint.

¿Como era esto posible? Bueno nuestro sitema operativo se encarga de eso, de alternar rapidamente entre cada tarea de tal forma que parezca que todo sucede al mismo tiempo.

## Paralelismo
Este es mas sencillo, se refiere a ejecutar dos tareas en paralelo. Ejemplo: Tu puede caminar al mismo tiempo que hablas. Son dos tareas que se pueden ejecutan en un mismo instante de tiempo. En nuestras PCs actuales esta forma de trabajar existe gracias a que nuestros CPUs(en su mayoria) ya son todos multinucleos.

## Proceso
Son la instancia de un programa, asi como en programación orientada a objetos(OOP) los objectos son instancias de las Clases. 

**NOTA**: Para que varios procesos se ejecuten en paralelo es necesario que cada uno de ellos se ejecute en un nucleo de la CPU.

## Threads
En español llamados subprocesos o hilos, son la unidad mas pequeña a la cual un procesador puede asignar tiempo. Cada proceso contiene al menos un hilo.

## Concurrencia colaborativa
Es muy similar a la concurrencia normal, pero en este caso son las mismas tareas encargadas de seder el "**control**". Visto de otro punto de vista, la concurrencia colaborativa es posible gracias a la ejecución de instrucciones no bloqueantes. Un ejemplo claro de esto lo vimos cuando nuestro cocinero le entrego un orden al chef y este le dijo que podia ir haciendo otras tareas.

La concurrencia colaborativa la vemos comunmente en aplicaciones o lenguajes monohilos, tienen una gran ventaja al ser mas ligeras. Pero tiene un problema, nos oblican a pensar de una manera distinta y libre de instrucciones bloqueantes. Debido a que es el mismo programa el encargado de ir "**liberando el control**", si se ejecuta una sentencia bloqueante no hay nada que hacer, solo esperar a que esas instrucción termine.

## Asincronia
creo que la mejor forma de explicarlo es con su etimología:
    Asíncrono (pronunciado ay-SIHN-kro-nuhs, del griego ASYN-, que significa “no con” y cronos, que significa     “tiempo”) es un adjetivo que describe objetos o eventos que no están coordinados en el tiempo.
    Un programa asincrono lo podemos ver con un programa donde sus instrucciones o sentencias no se ejecutan en el mismo orden en cada ejecución.

# Una cocina en Python

Para explicar un poco la asincronia usaremos el ejemplo de un restaurante y como se comportan sus mesoneros. En el habran dos objetos:

**NOTA:**
Veras el codigo un poco grande, pero son [*logs*](https://docs.python.org/3.8/library/logging.html) mas que todo , no te asustes.

Los identificadores del codigo y los logs estan en ingles. Su documentación en español(aunque no es el estandar en la industria).

**NOTA2:**
No se aplican las mejores tecnicas de clean code.

## 1. Waiter
El mesonero sera el encargado de realizar las tareas "*costosas*" de **I/O**. Estas haran referencia a las ordenes que el tiene que pedir a la cocina.

```python
import time
import logging

class Waiter:
    PREPARATION_TIME = {
        'burger':7.5,
        'frites':4,
        'soda':1,
        'beer':1.2,
    }

    def __init__(self, orders, id):
        """
        Recibe las ordenes y su carnet de identificación
        """
        self.orders = orders
        self.id = id

    def request_orders(self):
        """
        Mientra tengas ordenes por entregar, las ira pidiendo a la cocina.
        """        
        while not self.orders.empty():
            order = self.orders.get()
            self.request_order(order)

    def request_order(self, order):
        """
        Solicita a la cocina una orden(es decir una lista de productos).
        """
        logging.info('<Waiter: {}> [Order: {}] {:*^30}'.format(self.id, order['id'], 'Request order!'))
        for product in order['products']:
            self.request_product(product, order['id'])
        self.dispatch_order(order)

    def request_product(self,product, order_id):
        """
        Solicita un producto y espera a que se le entregue.
        """
        time_sleep = self.PREPARATION_TIME[product]
        logging.info(f'<Waiter: {self.id}> [Order: {order_id}] Request {product}. Wait {time_sleep} seg...')
        time.sleep(time_sleep)
        logging.info(f'<Waiter: {self.id}> [Order: {order_id}] Done {product}')

    def dispatch_order(self, order):
        """
        Despacha los producto de una orden.
        """
        logging.info(f'<Waiter: {self.id}> [Order: {order["id"]}] Done order!')
        for product in order['products']:
            logging.info(f'<Waiter: {self.id}> [Order: {order["id"]}] Dispatch {product}')
        logging.info('<Waiter: {}> [Order: {}] {:-^30}\n'.format(self.id, order["id"], 'Done dispatch!'))
```

Lo mas importante acá pueden ser dos cosas:
1. La variable `PREPARATION_TIME`, que indica los tiempos estimados de "preparación" para cada producto.
2. La funcion `request_product`: Esta funcion es la que esta "bloqueando" el proceso, `time.sleep(time_sleep)` espeficicamente. El camarero solicita una producto a la cocina y se queda allí parado sin hacer nada hasta que se lo entregan.

## 2. Cashier
La *cajera* sera una quien reciba las "ordenes" y se las pase al(o los) "mesonero(s)".

```python
from queue import Queue
import logging

class Cashier:
    orders = Queue()

    def __init__(self):
        """
        Registra el turno de cada mesonero.
        """
        self.waiters = [Waiter(self.orders, id+1) for id in range(2)]

    def receive_orders(self, orders:list):
        """
        Se reciben las ordenes de los clientes.
        Y se les indica a los mesoneros para que las atiendan.
        """
        for i, value in enumerate(orders):
            order = {
                'id': i,
                'products':value
            }
            self.orders.put(order)
        logging.info('Received orders')
        for waiter in self.waiters:
            waiter.request_orders()
```

El flujo es relativamente sencillo. La cajera recibe las ordenes y le indica a los camareros(Hay dos) de forma secuencia(primero a uno y luego al otro) que las despachen.


## Manos a la obra
En todos los ejemplos trabajaremos con el siguiente punto y datos de entrada:

```python
#! /usr/bin/python3
import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=10, datefmt='%H:%M:%S')


class Waiter:
    ...

class Cashier:
    ...

def main():
    orders = [
        ('burger','soda',), # Orden 1
        ('burger','burger', 'beer', 'frites'), # Orden 2
        ('beer', 'beer', 'beer'), # Orden 3
        ('burger','frites'), # Orden 4
    ]
    cashier = Cashier()
    cashier.receive_orders(orders)

if __name__ == '__main__':
    main()
```

Para este ejemplo contamos con 2 mesoneros y una cajera. ¿Que creen que pasara?

Veamos el output:
```bash
time python examples/asyncronia_en_python/sync.py
18:24:55 Received orders
18:24:55 <Waiter: 1> [Order: 0] ********Request order!********
18:24:55 <Waiter: 1> [Order: 0] Request burger. Wait 7.5 seg...
18:25:02 <Waiter: 1> [Order: 0] Done burger
18:25:02 <Waiter: 1> [Order: 0] Request soda. Wait 1 seg...
18:25:03 <Waiter: 1> [Order: 0] Done soda
18:25:03 <Waiter: 1> [Order: 0] Done order!
18:25:03 <Waiter: 1> [Order: 0] Dispatch burger
18:25:03 <Waiter: 1> [Order: 0] Dispatch soda
18:25:03 <Waiter: 1> [Order: 0] --------Done dispatch!--------

18:25:03 <Waiter: 1> [Order: 1] ********Request order!********
18:25:03 <Waiter: 1> [Order: 1] Request burger. Wait 7.5 seg...
18:25:11 <Waiter: 1> [Order: 1] Done burger
18:25:11 <Waiter: 1> [Order: 1] Request burger. Wait 7.5 seg...
18:25:18 <Waiter: 1> [Order: 1] Done burger
18:25:18 <Waiter: 1> [Order: 1] Request beer. Wait 1.2 seg...
18:25:19 <Waiter: 1> [Order: 1] Done beer
18:25:19 <Waiter: 1> [Order: 1] Request frites. Wait 4 seg...
18:25:23 <Waiter: 1> [Order: 1] Done frites
18:25:23 <Waiter: 1> [Order: 1] Done order!
18:25:23 <Waiter: 1> [Order: 1] Dispatch burger
18:25:23 <Waiter: 1> [Order: 1] Dispatch burger
18:25:23 <Waiter: 1> [Order: 1] Dispatch beer
18:25:23 <Waiter: 1> [Order: 1] Dispatch frites
18:25:23 <Waiter: 1> [Order: 1] --------Done dispatch!--------

18:25:23 <Waiter: 1> [Order: 2] ********Request order!********
18:25:23 <Waiter: 1> [Order: 2] Request beer. Wait 1.2 seg...
18:25:24 <Waiter: 1> [Order: 2] Done beer
18:25:24 <Waiter: 1> [Order: 2] Request beer. Wait 1.2 seg...
18:25:26 <Waiter: 1> [Order: 2] Done beer
18:25:26 <Waiter: 1> [Order: 2] Request beer. Wait 1.2 seg...
18:25:27 <Waiter: 1> [Order: 2] Done beer
18:25:27 <Waiter: 1> [Order: 2] Done order!
18:25:27 <Waiter: 1> [Order: 2] Dispatch beer
18:25:27 <Waiter: 1> [Order: 2] Dispatch beer
18:25:27 <Waiter: 1> [Order: 2] Dispatch beer
18:25:27 <Waiter: 1> [Order: 2] --------Done dispatch!--------

18:25:27 <Waiter: 1> [Order: 3] ********Request order!********
18:25:27 <Waiter: 1> [Order: 3] Request burger. Wait 7.5 seg...
18:25:34 <Waiter: 1> [Order: 3] Done burger
18:25:34 <Waiter: 1> [Order: 3] Request frites. Wait 4 seg...
18:25:38 <Waiter: 1> [Order: 3] Done frites
18:25:38 <Waiter: 1> [Order: 3] Done order!
18:25:38 <Waiter: 1> [Order: 3] Dispatch burger
18:25:38 <Waiter: 1> [Order: 3] Dispatch frites
18:25:38 <Waiter: 1> [Order: 3] --------Done dispatch!--------

python examples/asyncronia_en_python/sync.py  0,07s user 0,04s system 0% cpu 43,943 total
```

### ¿Ven algo raro?
Acaso no teniamos dos camareros. ¿Donde esta el segundo?

Pues esta es parte del problema. El codigo se ejecuta de manera secuencial y bloqueante. Por lo que el segundo camarero no es llamado hasta que el primero termine su tarea. Y adivinen, el primer camarero no suelta el control hasta haber despachado todas la ordenes. ¿Un problema, verdad?

No obstante, si se fijan el camarero pide un producto y se queda esperando(mirando al piso supongo) hasta que le entregue ese producto. Lo se, le hace falta activarse un poco.

Vemos como podemos "solucionar" esto.

# Con concurrencia(usando multiples hilos)

## Hilos en python

La manera mas "facil" de trabajar concurrencia en python es con el uso de [Threads](https://docs.python.org/3/library/threading.html) o [Hilos](https://es.wikipedia.org/wiki/Hilo_(inform%C3%A1tica)).

Como ya vimos un hilo es un sub-proceso de nuestro programa. Tenemos que tener en cuenta que si bien esto no es muy costoso, si tiene un coste para nuestro sistema.

Te dejo una [charla](https://www.youtube.com/watch?v=xbNrROaPYFY) muy completa sobre concurrencia y paralelismo. Este es un tema bastante profundo que da tela para otro post.

Para nuestro  ejemplo tendremos un hilo por cada "camarero", con esto le daremos la indepencia necesaria a cada uno para trabajar sin importar si el otro termino o no con las ordenes pendientes.

Vayamos al codigo:

Solo cambiaremos un par de lineas en nuesta "Cajera", espeficamente en la funcion `receive_orders`, quedaria algo así:

```python
import threading
    ...

class Cashier:
    ...
    def receive_orders(self, orders:list):
        """
        Se reciben las ordenes de los clientes.
        Y se les indica a los mesoneros para que las atiendan.
        """
        for i, value in enumerate(orders):
            order = {
                'id': i,
                'products':value
            }
            self.orders.put(order)
        logging.info('Received orders')
        for waiter in self.waiters:
            thread = Thread(target=waiter.request_orders)
            thread.start()
```
¿Que ha cambiado?
Bueno ya no llamamos a cada camarero de manera secuencial, sino que creamos un par de hilos y llamamos a cada uno de ellos por separado.

Bien, ¿que tal nos ira ahora atendiendo a nuestros clientes?

```bash
time python examples/asyncronia_en_python/threads.py                                                                                                
19:02:45 Received orders
19:02:45 <Waiter: 1> [Order: 0] ********Request order!********
19:02:45 <Waiter: 1> [Order: 0] Request burger. Wait 7.5 seg...
19:02:45 <Waiter: 2> [Order: 1] ********Request order!********
19:02:45 <Waiter: 2> [Order: 1] Request burger. Wait 7.5 seg...
19:02:52 <Waiter: 1> [Order: 0] Done burger
19:02:52 <Waiter: 1> [Order: 0] Request soda. Wait 1 seg...
19:02:52 <Waiter: 2> [Order: 1] Done burger
19:02:52 <Waiter: 2> [Order: 1] Request burger. Wait 7.5 seg...
19:02:53 <Waiter: 1> [Order: 0] Done soda
19:02:53 <Waiter: 1> [Order: 0] Done order!
19:02:53 <Waiter: 1> [Order: 0] Dispatch burger
19:02:53 <Waiter: 1> [Order: 0] Dispatch soda
19:02:53 <Waiter: 1> [Order: 0] --------Done dispatch!--------

19:02:53 <Waiter: 1> [Order: 2] ********Request order!********
19:02:53 <Waiter: 1> [Order: 2] Request beer. Wait 1.2 seg...
19:02:54 <Waiter: 1> [Order: 2] Done beer
19:02:54 <Waiter: 1> [Order: 2] Request beer. Wait 1.2 seg...
19:02:55 <Waiter: 1> [Order: 2] Done beer
19:02:55 <Waiter: 1> [Order: 2] Request beer. Wait 1.2 seg...
19:02:57 <Waiter: 1> [Order: 2] Done beer
19:02:57 <Waiter: 1> [Order: 2] Done order!
19:02:57 <Waiter: 1> [Order: 2] Dispatch beer
19:02:57 <Waiter: 1> [Order: 2] Dispatch beer
19:02:57 <Waiter: 1> [Order: 2] Dispatch beer
19:02:57 <Waiter: 1> [Order: 2] --------Done dispatch!--------

19:02:57 <Waiter: 1> [Order: 3] ********Request order!********
19:02:57 <Waiter: 1> [Order: 3] Request burger. Wait 7.5 seg...
19:03:00 <Waiter: 2> [Order: 1] Done burger
19:03:00 <Waiter: 2> [Order: 1] Request beer. Wait 1.2 seg...
19:03:01 <Waiter: 2> [Order: 1] Done beer
19:03:01 <Waiter: 2> [Order: 1] Request frites. Wait 4 seg...
19:03:04 <Waiter: 1> [Order: 3] Done burger
19:03:04 <Waiter: 1> [Order: 3] Request frites. Wait 4 seg...
19:03:05 <Waiter: 2> [Order: 1] Done frites
19:03:05 <Waiter: 2> [Order: 1] Done order!
19:03:05 <Waiter: 2> [Order: 1] Dispatch burger
19:03:05 <Waiter: 2> [Order: 1] Dispatch burger
19:03:05 <Waiter: 2> [Order: 1] Dispatch beer
19:03:05 <Waiter: 2> [Order: 1] Dispatch frites
19:03:05 <Waiter: 2> [Order: 1] --------Done dispatch!--------

19:03:08 <Waiter: 1> [Order: 3] Done frites
19:03:08 <Waiter: 1> [Order: 3] Done order!
19:03:08 <Waiter: 1> [Order: 3] Dispatch burger
19:03:08 <Waiter: 1> [Order: 3] Dispatch frites
19:03:08 <Waiter: 1> [Order: 3] --------Done dispatch!--------

python examples/asyncronia_en_python/threads.py  0,08s user 0,02s system 0% cpu 23,725 total
```

Okey, mejoramos un 2x nuestro tiempo de respuesta. Ahora si cada mesonero esta "trabajando", pero aun asi estamos perdiendo mucho tiempo en la espera de cada producto. Esto lo podriamos solucionar creando un hilo cada vez que le pidamos un producto a la cocina. Pero esto es algo costoso, tal vez no en nuestro ejemplo, pero imaginos un [scraper](https://es.wikipedia.org/wiki/Web_scraping) de amazon para un ecommerce dedicado al [dropshipping](https://es.shopify.com/blog/12377277-guia-completa-de-dropshipping), levantar 1000 hilos, cada uno para hacer una request(y scrapear un sitio web) no es algo trivial.

Por otra parte el uso de Threads es algo delicado. Cuando usamos threads y estos comparten recursos(aunque nuestros camareros comparten el objecto `orders`, este no es un caso problematico) se puede ocasionar una "sección critica", veamos un ejemplo que tome prestado del curso de [Progración concurrende en Codigo facilito](https://codigofacilito.com/cursos/python-concurrente), que imparte [Eduardo](https://twitter.com/eduardo_gpg), el cual les recomiendo mucho:

```python
import logging
import threading

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

BALANCE = 0
def depositos():
    global BALANCE

    for _ in range(0, 1_000_000):
        BALANCE += 1

def retiros():
    global BALANCE

    for _ in range(0, 1_000_000):
        BALANCE -= 1 # Sección critica

if __name__ == '__main__':
    thread1 = threading.Thread(target=depositos)
    thread2 = threading.Thread(target=retiros)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    logging.info(f'El valor final del balance es: {BALANCE}')
```
El codigo es sencillo, existe un `BALANCE`(inicializado en 0), supongamos que es de una cuenta bancaria, al cual le restaremos y sumaremos 1(uno) un millon de veces.

Uno esperaria que el resultado sea 0 siempre, ¿cierto?. Bueno esto casi nunca pasa. Te invido a ejecutar el [script](https://code.sololearn.com/cHg1nXgonugV/#py) y verlo por ti mismo. Esto sucedio por algo llamado condición de carrera, donde los procesos compiten por obtener un recurso(en este caso `BALANCE`).

La forma correcta de este codigo se veria así:
```python
import logging
import threading

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

BALANCE = 0

lock = threading.Lock()

def depositos():
    global BALANCE

    for _ in range(0, 1000000):
        try:
            lock.acquire()
            BALANCE += 1
        finally:
            lock.release()

def retiros():
    global BALANCE

    for _ in range(0, 1000000):
        with lock:
            BALANCE -= 1 # Sección critica

if __name__ == '__main__':
    thread1 = threading.Thread(target=depositos)
    thread2 = threading.Thread(target=retiros)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    logging.info(f'El valor final del balance es: {BALANCE}')
```
El `lock` nos servira como una especie de "seguro" donde nosotros sabremos que todo lo que este allí dentro solo estara accesible para un solo thread a la vez. Prueba el codigo [acá](https://code.sololearn.com/cFZYU7ViCPps/#py)

## Concurrencia colaborativa

Ahora si llegamos a la parte central de ese Post, el **asincronismo**.

Para continuar tenemos que aclarar dos conceptos fundamentales:

### Event loop
Es el administrador central, es un ciclo que itera contantemente entre los distintas tareas pendientes por ejecutar. Cuando una **tarea#1** necesita esperar un I/O esta le retorna el "control" al Event Loop para que ejecute la siguiente tarea pendiente. Cuando la **tarea#1** termina de recibir o enviar la información se quedara a la espera de que el Event Loop le retorne el control lo antes posible para continuar con su trabajo.

### Corutinas
Son funciones o rutinas bastante "normales", su diferencia radica en que pueden ser suspendidas o retormadas en ciertos espacios del codigo. Lo que nos ayuda muchisimo en estos casos, pues nosotros necesitaremos suspender su ejecución en operaciones de I/O y retomarla una vez esta operación hayan concluido.


### Muy bonito todo pero, ¿como se usa?
Bueno como su nombre lo indica, la idea es trabajar colaborativamente(hacer y no bloquear).

¿Necesitamos hacer algo que va a tardar?

1. Pedimos la informacion.
2. Esperamos y liberamos(le retornamos el control al event loop)
3. Luego que obtengamos la informacion el event loop nos dara el control eventualmente.

NOTA:
> Te dejo una charla de [entendiendo asyncio sin usar asyncio](https://youtu.be/BenwwgMx3Hg) donde explican esto con peras y manzanas. Por si luego le quieres echar un ojo.


# Async Nativo en Python3
Veamos un clasico "Hola mundo" mientras esperamos unos segundo:
```python
import asyncio

async def main(msg:str, seg:int):
    """
    Esta es una corutina, la identificamos por la palabra reservada
    `async`.
    """
    # Con `await` ejecutamos otra corutina y mientras, le damos el control al Event Loop.
    # En pocas palabras: "Esperamos y liberamos"
    await asyncio.sleep(seg)
    print(f'Espere {seg} seg para decirte:', msg)

if __name__ == "__main__":
    # Este es el Event Loop, es el punto de partida de toda la magia. Siempre lo requerimos.
    loop = asyncio.get_event_loop()

    # Le indicamos al loop que ejecute la corutina hasta que esta termine.
    loop.run_until_complete(main('Hola mundo con Asyncio', 2))

    """
    Desde python 3.7 esas dos linea pueden ser resumidas con
    """
    asyncio.run(main('Hola mundo con Asyncio en Python 3.7', 1))
```

Salida:
```shell
>>> Espere 2 seg para decirte: Hola mundo con Asyncio
>>> Espere 1 seg para decirte: Hola mundo con Asyncio en Python3.7

```

## ¿Que tenemos de nuevo?
- Una sentencia **await**: Se utiliza para esperar la respuesta de otra corrutina, y significa *asynchronous wait*(espera asincrónica), esa sentencia es la que le retorna el control al event loop. Y es la clave de todo.

## Corrutinas en "paralelo"

Supongamos que queremos ejecutar varias request a una API de forma simultanea. Veamos un codigo de como lo podriamos hacer:

```python
#! /usr/bin/python3
import asyncio
import logging
import aiohttp # Libreria externa de PiPy: https://docs.aiohttp.org/en/v2.3.4/

logging.basicConfig(format='[ %(asctime)s ]  %(message)s', level=10)

API = 'https://swapi.dev/api/people/{id}/'

async def get_person(session, id):
    """Haces las request a la URL e imprimimos el resultado"""
    url = API.format(id=id)
    # Relizamos la request a las URL
    async with session.get(url) as response:
        logging.info(f'Request person number {id}')

        # Obtenemos el resultado de la peticion como un dict de python
        person = await response.json()

        logging.info(f'Person number {id} = {person["name"]}')

async def main():

    # Inicializamos una session en el cliente WEB
    async with aiohttp.ClientSession() as session:
        # Creamos una lista con todas las corrutinas que queremos ejecutar
        coros = [get_person(session, id) for id in range(1, 10)]

        # Esperamos que todas las corrutinas terminen su ejecución
        await asyncio.gather(*coros)

if __name__ == '__main__':
    asyncio.run(main())
```
Veamos el output:
```bash
time python examples/asyncronia_en_python/asinc2.py

[ 2020-09-05 19:24:27,760 ]  Using selector: EpollSelector
[ 2020-09-05 19:24:29,294 ]  Request person number 1
[ 2020-09-05 19:24:29,294 ]  Person number 1 = Luke Skywalker
[ 2020-09-05 19:24:29,347 ]  Request person number 2
[ 2020-09-05 19:24:29,347 ]  Person number 2 = C-3PO
[ 2020-09-05 19:24:29,349 ]  Request person number 7
[ 2020-09-05 19:24:29,349 ]  Person number 7 = Beru Whitesun lars
[ 2020-09-05 19:24:29,350 ]  Request person number 6
[ 2020-09-05 19:24:29,350 ]  Person number 6 = Owen Lars
[ 2020-09-05 19:24:29,353 ]  Request person number 8
[ 2020-09-05 19:24:29,354 ]  Person number 8 = R5-D4
[ 2020-09-05 19:24:29,358 ]  Request person number 5
[ 2020-09-05 19:24:29,359 ]  Person number 5 = Leia Organa
[ 2020-09-05 19:24:29,362 ]  Request person number 4
[ 2020-09-05 19:24:29,363 ]  Person number 4 = Darth Vader
[ 2020-09-05 19:24:29,364 ]  Request person number 3
[ 2020-09-05 19:24:29,365 ]  Person number 3 = R2-D2
[ 2020-09-05 19:24:29,366 ]  Request person number 9
[ 2020-09-05 19:24:29,366 ]  Person number 9 = Biggs Darklighter

python examples/asyncronia_en_python/asinc2.py  0,27s user 0,05s system 17% cpu 1,859 total
```

**Podemos ver algunas cosas interesantes**:
1. Las 9 request a la API se realizaron en menos de 2 seg, Algo bastante dificil si lo hicieramos con las libreria [requests](https://requests.readthedocs.io/en/master/), la cual es una libreria bloqueante.
2. A pesar de que creamos nuestras corrutinas de una manera secuencial, no podemos predecir el orden en el que se ejecutan(cual finalizara primero).
3. La sentencia `asyncio.gather(*coros)`: recibe una lista de corrutinas y nos devuelve sus valores. Esta sentencia a su vez tambien es una corrutina por lo que tenemos que utilizar `await` para esperar su resultado final.

## Restaurante asincrono
Volvamos un momento a restaurante y hagamosle algunos cambios al mesonero para que no se quede esperando sin hacer nada hasta que le entregen el producto.

```python
class Waiter:
    ...

    async def request_orders(self):
        """
        Pedimos todas las ordenes casi en el mismo momento.
        Sin importar si ya la orden anterior esta lista.
        """
        coros = list()
        while not self.orders.empty():
            order = self.orders.get()
            coros.append(self.request_order(order))
        await asyncio.gather(*coros)

    async def request_order(self, order):
        """
        Pedir los productos a la cocina y dispachar la orden.
        """
        logging.info('<Waiter: {}> [Order: {}] {:*^30}'.format(self.id, order['id'], 'Request order!'))
        coros = [
            self.request_product(product, order['id']) for product in order['products']
        ]
        await asyncio.gather(*coros)
        self.dispatch_order(order)

    async def request_product(self,product, order_id):
        """
        Pedir un producto a la cocina.
        """
        time_sleep = self.PREPARATION_TIME[product]
        logging.info(f'<Waiter: {self.id}> [Order: {order_id}] Request {product}. Wait {time_sleep} seg...')
        await asyncio.sleep(time_sleep)
        logging.info(f'<Waiter: {self.id}> [Order: {order_id}] Done {product}')

    ...
```
Hicismos varios cambios, pero el mas importante es `await asyncio.sleep(time_sleep)` que esta dentro de `request_product`.
Esta setencia es la unica sentencia bloqueante que teniamos dentro de nuestro proceso. Ten en cuanta este cambio, hablaremos de el al final.

Los demas cambios son los de convertir todos los metodos involucrados en corutinas. Recordemos que solo dentro de las corutinas se pueden ejecutar sentencias no bloqueantes.


Pero falta algo, como ahora nuestro camarero esta trabajando de forma asincrona, debemos darle un punto de partida a nuestro event loop y eso lo haremos desde nuestra cajera.
```python
class Cashier:
    orders = Queue()

    def __init__(self):
        self.waiter = Waiter(self.orders, 1)
    def receive_orders(self, orders:list):
        for i, value in enumerate(orders):
            order = {'id': i, 'products': value}
            self.orders.put(order)
        logging.info('Received orders')
        asyncio.run(self.waiter.request_orders())
```

Como podran notar, ahora solo tenemos un camarero(al otro lo despedimos🤷‍♂️). Veamos como trabaja

```bash
time python examples/asyncronia_en_python/asinc.py
[Thr:MainThread]  Received orders
[Thr:MainThread]  Using selector: EpollSelector
[Thr:MainThread]  <Waiter: 1> [Order: 0] ********Request order!********
[Thr:MainThread]  <Waiter: 1> [Order: 1] ********Request order!********
[Thr:MainThread]  <Waiter: 1> [Order: 2] ********Request order!********
[Thr:MainThread]  <Waiter: 1> [Order: 3] ********Request order!********
[Thr:MainThread]  <Waiter: 1> [Order: 0] Request burger. Wait 7.5 seg...
[Thr:MainThread]  <Waiter: 1> [Order: 0] Request soda. Wait 1 seg...
[Thr:MainThread]  <Waiter: 1> [Order: 1] Request burger. Wait 7.5 seg...
[Thr:MainThread]  <Waiter: 1> [Order: 1] Request burger. Wait 7.5 seg...
[Thr:MainThread]  <Waiter: 1> [Order: 1] Request beer. Wait 1.2 seg...
[Thr:MainThread]  <Waiter: 1> [Order: 1] Request frites. Wait 4 seg...
[Thr:MainThread]  <Waiter: 1> [Order: 2] Request beer. Wait 1.2 seg...
[Thr:MainThread]  <Waiter: 1> [Order: 2] Request beer. Wait 1.2 seg...
[Thr:MainThread]  <Waiter: 1> [Order: 2] Request beer. Wait 1.2 seg...
[Thr:MainThread]  <Waiter: 1> [Order: 3] Request burger. Wait 7.5 seg...
[Thr:MainThread]  <Waiter: 1> [Order: 3] Request frites. Wait 4 seg...
[Thr:MainThread]  <Waiter: 1> [Order: 0] Done soda
[Thr:MainThread]  <Waiter: 1> [Order: 1] Done beer
[Thr:MainThread]  <Waiter: 1> [Order: 2] Done beer
[Thr:MainThread]  <Waiter: 1> [Order: 2] Done beer
[Thr:MainThread]  <Waiter: 1> [Order: 2] Done beer
[Thr:MainThread]  <Waiter: 1> [Order: 2] Done order!
[Thr:MainThread]  <Waiter: 1> [Order: 2] Dispatch beer
[Thr:MainThread]  <Waiter: 1> [Order: 2] Dispatch beer
[Thr:MainThread]  <Waiter: 1> [Order: 2] Dispatch beer
[Thr:MainThread]  <Waiter: 1> [Order: 2] --------Done dispatch!--------

[Thr:MainThread]  <Waiter: 1> [Order: 1] Done frites
[Thr:MainThread]  <Waiter: 1> [Order: 3] Done frites
[Thr:MainThread]  <Waiter: 1> [Order: 0] Done burger
[Thr:MainThread]  <Waiter: 1> [Order: 1] Done burger
[Thr:MainThread]  <Waiter: 1> [Order: 1] Done burger
[Thr:MainThread]  <Waiter: 1> [Order: 3] Done burger
[Thr:MainThread]  <Waiter: 1> [Order: 0] Done order!
[Thr:MainThread]  <Waiter: 1> [Order: 0] Dispatch burger
[Thr:MainThread]  <Waiter: 1> [Order: 0] Dispatch soda
[Thr:MainThread]  <Waiter: 1> [Order: 0] --------Done dispatch!--------

[Thr:MainThread]  <Waiter: 1> [Order: 1] Done order!
[Thr:MainThread]  <Waiter: 1> [Order: 1] Dispatch burger
[Thr:MainThread]  <Waiter: 1> [Order: 1] Dispatch burger
[Thr:MainThread]  <Waiter: 1> [Order: 1] Dispatch beer
[Thr:MainThread]  <Waiter: 1> [Order: 1] Dispatch frites
[Thr:MainThread]  <Waiter: 1> [Order: 1] --------Done dispatch!--------

[Thr:MainThread]  <Waiter: 1> [Order: 3] Done order!
[Thr:MainThread]  <Waiter: 1> [Order: 3] Dispatch burger
[Thr:MainThread]  <Waiter: 1> [Order: 3] Dispatch frites
[Thr:MainThread]  <Waiter: 1> [Order: 3] --------Done dispatch!--------

python examples/asyncronia_en_python/asinc.py  0,13s user 0,02s system 2% cpu 7,662 total
```

Ahora si, esto es lo que queriamos. Se redujo casi al maximo nuestro tiempo de espera, estamos tardando en despachar todas la  ordenes casi 7.5 seg, que es el tiempo de preparacion mas largo que tenemos(el de la hamburguesa).


# Conclusiones

¿Que genial, cierto?, todo lo que pudismos reducir nuestro tiempo de espera. ¿Piensa esto a gran escala en tus proyectos?. ¿Cuanto tiempo tardas buscando algo en la red? ¿Cuanto tiempo tarda tu base de datos en procesar una query? las ventajas trabajar con asincronia pueden ser muchas. Lamentablemente las desventajas tambien son varias. Vamos a listar algunas.

## Ventajas
El asincronismo nos permite trabajar con algunas de las ventajas que tendriamos al usar multi hilos sin problemas de "sección critica" y muchimo mas barato en terminos de recursos.

- Escala muy facil: Muchos miles de operaciones I/O concurrentes
- Es facil compartir recursos: No tenemos que preocuparnos por "secciones criticas" dado que todo corre bajo un mismo thread y un mismo proceso
- Mucho mas barato que usar hilos

## Desventajas
- Es mas "dificil" programar, hay que estar pendiente de que bloquea y que no.
- No todas las librerias son asincronas, por lo tanto, no podemos usar cualquier libreria en nuestros proyectos.

Quiero aclarar este ultimo punto de porque no podemos usar cualquier libreria. ¿Recuerdas esta sentencia del ultimo ejemplo `await asyncio.sleep(time_sleep)`?

Asyncio es el modulo principal de asincronia en python. la funcion `sleep` de asyncio es una funcion asincrona(es no bloqueante), en su contraparte la funcion `time.sleep` del modulo `time`, es una funcion bloqueante. Todo los cambio que hicimos en nuestro ultimo ejemplo no servirian de nada si hubieramos seguido trabajando con el modulo `time`.

Dicho esto hay que tener mucho cuidado. Python esta dividido en dos ecosistemas: el asincrono y el sincrono. Esto causa que al iniciar un proyecto no veamos en la dificil tarea de elegir que ecosistema utilizaremos.

El asincrono por un lado cuenta con las maravillas que ya vimos de la concurrencia colaborativa, pero no cuenta con tanta librerias de terceros como las que existen en el ecosistema sincrono.

Aca te dejo un [repo en github](https://github.com/timofurrer/awesome-asyncio) donde encontraras algunas librerias asincronas.

# Despedida

Espero hayas quedado con ganas de crear futuros proyectos utilizando asyncio en python y con el hambre de investigar mas sobre esta tecnologia. El ecosistema de asyncio ha venido creciendo en los ultimos años. 


Me despido, ojala hayas disfrutado esta lectura tanto como yo crearla. Si quieres dejarme algun feedback lo puedes hacer mencionandome Twitter como [jgmc3012](https://twitter.com/jgmc3012).

Hasta la proximas Dev🤘.
