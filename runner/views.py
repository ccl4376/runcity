# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from .models import *
from .forms import *
#from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
import datetime
from haystack.query import SearchQuerySet


def index(request):
    # this is your new view
    RunHere = Runone.objects.order_by('-created')
    paginator = Paginator(RunHere, 5) # 5 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'page': page, 'posts': posts})


def RunHere_detail(request, slug):
# grab the object...
    RunHere = Runone.objects.get(slug=slug)
    uploads = RunHere.uploads.all()

    comments = RunHere.comments.filter(active=True)
    if request.method == 'POST':

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)

            new_comment.post = RunHere
            # Save the comment to the database
            new_comment.user = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()

# and pass to the template
    return render(request, 'RunDate/RunHere_detail.html', { 'RunHere': RunHere,
                                                            'uploads': uploads,
                                                            'comments': comments,
                                                            'comment_form': comment_form
                                                            })


def create_RunDate(request):
    form_class = RunoneForm
# if we're coming from a submitted form, do this
    if request.method == 'POST':
# grab the data from the submitted form and apply to # the form
        form = form_class(request.POST,request.FILES)
        if form.is_valid():
# create an instance but do not save yet
            RunHere = form.save(commit=False)
# set the additional details
            RunHere.user = request.user
            RunHere.slug = RunHere.name
# save the object
            RunHere.save()
# redirect to our newly created thing
            return redirect('RunHere_detail', slug=RunHere.slug)
# otherwise just create the form
    else:
        form = form_class()
    return render(request, 'RunDate/create_RunDate.html', { 'form': form,})


@login_required
def edit_RunDate(request, slug):
# grab the object...
    RunHere = Runone.objects.get(slug=slug)
    # if thing.user != request.user:
    #     raise Http404
# set the form we're using...
    form_class = RunoneForm
    if request.method == 'POST':
# grab the data from the submitted form
        form = form_class(data=request.POST,files=request.FILES,instance=RunHere)

        if form.is_valid():

            form.save()
            form = form.save(commit=False)
            form.useredit = request.user.username

            form.save()
            return redirect('RunHere_detail', slug=RunHere.slug)
# otherwise just create the form
    else:
        form = form_class(instance=RunHere)
# and render the template
    return render(request, 'RunDate/edit_RunDate.html', {
        'RunHere': RunHere,
        'form': form,
    })


@login_required
def edit_RunDate_uploads(request, slug):
# grab the object...
    RunHere = Runone.objects.get(slug=slug)
# double checking just for security
    # if thing.user != request.user:
    #     raise Http404

    form_class = RunoneUploadForm
# if we're coming to this view from a submitted form,
    if request.method == 'POST':
# grab the data from the submitted form, # note the new "files" part
        form = form_class(data=request.POST,files=request.FILES, instance=RunHere)
        if form.is_valid():
            RunHere = form.save(commit=False)
            RunHere.useredit = request.user.username
            RunHere.save()
# create a new object from the submitted form
            Upload.objects.create(
                image=form.cleaned_data['image'],
                runshow=RunHere,
            )
            return redirect('edit_RunDate_uploads', slug=RunHere.slug)
# otherwise just create the form
    else:
        form = form_class(instance=RunHere)
# grab all the object's images
    uploads = RunHere.uploads.all()
# and render the template
    return render(request, 'RunDate/edit_RunDate_uploads.html', {
        'RunHere': RunHere,
        'form': form,
        'uploads': uploads,
    })

@login_required
def delete_product(request, id):
# grab the image
    dp = Runone.objects.get(id=id)
# security check
    if dp.user != request.user:
        raise Http404
# delete the image
    dp.delete()
# refresh the edit page
    return redirect('home')


@login_required
def delete_upload(request, id):
# grab the image
    upload = Upload.objects.get(id=id)
    upload.runshow.useredit = request.user.username
    upload.runshow.save()
# security check
    # if upload.thing.user != request.user:
    #     raise Http404
# delete the image
    upload.delete()
# refresh the edit page
    return redirect('edit_RunDate_uploads', slug=upload.runshow.slug)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)

        if user_form.is_valid() :
            user_form.save()

            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'edit.html', {'user_form': user_form })


@login_required
def user_list(request):
    object_list = Runone.objects.filter(user_id=request.user.id)
    return render(request, 'userlist.html', { 'userlist': object_list,})


def post_search(request):
    form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Runone).filter(content=cd['query']).load_all()
            # count total results
            total_results = results.count()
        return render(request, 'search.html', {'form': form,
                                                         'cd': cd,
                                                         'results': results,
                                                         'total_results': total_results})
    return render(request, 'search.html', {'form': form,})
