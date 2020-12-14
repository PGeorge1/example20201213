from flask import Flask, render_template, send_from_directory, send_file
import time
import seaborn as sns
import pandas as pd

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_data():
    return send_file("data/titanic_train.csv", as_attachment=True)

links = {"Download" : "/download",
         "Pairplot" : "/pairplot",
         "Fair vs Pclass"  : "fair_vs_pclass",
         "PClass vs Sex" : "pclass_vs_sex"}

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", links=links, image = None, code=time.time())

@app.route('/pairplot', methods=['GET'])
def pairplot():

    data = pd.read_csv ("data/titanic_train.csv")
    sns_plot = sns.pairplot(data[["Age", "Fare", "Survived"]], hue="Survived")
    sns_plot.savefig("static/tmp/pairplot.png")
    return render_template("index.html", links=links, image = ("pairplot.png", "pairplot"), code=time.time())

@app.route('/fair_vs_pclass', methods=['GET'])
def fair_vs_pclass():
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    data = pd.read_csv ("data/titanic_train.csv")
    filtered_data = data.query('Fare < 200')
    sns.boxplot(x='Pclass', y='Fare', data=filtered_data, ax=ax)
    plt.savefig('static/tmp/fair_vs_pclass.png')

    return render_template("index.html", links=links, image = ("fair_vs_pclass.png", "Fair vs Pclass"), code=time.time())

@app.route('/pclass_vs_sex', methods=['GET'])
def pclass_vs_sex():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    data = pd.read_csv ("data/titanic_train.csv")
    result = {}
    for (cl, sex), sub_df in data.groupby(['Pclass', 'Sex']):
        result[f"{cl} {sex}"] = sub_df['Age'].mean()

    plt.bar (result.keys(), result.values())
    plt.savefig('static/tmp/pclass_vs_sex.png')
    return render_template("index.html", links=links, image = ("pclass_vs_sex.png", ""), code=time.time())

if __name__ == '__main__':
    app.run(host="localhost", port=8888)