from osgeo import gdal
import numpy as np
import argparse
import os
import xlsxwriter
import math


# define los argumentos de entrada del script
parser = argparse.ArgumentParser(description='Calcula el WOE')
# tiene un numero n de argumentos de entrada donde cada entrada es una direccion de archivo
parser.add_argument('--t-maps', metavar='file', type=str, nargs='+',
                    help='Mapas tematicos, deben tener el mismo tamaño y el mismo tamaño de pixel' , required=True)
parser.add_argument('--inv_train', metavar='file', type=str, nargs=1, 
                    help='Inventario de entrenamiento de Procesos morfodinamicos, deben tener el mismo tamaño y el mismo tamaño de pixel', required=True)
parser.add_argument('--inv_test', metavar='file', type=str, nargs=1, 
                    help='Inventario de testeo de Procesos morfodinamicos, deben tener el mismo tamaño y el mismo tamaño de pixel', required=True)
parser.add_argument("--null", metavar='float', type=float, nargs=1,
                    help='Valor nulo de los mapas si este existe, debe ser el mismo para todos, por defecto es -1', default=-1)
parser.add_argument("--out", metavar='dir', type=str, nargs=1, required=True,
                    help='Directorio de salida')
args = parser.parse_args()

# lee los argumentos de entrada
t_maps = args.t_maps
null = args.null[0]
out = args.out
inv_train = args.inv_train[0]
inv_test = args.inv_test[0]

# lee los mapas tematicos
t_maps_ds = []
for t_map in t_maps:
    t_maps_ds.append(gdal.Open(t_map))

# lee el inventario de procesos morfodinamicos
inv_train_ds = gdal.Open(inv_train)
inv_test_ds = gdal.Open(inv_test)




# crea una matriz para guardar las dimensiones de los mapas tematicos
t_maps_shape = np.zeros((len(t_maps_ds), 2), dtype=int)

# obten las dimensiones de todos los raster de t_maps e imprime las dimensiones
for t_map_ds in t_maps_ds:
    t_map_ds_band = t_map_ds.GetRasterBand(1)
    t_map_ds_band_array = t_map_ds_band.ReadAsArray()
    # imprime las dimensiones de la matriz de cada raster de t_maps con su nombre
    #print(t_map_ds.GetDescription(), t_map_ds_band_array.shape)
    # guarda las dimensiones de la matriz de cada raster de t_maps
    t_maps_shape[t_maps_ds.index(t_map_ds), 0] = t_map_ds_band_array.shape[0]
    t_maps_shape[t_maps_ds.index(t_map_ds), 1] = t_map_ds_band_array.shape[1]

# obtiene las dimensiones del raster de inv train
inv_train_ds_band = inv_train_ds.GetRasterBand(1)
inv_train_ds_band_array = inv_train_ds_band.ReadAsArray()
# imprime las dimensiones de la matriz de inv
#print(inv_ds.GetDescription(), inv_ds_band_array.shape)

# guarda las dimensiones de la matriz de inv train en t_maps_shape usando append
t_maps_shape = np.append(t_maps_shape, np.array([[inv_train_ds_band_array.shape[0], inv_train_ds_band_array.shape[1]]]), axis=0)

# obtiene las dimensiones del raster de inv test
inv_test_ds_band = inv_test_ds.GetRasterBand(1)
inv_test_ds_band_array = inv_test_ds_band.ReadAsArray()

# guarda las dimensiones de la matriz de inv test en t_maps_shape usando append
t_maps_shape = np.append(t_maps_shape, np.array([[inv_test_ds_band_array.shape[0], inv_test_ds_band_array.shape[1]]]), axis=0)

# valida que todas las matrices tengan las mismas dimensiones y el mismo tamaño de pixel
# si no es asi, termina el script
# si es asi, solo continua
if np.all(t_maps_shape == t_maps_shape[0]):
    print("Las dimensiones de los mapas son iguales")
else:
    print("Las dimensiones de los mapas no son iguales")
    exit()

# crea una matriz con las dimensiones de los mapas llamada null_matrix con el valor de 1
null_matrix_train = np.ones((t_maps_shape[0, 0], t_maps_shape[0, 1]))

# crea una matriz llamada clases de dimension (10,numero de mapas tematicos,1) con el valor de null
clases = np.full((10, len(t_maps_ds), 1), null, dtype=float)
#print(clases)

# por cada mapa tematico detectar las clases y guardarlas en la matriz clases
for t_map_ds in t_maps_ds:
    t_map_ds_band = t_map_ds.GetRasterBand(1)
    t_map_ds_band_array = t_map_ds_band.ReadAsArray()
    #cambia todos los nan por null
    t_map_ds_band_array[np.isnan(t_map_ds_band_array)] = null
    #recorre la matriz de cada raster de t_maps
    for i in range(t_map_ds_band_array.shape[0]):
        for j in range(t_map_ds_band_array.shape[1]):
            # si el valor de la matriz es diferente de null
            if t_map_ds_band_array[i, j] != null:
                # si el valor de la matriz no esta en la matriz clases
                if t_map_ds_band_array[i, j] not in clases[0, t_maps_ds.index(t_map_ds), :]:
                    # validar que la matriz clases tiene algun null
                    if null in clases[0, t_maps_ds.index(t_map_ds), :]:
                        # si la matriz clases tiene algun null, reemplazar el primer null por el valor de la matriz
                        clases[0, t_maps_ds.index(t_map_ds), np.where(clases[0, t_maps_ds.index(t_map_ds), :] == null)[0][0]] = t_map_ds_band_array[i, j]
                        #print("------------------")
                        #print(clases)
                    # si la matriz clases no tiene null, agregar el valor de la matriz a la matriz clases
                    else:
                        clases = np.insert(clases, clases.shape[2], null, axis=2)
                        clases[0, t_maps_ds.index(t_map_ds), np.where(clases[0, t_maps_ds.index(t_map_ds), :] == null)[0][0]] = t_map_ds_band_array[i, j]
                        #print("------------------")
                        #print(clases)
                    
            # si el valor de la matriz es igual a null
            else:
                # agrega null a la matriz null_matrix
                null_matrix_train[i, j] = null

#print("------------------")
#print(clases)

null_matrix_test = null_matrix_train.copy()

null_matrix_total = null_matrix_train.copy()

null_matrix_train[inv_train_ds_band_array == null] = null

null_matrix_test[inv_test_ds_band_array == null] = null

# aplica los valores de null_matrix a inv_ds_90
inv_train_ds_band_array[null_matrix_train == null] = null

# aplica los valores de null_matrix a inv_ds_90
inv_test_ds_band_array[null_matrix_test == null] = null


# crea una variable llamda nmap que es una matriz booleana con True donde los valores son iguales a 1 en la null matriz y False en caso contrario
nmap = np.count_nonzero(null_matrix_train == 1)

#print("nmap", nmap)

# cuenta el numero de posiciones por clase en cada mapa tematico y que estas posiciones no sean null em la matriz null_matrix
for t_map_ds in t_maps_ds:
    t_map_ds_band = t_map_ds.GetRasterBand(1)
    t_map_ds_band_array = t_map_ds_band.ReadAsArray()
    t_map_ds_band_array[np.isnan(t_map_ds_band_array)] = null
    for clase in clases[0, t_maps_ds.index(t_map_ds), :]:
        if clase == np.nan:
            continue
        if clase != null:
            index = t_maps_ds.index(t_map_ds)
            clases[1, index, np.where(clases[0, index, :] == clase)[0][0]] = np.count_nonzero((null_matrix_train == 1) & (t_map_ds_band_array == clase))
            #print("------------------")
            #print(clases)


# cuenta el numero de 1 en la matriz inv_ds_band_array y que estas posiciones no sean null em la matriz null_matrix y guardarlo en la variable nslide
nslide = np.count_nonzero((null_matrix_train == 1) & (inv_train_ds_band_array == 1))
#print("nslide", nslide)

# cuenta el numero de posiciones por clase en cada mapa tematico y que estas posiciones no sean null em la matriz null_matrix
# y sean iguales a 1 en la matriz inv_ds_band_array
for t_map_ds in t_maps_ds:
    t_map_ds_band = t_map_ds.GetRasterBand(1)
    t_map_ds_band_array = t_map_ds_band.ReadAsArray()
    t_map_ds_band_array[np.isnan(t_map_ds_band_array)] = null
    for clase in clases[0, t_maps_ds.index(t_map_ds), :]:
        if clase != null:
            clases[2, t_maps_ds.index(t_map_ds), np.where(clases[0, t_maps_ds.index(t_map_ds), :] == clase)[0][0]] = np.count_nonzero((null_matrix_train == 1) & (t_map_ds_band_array == clase) & (inv_train_ds_band_array == 1))
            #print("------------------")
            #print(clases)


# a partir de la segunda posicion de la matriz clases y cuenta el numero de veces que suma uno
for i in range(1, clases.shape[0]):
    for j in range(clases.shape[1]):
        for k in range(clases.shape[2]):
            if clases[i, j, k] != null:
                clases[i, j, k] += 1
                

#print("------------------")
#print(clases)


# por cada clase en la matriz clases donde el valor de la matriz clases sea diferente de null
# clase(3,:,:) = npix1
# clase(4,:,:) = npix2
# clase(5,:,:) = npix3
# clase(6,:,:) = npix4
# npix1 = clase(2,:,:)
# npix2 = nslide - clase(2,:,:)
# npix3 = clase(1,:,:) - clase(2,:,:)
# npix4 = nmap - nslide - clase(1,:,:) + clase(2,:,:)
# clase(7,:,:) = ln((npix1*(npix3+npix4))/((npix1+npix2)*npix3))
# clase(8,:,:) = ln((npix2*(npix3+npix4))/((npix1+npix2)*npix4))
# clase(9,:,:) = clase(7,:,:) - clase(8,:,:)
for i in range(clases.shape[1]):
    for j in range(clases.shape[2]):
        if clases[0, i, j] != null:
            #agrega a m el numero de clases en la posicion 1 que no son null
            m = np.count_nonzero(clases[1, i, :] != null)
            npix1 = (clases[2, i, j])
            npix2 = (nslide+m) - (clases[2, i, j])
            npix3 = clases[1, i, j] - clases[2, i, j]
            npix4 = (nmap+m) - (nslide+m) - clases[1, i, j] + clases[2, i, j]
            clases[3, i, j] = npix1
            clases[4, i, j] = npix2
            clases[5, i, j] = npix3
            clases[6, i, j] = npix4
            clases[7, i, j] = np.log((npix1*(npix3+npix4))/((npix1+npix2)*npix3))
            clases[8, i, j] = np.log((npix2*(npix3+npix4))/((npix1+npix2)*npix4))
            clases[9, i, j] = clases[7, i, j] - clases[8, i, j]

#print("------------------")
#print(clases)

# crear un mapa con las dimensiones de los mapa tematicos e inicializarlo con null
# por cada celda donde sea diferente de null en la matriz null_matrix

n_null = np.min(clases[9, :, :]) - 9999

n_map = np.full((t_maps_ds[0].RasterYSize, t_maps_ds[0].RasterXSize), n_null, dtype=float)

# coloca los valores de n_map donde no sea null en la matriz null_matrix en 0
n_map[null_matrix_total != null] = 0


for t_map_ds in t_maps_ds:
    t_map_ds_band = t_map_ds.GetRasterBand(1)
    t_map_ds_band_array = t_map_ds_band.ReadAsArray()
    t_map_ds_band_array[np.isnan(t_map_ds_band_array)] = null
    for i in range(t_map_ds_band_array.shape[0]):
        for j in range(t_map_ds_band_array.shape[1]):
            if null_matrix_total[i, j] != null:
                n_map[i, j] += clases[9, t_maps_ds.index(t_map_ds), np.where(clases[0, t_maps_ds.index(t_map_ds), :] == t_map_ds_band_array[i, j])[0][0]]

# convierte n_map en un mapa tematico
n_map_ds = gdal.GetDriverByName('GTiff').Create(out[0]+'n_map.tif', t_maps_ds[0].RasterXSize, t_maps_ds[0].RasterYSize, 1, gdal.GDT_Float32)
n_map_ds.SetGeoTransform(t_maps_ds[0].GetGeoTransform())
n_map_ds.SetProjection(t_maps_ds[0].GetProjection())
n_map_ds.GetRasterBand(1).WriteArray(n_map)
n_map_ds.GetRasterBand(1).SetNoDataValue(n_null)
# guarda el mapa tematico
n_map_ds = None

#

#wt = np.full((clases.shape[1]), null, dtype=float)
#for i in range(clases.shape[1]):
#    wt[i] = np.sum(clases[9, i, :], where=clases[0, i, :] != null)

#print("------------------")
#print(wt)

for i in [1,2]:
    for j in range(clases.shape[1]):
        for k in range(clases.shape[2]):
            if clases[i, j, k] != null:
                clases[i, j, k] -= 1

# adiciona add a las variables nmap, nslide
# crea un archivo de excel con el nombre de out_excel
# y crea una hoja de calculo por cada mapa tematico
# y crea una columna por la profundidad de la matriz clases
# y crea una fila por cada valor diferente de null en la posicion 0 de la matriz clases
# y asigna a cada celda el valor de la matriz clases en la posicion 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
# y asigna a la celda A1 el valor de la variable nmap
# y asigna a la celda A2 el valor de la variable nslide

out_excel = out[0]+ "out_excel.xlsx"
workbook = xlsxwriter.Workbook(out_excel,{'nan_inf_to_errors': True})
for i in range(clases.shape[1]):
    #obten el nombre del archivo de cada mapa tematico separando por / o \ y obteniendo el ultimo valor
    map_name = t_maps[i].split("/")[-1].split("\\")[-1]
    
    # truncar a menos de 25 caracteres
    map_name = map_name[:25]
    worksheet = workbook.add_worksheet(map_name)
    worksheet.write(0, 0, "pixeles en el mapa")
    worksheet.write(0, 1, "pixeles con deslizamiento")
    worksheet.write(1, 0, nmap)
    worksheet.write(1, 1, nslide)
    worksheet.write(2, 0, "clase")
    worksheet.write(2, 1, "pixeles")
    worksheet.write(2, 2, "pixeles con deslizamiento")
    worksheet.write(2, 3, "npix1")
    worksheet.write(2, 4, "npix2")
    worksheet.write(2, 5, "npix3")
    worksheet.write(2, 6, "npix4")
    worksheet.write(2, 7, "W+")
    worksheet.write(2, 8, "W-")
    worksheet.write(2, 9, "Wf")
    for j in range(clases.shape[2]):
        if clases[0, i, j] != null:
            worksheet.write(j+3, 0, clases[0, i, j])
            worksheet.write(j+3, 1, clases[1, i, j])
            worksheet.write(j+3, 2, clases[2, i, j])
            worksheet.write(j+3, 3, clases[3, i, j])
            worksheet.write(j+3, 4, clases[4, i, j])
            worksheet.write(j+3, 5, clases[5, i, j])
            worksheet.write(j+3, 6, clases[6, i, j])
            worksheet.write(j+3, 7, clases[7, i, j])
            worksheet.write(j+3, 8, clases[8, i, j])
            worksheet.write(j+3, 9, clases[9, i, j])
workbook.close()

#guarda el archivo de excel
print("Proceso finalizado")
