import requests
from django.db import models
from django.contrib.postgres.fields import JSONField


class BaseAPISnapshotScraper:
    '''
    BaseAPIScraper for scraping an api.

    Due to the multiple reuse of the same logic when scraping
    for every datasource, this class has been created.

    Attributes:
    -----------
    url: dict
        The url of the api that will be scraped

    model: Django Model class
        The model that the scraped data will be saved
    '''
    url = None
    model = None

    def __init__(self):
        self.params = None
        self.session = None
        self.auth_url = None
        self.headers = {}
        self.validate_class_attributes()

    def validate_class_attributes(self):
        assert isinstance(self.url, str), 'url attribute missing or is not string'
        assert self.model and issubclass(self.model, models.Model), 'model attribute missing or not django model'
        assert isinstance(self.model._meta.get_field('data'), JSONField), \
            'data field is Not a JSONField'

    @property
    def requests(self):
        '''
        Retrieve Session or create new instance.
        Adds the ssl location if it has been added in the class

        Returns:
            Session obj: The requests.Session object
        '''
        if not self.session:
            self.session = requests.Session()
        return self.session

    def authenticate(self):
        '''
        Use this method to send an authentication request and update
        the session headers with the token. This method will be automatically
        called if the 'auth_url' variable is defined in the class.
        '''
        raise NotImplementedError

    def parse(self, response):
        '''
        Parses the response. Default is json, override to change it

        Args:
            response (obj:Response): the response object.

        Returns:
            dict: The json response converted dict
        '''
        return response.json()

    def fetch(self):
        response = self.requests.get(self.url, params=self.params, headers=self.headers)
        return self.parse(response)

    def store(self, data):
        self.model.objects.create(data=data)

    def start(self):
        '''
        Runs the scrape process:
        - Check if auth_url is in the class then calls the authenticate method
        - Fetches the data
        - Stores it in the db
        '''
        if self.auth_url:
            self.authenticate()
        data = self.fetch()
        self.store(data)
