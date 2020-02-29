from multiprocessing import Process
import numpy as np
import requests
import pickle
import os


def downloadImage(gen, links):
    for link in links:
        content = requests.get(link[1]).content
        try:
            os.makedirs(gen)
        except FileExistsError:
            pass
        with open(gen+'/'+link[0].replace('File:', ''), 'wb') as handler:
            handler.write(content)


def main():
    gen = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
    for i in range(8):
        p = Process(target=downloadImage, args=[
                    f'Generation {i+1}', pickle.load(open(f'Generation {gen[i]}', 'rb'))])
        p.start()


if __name__ == '__main__':
    main()
