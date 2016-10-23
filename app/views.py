from django.shortcuts import render
from django.http import JsonResponse
import string

def string_to_hex(request):
	a = request.GET.get('string')
	a = a.lower()

	a = a.replace(' ','')
	if len(a)%3 != 0:
		a += a[-1]*(3 - len(a)%3)

	a_list = []

	for i in range(0,len(a),3):
		a_list.append(a[i:i+3])


	alpha = list(string.ascii_lowercase)
	number = list(range(0,len(alpha)))



	values = []
	for i in a_list:
		hex_value = ''
		temp = [ str(number[alpha.index(ic)])  for ic in list(i)]
		for j in range(0,len(temp)):
			if len(temp[j]) == 1:
				temp[j] = '0' + temp[j]

			hex_value2 = hex(int(temp[j]))[2:]
			if len(hex_value2) == 1:
				hex_value2 = '0' + hex_value2
			hex_value += hex_value2

		if len(values)>0:
			for i in range(0,3):
				values[i] =  str(int(values[i]) * int(temp[i]))[:2]
		else:
			values = temp

	hex_value = ''
	for i in values:
		hex_value2 = hex(int(i))[2:]
		if len(hex_value2) == 1:
			hex_value2 =  '0'+ hex_value2
		hex_value += hex_value2

	return JsonResponse({'value': hex_value})

def home(request):
	return render(request, 'app/home.html', {
		'title' : 'Be Project',
		})