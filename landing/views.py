from django.shortcuts import render
from .forms import resaForm, contactForm
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponseRedirect

SCOPES = ['https://www.googleapis.com/auth/calendar']
service = None
UTC_France = ':00+01:00'
BETWEEN_DATE_AND_TIME = 'T'

# '2019-02-15T09:00'+UTC_France

dico_months = {
	'Jan': '01',
	'Feb': '02',
	'Mar': '03',
	'Apr': '04',
	'May': '05',
	'Jun': '06',
	'Jul': '07',
	'Aug': '08',
	'Sep': '09',
	'Oct': '10',
	'Nov': '11',
	'Dec': '12'
}

event = {
      'summary': None,
      'location': 'Salle des fêtes chez dudu, Saint Vincent Sterlanges',
      'description': None,
      'start': {
        'dateTime': None,
        'timeZone': 'Europe/Paris',
      },
      'end': {
        'dateTime': None,
        'timeZone': 'Europe/Paris',
      },
    }

# Create your views here.
def home(request):

	init_google_calendar()
	events_dates_tuples = retreive_events()
	events_dates = construct_list_of_dates(events_dates_tuples)

	if request.method == 'POST':
		resaForm_ = resaForm(request.POST)
		contactForm_ = contactForm(request.POST)
		if resaForm_.is_valid():
			name = resaForm_.cleaned_data['name_resa']
			email = resaForm_.cleaned_data['email_resa']
			dates_resa = resaForm_.cleaned_data['dates_resa']
			phone = resaForm_.cleaned_data['phone_number_resa']
			description = resaForm_.cleaned_data['message_resa']
			needs = []

			post_dict = request.POST.dict()
			for key in post_dict:
				if key == 'optradio1':
					presta = "fete"
				if key == 'optradio2':
					presta = "pro"
				if key == 'chkbox_video':
					needs.append("Video-Projecteur")
				if key == 'chkbox_sono':
					needs.append("Sono et Micro")
				if key == 'chkbox_dj':
					needs.append("DJ")
				
			if dates_resa == '':
				message = "Aucune(s) date(s) sélectionnée(s)."
			else:
				dates_resa_list = dates_resa.split(",")
				good_date_resa = []
				for date in dates_resa_list:
					good_date_resa.append(convert_js_to_google(date))

				if check_dates_before_creation(events_dates, good_date_resa):
					create_event(name, email, phone, good_date_resa, presta, needs, description)
					send_confirmation_mail(name, email, good_date_resa)
					successful_booking = True
				else:
					print("Deja des events à ces dates là...")

			messages.add_message(request, messages.SUCCESS, "successful_booking")
			return HttpResponseRedirect("/")

		if contactForm_.is_valid():
			name = contactForm_.cleaned_data['name_contact']
			email = contactForm_.cleaned_data['email_contact']
			phone_number = contactForm_.cleaned_data['phone_number_contact']
			message = contactForm_.cleaned_data['message_contact']
			message = "Nom : " + name + "\nE-mail : " + email + "\nTéléphone : " + phone_number + "\n\nSon message :\n" + message
			try:
				send_mail("Contact Salle Saint-Vincent", message, email, [settings.EMAIL_HOST_USER])
				successful_contact = True
				messages.add_message(request, messages.SUCCESS, "successful_contact")
				return HttpResponseRedirect("/")
			except BadHeaderError:
				print("JE PASSE DANS LERREUR MAIL CONTACT")



	events_dates_tuples = retreive_events()
	events_dates = construct_list_of_dates(events_dates_tuples)

	return render(request, 'index.html', locals())

def send_confirmation_mail(name, from_email, good_date_resa):
	events_dates = []
	for d in good_date_resa:
		date = d[8:10] + '/' + d[5:7] + '/' + d[:4]
		events_dates.append(date)

	try:
		message_name = "Cher " + name + ",\n\n"
		message_dudu = name + " vient de réserver pour "
		subject = "Confirmation de votre réservation"

		if len(events_dates) == 1:
			message_name += "Nous avons bien pris en compte votre réservation pour le " + events_dates[0]
			message_dudu += "le " + events_dates[0]
		else:
			events_dates_str = ""
			for i in range(len(events_dates)):
				if i < (len(events_dates)-1):
					events_dates_str += events_dates[i] + " - "
				else:
					events_dates_str += events_dates[i]

			message_name += "Nous avons bien pris en compte votre réservation pour les " + events_dates_str
			message_dudu += "les " + events_dates_str

		message_name += "\nNous vous contacterons par téléphone environ une semaine avant votre évènement. \n\nBien à vous, \nL'équipe Chez DUDU"
		send_mail(subject, message_name, settings.EMAIL_HOST_USER, [from_email])

		#### Sending mail to sallechezdudu@gmail.com to prevent of the new booking
		subject = "Nouvelle réservation"
		message_dudu += "\nVoir l'agenda google pour plus d'informations sur la résa !" 
		send_mail(subject, message_dudu, from_email, [settings.EMAIL_HOST_USER])
	except BadHeaderError:
		print("JE PASSE DANS LERREUR MAIL RESA")

def check_dates_before_creation(events_dates, good_date_resa):
	events_dates_2 = []
	is_possible = True
	for d in good_date_resa:
		date = d[8:10] + '/' + d[5:7] + '/' + d[:4]
		events_dates_2.append(date)

	for d1 in events_dates:
		for d2 in events_dates_2:
			if d2 == d1:
				is_possible = False

	return is_possible

def create_event(name, email, phone, good_date_resa, presta, needs, description):
	global event
	global service
	needs_str = "Besoins : ["
	for i in range(len(needs)):
		if i < (len(needs)-1):
			needs_str += needs[i] + ", " 
		else:
			needs_str += needs[i]
	needs_str += "]"
	local_event = dict(event)
	local_event['summary'] = name + ' | ' + email + ' | ' + phone + ' | Réservation pour pesta : ' + presta  
	local_event['description'] = description + " || " + needs_str
	local_event['start']['dateTime'] = good_date_resa[0] + BETWEEN_DATE_AND_TIME + '17:00' + UTC_France
	local_event['end']['dateTime'] = good_date_resa[-1] + BETWEEN_DATE_AND_TIME + '17:00' + UTC_France
	service.events().insert(calendarId='primary', body=local_event).execute()


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


def convert_js_to_google(date):
	month_letter = date[4:7]
	month = dico_months[month_letter]
	day = date[8:10]
	year = date[11:15]

	return year+'-'+month+'-'+day

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
				"./static/credentials.json", SCOPES)
			# flow = InstalledAppFlow.from_client_secrets_file(
				# "/home/seevoid/seevoid.pythonanywhere.com/static/credentials.json", SCOPES)
			creds = flow.run_local_server()
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('calendar', 'v3', credentials=creds)