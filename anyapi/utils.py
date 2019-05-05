def retry_until(condition):
    def retry(request):
        try:
            return request()
        except Exception as e:
            if condition():
                return retry(request)
            else:
                raise e

    return retry


def retry(max_retries):
    retries = [0]

    def retry_count():
        retries[0] += 1
        return retries[0]

    return retry_until(lambda: retry_count() != max_retries)
