from detector import df  # Importa el DataFrame `df` desde el archivo `detector`. Este `df` contiene los datos que se graficarán.

from bokeh.plotting import figure, show, output_file  # Importa las funciones necesarias de Bokeh para crear y mostrar gráficos.

from bokeh.models import AdaptiveTicker  # Importa `AdaptiveTicker`, que se usa para configurar el número de marcas en el eje `y`.

# Crea una figura para el gráfico con ciertos parámetros:
p = figure(
    x_axis_type='datetime',    # Define el tipo de eje `x` como fecha y hora para mostrar datos de tiempo.
    height=100,                # Establece la altura del gráfico en píxeles.
    width=500,                 # Establece el ancho del gráfico en píxeles.
    sizing_mode="stretch_both", # Configura el gráfico para que se adapte al tamaño de su contenedor.
    title="Grafica"            # Asigna un título al gráfico.
)

# Desactiva las marcas menores en el eje `y`, configurando su color en `None`.
p.yaxis.minor_tick_line_color = None

# Asigna un `ticker` adaptable al primer elemento de la cuadrícula del eje `y`.
# `AdaptiveTicker` permite ajustar el número de marcas en el eje `y`.
p.ygrid[0].ticker = AdaptiveTicker(desired_num_ticks=1)  # Limita el número de marcas a 1 en el eje `y`.

# Añade un gráfico de barras (`quad`) al objeto `p`, representando intervalos de tiempo con barras rojas.
# Las barras usan los valores de inicio (`left=df["Start"]`) y fin (`right=df["End"]`) de `df`.
q = p.quad(
    left=df["Start"],   # Columna `Start` de `df`, define el borde izquierdo de cada barra.
    right=df["End"],    # Columna `End` de `df`, define el borde derecho de cada barra.
    bottom=0,           # Fija la base de las barras en 0.
    top=1,              # Fija la parte superior de las barras en 1.
    color="red"         # Colorea las barras en rojo.
)

# Genera un archivo HTML para visualizar el gráfico en un navegador.
output_file("Grafica.html")

# Muestra el gráfico en el navegador.
show(p)
