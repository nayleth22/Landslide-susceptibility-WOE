# Landslide-susceptibility-WOE 	

This Python script generates a landslide susceptibility model using weights of evidence. As input, the script requires the following variables:

- Output path
- Path of each of the thematic maps
- Path of the map with the sample inventory of morphodynamic processes to be used for training.
- Null value or no data value

Within the 'DATA' folder, you will find the maps used for my research work. These maps which are used for processing, are in raster format and are in the Magna-Sirgas 3116 coordinate reference system. Furthermore, they are precisely aligned, possess consistent resolution, and the classes are represented using numerical values.

Inside the 'FILES' folder, you will find the thematic maps together with the landslide susceptibility map in its final presentation version.

## The script will generate the following:

- The Landslide Susceptibility Index (LSI) map in TIFF format.
- An Excel file with a spreadsheet for each thematic map, indicating the necessary calculated variables and the weights assigned to each class of each thematic map.

## Installation:
To use the script, it is necessary to have Python and some additional libraries (numpy, os, xlsxwriter, osgeo, pandas, argparse, gdal. ) installed.

To install GDAL, I recommend you follow the tutorial below.
https://www.linkedin.com/pulse/instalar-gdal-windows-10-yineth-castiblanco-rojas

## Authorship:
This project was created by Nayleth Alexandra Rojas Becerra. You can contact the author at nayleth_alexandra@hotmail.com
You can access the complete document of this research through the following link: https://noesis.uis.edu.co/handle/20.500.14071/14313

# Modelo de susceptibilidad a deslizamientos con pesos de evidencia 
Este script de Python genera un modelo de susceptibilidad a deslizamientos utilizando pesos de evidencia. Como entrada, el script requiere las siguientes variables:

- Ruta de salida
- Ruta de cada uno de los mapas temáticos
- Ruta del mapa con la muestra del inventario de procesos morfodinámicos que se utilizará para el entrenamiento
- Valor nulo o valor de no dato

Dentro del directorio 'DATA', descubrirás los mapas empleados en mi investigación. Estos mapas que se usan para el procesamiento, se encuentran en formato ráster y se hallan en el sistema de coordenadas de referencia Magna-Sirgas 3116. Además, están perfectamente alineados, presentan una resolución uniforme y las distintas clases se encuentran representadas mediante valores numéricos.

Dentro de la carpeta 'FILES', encontrarás los mapas temáticos junto al mapa de susceptibilidad a deslizamientos en su versión de Presentación final.

## El script generará lo siguiente:

- El mapa de Índice de Susceptibilidad a Deslizamientos (LSI) en formato TIFF
- Un archivo de Excel con una hoja de cálculo por cada mapa temático, que indica las variables calculadas necesarias y los pesos asignados a cada clase de cada mapa temático.

## Instalación:
Para utilizar el script, es necesario tener instalado Python y algunas librerías adicionales (numpy, os, xlsxwriter, osgeo, pandas, argparse, gdal)

Para instalar GDAL, te recomiendo seguir el tutorial que se presenta a continuación.
https://www.linkedin.com/pulse/instalar-gdal-windows-10-yineth-castiblanco-rojas

## Autoría:
Este proyecto fue creado por Nayleth Alexandra Rojas Becerra. Puedes contactar al autor en nayleth_alexandra@hotmail.com
Puedes acceder al documento completo de esta investigación a través del siguiente enlace: https://noesis.uis.edu.co/handle/20.500.14071/14313
