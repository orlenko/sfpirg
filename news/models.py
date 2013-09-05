from mezzanine.utils.models import AdminThumbMixin
from mezzanine.core.models import Displayable
from mezzanine.core.models import RichText


class NewsPost(Displayable, RichText, AdminThumbMixin):
    pass