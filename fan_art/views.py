from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import FanArt
from profiles.models import UserProfile
from .forms import CreateFanArtForm, UpdateFanArtForm


def fan_art_gallery(request):
    """ A view to return all peices of fan art """

    fan_art = FanArt.objects.all().filter(is_approved=True)

    # Pagination
    paginator = Paginator(fan_art, 9)
    page = request.GET.get('page')
    paged_fan_art = paginator.get_page(page)

    context = {
        'fan_art': paged_fan_art,
        'current_page': 'fan_art_gallery',
    }

    return render(request, 'fan_art/fan_art_gallery.html', context)


def user_gallery(request):
    """ A view to return the user's submitted fan art """

    user_fan_art = FanArt.objects.all().filter(user_profile=request.user.id)

    # Checking for unapproved user_fan_art
    unapproved_art = False

    for art in user_fan_art:
        if not art.is_approved:
            unapproved_art = True

    # Pagination
    paginator = Paginator(user_fan_art, 9)
    page = request.GET.get('page')
    paged_user_fan_art = paginator.get_page(page)

    context = {
        'user_fan_art': paged_user_fan_art,
        'current_page': 'fan_art_gallery',
        'unapproved_art': unapproved_art,
    }

    return render(request, 'fan_art/user_art_gallery.html', context)


@login_required
def edit_art(request, art_id):
    """ A view to edit the user's own fan art """

    fan_art = get_object_or_404(FanArt, pk=art_id)

    if request.method == 'POST':
        update_fan_art_form = UpdateFanArtForm(request.POST, instance=fan_art)

        if update_fan_art_form.is_valid():
            fan_art = update_fan_art_form.save(commit=False)
            fan_art.is_approved = False
            fan_art.save()
            messages.success(request, 'Art updated successfully')

            redirect_url = reverse('user_gallery')
            return redirect(redirect_url)

    update_fan_art_form = UpdateFanArtForm(instance=fan_art)

    context = {
        'update_fan_art_form': update_fan_art_form,
        'fan_art': fan_art,
        'current_page': 'fan_art_gallery',
    }

    return render(request, 'fan_art/edit_fan_art.html', context)


@login_required
def delete_art(request, art_id):
    """ A view to delete the user's own fan art """

    # TODO: defensive programming
    if request.method == 'POST':
        selected_art = get_object_or_404(FanArt, pk=art_id)
        selected_art.delete()
        messages.success(request, 'Art deleted successfully')

    redirect_url = reverse('user_gallery')
    return redirect(redirect_url)


@login_required
def add_art(request):
    """ A view for the user to submit their own art to the gallery """

    if request.method == 'POST':
        add_art_form = CreateFanArtForm(request.POST, request.FILES)
        if add_art_form.is_valid():
            fan_art = add_art_form.save(commit=False)
            fan_art.user_profile = request.user.profile
            fan_art.save()
            messages.success(request, 'Image added successfully')

            redirect_url = reverse('user_gallery')
            return redirect(redirect_url)
        else:
            messages.error(request, 'Form not valid')
    else:
        add_art_form = CreateFanArtForm()

    context = {
        'add_art_form':  add_art_form,
        'current_page': 'fan_art_gallery',
    }

    return render(request, 'fan_art/add_fan_art.html', context)
