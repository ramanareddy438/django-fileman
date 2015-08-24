# Requirements #

  * PIL
  * Installed django.contrib.admin application.
  * Installed django.contrib.auth application.
  * pytils (http://www.pyobject.ru/projects/pytils) `optional`

# Instructions #

  1. Get app fileman: `svn checkout http://django-fileman.googlecode.com/svn/trunk/ fileman` and copy directory fileman to directory with your project.
  1. Edit `fileman/settings.py`
    * `BASKET_FOLDER` - your "recycle bin" directory
    * `MEDIA_ROOT` - absolute path to fileman media directory **or** you can comment ` (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),` in `fileman/urls.py` and publish media files using your web server.
    * `MEDIA_URL` - absolute url to fileman media directory
    * `ANONYMOUSES` - support anonymous users.(see Anonymouses)
    * `TEXT_EXT` - list of file extensions that can be opened in text mode
    * `PICTURE_EXT` - list of file extensions that can be opened as images
    * `PYTILS` - using pytils (need if you have files with Russian name)
  1. Edit `your_project/settings.py`
    * add `'your_project.fileman',` in `INSTALLED_APPS`
    * add `'your_project.fileman.context_processors.urls',` in `TEMPLATE_CONTEXT_PROCESSORS`
    * add `'fileman.middleware.Anonymous_fileman_Setting',` in `MIDDLEWARE_CLASSES`
    * add absolute path to `fileman/templates/` in `TEMPLATE_DIRS`
  1. Edit `your_project/urls.py`
    * add `(r'^fm/', include('cyxapeff_org.fileman.urls')),` in `patterns`
  1. Run `python manage.py syncdb`
  1. Open admin selection, go to Fileman -> Settings and create (or edit) profile for users.
    * Root - root directory for user
    * Home - home directory for user
  1. Give permission for non-admin users.
    * Select user in django site admin
    * Add user permissions (for example, "fileman | setting | Can look files list")
  1. You can add Alias. Example:
    * `Path: /mnt/H/My Developement/django/cyxapeff_org/media/`
    * `Url: http://127.0.0.1:8000/media/`

## Anonymouses ##
You can use the file manager to allow anonymous users. To do this, you must create a user with the name `Anonymous`. Set root and home directory for him, as well permission.
In settings.py `ANONYMOUSES` must be `True`.