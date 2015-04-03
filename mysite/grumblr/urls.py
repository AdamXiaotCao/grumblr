from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'grumblr.views.home', name = 'home'),
    url(r'^add_follow/(?P<id>\d+)$','grumblr.views.add_follow', name='follow'),
    url(r'^un_follow/(?P<id>\d+)$','grumblr.views.un_follow', name='unfollow'),
    url(r'^block/(?P<id>\d+)$','grumblr.views.block', name='block'),
    url(r'^unblock/(?P<id>\d+)$','grumblr.views.un_block', name='unblock'),
    url(r'^add-grumbl', 'grumblr.views.add_grumbl', name='add'),
    url(r'^delete-grumbl/(?P<id>\d+)$', 'grumblr.views.delete_grumbl', name='delete'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'registration.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^registration$', 'grumblr.views.register', name='register'),
    url(r'^edit-profile/(?P<id>\d+)$','grumblr.views.edit_profile', name='edit'),
    url(r'^view-profile/(?P<id>\d+)$','grumblr.views.show_profile', name='view'),
    url(r'^search$','grumblr.views.search', name='search'),
    url(r'^add_comment/(?P<id>\d+)$','grumblr.views.add_comment', name='comment'),
    url(r'^dislike/(?P<id>\d+)$','grumblr.views.dislike', name='dislike'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$','grumblr.views.confirm_registration', name='confirm'),
    url(r'^photo/(?P<id>\d+)$', 'grumblr.views.get_photo', name='photo'),
    
    url(r'^change_password/(?P<id>\d+)$','grumblr.views.change_password', name='change_password'),
    url(r'^forgot_password$', 'grumblr.views.forgot_password', name='forgot_password'),
    url(r'^set_password/(?P<id>\d+)$', 'grumblr.views.set_password', name='set_password'),
    url(r'^confirm-reset/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$','grumblr.views.confirm_reset', name='confirm_reset'),
    url(r'^grumbl_photo/(?P<id>\d+)$', 'grumblr.views.get_grumbl_photo', name='grumbl_photo'),
    url(r'^get_mygrumbl$', 'grumblr.views.get_mygrumbl', name='get_mygrumbl'),
)
    
