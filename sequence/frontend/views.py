from django.template import loader
from django.conf import settings
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse
from frontend.models import NumberForm
import urllib
import urllib2
import simplejson
import string

def home(request):
    number_form = NumberForm()
    out = ''
    out_ct = 0
    input_nums_array = []
    index_array = []
    error_msg = ''
    run_time = 0
    if request.method == "POST":
        # process the form NumberForm with an API call
        number_form = NumberForm(request.POST)
        if number_form.is_valid():
            input_nums = number_form.cleaned_data['number_list']
            input_nums = ''.join(input_nums.splitlines())
            input_nums_array = input_nums.split(',')

            # construct an API call to API server
            params = '{"num_array":"'+input_nums+'","verbose":1}'   
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            headers = {"ContentType":"application/json; charset=utf-8"}
            my_request = urllib2.Request(settings.BASE_URL+'/api/longest/',params,headers) 
            my_request.get_method = lambda: 'POST'
            my_response = opener.open(my_request)
            response_data = simplejson.load(my_response)

            error = response_data.get('error','')
            if error:
                error_msg = error
            else:
                # format out and indexes for the template
                out = response_data.get('out','')
                out_ct = out.count(',') + 1
                out = string.replace(out,',',', ')
                indexes = response_data.get('indexes','')
                index_array = indexes.split(',')
                run_time = response_data.get('time',0)

                number_form = NumberForm()
        
    t = loader.get_template('frontend/home.html')
    c = RequestContext(request, {
        'number_form':number_form,    
        'out':out,
        'out_ct':out_ct,
        'input_nums_array':input_nums_array,
        'index_array':index_array,
        'error_msg':error_msg,
        'run_time':run_time,
    })
    return HttpResponse(t.render(c))



