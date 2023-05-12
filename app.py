from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd 
import geopandas 
import os 
import contextily 
import matplotlib.pyplot as plt

regioni = geopandas.read_file("Regioni/Reg01012023_g_WGS84.dbf")
regioni3857 = regioni.to_crs(3857)
provincie = geopandas.read_file("Province/ProvCM01012023_g_WGS84.dbf")
provincie3857 = provincie.to_crs(3857)
comuni = geopandas.read_file("Comuni/Com01012023_g_WGS84.dbf")
comuni3857 = comuni.to_crs(3857)

@app.route('/')
def home():
    provi = list(provincie3857["DEN_UTS"])
    provi.sort()
    return render_template("home.html",lista = provi)

@app.route('/esercizio1', methods = ["GET"])
def esercizio():
    provinciaInput = request.args.get("provinciaInput")
    prov = provincie3857[provincie3857["DEN_UTS"]== provinciaInput]
    ax = prov.plot(edgecolor =  "red", facecolor = "None",figsize=(12,6),markersize = 5)
    contextily.add_basemap(ax)
    dir = "static/images"
    file_name = "es1.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("esercizio1.html")

@app.route('/esercizio2', methods = ["GET"])
def esercizio2():
    provinciaInput2 = request.args.get("provinciaInput2")
    prov = provincie3857[provincie3857["DEN_UTS"]== provinciaInput2]
    table = comuni3857[comuni3857.within(prov.geometry.item())]
    tabella = table.to_html()
    return render_template("esercizio2.html",tabella = tabella)


@app.route('/esercizio3', methods = ["GET"])
def esercizio3():
    provinciaInput3 = request.args.get("provinciaInput3")
    prov = provincie3857[provincie3857["DEN_UTS"]== provinciaInput3]
    comuni_provinciaselezionata = comuni3857[comuni3857.within(prov.geometry.item())]
    table = comuni_provinciaselezionata.sort_values(by = "COMUNE")[["COMUNE"]]
    tabella = table.to_html()
    return render_template("esercizio3.html",tabella = tabella)

@app.route('/esercizio4', methods = ["GET"])
def esercizio4():
    provinciaInput4 = request.args.get("provinciaInput4")
    prov = provincie3857[provincie3857["DEN_UTS"]== provinciaInput4]
    comuni_provinciaselezionata = comuni3857[comuni3857.within(prov.geometry.item())]
    dizionario = dict(zip(comuni_provinciaselezionata["COMUNE"], comuni_provinciaselezionata["Shape_Area"]))
    return render_template("esercizio4.html",tabella = dizionario)

@app.route('/esercizio5', methods = ["GET"])
def esercizio5():
        def conversione(kmq):
            miglia = kmq * 0.386102
            return miglia
        risultato = conversione(10)
        return render_template("esercizio5.html",tabella = risultato)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)