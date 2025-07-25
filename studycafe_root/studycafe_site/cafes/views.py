# --- Public Views (No Login Required) ---

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Cafe, Rating, CafePhoto, Follow
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CafePhotoForm
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db import models
from .models import Bookmark
from django.views.generic import TemplateView
from .forms import CafeForm

class CafeListView(ListView):
    model = Cafe
    template_name = 'cafes/cafe_list.html'
    context_object_name = 'cafes'
    ordering = ['-posted_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                models.Q(name__icontains=query) | models.Q(address__icontains=query)
            )
        # Filter
        if self.request.GET.get('wifi'):
            queryset = queryset.filter(has_wifi=True)
        if self.request.GET.get('power'):
            queryset = queryset.filter(has_power_outlet=True)
        if self.request.GET.get('restroom'):
            queryset = queryset.filter(has_restroom=True)
        return queryset

class CafeDetailView(DetailView):
    model = Cafe
    template_name = 'cafes/cafe_detail.html'
    context_object_name = 'cafe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cafe = self.get_object()
        context['is_bookmarked'] = False
        if user.is_authenticated:
            context['is_bookmarked'] = cafe.bookmarked_by.filter(user=user).exists()
        context['photos'] = cafe.photos.all()
        context['photo_form'] = CafePhotoForm()
        return context

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form}) 

# --- Authenticated Views (Login Required) ---

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

class CafeCreateView(LoginRequiredMixin, CreateView):
    model = Cafe
    form_class = CafeForm
    template_name = 'cafes/cafe_form.html'
    success_url = reverse_lazy('cafe-list')
    
    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        messages.success(self.request, 'Cafe added successfully!')
        return super().form_valid(form)

class CafeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Cafe
    form_class = CafeForm
    template_name = 'cafes/cafe_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Cafe updated successfully!')
        return reverse_lazy('cafe-detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        cafe = self.get_object()
        return cafe.posted_by == self.request.user

class CafeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cafe
    template_name = 'cafes/cafe_confirm_delete.html'
    success_url = reverse_lazy('cafe-list')
    
    def test_func(self):
        cafe = self.get_object()
        return cafe.posted_by == self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Cafe deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required
def add_rating(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    
    if request.method == 'POST':
        stars = request.POST.get('stars')
        comment = request.POST.get('comment', '')
        
        if stars:
            # Check if user already rated this cafe
            rating, created = Rating.objects.get_or_create(
                cafe=cafe,
                user=request.user,
                defaults={'stars': stars, 'comment': comment}
            )
            
            if not created:
                # Update existing rating
                rating.stars = stars
                rating.comment = comment
                rating.save()
                messages.success(request, 'Rating updated successfully!')
            else:
                messages.success(request, 'Rating added successfully!')
        else:
            messages.error(request, 'Please provide a rating.')
    
    return redirect('cafe-detail', pk=cafe_id)

@login_required
def delete_rating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id, user=request.user)
    cafe_id = rating.cafe.id
    rating.delete()
    messages.success(request, 'Rating deleted successfully!')
    return redirect('cafe-detail', pk=cafe_id) 

@method_decorator(login_required, name='dispatch')
class UserProfileView(DetailView):
    model = User
    template_name = 'cafes/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cafes'] = self.request.user.cafe_set.all()
        context['ratings'] = self.request.user.rating_set.all()
        # Add bookmarks
        context['bookmarked_cafes'] = [bookmark.cafe for bookmark in self.request.user.bookmarks.all()]
        # Add followers and following
        context['followers'] = self.request.user.followers.all()
        context['following'] = self.request.user.following.all()
        return context

@login_required
def custom_password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')  # or wherever you want
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'registration/custom_password_change.html', {'form': form}) 

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'cafes/edit_profile.html', {'u_form': u_form, 'p_form': p_form}) 



# bookmark

@login_required
def add_bookmark(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    Bookmark.objects.get_or_create(user=request.user, cafe=cafe)
    messages.success(request, "Cafe saved!")
    return redirect('cafe-detail', pk=cafe_id)

@login_required
def remove_bookmark(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    Bookmark.objects.filter(user=request.user, cafe=cafe).delete()
    messages.success(request, "Removed from saved.")
    return redirect('cafe-detail', pk=cafe_id)


# map integration
# home mapview

class MapView(TemplateView):
    template_name = 'cafes/map.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all cafes with coordinates
        cafes_with_location = Cafe.objects.exclude(
            latitude__isnull=True
        ).exclude(
            longitude__isnull=True
        )
        context['cafes'] = cafes_with_location
        return context


# Photo gallery views
@login_required
def add_photo(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    
    if request.method == 'POST':
        form = CafePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.cafe = cafe
            photo.uploaded_by = request.user
            photo.save()
            messages.success(request, 'Photo added successfully!')
        else:
            messages.error(request, 'Please provide a valid image.')
    
    return redirect('cafe-detail', pk=cafe_id)


@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(CafePhoto, id=photo_id)
    cafe_id = photo.cafe.id
    
    # Only allow the uploader or the cafe owner to delete
    if request.user == photo.uploaded_by or request.user == photo.cafe.posted_by:
        photo.delete()
        messages.success(request, 'Photo deleted successfully!')
    else:
        messages.error(request, 'You do not have permission to delete this photo.')
    
    return redirect('cafe-detail', pk=cafe_id)


# Follow/Unfollow views
@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    
    if request.user != user_to_follow:
        Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        messages.success(request, f'You are now following {user_to_follow.username}!')
    else:
        messages.error(request, 'You cannot follow yourself.')
    
    return redirect('profile')


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    
    Follow.objects.filter(
        follower=request.user,
        following=user_to_unfollow
    ).delete()
    
    messages.success(request, f'You have unfollowed {user_to_unfollow.username}.')
    return redirect('profile')


@login_required
def user_followers(request, user_id):
    """View to show all followers of a specific user"""
    profile_user = get_object_or_404(User, id=user_id)
    followers = profile_user.followers.all()
    
    context = {
        'profile_user': profile_user,
        'followers': followers,
        'page_title': f"{profile_user.username}'s Followers"
    }
    return render(request, 'cafes/user_followers.html', context)


@login_required
def user_following(request, user_id):
    """View to show all users that a specific user is following"""
    profile_user = get_object_or_404(User, id=user_id)
    following = profile_user.following.all()
    
    context = {
        'profile_user': profile_user,
        'following': following,
        'page_title': f"Users {profile_user.username} follows"
    }
    return render(request, 'cafes/user_following.html', context)

