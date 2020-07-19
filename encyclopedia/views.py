from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
import markdown2
import random
from . import util

class NewSearchForm(forms.Form):
    """
        Form to search (in the sidebar)
    """
    title = forms.CharField()

class NewCreateForm(forms.Form):
    """
        Form to create a new page
    """
    title = forms.CharField()
    content = forms.CharField(required=True, widget=forms.Textarea())

class NewEditForm(forms.Form):
    """
        Form to edit a page
    """
    content = forms.CharField(required=True, widget=forms.Textarea())


def index(request):
    if request.method == "GET":
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": NewSearchForm()
        })
    else:
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["title"].capitalize()
            data = util.get_entry(search)
            if data != None:
                return HttpResponseRedirect("/wiki/"+search)
            else:
                my_list = []
                list_data = util.list_entries()
                for item in list_data:
                    if search in item:
                        my_list.append(item)
                return render(request, "encyclopedia/index.html", {
                    "entries": my_list,
                    "form": NewSearchForm()
                })

def myWiki(request, name):
    """
        Display the content of an entry
    """

    new_entry = util.get_entry(name)
    name = name.capitalize()
    if new_entry == None:
        return render(request, "encyclopedia/error404.html")
    else:
        new_entry = markdown2.markdown(new_entry)
        return render(request, "encyclopedia/content.html", {
            "content": new_entry,
            "name": name,
            "form": NewSearchForm()
        })

def create(request):
    """
        Create a new entry
    """
    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
                    "form": NewSearchForm(),
                    "create_form": NewCreateForm(),

                })
    else:
        form = NewCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].capitalize()
            data = util.get_entry(title)
            if data == None:
                content = form.cleaned_data['content']
                util.save_entry(title, content)
                return HttpResponseRedirect("/wiki/"+title)  
            else:
                return render(request, "encyclopedia/create.html",{
                    "form": NewSearchForm(),
                    "create_form": NewCreateForm(request.POST),
                    "error": "That wiki already exists"
                })

def edit(request, title):
    """ 
        Edit an entry
    """
    if request.method == "GET":
        title = title.capitalize()
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
                    "form": NewSearchForm(),
                    "edit_form": NewEditForm(initial={'content': content}),
                    "name": title
                })
    else:
        form = NewEditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            title = title.capitalize()
            util.save_entry(title, content)
            return HttpResponseRedirect('/wiki/'+title)  

def random_wiki(request):
    """
        Pick a random entry
    """
    my_list = util.list_entries()
    title = random.choice(my_list)
    return HttpResponseRedirect('/wiki/' + title)
