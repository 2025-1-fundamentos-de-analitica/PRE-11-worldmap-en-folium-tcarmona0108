import os
import matplotlib.pyplot as plt  # type: ignore
import pandas as pd              # type: ignore

def load_affiliations():
    return pd.read_csv(
        "https://raw.githubusercontent.com/jdvelasq/datalabs/"
        "master/datasets/scopus-papers.csv",
        usecols=["Affiliations"]
    )

def remove_na_rows(affiliations):
    return affiliations.dropna(subset=["Affiliations"]).copy()

def create_countries_column(affiliations):
    aff = affiliations.copy()
    aff["countries"] = (
        aff["Affiliations"]
        .str.split(";")
        .map(lambda lst: [s.strip().split(",")[-1] for s in lst])
        .map(set)
        .map(sorted)
        .str.join(", ")
    )
    return aff

def count_country_frequency(affiliations):
    freq = (
        affiliations["countries"]
        .str.split(", ")
        .explode()
        .value_counts()
    )
    return freq

def make_plot(n_countries):
    # 1) Asegura carpeta
    os.makedirs("files", exist_ok=True)

    # 2) Prepara datos
    aff = load_affiliations()
    aff = remove_na_rows(aff)
    aff = create_countries_column(aff)
    freq = count_country_frequency(aff)

    # 3) Guarda completo (opcional)
    freq.to_csv("files/countries.csv")

    # 4) Filtra top-N y grafica
    top_n = freq.head(n_countries)
    plt.figure(figsize=(10, 6))
    top_n.plot(kind="bar")
    plt.title(f"Top {n_countries} países por frecuencia")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    # 5) Devuelve el top-N si quieres usarlo luego
    return top_n

if __name__ == "__main__":
    top20 = make_plot(n_countries=20)
