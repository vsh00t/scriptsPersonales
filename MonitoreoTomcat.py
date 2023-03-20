import sqlite3
import time
from jmxquery import JMXConnection, JMXQuery

jmx_host = "localhost"
jmx_port = 9090

jmx_url = f"service:jmx:rmi:///jndi/rmi://{jmx_host}:{jmx_port}/jmxrmi"
jmx_connection = JMXConnection(jmx_url)

memory_usage_query = JMXQuery(
    "java.lang:type=MemoryPool,name=*",
    attribute="Usage",
    metric_name="memory_pool_{name}",
    metric_labels={"name": "{name}"}
)

# Crear una base de datos SQLite en memoria
conn = sqlite3.connect('/root/scripts/memory_usage.db')
c = conn.cursor()

# Crear tabla para almacenar los datos, si no existe
c.execute('''CREATE TABLE IF NOT EXISTS memory_usage
             (timestamp INTEGER, pool_name TEXT, used_memory REAL, max_memory REAL)''')

def store_memory_usage():
    memory_usage = jmx_connection.query([memory_usage_query])
    memory_pool_dict = {}

    for metric in memory_usage:
        pool_name = metric.metric_labels["name"].replace(" ", "_").replace("-", "_")
        used_memory = metric.value
        max_memory = metric.value

        memory_pool_dict[pool_name] = (used_memory, max_memory)

    # Consulta para obtener el valor máximo de memoria
    memory_max_query = JMXQuery(
        "java.lang:type=MemoryPool,name=*",
        attribute="PeakUsage",
        metric_name="memory_pool_{name}_max",
        metric_labels={"name": "{name}"}
    )

    memory_max = jmx_connection.query([memory_max_query])

    # Actualizar los valores máximos de memoria en el diccionario
    for metric in memory_max:
        pool_name = metric.metric_labels["name"].replace(" ", "_").replace("-", "_")
        max_memory = metric.value
        used_memory = memory_pool_dict[pool_name][0]
        memory_pool_dict[pool_name] = (used_memory, max_memory)

    timestamp = int(time.time())

    for pool_name, memory_info in memory_pool_dict.items():
        used_memory, max_memory = memory_info
        c.execute("INSERT INTO memory_usage VALUES (?, ?, ?, ?)",
                  (timestamp, pool_name, used_memory, max_memory))

    # Guardar cambios en la base de datos
    conn.commit()

store_memory_usage()

# No olvides cerrar la conexión a la base de datos cuando termines
conn.close()
