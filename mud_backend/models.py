from django.db import models
import string, random

class User(models.Model):
    login = models.CharField(max_length=25)
    token = models.CharField(max_length=64)

    def prefill_token(self, token_length=32):
        letters = (string.ascii_uppercase + string.ascii_lowercase + string.digits) * token_length
        return self.token = ''.join(random.sample(letters, token_length))
