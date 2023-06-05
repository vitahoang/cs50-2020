from apiflask import HTTPError


class LowBalance(HTTPError):
    status_code = 400
    message = "Your balance is too low for this call"
    extra_data = {
        'error_type': 'Balance Error',
        'error_code': '001',
    }


class LowPortfolio(HTTPError):
    status_code = 400
    message = "Your portfolio is too low for this call"
    extra_data = {
        'error_type': 'Portfolio Error',
        'error_code': '002',
    }


class BidZero(HTTPError):
    status_code = 400
    message = "Bid size cannot be zero"
    extra_data = {
        'error_type': 'Balance Error',
        'error_code': '002',
    }
