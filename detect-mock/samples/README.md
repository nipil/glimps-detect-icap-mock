# Samples

Any file can be submitted and will be "processed" (nothing is done) and a "valid" result is returned.

But if you submit a JSON file with the bellow flags, the mocked application will behave as requested.

## Expectations

Json file, holding object with allowed boolean flags:

- `invalid_token` : generates a 401 error
- `invalid_file` : generates a 400 error
- `bypass_denied` : generates a 403 error
- `quota_exceeded` : generates a 429 error
- `internal_error` : generates a 500 error
- `not_found` : generates a 404 error
- `malware` : if final result should be detected as a malware
- `data` : random string data you can use to simulate different (or random) sha256 sum (for caching)
- `cache_result` : specifies whether the submitted file should be stored in sha256 cache table or not
- `wait_seconds` : amount to wait before marking submission as done (defaults to 0 seconds)
