# Notes

> So to speak all the modification I did

## Login

- `app.secret_key` should be random. In order to do that:
    - [os.urandom](https://docs.python.org/3/library/os.html#os.urandom)
    - It's random enough for security purpouses


- Authentiaction header:
    - deleted the basic autentication method, [can be cached in the browser](https://security.stackexchange.com/questions/988/is-basic-auth-secure-if-done-over-https) introducing a vulnerabilty (could be used alongside an CSRF).


- Password hashing
    - [to secure hashing the password](https://docs.python.org/3/library/hashlib.html#key-derivation)
    - salt



## Application itself


- 
