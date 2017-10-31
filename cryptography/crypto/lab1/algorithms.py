import re

from django.http import JsonResponse


def validate_data(request, crypt):
    key = ''
    alphabet = ' abcdefghijklmnopqrstuvwxyz'
    data = ''
    if 'key' not in request.POST:
        return {'msg': 'Key is missing'}
    if 'data' not in request.POST:
        return {'msg': 'Data is missing'}
    if 'alphabet' in request.POST and len(request.POST['alphabet']) > 0:
        alphabet = request.POST['alphabet']
    
    key = request.POST['key']
    data = request.POST['data']
    if len(alphabet) == 0:
        return {'msg': 'Alphabet is empty'}
    if len(key) == 0:
        return {'msg': 'Key is empty'}
    if len(data) == 0:
        return {'msg': 'success', 'data': ''}
    
    for x in xrange(len(alphabet) - 1):
        for y in xrange(x+1, len(alphabet)):
            if alphabet.lower()[x] == alphabet.lower()[y]:
                return {'msg': 'Alphabet has duplicate characters'}
    
    ALPHABET_REGEX = r'^[' + ''.join(list(alphabet.lower())) + ']*$'
    ALPHABET_REGEX_UPPER = r'^[' + ''.join(list(alphabet.upper())) + ']*$'

    if crypt == 1 and not re.search(ALPHABET_REGEX, data):
        return {'msg': 'Data contains invalid characters'}
    if crypt == -1 and not re.search(ALPHABET_REGEX_UPPER, data):
        return {'msg': 'Data contains invalid characters'}
    if not re.search(ALPHABET_REGEX_UPPER, key):
        return {'msg': 'Key contains invalid characters'}
    
    return {
        'key': key,
        'alphabet': alphabet,
        'data': data,
    }

def crypto(key, alphabet, data, multiplier):
    key = key.lower()
    data = data.lower()
    alphabet = alphabet.lower()
    out = ''
    for x in xrange(len(data)):
        adds = (len(alphabet) + multiplier * alphabet.index(key[x % len(key)])) % len(alphabet)
        out += alphabet[(alphabet.index(data[x]) + adds) % len(alphabet)]
    if multiplier == 1:
        return out.upper()
    else:
        return out.lower()

def belaso_encrypt(request):
    inp = validate_data(request, 1)
    
    if 'msg' in inp:
        return JsonResponse(inp)
    inp['multiplier'] = 1

    return JsonResponse({'msg': 'success',
                         'data': crypto(**inp)})

def belaso_decrypt(request):
    inp = validate_data(request, -1)
    
    if 'msg' in inp:
        return JsonResponse(inp)
    inp['multiplier'] = -1
    
    return JsonResponse({'msg': 'success',
                         'data': crypto(**inp)})