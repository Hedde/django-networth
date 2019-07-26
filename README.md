django-networth
===
*Valuate instances of Django Models.*

<p><a href="https://vimeo.com/120032556">Use case example</a> from <a href="https://vimeo.com/user37568641">Hedde van der Heide</a> on <a href="https://vimeo.com">Vimeo</a>.</p>

#### Description

    Adds a '_networth' and '_relative_networth' field to your model
    which hold information about the instance's 'total value'.
    
    note: (currently) does not support floats, nor supports negative
          values (i.e. penalties)
    

[![Build Status](https://travis-ci.org/Hedde/django-networth.svg?branch=develop)](https://travis-ci.org/Hedde/django-networth)

#### Installation

    $ pip install django-networth
    
#### Setup

    1. Add 'networth' to your INSTALLED_APPS
    2. Optionally change the default networth setting NETWORTH_DEFAULT
       to a POSITIVE interger (defaults to 1)
    3. Make your model(s) inherit NetworthModel (see below)
    4. Create networth rules (see below)
    5. Run a schemamigration / migrate cycle
    
    note: make sure you inherit the NetworthManager also if you're not 
          using a default manager for your model(s)

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

So,

    1. Networth.fields holds a tuple with tuples
    2. The first value of the tuple has to be the field's name
    3. The second argument must be a tuple with two parts
    
        fields = (
            (field_name, (condition, award)),
        )
    
        a. the condition;
           can be any callable or non callable (e.g. a boolean).
           if callable, receives the instance as its first argument.
        
        b. the award;
           can be any callable or integer, but MUST return an 
           integer.
           if the condition is met, this represents the field's networth 
           return value.
           if callable, receives the condition's result as its first 
           argument.
           
    note: it's perfectly legit to declare the same field twice.
           

Consider the following pseudo instances (first_name, last_name, tags, other_tags,):

    ('Pete', None, None, None).networth()
    >>> 1
    ('Pete', 'James', None, None).networth()
    >>> 1
    ('Pete', 'Philly', None, None).networth()
    >>> 1
    ('Pete', 'Philly', None, None).networth(realtime=True, commit=True)  # commit to db (self._networth)
    >>> 6
    
The penultimate example returned 1 because by default networth() and relative_networth() 
return the database value, to force the realtime value use networth(realtime=True) and 
relative_networth(realtime=True)

    ('Pete', 'Philly', None, None)._networth  # test commit
    >>> 6
    ('Pete', 'Philly', <TagManager (1 tag)>, None).networth(realtime=True, commit=True)
    >>> 7
    ('Pete', 'Philly', <TagManager (1 tag)>, <OtherTagManager (1 tag)>).networth(realtime=True)
    >>> 9
    ('Pete', 'Philly', <TagManager (1 tag)>, <OtherTagManager (1 tag)>)._networth  # I didn't commit !
    >>> 7

In the penultimate example 'result' defines to use the outcome of the function 
itself as the net result, the last example defines a callable, which in this case
is used to multiply the result by a factor 2.

##### Calculating relative networth (requires committed networth for objects to have any useful meaning)

    ('Pete', 'Philly', <TagManager (1 tag)>, <OtherTagManager (1 tag)>).relative_networth(realtime=True, commit=True)
    >>> 100
    ('Pete', 'Philly', <TagManager (1 tag)>, <OtherTagManager (1 tag)>)._relative_networth  # test commit
    >>> 100
    
Relative networth calculates the percentage of the current object's networth compared to the highest valued object known. This can be useful when calculating profile completeness for example.


##### Declaring your own Networth logic:

    from networth.models import NetworthModel as BaseNetworthModel

    class NetworthModel(BaseNetworthModel):
        def networth(self, realtime=False, commit=False):
            return super(NetworthModel, self).networth(realtime=realtime, commit=commit)
            
            
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
        def networth(self, realtime=False, commit=False):
            return super(Pizza, self).networth(realtime=realtime, commit=commit)

    # views.py

    class PizzaDetailView(DetailView):
        queryset = Pizza.objects.all()
        
        def render_to_response(self, context, **response_kwargs):    
            self.object.networth.delay(realtime=True, commit=True)
            
            return super(PizzaDetailView, self).render_to_response(context, **response_kwargs)
            
    # pizza_detail.html
    
    <div>{{ object.networth }}</div>
