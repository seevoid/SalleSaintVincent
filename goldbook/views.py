from django.shortcuts import render
from .models import GoldenMessage
from .forms import GoldenForm

# Create your views here.

def goldenbook(request):

	if request.method == 'POST':
		golden_form = GoldenForm(request.POST)
		if golden_form.is_valid():

			post_dict = request.POST.dict()
			print("post_dict : ", post_dict)

			name = golden_form.cleaned_data['name']
			title = golden_form.cleaned_data['title']
			message = golden_form.cleaned_data['message']
			rate = golden_form.cleaned_data['rate']

			goldenmessage = GoldenMessage()
			goldenmessage.name = name
			goldenmessage.title = title
			goldenmessage.message = message
			goldenmessage.rate = int(rate)
			goldenmessage.save()

	goldenmessages = GoldenMessage.objects.all()
	return render(request, 'goldenbook_minified.html', locals())