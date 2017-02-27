from rest_framework import serializers, renderers, parsers
import re
import os
import csv
import logging
LOG = logging.getLogger('impaqd')

class ResponseStatusRenderer(renderers.JSONRenderer):
    """
    Default renderer. Should be used on ALL views.

    All views should implement this renderer OR if it implements another
    renderer, this
    `ResponseStatusRenderer.render(ResponseStatusRenderer(), data, *args, **kwargs)`
    should be added as the first line in the render function.
    """

    def render(self, data, *args, **kwargs):
        # default values (Should never be used)
        #code = 0
        #title = 'Error'
        #text = 'We apologize, but something went wrong' 

        #http_status_code = args[1].get('response').status_code
        #response_mappings = []
        #if hasattr(args[1].get('view'), 'status_mappings'):
        #    view_status_mappings = args[1].get('view').status_mappings
        #    response_mappings = [m for m in view_status_mappings if m[0] == http_status_code]
        #if len(response_mappings) > 0:
        #    # First try and get responsestatus from mapping
        #    try:
        #        code = response_mappings[0][1]
        #        status_obj = ResponseStatus.objects.get(code=code)
        #        title = status_obj.title
        #        text = status_obj.text
        #    except Exception, e:
        #        code = 0
        #        import traceback
        #        print traceback.format_exc()
        #        LOG.error(traceback.format_exc())
        #if code == 0:
        #    # Otherwise fall back on default (three digit) codes
        #    try:
        #        code = http_status_code
        #        status_obj = ResponseStatus.objects.get(code=code)
        #        title = status_obj.title
        #        text = status_obj.text
        #    except Exception, e:
        #        code = 0
        #        import traceback
        #        print traceback.format_exc()
        #        LOG.error(traceback.format_exc())
        #status = {'status': {'code' : code, 'title': title, 'text' : text}}
        #data.update(status)
        return super(ResponseStatusRenderer, self).render(data, *args, **kwargs)


#####
# Underscore to CamelCase renderer
# Adapted from https://gist.github.com/johtso/5881137
# recursive_key_map(camelcase_to_underscore, dict) to convert back to underscore
####

class CamelCaseJSONRenderer(renderers.JSONRenderer):
    def render(self, data, *args, **kwargs):
        # Always use ResponseStatusRenderer on all custom renderes
        ResponseStatusRenderer.render(ResponseStatusRenderer(), data, *args, **kwargs)
        if data:
            data = recursive_key_map(underscore_to_camelcase, data)
        return super(CamelCaseJSONRenderer, self).render(data, *args, **kwargs)
 
 
class CamelCaseToJSONParser(parsers.JSONParser):
    def parse(self, *args, **kwargs):
        obj = super(CamelCaseToJSONParser, self).parse(*args, **kwargs)
        return recursive_key_map(camelcase_to_underscore, obj)
 
 
def underscore_to_camelcase(word, lower_first=True):
    result = ''.join(char.capitalize() for char in word.split('_'))
    if lower_first:
        return result[0].lower() + result[1:]
    else:
        return result
 
_first_cap_re = re.compile('(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')
 
 
# http://stackoverflow.com/a/1176023
def camelcase_to_underscore(word):
    s1 = _first_cap_re.sub(r'\1_\2', word)
    return _all_cap_re.sub(r'\1_\2', s1).lower()
 
 
def recursive_key_map(function, obj):
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.iteritems():
            if isinstance(key, basestring):
                key = function(key)
            new_dict[key] = recursive_key_map(function, value)
        return new_dict
    if hasattr(obj, '__iter__'):
        return [recursive_key_map(function, value) for value in obj]
    else:
        return obj
