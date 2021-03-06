from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import FanArt
from profiles.models import UserProfile
from .forms import CreateFanArtForm, UpdateFanArtForm
from series.models import Series


def all_fan_art(request):
    """ A view to return all peices of fan art """

    fan_art = FanArt.objects.all().filter(is_approved=True)
    series_list = Series.objects.all()

    # Variables for filtering
    selected_series = request.GET.get('series', '')

    # Filtering code
    if selected_series != '':
        try:
            selected_series = int(selected_series)
            fan_art = fan_art.filter(series__id=selected_series)
        except ValueError:
            selected_series = ''

    # Pagination
    paginator = Paginator(fan_art, 9)
    page = request.GET.get('page')
    paged_fan_art = paginator.get_page(page)

    context = {
        'fan_art': paged_fan_art,
        'current_page': 'all_fan_art',
        'series_list': series_list,
        'selected_series': selected_series,
    }

    return render(request, 'fan_art/all_fan_art.html', context)


def user_fan_art(request):
    """ A view to return the user's submitted fan art """

    user_fan_art = FanArt.objects.all().filter(user_profile=request.user.profile)

    # Checking for unapproved user_fan_art
    unapproved_fan_art = False

    for art in user_fan_art:
        if not art.is_approved:
            unapproved_fan_art = True

    # Pagination
    paginator = Paginator(user_fan_art, 9)
    page = request.GET.get('page')
    paged_user_fan_art = paginator.get_page(page)

    context = {
        'user_fan_art': paged_user_fan_art,
        'current_page': 'all_fan_art',
        'unapproved_fan_art': unapproved_fan_art,
    }

    return render(request, 'fan_art/user_fan_art.html', context)


@login_required
def edit_fan_art(request, art_id):
    """ A view to edit the user's own fan art """

    fan_art = get_object_or_404(FanArt, pk=art_id)

    if not request.user.id == fan_art.user_profile.user.id:
        messages.warning(
            request,
            'You can only edit your own art!'
        )
        redirect_url = reverse('all_fan_art')
        return redirect(redirect_url)

    if request.method == 'POST':
        update_fan_art_form = UpdateFanArtForm(request.POST, instance=fan_art)

        if update_fan_art_form.is_valid():
            fan_art = update_fan_art_form.save(commit=False)
            fan_art.is_approved = False
            fan_art.save()
            messages.success(request, 'Art updated successfully')

            redirect_url = reverse('user_fan_art')
            return redirect(redirect_url)

    update_fan_art_form = UpdateFanArtForm(instance=fan_art)

    context = {
        'update_fan_art_form': update_fan_art_form,
        'fan_art': fan_art,
        'current_page': 'user_fan_art',
    }

    return render(request, 'fan_art/edit_fan_art.html', context)


@login_required
def delete_fan_art(request, art_id):
    """ A view to delete the user's own fan art """

    if request.method == 'POST':
        selected_fan_art = get_object_or_404(FanArt, pk=art_id)

        if not request.user.id == selected_fan_art.user_profile.user.id:
            messages.warning(
                request,
                'You can only delete your own art!'
            )
            redirect_url = reverse('all_fan_art')
            return redirect(redirect_url)

        selected_fan_art.delete()
        messages.success(request, 'Art deleted successfully')

    redirect_url = reverse('user_fan_art')
    return redirect(redirect_url)


@login_required
def add_fan_art(request):
    """ A view for the user to submit their own art to the gallery """

    if request.method == 'POST':
        add_art_form = CreateFanArtForm(request.POST, request.FILES)
        if add_art_form.is_valid():
            fan_art = add_art_form.save(commit=False)
            fan_art.user_profile = request.user.profile
            fan_art.save()
            messages.success(request, 'Image added successfully')

            redirect_url = reverse('user_fan_art')
            return redirect(redirect_url)
        else:
            messages.error(request, 'Form not valid')
    else:
        add_fan_art_form = CreateFanArtForm()

    context = {
        'add_fan_art_form':  add_fan_art_form,
        'current_page': 'all_fan_art',
    }

    return render(request, 'fan_art/add_fan_art.html', context)
