from django.shortcuts import render
from django.http import JsonResponse
import string
import logging

def int_to_string(a):
	a = str(a).strip()
	if len(a) == 1:
		return "0" + a
	else:
		return a

def string_to_hex(request):
	a = request.GET.get('string')
	a = a.replace('+',' ')
	a = a.lower()

	a = a.replace(' ','')
	if len(a)%3 != 0:
		a += str(a[-1])*(3 - len(a)%3)

	a_n = []

	for i in range(0,len(a),3):
		a_n.append(a[i:i+3])

	alpha = list(string.ascii_lowercase) + [str(i) for i in range(10)]
	# print alpha
	number = list(range(0,len(alpha)))
	values = [0,1,2]
	for i in a_n:
		if len(i) != 3:
			logging.error("Length  not as expected " + i)
		hex_value = ''
		temp = [ number[alpha.index(str(ic))] for ic in i]
		# print temp
		# print values
		for j in range(0,3):
			values[j] =  values[j] + temp[j]
			values[j] = int(int_to_string(values[j])[:2])

	# print values
	hex_value = ''
	for i in values:
		hex_value2 = str(hex(int(i))[2:])
		hex_value2 = int_to_string(hex_value2)
		hex_value += hex_value2
	# print hex_value

	return JsonResponse({'value': hex_value})

def home(request):
	return render(request, 'app/home.html', {
		'title' : 'Be Project',
		})
