from django.shortcuts import render

# Create your views here.

def goldenbook(request):
	return render(request, 'goldenbook.html', locals())