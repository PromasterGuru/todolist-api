# todolist/test_views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework import generics


# Create your views here.
class HomeView(generics.ListAPIView):
    def get(self, request, **kwargs):
        # return render(request, 'index.html', context=None)
        #Query to fetch all counties from the DB

        return Response({"profile": {"username": "Paul", "age": 46, "gender": "Male"}})


class AboutView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'about.html', context=None)
