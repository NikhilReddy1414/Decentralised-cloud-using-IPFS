# ipfs_project/ipfs_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/' , views.registration , name='register'),
    path('login/' , views.loginProcess , name='login'),
    path('upload/', views.upload, name='upload'),
    path('download/<str:ipfs_hash>/', views.download, name='download'),
    path('show_text/<str:ipfs_hash>/', views.show_text, name='show_text'),
    path('peers/',views.get_connected_peers,name='peers'),
    path('node_status/', views.get_node_status,name='node_status'),
    path('show_files/' , views.show_files,name='show_files'),
    path('direct_download', views.direct_download,name='direct_download'),
    path('peersStoringFile/<str:ipfs_hash>/', views.peersStoringFile , name='peersStoringFile'),
    path('delete_all_files/' , views.delete_all_files , name = 'delete_all_files'),
    path('delete_user_db' , views.delete_user_db , name = 'delete_user_db'),
    path('display_File_DB/' , views.display_File_DB , name='display_File_DB'),
    path('display_User_DB/' , views.display_User_DB , name='display_User_DB'),
    path('delete_file/<str:ipfs_hash>' , views.delete_file , name='delete_file'),
    path('balance' , views.show_balance , name='balance')
]
