from django.contrib.auth.tokens import PasswordResetTokenGenerator  # usually it is used to generate a reset password

from six import text_type

class TOkenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) # make hash based on user id and time
        )


generate_token = TOkenGenerator()   # create an object
        

"""_make_hash_value => Hash the user's primary key, email (if available), and some user state that's sure to change after a password reset to produce a token that is invalidated when it's used:"""
