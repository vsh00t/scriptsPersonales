import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import os

# Conectar a la base de datos
conn = sqlite3.connect('/root/scripts/memory_usage.db')
c = conn.cursor()

# Consultar los datos de las últimas 24 horas
timestamp_24h_ago = int((datetime.datetime.now() - datetime.timedelta(hours=24)).timestamp())
query = f"SELECT * FROM memory_usage WHERE timestamp >= {timestamp_24h_ago}"
c.execute(query)
rows = c.fetchall()

# Procesar los datos
data = {}
for row in rows:
    timestamp, pool_name, used_memory, max_memory = row
    if pool_name not in data:
        data[pool_name] = {"timestamps": [], "used_memory": [], "max_memory": max_memory}

    data[pool_name]["timestamps"].append(datetime.datetime.fromtimestamp(timestamp))
    data[pool_name]["used_memory"].append(used_memory / (1024 * 1024 * 1024))  # Convertir a GB

# Crear el gráfico
fig, ax = plt.subplots()

for pool_name, pool_data in data.items():
    max_memory_gb = pool_data['max_memory'] / (1024 * 1024 * 1024)
    ax.plot(pool_data["timestamps"], pool_data["used_memory"], label=f"{pool_name} MAX: {max_memory_gb:.2f} GB")

ax.set_xlabel("Tiempo")
ax.set_ylabel("Memoria usada (GB)")
ax.legend(title="Pool de memoria")

# Formatear el eje X para mostrar solo la hora
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# Agregar cuadrícula
ax.grid(True)

# Establecer la escala del eje Y en incrementos de 0.001 GB
ax.yaxis.set_ticks([x * 0.1 for x in range(0, int(ax.get_ylim()[1] // 0.1) + 1)])

# Establecer la escala del eje X en intervalos de minutos
# ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
# ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=10))

plt.savefig('/root/scripts/memory_usage.jpg')

# Enviar la imagen a través de Telegram
os.system(f"/usr/local/bin/telegram-send --image /root/scripts/memory_usage.jpg --caption ' Consumo de Memoria en {os.uname().nodename}'")
