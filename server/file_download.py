from django.http import FileResponse
import os
from utils import TMP_DIR


def file_download(request):
    filename = '{}.{}'.format(request.GET.get('uuid', ''), request.GET.get('type', ''))
    file_path = os.path.join(TMP_DIR, filename)
    if os.path.isfile(file_path):
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=\"{}\"'.format(filename)
        return response
    else:
        raise RuntimeError('file not exist')
