from .demo import *
SITE = Site(
    globals(), remote_user_header='REMOTE_USER',
    strict_dependencies=False)

