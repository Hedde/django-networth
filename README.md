django-networth
===
*valued instances*

#### Examples

##### Using django-taggit

    class Object(NetworthModel):
        first_name = models.CharField(max_length=25)
        last_name = models.CharField(max_length=75, blank=True, null=True)
    
        tags = TaggableManager(through=TaggedItem, blank=True)
    
        class Networth:
            fields = (
                ('first_name', (True, 1)),
                ('last_name', (lambda f: f.startswith('P'), 5)),
                ('tags', (lambda f: f.count(), 'result'))
            )

Consider the following pseudo instances:

    ('Pete',).networth()
    >>> 1
    ('Pete', 'James').networth()
    >>> 1
    ('Pete', 'Philly').networth()
    >>> 6
    ('Pete', 'Philly', <TagManager>).networth()
    >>> 0

In the last example 'result' defines to use the outcome of the function 
itself as the net result. As we have not added any tags to Pete yet, 
the count() will be zero.


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