from django.shortcuts import render
from .forms import BookForm
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']
service = None
UTC_France = ':00+01:00'
BETWEEN_DATE_AND_TIME = 'T'

# '2019-02-15T09:00'+UTC_France

event = {
      'summary': None,
      'location': None,
      'description': None,
      'start': {
        'dateTime': None,
        'timeZone': None,
      },
      'end': {
        'dateTime': None,
        'timeZone': None,
      },
    }

# Create your views here.
def home(request):

	init_google_calendar()
	events_dates_tuples = retreive_events()
	events_dates = construct_list_of_dates(events_dates_tuples)

	if request.method == 'GET':
		bookForm = BookForm()

	elif request.method == 'POST':
		bookForm = BookForm(request.POST)
		if bookForm.is_valid():
			date_entry = form.cleaned_data['date_entrée']
			date_exit = form.cleaned_data['date_sortie']
			print("date_entry : ", date_entry)
			print("date_exit : ", date_exit)

	return render(request, 'index.html', locals())

def construct_list_of_dates(events_dates_tuples):
	events_dates = []
	for e in events_dates_tuples:
		events_dates.append(e[0])
		nb_range = int(e[1][:2]) - int(e[0][:2])
		if nb_range > 0:
			for i in range(nb_range):
				events_dates.append(str(int(e[0][:2])+i+1)+e[0][2:])

	return events_dates

def retreive_events():
	now = datetime.datetime.utcnow().isoformat() + 'Z'
	events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=200, singleEvents=True,
                                        orderBy='startTime').execute()
	events = events_result.get('items', [])

	events_dates = []
	for event in events:
		start_date = event['start'].get('dateTime', event['start'].get('date'))
		end_date = event['end'].get('dateTime', event['end'].get('date'))
		start_date, end_date = convert_google_to_js(start_date, end_date)
		events_dates.append((start_date, end_date))
		print(start_date, event['summary'])

	return events_dates

def convert_google_to_js(start_date, end_date=None):
	"""Convert 1 or 2 dates
	"""
	if not end_date:
		js_start_date = start_date[8:10] + '/' + start_date[5:7] + '/' + start_date[:4]
		return js_start_date
	else:
		js_start_date = start_date[8:10] + '/' + start_date[5:7] + '/' + start_date[:4]
		js_end_date = end_date[8:10] + '/' + end_date[5:7] + '/' + end_date[:4]
		return js_start_date, js_end_date



def init_google_calendar():
	"""Shows basic usage of the Google Calendar API.
	Prints the start and name of the next 10 events on the user's calendar.
	"""
	global service
	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)

	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				"static/45(_ç_-789)à&_&è_(357899=()=è)ç_-'ç_à/credentials.json", SCOPES)
			creds = flow.run_local_server()
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('calendar', 'v3', credentials=creds)