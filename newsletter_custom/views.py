from newsletter.views import *

class UpdateSubscriptionVievCustom(UpdateSubscriptionViev):
    print 'testando...'
    
    def __init__(self):
        print "teste com init"
    
    def get_initial(self):
        print '123 testando...'
        UpdateSubscriptionViev.get_initial(self)
        #super(self.__class__, self).get_initial(*args, **kwargs)