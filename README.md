<h1 style="color: red;">Landslide-susceptibility-WOE</h1>
# Landslide-susceptibility-WOE 	

This Python script generates a landslide susceptibility model using weights of evidence. As input, the script requires the following variables:

- Output path
- Path of each of the thematic maps
- Path of the map with the sample inventory of morphodynamic processes to be used for training.
- Null value or no data value

## The script will generate the following:

- The Landslide Susceptibility Index (LSI) map in TIFF format.
- An Excel file with a spreadsheet for each thematic map, indicating the necessary calculated variables and the weights assigned to each class of each thematic map.

## Installation:
To use the script, it is necessary to have Python and some additional libraries (numpy, os, xlsxwriter, osgeo, pandas, argparse. ) installed.

## Authorship:
This project was created by Nayleth Alexandra Rojas Becerra. You can contact the author at nayleth_alexandra@hotmail.com

# Modelo de susceptibilidad a deslizamientos con pesos de evidencia 
Este script de Python genera un modelo de susceptibilidad a deslizamientos utilizando pesos de evidencia. Como entrada, el script requiere las siguientes variables:

- Ruta de salida
- Ruta de cada uno de los mapas temáticos
- Ruta del mapa con la muestra del inventario de procesos morfodinámicos que se utilizará para el entrenamiento
- Valor nulo o valor de no dato

## El script generará lo siguiente:

- El mapa de Índice de Susceptibilidad a Deslizamientos (LSI) en formato TIFF
- Un archivo de Excel con una hoja de cálculo por cada mapa temático, que indica las variables calculadas necesarias y los pesos asignados a cada clase de cada mapa temático.

## Instalación:
Para utilizar el script, es necesario tener instalado Python y algunas librerías adicionales (numpy, os, xlsxwriter, osgeo, pandas, argparse)

## Autoría:
Este proyecto fue creado por Nayleth Alexandra Rojas Becerra. Puedes contactar al autor en nayleth_alexandra@hotmail.com
