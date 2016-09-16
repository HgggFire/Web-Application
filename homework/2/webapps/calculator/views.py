from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

def notFound(request):
    return render(request, 'not_found.html')

def calc(request):
    context = {}
    context['newnum'] = 0
    context['prev'] = ''

    # Retrieve attributes from request
    if 'num' in request.POST:
        num = request.POST['num']
        if 'dig' in request.POST:
            dig = request.POST['dig']
            new_num = int(num)*10 + int(dig)

            # if previous operation is '=', then we just
            # display the dig as the new num (a new computation)
            if 'last_btn' in request.POST:
                if request.POST['last_btn'] == '=':
                    new_num = int(dig)

        else:
            new_num = int(num)
        context['newnum'] = new_num
        context['last_btn'] = request.POST['num']

    if 'prev' in request.POST:
        context['prev'] = request.POST['prev']


    if 'prev_op' in request.POST:
        context['prev_op'] = request.POST['prev_op']


    # print('prev_num:'+context['prev'])

    if 'opr' in request.POST:
        # print(request.POST['opr'])
        # print('prevnum:'+context['prev'])
        # print('prevop:'+context['prev_op'])
        # print('num:'+ str(request.POST['num']))

        # hopefully this 0 is never the case (result will be overwritten by following steps)
        # result = 0

        # first operation, return result as the currently displaying number: num
        if 'last_btn' in request.POST:
            last_btn = request.POST['last_btn']
            if last_btn == '+' or last_btn == '-' or last_btn == 'x' or last_btn == '/':
                context['prev_op'] = request.POST['opr']
                context['prev'] = request.POST['prev']
                context['last_btn'] = request.POST['opr']
                context['result'] = request.POST['prev']
                if request.POST['opr'] == '=':
                    context['newnum'] = request.POST['prev']
                else:
                    context['newnum'] = 0
                print(request.POST['prev'])
                return render(request, 'calc.html', context)

        if request.POST['num'] == 'ERROR:Invalid_Operation':
            context['result'] = 0
            context['prev_op'] = ''
            context['prev'] = ''
            context['last_btn'] = ''
            context['newnum'] = 0
            return render(request, 'calc.html', context)

        if context['prev_op'] == '' or (not 'prev' in request.POST):
            # print('op empty')
            result = int(request.POST['num'])
        # not the first operation. return prev + num
        elif context['prev_op'] == '+':
            # print('op+')
            result = int(context['prev']) + int(request.POST['num'])
        elif context['prev_op'] == '-':
            # print('op-')
            result = int(context['prev']) - int(request.POST['num'])
        elif context['prev_op'] == 'x':
            # print('opx')
            result = int(context['prev']) * int(request.POST['num'])
        elif context['prev_op'] == '/':
            # print('op/')
            if int(request.POST['num']) == 0:
                result = 'ERROR:Invalid_Operation'
            else:
                result = int(context['prev']) / int(request.POST['num'])
        elif context['prev_op'] == '=':
            # print('op=')
            result = int(request.POST['num'])
            # if 'last_btn' in request.POST and request.POST['last_btn'] != '' and re
        else:
            # print('result:' + str(result))
            result = int(request.POST['num'])

        if result == 'ERROR:Invalid_Operation':
            context['prev_op'] = ''
            context['prev'] = ''
        else:
            context['prev_op'] = request.POST['opr']
            # store result as prev anyway.
            context['prev'] = str(result)

        if context['prev_op'] == '=':
            context['newnum'] = result
            print('result:' + str(result))
        else:
            context['result'] = result
            # newnum is 0 from initial value at the beginning of the program.
            # However this 0 won't be dispalyed, and 'result' is displayed instead
            context['newnum'] = 0
        context['last_btn'] = request.POST['opr']

    return render(request, 'calc.html', context)