# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
import base64
from Crypto.Cipher import XOR

from ...models import AdaptorInitParam
from ...models.base import WavesBaseModel
from ...settings import waves_settings
from ...utils.encrypt import Encrypt
from cryptography.fernet import InvalidToken


class ObsoleteEncrypt(object):
    """ Encrypt values based on Django settings secret key substring """

    def __init__(self):
        raise RuntimeError('This class is intended to be used statically')

    @staticmethod
    def decrypt(to_decode):
        """ Decrypt previously encoded 'to_decode'
        :param to_decode: value to decode
        :return: string initial value
        """
        if len(waves_settings.SECRET_KEY) != 32:
            raise RuntimeError('Encoded values must use a key at least a 32 chars length secret')
        cipher = XOR.new(waves_settings.SECRET_KEY)
        return cipher.decrypt(base64.b64decode(to_decode))


class TmpAdaptorInitParam(AdaptorInitParam):

    class Meta:
        app_label = "waves.wcore"
        proxy = True

    @classmethod
    def from_db(cls, db, field_names, values):
        return super(WavesBaseModel, cls).from_db(db, field_names, values)


class Command(BaseCommand):
    help = 'Update the current encrypted values in WAVES database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting patching ...")
        all_encrypted = TmpAdaptorInitParam.objects.filter(crypt=True)
        for encrypted in all_encrypted:
            error = False
            old_decrypted = ""
            try:
                Encrypt.decrypt(bytes(encrypted.value))
                self.stdout.write("Value already encrypted with current algorithm %s" % encrypted.value)
            except InvalidToken:
                self.stdout.write("Updating encrypted value: %s - %s " % (encrypted, encrypted.value))

                try:
                    old_decrypted = ObsoleteEncrypt.decrypt(encrypted.value)
                except StandardError as e:
                    self.stderr.write("An error occured decrypting value with previous cryptography system ")
                    self.stderr.write("Related info [id:%s] [related object:%s] [related id:%s]" % (encrypted.id, encrypted.content_object, encrypted.content_object.id))
                    error = True
                if not error:
                    new_value = Encrypt.encrypt(old_decrypted)
                    encrypted.value = new_value
                    self.stdout.write("Saving new updated value: %s " % encrypted.value)
                    encrypted.save()
        self.stdout.write('Checking current values...')
        try:
            all_encrypted = AdaptorInitParam.objects.filter(crypt=True)
            for decrypted in all_encrypted:
                self.stdout.write('Successfully migrated %s for "%s"' % (decrypted, decrypted.content_object))
        except StandardError as e:
            self.stderr.write("Error occurred while controlling values see log ")
            self.stderr.write(e)
        self.stdout.write("All done ...")
