
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ipfshttpclient import connect
import requests 
from django.http import JsonResponse
from .models import File,User

# Connect to IPFS 
client = connect('/ip4/127.0.0.1/tcp/5001/http')

# initialize a dictionary to store the filenames and hashes

file_data = {}
peers = []
UserName = ''

def registration(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_exists = User.objects.filter(username=username).exists()
        if(user_exists):
            return HttpResponse("USER NAME ALREADY EXISTS.PLEASE SELECT OTHER USERNAME")
        else:
            temp_User = User(username = username , password = password , uc_tokens = 100 , peer_id = get_id())
            temp_User.save()
            return HttpResponse("REGISTERED SUCCESSFULLY")
    else:
        return render(request,'register.html')


def loginProcess(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        UserName = username
        db_password = User.objects.get(username=username).password
        if(User.objects.filter(username=username).exists()):
            if(db_password==password):
                return render(request , 'index.html')
            else :
                return HttpResponse("Incorrect Password")
        else:
            return HttpResponse("Incorrect User Name ")
    else:
        return render(request,'login.html')


def home(request):
    return render(request, 'home.html')


def get_node_status(request):
    peer_data = client.id()
    return render(request , 'node_status.html',{'peer_data' : peer_data })


@csrf_exempt
def upload(request):
    ipfs_hash = ''
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        size = uploaded_file.size
        file_name = request.POST.get('file_name')
        res = client.add(uploaded_file)
        ipfs_hash = res['Hash']
        file_data[ipfs_hash] = file_name
        data = []
        peer_id = get_id() 

        # save the file name and hash in database

        try: 
            file = File.objects.get(file_name=file_name , file_hash = ipfs_hash)
            # file_hash = File.objects.get(file_hash = ipfs_hash)
            return HttpResponse('THIS FILE IS ALREADY GOT STORED IN IPFS')
        except File.DoesNotExist:
            file_obj = File(file_name = file_name , file_hash = ipfs_hash , username = UserName)
            file_obj.save()
            send_uc_tokens(ipfs_hash,size)
        return HttpResponse('File uploaded Successfully')
    else:
        return HttpResponse('Invalid request method.Submit the form again')


def download(request, ipfs_hash):
    file_content = client.cat(ipfs_hash)
    response = HttpResponse(file_content, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{ipfs_hash}.txt"'
    
    return response


def show_text(request,ipfs_hash):
    file_content = client.cat(ipfs_hash)
    return render(request, 'show_text.html', {'text_content': file_content})


def get_connected_peers(request):
    url = 'http://localhost:5001/api/v0/swarm/peers'
    response = requests.post(url)

    if(response.status_code == 200):
        peers_data = response.json()
        if(peers_data['Peers']!=None):
            for peer_info in peers_data['Peers']:
                peer_id = peer_info['Peer']
                address = peer_info['Addr']
                peers.append([peer_id,address])

    if(len(peers)==0):
        return HttpResponse("No Peers are connnected")
    else:
        return render(request, 'peers.html' , {'peers' : peers})
    


def show_files(request):
    data = File.objects.filter(username=UserName).all()
    file_list={}
    for file in data:
        hash = file.file_hash
        name = file.file_name
        file_list[hash] = name
    print(file_list)
    return render(request, 'download.html', {'file_data': file_list})


def direct_download(request):
    file_name = request.POST.get('file_name')
    file_obj = File.objects.get(file_name=file_name)
    print(file_obj)
    file_hash=file_obj.file_hash
    print(file_hash)
    file_content = client.cat(file_hash)
    response = HttpResponse(file_content, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file_hash}.txt"'
    return response


def peersStoringFile(request,ipfs_hash):
    peers = client.dht.findprovs(ipfs_hash)
    peers_storing_file = []
    for peer in peers:
        if peer['ID'] not in peers_storing_file:
            peers_storing_file.append(peer['ID'])

    return render(request , 'show_peers_storing_file.html' , {'peers_storing_file' : peers_storing_file})


def send_uc_tokens(ipfs_hash,size):
    peers = client.dht.findprovs(ipfs_hash)
    peers_storing_file = []
    for peer in peers:
        if peer['ID'] not in peers_storing_file:
            peers_storing_file.append(peer['ID'])
    if peers_storing_file:
        tokens_to_distribute = size/1000
        user = User.objects.filter(peer_id=get_id()).last()
        user.uc_tokens -= tokens_to_distribute
        user.save()
        tokens_per_peer = tokens_to_distribute/len(peers_storing_file)
        for peer in peers_storing_file:
            try:
                User.objects.get(peer_id = peer).uc_tokens += tokens_per_peer
            except:
                if peer:
                    temp_user=User(uc_tokens = tokens_per_peer , peer_id = peer)
                    temp_user.save()


def get_id():
    id = client.id()
    return id['ID']


def delete_all_files(request):
    File.objects.all().delete()
    return HttpResponse("ALL FILES ARE DELETED")


def delete_user_db(request):
    User.objects.all().delete()
    return HttpResponse("ALL USER RECORDS ARE CLEARED")


def display_File_DB(request):
    files = File.objects.all()
    return render(request , 'display_File_DB.html' , {'files' : files})


def display_User_DB(request):
    Users = User.objects.all()    
    return render(request , 'display_User_DB.html' , {'Users' : Users})


def delete_file(request,ipfs_hash):
    File.objects.filter(file_hash=ipfs_hash).delete()
    return HttpResponse("File is Deleted")


def show_balance(request):
    balance = User.objects.filter(peer_id = get_id()).last().uc_tokens
    return render(request , 'balance.html' , {'balance' : balance})