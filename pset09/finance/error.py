from werkzeug.exceptions import HTTPException


class LowBalance(HTTPException):
    status_code = 400
    message = "Your balance is too low for this call"
    extra_data = {
        'error_type': 'Balance Error',
        'error_code': '001',
    }


class LowPortfolio(HTTPException):
    status_code = 400
    message = "Your portfolio is too low for this call"
    extra_data = {
        'error_type': 'Portfolio Error',
        'error_code': '002',
    }


class BidZero(HTTPException):
    status_code = 400
    message = "Bid size cannot be zero"
    extra_data = {
        'error_type': 'Balance Error',
        'error_code': '002',
    }
