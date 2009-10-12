django-fileman

Web-based files manager. (using Django + jQuery)
http://code.google.com/p/django-fileman/


FEATURES:
  * Based operations with files and directories:
    created, upload, rename, copy, move, delete 
  * History
  * Preview text files and images
  * Alias (return url)
    

GETTING:
  svn checkout http://django-fileman.googlecode.com/svn/trunk/ fileman


INSTALLATION:
  Requirements
  
      * PIL
      * Installed django.contrib.admin application.
      * Installed django.contrib.auth application.
      * pytils (http://www.pyobject.ru/projects/pytils) [optional]
  
  Instructions
  
     1. Get app fileman: 
        svn checkout http://django-fileman.googlecode.com/svn/trunk/ fileman 
        and copy directory fileman to directory with your project.
     2. Edit fileman/settings.py
            * BASKET_FOLDER - your "recycle bin" directory
            * MEDIA_ROOT - absolute path to fileman media directory
              or you can comment (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
              in fileman/urls.py and publish media files using your web server.
            * MEDIA_URL - absolute url to fileman media directory
            * ANONYMOUSES - support anonymous users.(see Anonymouses)
            * TEXT_EXT - list of file extensions that can be opened in text mode
            * PICTURE_EXT - list of file extensions that can be opened as images
            * PYTILS - using pytils (need if you have files with Russian name)
     3. Edit your_project/settings.py
            * add 'your_project.fileman', in INSTALLED_APPS
            * add 'your_project.fileman.context_processors.urls', in TEMPLATE_CONTEXT_PROCESSORS
            * add 'fileman.middleware.Anonymous_fileman_Setting', in MIDDLEWARE_CLASSES
            * add absolute path to fileman/templates/ in TEMPLATE_DIRS
     4. Edit your_project/urls.py
            * add (r'^fm/', include('cyxapeff_org.fileman.urls')), in patterns
     5. Run python manage.py syncdb
     6. Open admin selection, go to Fileman -> Settings and create (or edit) profile for users.
            * Root - root directory for user
            * Home - home directory for user 
     7. Give permission for non-admin users.
            * Select user in django site admin
            * Add user permissions (for example, "fileman | setting | Can look files list")
     8. You can add Alias. Example:
            * Path: /mnt/H/My Developement/django/cyxapeff_org/media/
            * Url: http://127.0.0.1:8000/media/ 

  Anonymouses
  
  You can use the file manager to allow anonymous users.
  To do this, you must create a user with the name Anonymous.
  Set root and home directory for him, as well permission.
  In settings.py ANONYMOUSES must be True. 
  
  
CONTACTS:
  Email: max@cyxapeff.org
  Issues: http://code.google.com/p/django-fileman/issues/list
