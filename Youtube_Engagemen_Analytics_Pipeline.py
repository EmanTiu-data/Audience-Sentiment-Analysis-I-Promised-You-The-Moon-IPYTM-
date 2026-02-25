from googleapiclient.discovery import build
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

API_KEY = 'AIzaSyDc8b5hJrpoSvoBA2G1lhvQLBnO0c6YLzQ'
Youtube = build('youtube', 'v3', developerKey=API_KEY)
call = Youtube.search().list(
    q = 'PP Krit clips',
    part = 'snippet',
    type = 'video',
    order = 'viewCount',
    maxResults = 10
)
response = call.execute()
datos = []
for video in response['items']:
    titulo = video['snippet']['title']
    video_id = video['id']['videoId']
    try:
        stats_request = Youtube.videos().list(
            part = 'statistics',
            id = video_id
            )
        stats_response = stats_request.execute()
        stats = stats_response['items'][0]['statistics']
        vistas = int(stats.get('viewCount', 0))
        likes = int(stats.get('likeCount', 0))
        comentarios = int(stats.get('commentCount', 0))
        if vistas > 0:
            engagement = ((likes + comentarios)/vistas) * 100
        else:
            engagement = 0
        datos.append({
            'Titulo': titulo,
            'Vista': vistas,
            'Likes': likes,
            'Comentarios':comentarios,
            'Engagement': round(engagement, 2)
            })
    except Exception as e:
        print(f'Error: {e}')
df = pd.DataFrame(datos)
df.to_csv('metrics_pp_Krit.csv', index=False) 
df = pd.read_csv('metrics_pp_Krit.csv')
df = df.sort_values('Engagement', ascending=False)
print(df)
colores = plt.cm.magma(np.linspace(0.4, 0.8, len(df)))
plt.figure(figsize=(10, 6))
plt.barh(df['Titulo'], df['Engagement'], color=colores)
plt.xlabel('Tasa de Engagement (%)')
plt.title('Analises de engagement: Clips de PP Krit', fontsize=14)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(' Grafica_engagement_ppKrit.png')
print('\n Grafica generada')
plt.show()