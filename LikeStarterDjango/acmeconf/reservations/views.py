from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.views.generic import View
from .forms import UserForm
from django.http import HttpResponse
from django.template import loader
from .models import Event
from .models import Like
from .models import Wallet, ArtistContracts
from .models import EventReservation
from django.views.generic import DetailView
from .forms import EventReservationForm
from .forms import DocumentForm
#added for blockchain project
from .forms import EventForm, WalletForm
#added for blockchain project
from django.contrib.auth.models import User
from zeep import Client
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.authtoken import views as authviews
from django.contrib.auth import logout
import json
from django.shortcuts import get_object_or_404
#like view
from django.views.decorators.http import require_POST
#smart contract implementation
import web3
from web3 import Web3, HTTPProvider
#ETHEREUM CONTRACT TEST Import
from solc import compile_source
from web3.contract import ConciseContract
from django.template import RequestContext

def index(request):
    latest_event_list = Event.objects.order_by('-date')[:100]
    #wallets = Wallet.objects.all()
    contracts_list = ArtistContracts.objects.all()

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

    #reading generic bin and abi contract files.

    with open("reservations/contracts/compiled/Likoin.abi") as likoin_abi:
        contract_likoin_abi = json.load(likoin_abi)

    with open("reservations/contracts/compiled/Likoin.bin") as likoin_bin:
        contract_likoin_bin = '0x' + likoin_bin.read()

    with open("reservations/contracts/compiled/Buck.abi") as buck_abi:
        contract_buck_abi = json.load(buck_abi)

    with open("reservations/contracts/compiled/Buck.bin") as buck_bin:
        contract_buck_bin = '0x' + buck_bin.read()

    with open("reservations/contracts/compiled/Crowdsale.abi") as crowdsale_abi:
        contract_crowdsale_abi = json.load(crowdsale_abi)

    with open("reservations/contracts/compiled/Crowdsale.bin") as crowdsale_bin:
        contract_crowdsale_bin = '0x' + crowdsale_bin.read()

    #finish

    template = loader.get_template('reservations/index.html')
    context = {
        'latest_event_list': latest_event_list,
        'contractABI_likoin': json.dumps(contract_likoin_abi),
        'contractABI_buck': json.dumps(contract_buck_abi),
        'contractABI_crowdsale': json.dumps(contract_crowdsale_abi),
        'contracts_list': contracts_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, event_id):
    return HttpResponse("You're looking at event %s." % event_id)

class UserFormView(View):
    form_class = UserForm
    template_name = 'reservations/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            #istantiates a user from the form, that is added to the user that we will see in the admin panel
            user = form.save(commit=False)

            #cleaned (normalized) databases
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            #save the user in the database
            user.save()

            #returns User object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('reservation:index')

        return render(request, self.template_name, {'form': form})

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        wallet = form.cleaned_data['wallet']

        wallet_reference = Wallet()

        user.set_password(password)
        user.save()

        wallet_reference.accountholder = get_object_or_404(User, username=username)
        wallet_reference.public_key = wallet

        wallet_reference.save()

        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
        block = w3.eth.getBlock('latest')
        blocknumber = block['number']

        w3.eth.defaultAccount = w3.eth.accounts[1]

        with open("reservations/contracts/compiled/Likoin.abi") as likoin_abi:
            contract_likoin_abi = json.load(likoin_abi)

        with open("reservations/contracts/compiled/Likoin.bin") as likoin_bin:
            contract_likoin_bin = '0x' + likoin_bin.read()

        with open("reservations/contracts/compiled/Buck.abi") as buck_abi:
            contract_buck_abi = json.load(buck_abi)

        with open("reservations/contracts/compiled/Buck.bin") as buck_bin:
            contract_buck_bin = '0x' + buck_bin.read()

        with open("reservations/contracts/compiled/Crowdsale.abi") as crowdsale_abi:
            contract_crowdsale_abi = json.load(crowdsale_abi)

        with open("reservations/contracts/compiled/Crowdsale.bin") as crowdsale_bin:
            contract_crowdsale_bin = '0x' + crowdsale_bin.read()

        #loading abi and bin contracts files
        likoin = w3.eth.contract(abi=contract_likoin_abi, bytecode=contract_likoin_bin)

        buck = w3.eth.contract(abi=contract_buck_abi, bytecode=contract_buck_bin)

        crowdsale = w3.eth.contract(abi=contract_crowdsale_abi, bytecode=contract_crowdsale_bin)
        #finish

        #transact into blockchain: likoin and buck
        tx_hash_likoin = likoin.constructor(wallet, "Likoin" + username, "LK" + username[0]).transact()

        tx_receipt_likoin = w3.eth.waitForTransactionReceipt(tx_hash_likoin)

        tx_hash_buck = buck.constructor(wallet, "Buck" + username, "BK" + username[0]).transact()

        tx_receipt_buck = w3.eth.waitForTransactionReceipt(tx_hash_buck)

        buck1_instance = w3.eth.contract(
            address=tx_receipt_buck.contractAddress,
            abi=contract_buck_abi,
        )

        likoin1_instance = w3.eth.contract(
            address=tx_receipt_likoin.contractAddress,
            abi=contract_likoin_abi,
        )
        #after receiving the information of deployment I'll pass these variables to the crowdsale constructor

        tx_hash_crowdsale = crowdsale.constructor(10, wallet,
                                                  tx_receipt_likoin.contractAddress,
                                                  tx_receipt_buck.contractAddress).transact()

        #transact receipt from crowdsale contract
        tx_receipt_crowdsale = w3.eth.waitForTransactionReceipt(tx_hash_crowdsale)

        crowdsale1_instance = w3.eth.contract(
            address=tx_receipt_crowdsale.contractAddress,
            abi=contract_crowdsale_abi,
        )

        artist_contracts_reference = ArtistContracts()
        artist_contracts_reference.artist = get_object_or_404(User, username=username)
        artist_contracts_reference.likoin_address = tx_receipt_likoin.contractAddress
        artist_contracts_reference.buck_address = tx_receipt_buck.contractAddress
        artist_contracts_reference.crowdsale_address = tx_receipt_crowdsale.contractAddress
        artist_contracts_reference.save()

        print("ok")
        print(likoin1_instance.functions.name().call())
        print("ok")

        likoin1_instance.functions.addMinter(tx_receipt_crowdsale.contractAddress).transact()
        print(likoin1_instance.functions.isMinter(tx_receipt_crowdsale.contractAddress).call())

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('reservations:index')
    context = {
        "form": form,
    }
    return render(request, 'reservations/register.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('reservations:index')
            else:
                return render(request, 'reservations/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'reservations/login.html', {'error_message': 'Invalid login'})
    return render(request, 'reservations/login.html')

class EventDetailView(generic.DetailView):
    model = Event
    def get_context_data(self, **kwargs):

        ctx = super(EventDetailView, self).get_context_data(**kwargs)
        ctx['reservations'] = EventReservation.objects.all()
        ctx['wallets'] = Wallet.objects.all()
        ctx['contracts'] = ArtistContracts.objects.all()
        return ctx

    #def get(self, request, pk):
    #    try:
    #        original_reservation = EventReservation.objects.get(event=33, user=request.user.id, is_staff=True)
    #    except EventReservation.DoesNotExist:
    #        return HttpResponseRedirect(reverse('reservations:event_detail', args=[pk]))
    #        break
    #    return redirect('reservations:upload')


@login_required
def reservation(request, event_id):

    #retrieve an event object by id
    original_event = Event.objects.get(id=event_id)

    if original_event.available_seats > 0 and original_event.is_open == True and original_event.is_open_contr == True:

        if request.method == 'POST':
            form = EventReservationForm(request.POST)

            if form.is_valid():

                event = form.save()
                event.user = request.user.id
                event.event = original_event.id
                original_event.available_seats = original_event.available_seats - 1

                try:
                    #establish the connection to the bank server
                    client = Client('http://jolie/server.wsdl')

                    #get bank username and password from the validate form
                    name = form.cleaned_data['name']
                    password = form.cleaned_data['password']

                    event.bank_user = form.cleaned_data['name']

                    #send form data to the bank login service
                    risposta = client.service.userLogin(name, password)

                    if risposta['userID'] == "-1":
                        request.session['except'] = 1
                        return HttpResponseRedirect(request.path_info)

                    if event.is_staff == True:
                        original_event.available_money = original_event.available_money + original_event.staff_ticket_price
                        client.service.transferPayment(original_event.staff_ticket_price, 'ACME', risposta['userID'])
                    else:
                        original_event.available_money = original_event.available_money + original_event.ticket_price
                        client.service.transferPayment(original_event.ticket_price, 'ACME', risposta['userID'])

                    client.service.userLogout(risposta['userID'])

                    original_event.save()
                    event.save()
                    request.session['except_server'] = 0
                    request.session['except'] = 0
                    return render_to_response('reservations/booked.html')
                except:
                    request.session['except_server'] = 2
                    return HttpResponseRedirect(request.path_info)

        else:
            form = EventReservationForm()

            if request.user.is_staff == True:
                return render(request, 'reservations/reservation.html', {
                    'form': form,
                    'price_staff': original_event.staff_ticket_price,
                    'price_standard': original_event.ticket_price
                })

            else:
                return render(request, 'reservations/reservation.html', {
                    'form': form,
                    'price_staff': original_event.staff_ticket_price,
                    'price_standard': original_event.ticket_price
                })

    else:
        original_event.is_open = False
        original_event.save()
        return render_to_response('reservations/closed.html')


def model_form_upload(request, event_id):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save()

            original_reservation = EventReservation.objects.get(event=event_id, user=request.user.id)

            upload.reservation = original_reservation.id

            upload.save()

            return redirect('reservations:index')
    else:
        form = DocumentForm()
    return render(request, 'reservations/model_form_upload.html', {
        'form': form
    })

def user_reservations(request):

    user_event_list = Like.objects.all()
    like_list = []
    for like in user_event_list:
        if like.owner.id == request.user.id:
            like_list.append(like)

    event_list = Event.objects.all()

    template = loader.get_template('reservations/user_reservations.html')
    context = {
        'like_list': like_list,
        'event_list': event_list,
    }
    return HttpResponse(template.render(context, request))

def delete_reservation(request, event_id):

    delete_event = EventReservation.objects.filter(event=event_id, user=request.user.id)
    delete_event.delete()

    template = loader.get_template('reservations/delete_confirm.html')

    context = {
            'delete_event': delete_event,
    }

    return HttpResponse(template.render(context, request))


def logout_usr(request):
    logout(request)
    return redirect('reservations:index')

@login_required
def event_form(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            #associa ad un evento il suo creatore tramite una ForeignKey
            event.user = get_object_or_404(User, username=request.user.username)
            handle_uploaded_file(form.cleaned_data['crowd_pic'])
            event.crowd_pic = form.cleaned_data['crowd_pic']

            #url modifier for the correct upload of the images
            event.save()
            stringa = event.crowd_pic.url
            y = stringa.replace('reservations','')
            event.crowd_pic = y
            event.save()

            return redirect('reservations:index')
    else:
        form = EventForm()
    return render(request, 'reservations/add_event.html', {
        'form': form
    })

def likes(request):
        event_id = request.POST.get('pk', None)
        event = get_object_or_404(Event, id=event_id)
        contracts_list = ArtistContracts.objects.all()
        wallet_list = Wallet.objects.all()

        for contract in contracts_list:
            if event.user == contract.artist:
                crowdsale_address = contract.crowdsale_address
                likoin_address = contract.likoin_address

        for wallet in wallet_list:
            if request.user == wallet.accountholder:
                sender_wallet = wallet.public_key
            if event.user == wallet.accountholder:
                receiver_wallet = wallet.public_key

        like_reference = Like()

        like_reference.owner = get_object_or_404(User, username=request.user.username)
        like_reference.pref_link = get_object_or_404(Event, id=event_id)

        like_reference.save()

        message = "You have liked this post, wait for Metamask Wallet opening."

        event.likes += 1
        event.save()
        context = {'like_count': event.likes,
                   'message': message,
                   'nickname': request.user.username,
                   'crowdsale_address': crowdsale_address,
                   'sender_wallet': sender_wallet,
                   'receiver_wallet': receiver_wallet,
                   'likoin_address': likoin_address,}

        return HttpResponse(json.dumps(context), content_type="application/json")


def ethTest(request):

    #ropsten.infura.io/v3/717987ef4b7c4d6487c801151d5a4a90

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
    block = w3.eth.getBlock('latest')
    blocknumber = block['number']

    w3.eth.defaultAccount = w3.eth.accounts[1]

    tx_param = {
        'from': w3.eth.accounts[1],
        'gasPrice': 10,
    }


    with open("reservations/contracts/compiled/Likoin.abi") as likoin_abi:
        contract_likoin_abi = json.load(likoin_abi)

    with open("reservations/contracts/compiled/Likoin.bin") as likoin_bin:
        contract_likoin_bin = '0x' + likoin_bin.read()

    with open("reservations/contracts/compiled/Buck.abi") as buck_abi:
        contract_buck_abi = json.load(buck_abi)

    with open("reservations/contracts/compiled/Buck.bin") as buck_bin:
        contract_buck_bin = '0x' + buck_bin.read()

    with open("reservations/contracts/compiled/Crowdsale.abi") as crowdsale_abi:
        contract_crowdsale_abi = json.load(crowdsale_abi)

    with open("reservations/contracts/compiled/Crowdsale.bin") as crowdsale_bin:
        contract_crowdsale_bin = '0x' + crowdsale_bin.read()

    #loading abi and bin contracts files
    likoin = w3.eth.contract(abi=contract_likoin_abi, bytecode=contract_likoin_bin)

    buck = w3.eth.contract(abi=contract_buck_abi, bytecode=contract_buck_bin)

    crowdsale = w3.eth.contract(abi=contract_crowdsale_abi, bytecode=contract_crowdsale_bin)
    #finish

    #transact into blockchain: likoin and buck
    tx_hash_likoin = likoin.constructor(w3.eth.accounts[3], "Likoin1", "LK1").transact()

    tx_receipt_likoin = w3.eth.waitForTransactionReceipt(tx_hash_likoin)

    tx_hash_buck = buck.constructor(w3.eth.accounts[3], "Buck1", "BK1").transact()

    tx_receipt_buck = w3.eth.waitForTransactionReceipt(tx_hash_buck)

    buck1_instance = w3.eth.contract(
        address=tx_receipt_buck.contractAddress,
        abi=contract_buck_abi,
    )

    likoin1_instance = w3.eth.contract(
        address=tx_receipt_likoin.contractAddress,
        abi=contract_likoin_abi,
    )
    #after receiving the information of deployment I'll pass these variables to the crowdsale constructor

    tx_hash_crowdsale = crowdsale.constructor(10, w3.eth.accounts[3],
                                              tx_receipt_likoin.contractAddress,
                                              tx_receipt_buck.contractAddress).transact()

    #transact receipt from crowdsale contract
    tx_receipt_crowdsale = w3.eth.waitForTransactionReceipt(tx_hash_crowdsale)

    crowdsale1_instance = w3.eth.contract(
        address=tx_receipt_crowdsale.contractAddress,
        abi=contract_crowdsale_abi,
    )

    print("crowdsale tx receipt")
    print(tx_receipt_crowdsale)

    #print the name of the ERC20 coin
    print(likoin1_instance.functions.name().call())
    #print(likoin1_instance.functions.mint(w3.eth.accounts[3], 1000).call())
    likoin1_instance.functions.mint(w3.eth.accounts[3], 1000).transact()
    #tx_receipt_likoin_temp = w3.eth.waitForTransactionReceipt(likoin1_instance.functions.balanceOf(w3.eth.accounts[3]).transact())
    print(likoin1_instance.functions.balanceOf(w3.eth.accounts[3]).call())

    w3.eth.waitForTransactionReceipt(likoin1_instance.functions.addMinter(tx_receipt_crowdsale.contractAddress).transact())
    print(likoin1_instance.functions.isMinter(tx_receipt_crowdsale.contractAddress).call())

    temp_tx_crowdsale = crowdsale1_instance.functions.buyTokens(w3.eth.accounts[6]).transact({'from': w3.eth.accounts[3], 'value': 10000})
    tx_receipt_crowdsale = w3.eth.waitForTransactionReceipt(temp_tx_crowdsale)

    print("ok")
    print(tx_receipt_crowdsale)
    print("ok")
    print(likoin1_instance.functions.balanceOf(w3.eth.accounts[6]).call())

    #print the totalSupply of ERC20 coin
    #print(coin_instance.functions.totalSupply().call())

    #print("deploying, tx_hash {}".format(Web3.toHex(tx_hash)))
    #print(tx_receipt_likoin.contractAddress)
    #print(likoin1_instance)

    return render(request, 'reservations/ethtest.html', {
        'ethBlockNumber': blocknumber,
        'contractAddress': tx_receipt_likoin.contractAddress,
        'txhash': tx_hash_likoin,
        #'contractABI': json.dumps(contract_abi_coin),
    })


def update_wallet(request):
    users_wallets = Wallet.objects.all()

    for single_wallet in users_wallets:
        if single_wallet.accountholder == request.user:
            instance=single_wallet

    form = WalletForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()

        return redirect('reservations:index')


    return render(request, 'reservations/up_wallet.html', {
        'form': form,
    })


#A function to upload files, really!
def handle_uploaded_file(f):
    destination = open('static', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
