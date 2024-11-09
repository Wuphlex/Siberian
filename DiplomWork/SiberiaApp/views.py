from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from SiberiaApp.models import Person
from SiberiaApp.models import History

from datetime import datetime, timedelta

import requests
import json
from requests.structures import CaseInsensitiveDict
import time
import re

from django.shortcuts import render, redirect
from SiberiaApp.forms import LoginForm

from django.http import (
    Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect,
)


def ReturnJson(code, data):
    httpRespon = HttpResponse()
    httpRespon['Content-Type'] = 'application/json'
    httpRespon['charset'] = 'ASCII'
    httpRespon.status_code = code
    httpRespon.write(json.dumps(data, sort_keys=True, indent=4))
    return httpRespon


def index(request):
    return render(request, 'SiberiaApp/index.html')


@login_required
def indexRework(request):
    if request.user.is_authenticated:
        return render(request, 'SiberiaApp/indexRework.html')
    else:
        return render(request, 'SiberiaApp/login.html', {'form': LoginForm()})


def check_api_connection():
    url = 'https://178.176.241.200/'  # Replace with your API endpoint
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False





def search(request):
    person_name = request.GET.get('person_name', None)
    print(person_name)
    person = Person.objects.get(FIO_text=person_name)

    response = {"name": person.FIO_text, "work": person.work_text, "place": person.place_text,
                "marker": person.marker_text}

    print(response)
    return JsonResponse(response)


def counterPeopleOnMarker(request):
    marker_name = request.GET.get('marker_name', None)
    build_name = request.GET.get('build_name', None)
    print(marker_name)
    print(build_name)
    people = Person.objects.filter(place_text=build_name).filter(marker_text=marker_name).count()
    response = {"count": people}
    print(response)
    return JsonResponse(response)


def peopleOnMarker(request):
    marker_name = request.GET.get('marker_name', None)
    build_name = request.GET.get('build_name', None)
    print(marker_name)
    print(build_name)
    people_enter = []
    people = list(Person.objects.filter(place_text=build_name).filter(marker_text=marker_name).values())
    number = Person.objects.filter(place_text=build_name).filter(marker_text=marker_name).count()
    print(people)

    for y in people:
        person = dict()
        person.update(FIO_text=y['FIO_text'])
        people_enter.append(person)

    response = {"people": people_enter, "count": number}
    print(response)
    return JsonResponse(response)


def allpeople(request):
    people_enter = []
    people = list(Person.objects.all().values())
    number = Person.objects.all().count()
    print(people)

    for y in people:
        person = dict()
        person.update(FIO_text=y['FIO_text'])
        people_enter.append(person)

    response = {"people": people_enter, "count": number}
    print(response)
    return JsonResponse(response)


def needHistory(request):
    true_current_datetime = datetime.now()
    current_datetime = datetime(2023, 5, 15, 15, 0, 0)

    history_enter = []
    person_name = request.GET.get('person_name', None)
    section = request.GET.get('section', None)
    print(person_name)
    # current_datetime = datetime.now()
    print("Текущее datetime:", current_datetime)

    delta = {
        'hour': timedelta(hours=1),
        'day': timedelta(days=1),
        'week': timedelta(days=7),
        'month': timedelta(days=31)
    }

    last_datetime = current_datetime - delta[section]

    history = list(History.objects.filter(FIO_text=person_name).filter(
        time_date__range=(last_datetime, current_datetime)).values())

    for y in history:
        string = dict()
        string.update(time_date=y['time_date'])
        string.update(place_text=y['place_text'])
        string.update(marker_text=y['marker_text'])
        history_enter.append(string)

    response = {"history": history_enter}

    print(response)
    return JsonResponse(response)


def needHistoryMarker(request):
    true_current_datetime = datetime.now()
    current_datetime = datetime(2023, 5, 15, 15, 0, 0)

    history_enter = []
    build_name = request.GET.get('build_name', None)
    marker_name = request.GET.get('marker_name', None)
    section = request.GET.get('section', None)

    print(marker_name)
    # current_datetime = datetime.now()
    print("Текущее datetime:", current_datetime)

    delta = {
        'hour': timedelta(hours=1),
        'day': timedelta(days=1),
        'week': timedelta(days=7),
        'month': timedelta(days=31)
    }

    last_datetime = current_datetime - delta[section]

    history = list(History.objects.filter(place_text=build_name).filter(marker_text=marker_name).filter(
        time_date__range=(last_datetime, current_datetime)).values())

    for y in history:
        string = dict()
        string.update(time_date=y['time_date'])
        string.update(FIO_text=y['FIO_text'])
        history_enter.append(string)

    response = {"history": history_enter}

    print(response)
    return JsonResponse(response)


def giveInfo(request):
    site_name = []
    keeper = []
    anchors = []

    url = "https://178.176.241.20/auth/token"
    data = {'username': 'system', 'password': 'admin'}
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
    token = r.json()['token']

    time.sleep(1)

    print("Hi from views")

    if len(token) != 0:

        url_anchor = "https://178.176.241.20/CFG-API/v0.1/data/anchors"
        headers = CaseInsensitiveDict()
        headers['Authorization'] = "Bearer " + token
        resp_anchor = requests.get(url_anchor, headers=headers, verify=False)

        url_keeper = "https://178.176.241.20/BA-API/v0.1/monitor/keeper_areas"
        headers = CaseInsensitiveDict()
        headers['Authorization'] = "Bearer " + token
        resp_keeper = requests.get(url_keeper, headers=headers, verify=False)

        for y in resp_keeper.json()['items']:
            keeper_data = dict()

            keeper_data.update(x=y['x'])
            keeper_data.update(y=y['y'])
            keeper_data.update(z=y['z'])
            keeper_data.update(sn=y['_links']['tag']['id'])

            keeper.append(keeper_data)

        for i in resp_anchor.json()['items']:
            for t in keeper:
                if t['x'] == i['x'] and t['y'] == i['y'] and t['z'] == i['z']:
                    out = dict()
                    sn = [t["sn"]]
                    out.update(site_name=i['site_name'])
                    out.update(sn=sn)
                    anchors.append(out)
                else:
                    out = dict()
                    sn = []
                    out.update(site_name=i['site_name'])
                    out.update(sn=sn)
                    anchors.append(out)
                print("out " + out)
            try:
                if i['site_name'] not in site_name:
                    site_name.append(i['site_name'])
                    print("site name " + i['site_name'])
            except KeyError as k:
                print(k)

        print("=========")
        print(anchors)
        res = dict()

        for obj in anchors:
            print(obj['site_name'])
            if obj['site_name'] not in res:
                res[obj['site_name']] = obj
                print(res)
                print("if")
            else:
                res[obj['site_name']]['sn'] += obj['sn']
                print(res)
                print("else")
        # print(res)
        print(list(res.values()))

        change = False
        info = res

        for key, val in info.items():
            # place = re.sub("[^A-Za-z]", "", str(y['site_name']))
            # marker = re.sub("[^0-9]", "", str(y['site_name']))
            place = re.sub("[^A-Za-z]", "", str(key))
            marker = re.sub("[^0-9]", "", str(key))
            for i in val:
                person = Person.objects.get(sn_int=i)
                if person.place_text != place or person.marker_text != marker:
                    person.place_text = place
                    person.marker_text = marker
                    new_history = History(FIO_text=person.FIO_text, place_text=person.place_text,
                                          marker_text=person.marker_text, time_date=datetime.now())
                    new_history.save()
                    change = True

        response = {"change": change}

        print(response)
        return JsonResponse(response)


def giveInfoTest(request):
    person_name = request.GET.get('person_name', None)
    marker_name = request.GET.get('marker_name', None)
    build_name = request.GET.get('build_name', None)
    hour = request.GET.get('hour', None)
    minute = request.GET.get('minute', None)
    second = request.GET.get('second', None)
    current_datetime = datetime(2023, 5, 15, int(hour), int(minute), int(second))
    change = False

    person = Person.objects.get(FIO_text=person_name)
    if person.place_text != build_name or person.marker_text != marker_name:
        person.place_text = build_name
        person.marker_text = marker_name
        person.save()
        new_history = History(FIO_text=person.FIO_text, place_text=person.place_text,
                              marker_text=person.marker_text, time_date=current_datetime)
        new_history.save()
        change = True

    response = {"change": change}

    print(response)
    return JsonResponse(response)


def cybercode(request):
    site_name = []
    keeper = []
    out_data = []

    anchors = []

    url = "https://178.176.241.20/auth/token"
    data = {'username': 'system', 'password': 'admin'}
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
    token = r.json()['token']

    time.sleep(1)

    print("Hi from views")

    if len(token) != 0:

        url_anchor = "https://178.176.241.20/CFG-API/v0.1/data/anchors"
        headers = CaseInsensitiveDict()
        headers['Authorization'] = "Bearer " + token
        resp_anchor = requests.get(url_anchor, headers=headers, verify=False)

        url_keeper = "https://178.176.241.20/BA-API/v0.1/monitor/keeper_areas"
        headers = CaseInsensitiveDict()
        headers['Authorization'] = "Bearer " + token
        resp_keeper = requests.get(url_keeper, headers=headers, verify=False)

        for y in resp_keeper.json()['items']:
            keeper_data = dict()

            keeper_data.update(x=y['x'])
            keeper_data.update(y=y['y'])
            keeper_data.update(z=y['z'])
            keeper_data.update(sn=y['_links']['tag']['id'])

            keeper.append(keeper_data)

        for i in resp_anchor.json()['items']:
            for t in keeper:
                if t['x'] == i['x'] and t['y'] == i['y'] and t['z'] == i['z']:
                    out = dict()
                    sn = [t["sn"]]
                    out.update(site_name=i['site_name'])
                    out.update(sn=sn)
                    anchors.append(out)
                else:
                    out = dict()
                    sn = []
                    out.update(site_name=i['site_name'])
                    out.update(sn=sn)
                    anchors.append(out)
                print("out " + out)
            try:
                if i['site_name'] not in site_name:
                    site_name.append(i['site_name'])
                    print("site name " + i['site_name'])
            except KeyError as k:
                print(k)

        print("=========")
        print(anchors)
        res = dict()

        for obj in anchors:
            print(obj['site_name'])
            if obj['site_name'] not in res:
                res[obj['site_name']] = obj
                print(res)
                print("if")
            else:
                res[obj['site_name']]['sn'] += obj['sn']
                print(res)
                print("else")
        # print(res)
        print(list(res.values()))

        return ReturnJson(200, list(res.values()))


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('rework/')
    else:
        form = LoginForm()
    return render(request, 'SiberiaApp/login.html', {'form': form})
