from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import get_authorization_header
from django.contrib.auth import authenticate
from django.core.exceptions import ImproperlyConfigured
from rest_framework import exceptions, HTTP_HEADER_ENCODING
from rest_framework.authtoken.models import Token
from django.core.context_processors import request
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http.response import HttpResponse

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def get_token(user):
    print "get_token is called"
    print " get -----"
    token, created = Token.objects.get_or_create(user=user)
    print "token =",token.key
    return token.key

    
#we are implementing out own token authenticator because if token is not present then default implementation
#returns valid token
class TokenAuthenticator(TokenAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    model = Token
    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request):
        print "autheniticate is called for ToeknAuthenticator"
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            msg = "token is not present"
            print "token is not present"
            raise exceptions.AuthenticationFailed(msg)
            #return None        

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            print 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            print 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(auth[1])

    def authenticate_credentials(self, key):
        print "autheniticate_credential is called for token auth---->"
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        return (token.user, token)
    
    def authenticate_header(self, request):
        return 'Token'

    '''
    def get_user(self,request):
        auth = get_authorization_header(request).split()
        user,token=self.authenticate_credentials(auth[1])
        return user
    '''    