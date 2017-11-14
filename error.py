SERVER_ERR_INTERNAL = 10000
SERVER_ERR_WRONG_PARAM = 10001
SERVER_ERR_DOWNLOAD_FAILED = 10002

SERVER_ERR_DICT = {
    SERVER_ERR_INTERNAL: 'internal error',
    SERVER_ERR_WRONG_PARAM: 'wrong param',
    SERVER_ERR_DOWNLOAD_FAILED: 'download file from internet failed',
}


class ServerException(RuntimeError):
    def __init__(self, err_code, err_detail=None):
        err_msg = '{}, details: {}'.format(SERVER_ERR_DICT.get(err_code, SERVER_ERR_INTERNAL), err_detail)
        super(RuntimeError, self).__init__(str(err_code), err_msg)
        self.err_code = err_code
        self.err_detail = 'None' if err_detail is None else err_detail
        self.err_msg = err_msg


def exception_string(e):
    if isinstance(e, ServerException):
        return e.err_msg
    else:
        import traceback
        return '\n{}\n{}'.format(e, traceback.format_exc())
