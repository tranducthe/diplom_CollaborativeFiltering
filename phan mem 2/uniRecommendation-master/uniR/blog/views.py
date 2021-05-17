from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import os
import pickle
import random
import pandas as pd

def models(request):
    filename=os.path.dirname(os.path.abspath(__file__))+'/unis_pickle'
    with open(filename,'rb') as f:
        model=pickle.load(f)
    return model

def home(request):
    model=models(request)
    uni=[]
    s=model.index.size
    for i in range(21):
        r=random.randint(1,s)
        uni.append(model.index[r])
    return render(request,'home.html',{'unis':uni})

def detail(request):
    model=models(request)
    uni=request.GET['uni']
    if uni in model.index:
        return render(request,'detail.html',{'uni':uni})
    else:
        return render(request,'detail.html',{'uni':uni,'message':'uni Not found'})


def get_similar(request,uni_name,rating):
    model=models(request)
    similar_ratings = model[uni_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings

def recommend_uni(request,uni_collection):
    similar_unis = pd.DataFrame()
    for uni,rating in uni_collection:
        similar_unis = similar_unis.append(get_similar(request,uni,rating),ignore_index = True)
    unis=similar_unis.sum().sort_values(ascending=False).head(10).index
    return unis
    
def recommendation(request):
    uni_name=request.GET['uni']
    rating=request.GET['ratings']
    uni_collection=[]
    uni_collection.append((uni_name,int(rating)))
    unis=recommend_uni(request,uni_collection)
    return render(request,'recommendation.html',{'uniss':unis,'m':uni_name})
