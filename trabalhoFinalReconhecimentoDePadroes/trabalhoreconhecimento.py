# -*- coding: utf-8 -*-
"""trabalhoReconhecimento.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1E3E1QQOM_4WSeVMEHLK69ARc8msrs853

# Bibliotecas
"""

## Importando as Bibliotecas Necessárias ##
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix, ConfusionMatrixDisplay, f1_score, cohen_kappa_score, precision_score, recall_score
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import make_classification
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from numpy.linalg import inv
from copy import copy
from sklearn.metrics import RocCurveDisplay

sns.set()

# Lendo a base de dados
df = pd.read_excel("m.xlsx")

xp = copy(df)

xraw = copy(xp)

xp.shape

"""# Codigo processamento"""

df = copy(xp)
df.isnull().sum()

xp['Arrival Delay in Minutes'] = xp['Arrival Delay in Minutes'].replace(np.nan, 0)

# Contando a quantidade de dados de cada classe
df=xp
contagem_classes = df['Customer Type'].value_counts()

# Plotando o histograma das classes
plt.figure(figsize=(10, 5))
contagem_classes.plot(kind='bar')
plt.xlabel('Customer Type')
plt.ylabel('Número de Amostras')
plt.title('Histograma do Customer Type em Função do Número de Amostras')
plt.xticks(rotation=360)
plt.show()

# Contando a quantidade de dados de cada classe
df=xp
contagem_classes = df['Class'].value_counts()

# Plotando o histograma das classes
plt.figure(figsize=(10, 5))
contagem_classes.plot(kind='bar')
plt.xlabel('Class')
plt.ylabel('Número de Amostras')
plt.title('Histograma da Class em Função do Número de Amostras')
plt.xticks(rotation=360)
plt.show()

# Contando a quantidade de dados de cada classe
df=xp
contagem_classes = df['Type of Travel'].value_counts()

# Plotando o histograma das classes
plt.figure(figsize=(10, 5))
contagem_classes.plot(kind='bar')
plt.xlabel('Type of Travel')
plt.ylabel('Número de Amostras')
plt.title('Histograma do Type of Travel em Função do Número de Amostras')
plt.xticks(rotation=360)
plt.show()

# Contando a quantidade de dados de cada classe
df=xp
contagem_classes = df['satisfaction'].value_counts()

# Plotando o histograma das classes
plt.figure(figsize=(10, 5))
contagem_classes.plot(kind='bar')
plt.xlabel('satisfaction')
plt.ylabel('Número de Amostras')
plt.title('Histograma da satisfaction em Função do Número de Amostras')
plt.xticks(rotation=360)
plt.show()

atributos_numericos = df.select_dtypes(include=['float64', 'int64'])

# Calcula a assimetria para cada atributo numérico
assimetria = atributos_numericos.skew()

# Exibe a assimetria de cada atributo
print(assimetria)

#aplicando histogramas para os atributos contínuos:
def multigraficos_histograma(data, nrows, ncols, nomes):
    fig, axs = plt.subplots(nrows = nrows, ncols = ncols, figsize=(15, 5*nrows))
    k = 0
    for i in range(nrows):
        for j in range(ncols):
            sns.histplot(ax = axs[i,j], data = data, x = nomes[k])
            axs[i, j].set_xlabel(nomes[k])
            axs[i, j].set_ylabel("contagem")
            k+=1
        #
    #
#

nrows = 9
ncols = 2
multigraficos_histograma(df, nrows, ncols, var_num)

# boxplot

var_num = ['Age', 'Flight Distance', 'Inflight wifi service', 'Departure/Arrival time convenient', 'Ease of Online booking',
           'Gate location', 'Food and drink', 'Online boarding', 'Seat comfort', 'Inflight entertainment', 'On-board service',
           'Leg room service', 'Baggage handling', 'Checkin service', 'Inflight service', 'Cleanliness',
           'Departure Delay in Minutes', 'Arrival Delay in Minutes']

nrows = 9
ncols = 2
fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 5*nrows))

for i, var in enumerate(var_num):
    row = i // ncols
    col = i % ncols
    sns.boxplot(ax=axs[row, col], data=df[var].dropna(), orient='h')
    axs[row, col].set_xlabel(var)

plt.tight_layout()

print("Variaveis com outliers: \n")

dsc = df[var_num].describe() #obtendo estatísticas descritivas dos atributos numericos

for name in dsc.columns:
    q1 = dsc[name]["25%"]
    q3 = dsc[name]["75%"]
    iqr = q3-q1

    min_ = q1 - 1.5*iqr
    max_ = q3 + 1.5*iqr

    out_inf = np.where(df[name] < min_)[0]
    out_sup = np.where(df[name] > max_)[0]

    if ((out_inf.shape[0] > 0) or (out_sup.shape[0] > 0)):
        print(name)
    #
#

"""# Classificação Linear"""

df.corr(method='spearman').style.background_gradient(cmap='coolwarm')

df = copy(xp)
leal = df[df['Customer Type'] == 'Loyal Customer'].iloc[:500]
desleal = df[df['Customer Type'] == 'disloyal Customer'].iloc[:500]

df = pd.concat([leal, desleal])

df['Customer Type'] = df['Customer Type'].map({'Loyal Customer': 1, 'disloyal Customer': -1})

df['Age'] = (df['Age'])
df['Flight Distance'] = (df['Flight Distance'])
df['Gate location'] = (df['Gate location'])
df['Food and drink'] = (df['Food and drink'])
df['On-board service'] = (df['On-board service'])
df['Leg room service'] = (df['Leg room service'])
df['Baggage handling'] = (df['Baggage handling'])
df['Checkin service'] = (df['Checkin service'])

X = df[['Age', 'Flight Distance', 'Checkin service', 'Baggage handling', 'Leg room service', 'On-board service', 'Food and drink', 'Gate location']].values
y = df['Customer Type'].values

X = np.concatenate((X, np.ones((X.shape[0], 1))), axis=1)

w = np.dot(inv(np.dot(X.T, X)), np.dot(X.T, y))

w1, w2, w0 = w[0], w[1], w[8]

x_hyperplane = np.linspace(X[:, 0].min(), X[:, 0].max(), 1000)
y_hyperplane = (-w0 - w1 * x_hyperplane) / w2

plt.figure(figsize=(10, 6))
plt.scatter(X[y == 1][:, 0], X[y == 1][:, 1], label='Leal', c='blue')
plt.scatter(X[y == -1][:, 0], X[y == -1][:, 1], label='Desleal', c='red')
plt.plot(x_hyperplane, y_hyperplane, color='green', label='Hiperplano de Separação')
plt.legend()
plt.title('Gráfico de Dispersão com Classificador Linear e Reta de Separação')
plt.grid(True)
plt.show()

"""# Criação dos dados iniciais"""

df = copy(xp)

leal = df[df['Customer Type'] == 'Loyal Customer'].iloc[:12000]
desleal = df[df['Customer Type'] == 'disloyal Customer'].iloc[:12000]

df = pd.concat([leal, desleal])

df['Customer Type'] = df['Customer Type'].map({'Loyal Customer': 1, 'disloyal Customer': -1})
df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})
df['Type of Travel'] = df['Type of Travel'].map({'Business travel': 1, 'Personal Travel': 0})
df['Class'] = df['Class'].map({'Business': 1, 'Eco': -1, 'Eco Plus': 0})
df['satisfaction'] = df['satisfaction'].map({'satisfied': 1, 'neutral or dissatisfied': 0})

df['Flight Distance'] = np.log(df['Flight Distance'])
df['Arrival Delay in Minutes'] = np.log1p(df['Arrival Delay in Minutes'])
df['Age'] = np.sqrt(df['Age'])
df['Departure Delay in Minutes'] = np.log1p(df['Arrival Delay in Minutes'])

df.drop(['id'], axis = 1, inplace = True)
df.drop(['Column1'], axis = 1, inplace = True)
df.drop(['Cleanliness'], axis = 1, inplace = True)
df.drop(['Ease of Online booking'], axis = 1, inplace = True)
df.drop(['Inflight entertainment'], axis = 1, inplace = True)
df.drop(['Arrival Delay in Minutes'], axis = 1, inplace = True)

X = df.drop(['satisfaction'], axis = 1).values
y = df['satisfaction'].values

"""# Classifição Naive-Bayes

"""

#Frequencia:
#    Não     Sim
#0 = 2     = 811  = 813/25976  = 0.0313%
#1 = 2966  = 1522 = 4488/25976 = 0.1727%
#2 = 4923  = 1567 = 6490/25976 = 0.2498%
#3 = 4694  = 1623 = 6317/25976 = 0.2431%
#4 = 1953  = 3028 = 4981/25976 = 0.1917%
#5 = 35    = 2852 = 2887/25976 = 0.1111%
#Total = 14573/25976 = 0.561% | 11403/25976 = 0.439%
#TotalTudo = 25976

#Prob ser insatisfeito e dar 0:
#P0N = 2/14573 PN = 14573/25976 P0 = 813/25976
PN0 = (2/14573) * (0.561)/(0.0313)
PS0 = 1 - PN0
#Prob ser insatisfeito e dar 1:
#P0N = 2/14573 PN = 14573/25976 813/25976
PN1 = (2966/14573) * (0.561)/(0.1727)
PS1 = 1 - PN1
#Prob ser insatisfeito e dar 2:
#P0N = 2/14573 PN = 14573/25976 813/25976
PN2 = (4923/14573) * (0.561)/(0.2498)
PS2 = 1 - PN2
#Prob ser insatisfeito e dar 3:
#P0N = 2/14573 PN = 14573/25976 813/25976
PN3 = (4694/14573) * (0.561)/(0.2431)
PS3 = 1 - PN3
#Prob ser insatisfeito e dar 4:
#P0N = 2/14573 PN = 14573/25976 813/25976
PN4 = (1953/14573) * (0.561)/(0.1917)
PS4 = 1 - PN4
#Prob ser insatisfeito e dar 5:
#P0N = 2/14573 PN = 14573/25976 813/25976
PN5 = (35/14573) * (0.561)/(0.1111)
PS5 = 1/100 - PN5

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=125, stratify = y
)

# Build a Gaussian Classifier
clf = GaussianNB()

# Model training
clf.fit(X_train, y_train)

# Predict Output
predicted = clf.predict([X_test[6]])

print("Actual Value:", y_test[6])
print("Predicted Value:", predicted[0])

y_pred = clf.predict(X_test)
accuray = accuracy_score(y_pred, y_test)
f1 = f1_score(y_pred, y_test, average="weighted")
kappa = cohen_kappa_score(y_pred, y_test)
prec = precision_score(y_pred, y_test)
recal = recall_score(y_pred, y_test)

print("Accuracy:", accuray)
print("F1 Score:", f1)
print("Kappa:", kappa)
print("Precision:", prec)
print("Recall:", recal)

labels = [0,1]
cm = confusion_matrix(y_test, y_pred, labels=labels)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot();

"""# Classificação Árvore de Decisão (simples)"""

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, y.astype(float))
tree.plot_tree(clf,filled=True)
y_pred = clf.predict(X_test)

accuray = accuracy_score(y_pred, y_test)
f1 = f1_score(y_pred, y_test, average="weighted")
kappa = cohen_kappa_score(y_pred, y_test)
prec = precision_score(y_pred, y_test)
recal = recall_score(y_pred, y_test)

print("Accuracy:", accuray)
print("F1 Score:", f1)
print("Kappa:", kappa)
print("Precision:", prec)
print("Recall:", recal)

labels = ["Leal", "Desleal"]
cm = confusion_matrix(y_test, y_pred)
labels = ["Leal", "Desleal"]
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot();

"""# Classificação Rede Neural MLP

"""

clf = MLPClassifier(random_state=1, max_iter=300).fit(X_train, y_train)
clf.predict_proba(X_test[:1])
y_pred = clf.predict(X_test)

accuray = accuracy_score(y_pred, y_test)
f1 = f1_score(y_pred, y_test, average="weighted")
kappa = cohen_kappa_score(y_pred, y_test)
prec = precision_score(y_pred, y_test)
recal = recall_score(y_pred, y_test)

print("Accuracy:", accuray)
print("F1 Score:", f1)
print("Kappa:", kappa)
print("Precision:", prec)
print("Recall:", recal)

labels = ["Leal", "Desleal"]
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot();

"""# Random Florest"""

clf = RandomForestClassifier(n_estimators = 800)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

accuracy = metrics.accuracy_score(y_test, y_pred)
f1 = f1_score(y_pred, y_test, average="weighted")
kappa = cohen_kappa_score(y_pred, y_test)
prec = precision_score(y_pred, y_test)
recal = recall_score(y_pred, y_test)

print("Accuracy:", accuray)
print("F1 Score:", f1)
print("Kappa:", kappa)
print("Precision:", prec)
print("Recall:", recal)

labels = ["Leal", "Desleal"]
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot();

"""# ROC"""

clf = SVC(random_state=0).fit(X_train, y_train)
y_pred = clf.decision_function(X_test)
RocCurveDisplay.from_predictions(y_test, y_pred,name='classe')
plt.show()