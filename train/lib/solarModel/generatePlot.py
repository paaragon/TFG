import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":

    df = pd.read_csv('../../data/csvWithCondition/2015010120150131.csv')
    radiacion = list()

    horas = df['hora'].unique()
    for hora in horas:
        radiacion.append(df[df['hora'] == hora]['radiacion'].mean())

    plt.plot(horas, radiacion)
    plt.show()
