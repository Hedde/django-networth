django-networth
===
*Valuate instances of Django Models.*

#### Installation

    $ pip install django-networth

#### Examples

##### Using django-taggit

    class Object(NetworthModel):
        first_name = models.CharField(max_length=25)
        last_name = models.CharField(max_length=75, blank=True, null=True)
    
        tags = TaggableManager(through=TaggedItem, blank=True)
        
        other_tags = TaggableManager(through=OtherTaggedItem, blank=True)
    
        class Networth:
            fields = (
                ('first_name', (True, 1)),
                ('last_name', (lambda f: f.startswith('P'), 5)),
                ('tags', (lambda f: f.count(), 'result')),
                ('other_tags', (lambda f: f.count(), lambda result: result * 2))
            )

Consider the following pseudo instances (first_name, last_name, tags, other_tags,):

    ('Pete', None, None, None).networth()
    >>> 1
    ('Pete', 'James', None, None).networth()
    >>> 1
    ('Pete', 'Philly', None, None).networth()
    >>> 6
    ('Pete', 'Philly', <TagManager (1 tag)>, None).networth()
    >>> 7
    ('Pete', 'Philly', <TagManager (1 tag)>, <OtherTagManager (1 tag)>).networth()
    >>> 8

In the penultimate example 'result' defines to use the outcome of the function 
itself as the net result, the last example defines a callable, which in this case
is used to multiply the result by a factor 2.


##### Declaring your own Networh logic:

    from networth.models import NetworthModel as BaseNetworthModel

    class NetworthModel(BaseNetworthModel):
        def networth(self):
            return super(NetworthModel, self).networth()
            
            
##### Using celery

    # models.py
    
    from celery import current_app
    from celery.contrib.methods import task_method
    from networth.models import NetworthModel


    class Pizza(NetworthModel):
        name = models.CharField(max_length=140, blank=True, null=True)
        toppings = models.ForeignKey('takeaway.Topping', null=True)
    
        class Meta:
            verbose_name = _(u"Pizza")
            verbose_name_plural = _(u"Pizze")
    
        class Networth:
            fields = (
                ('name', (True, 0)),
                ('toppings', (lambda m: m.count(), 'result'))
            )
    
        @current_app.task(filter=task_method)
        def _networth(self, commit=False):
            return super(Lawyer, self)._networth(commit)

    # views.py

    class PizzaDetailView(DetailView):
        queryset = Pizza.objects.all()
        
        def render_to_response(self, context, **response_kwargs):    
            self.object._networth.delay(commit=True)
            
            return super(PizzaDetailView, self).render_to_response(context, **response_kwargs)
            
    # pizza_detail.html
    
    <div>{{ object.networth }}</div>
