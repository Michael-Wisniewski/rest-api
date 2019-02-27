from .models import ExamSheet
from django.core.exceptions import ObjectDoesNotExist

class SchoolboyExamSheetValidator(object):
    _is_valid = False
    _error_msg, _error_code, _examsheet = (None,)*3

    def __init__(self, pk):
        try:
            self._examsheet = ExamSheet.objects.get(pk=pk)
            if self._examsheet.deleted:
                self._error_msg = 'This exam is no longer available.'
                self._error_code = 410
            elif not self._examsheet.available:
                self._error_msg = 'This exam is not available at this moment.'
                self._error_code = 404
            else:
                self._is_valid = True
        except ObjectDoesNotExist:
            self._error_msg = 'The exam sheet does not exist.'
            self._error_code = 404

    def is_valid(self):
        return self._is_valid

    def get_errors(self):
        return {'data': {'message': self._error_msg}, 'status': self._error_code}

    def get_examsheet(self):
        return self._examsheet