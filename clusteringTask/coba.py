def Initiate_Centroid(df,x,y,k):
  random.seed(10)
  centroids = {i + 1 : [random.choices(df[x]),random.choices(df[y])] for i in range(k)}
  return centroids

def Calc_Dist(df,x,y,centroid):
  for i in centroid.keys():
    #menambahkan kolom i(1,2,..,n) yaitu jarak antara objek x dan y dengan masing masing centroid
    df[str(i)] = np.sqrt((df[x] - centroid[i][0]) ** 2 + (df[y] - centroid[i][1]) ** 2) 
  return df #jarak antara (umur, premi)[i] dg centroid

def df_membership(df,centroid):
  '''menambahkan kolom 'index cluster' yang berisi nilai MINIMUM dari masing-masing jarak 
  atribut dengan centroid. Contoh pada baris pertama, atribut Umur dan Premi 
  memiliki jarak paling dekat dengan centroid 1 sehingga index cluster nya adalah 1'''
  df['index cluster'] = (df.loc[:, ['{}'.format(i) for i in centroid.keys()]].idxmin(axis=1)).astype('int') 
  
  '''menambahkan kolom 'color' yang nantinya akan berguna untuk visualisasi data agar 
  tiap2 kluster objek memiliki warna yg seragam'''
  df['color'] = df['index cluster'].map(lambda x: colmap[x])
  return df

def rearrange_centroid(df,centroid):
  for i in centroid.keys():
    centroid[i][0] = np.mean(df[df['index cluster'] == i][x])
    centroid[i][1] = np.mean(df[df['index cluster'] == i][y])
  return centroid


def clusterisasi(df,x,y,k):
  centroid = Initiate_Centroid(df,x,y,k)
  df2 = copy.deepcopy(df)
  df2 = Calc_Dist(df2,x,y,centroid)
  df2 = df_membership(df2,centroid)
  centroid = rearrange_centroid(df2,centroid)
  while (True):
    oldcentroid = copy.deepcopy(centroid)
    df2 = Calc_Dist(df2,x,y,centroid)
    df2 = df_membership(df2,centroid)
    centroid = rearrange_centroid(df2,centroid)
    if (oldcentroid == centroid):
      break
  return (df2,centroid)