# this files reads the database and build the corresponding files !

import pandas as pd
import os
import yaml

CONTENT_PATH = 'content/sections/'

def normalize(s):
  s = s.replace('é', 'e').replace('è', 'e').replace('ê', 'e').replace('à', 'a')
  s = s.lower().replace(' ', '_').replace('.', '').replace(',','').replace('?', '')
  return s

def build_path(path):
  # ex: "Sciences humaines / Histoire / Histoire de la médecine"
  f_names = path.split(' / ')
  folders = [normalize(s) for s in f_names]
  for i in range(len(folders)):
    foldi = os.path.join(CONTENT_PATH, *folders[:i+1])
    if not os.path.exists(foldi):
      os.mkdir(foldi)
      with open(foldi+'/_index.fr.md', 'w') as f:
        f.write(f'---\ntype: "playlist"\ntitle: "{f_names[i]}"\n---\n\n')
  # returns file where you want to add video
  return os.path.join(CONTENT_PATH, *folders, '_index.fr.md')

# STEP 1: build channels files
channel_db = pd.read_csv('webdata/chaines.csv', delimiter=',', encoding='utf-8')
thumbnails = {val.nom: val.thumbnail for key, val in channel_db.iterrows()}
langs = {val.nom: val.lang for key, val in channel_db.iterrows()}
topics = {val.nom: val.topic for key, val in channel_db.iterrows()}
with open('data/chanlogos.yaml', 'w') as outfile:
    yaml.dump(thumbnails, outfile, default_flow_style=False, allow_unicode=True)
with open('data/chanlangs.yaml', 'w') as outfile:
    yaml.dump(langs, outfile, default_flow_style=False, allow_unicode=True)

# build channels list file
chan_list = {top: [c for c, t in topics.items() if t==top] for top in set(topics.values())}
with open('content/about/_index.fr.md', 'w') as f:
  _ = f.write('---\ndisableToc: "true"\ntype: "page"\ntitle: "Liste des chaînes"\n---\n&nbsp;\n&nbsp;\n\n\n')
  for key, val in sorted(chan_list.items()):
    _ = f.write('#### '+key+'\n')
    for v in val:
      _ = f.write('{{< chan "'+v+'" >}}\n')

#STEP 2: build video files

# load databases
db1 = pd.read_csv('webdata/database1.csv', delimiter=',', encoding='utf-8')
db2 = pd.read_csv('webdata/database2.csv', delimiter=',', encoding='utf-8')

# optional: build file (useless for now)
#videos = {}
#for db in (db1, db2):
#  for key, val in db.iterrows():
#    desc = val.description.replace('\n', '<br>') if not pd.isnull(val.description) else ""
#    videos[val.videoID] = {'channel': val.channel, 'abstract':val.abstract, 
#    'desc': desc}
#with open('data/videos.yml', 'w') as outfile:
#    yaml.dump(videos, outfile, default_flow_style=False, allow_unicode=True)


for db in (db1, db2):
  for key, val in db.iterrows():
    # get good file path
    if val.publish == 'yes' and not pd.isnull(val.videoID):
      for cat in (val.category, val.cat2, val.cat3):
        if not pd.isnull(cat):
          path = build_path(cat)
          with open(path, 'a') as f:
            _ = f.write("\n{{< yt ")
            try:
              desc = val.description.replace('\n', '<br>').replace('"', '')
            except:
              desc = ""
            abst = val.abstract if not pd.isnull(val.abstract) else ""
            _ = f.write(f'"{val.channel}" {val.videoID} "{abst}" "{desc}"')
            _ = f.write(" >}}\n")

