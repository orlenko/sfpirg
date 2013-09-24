from django.db import models
from mezzanine.utils.models import AdminThumbMixin
from mezzanine.utils.models import upload_to
from mezzanine.core.fields import FileField
from django.contrib.auth.models import User
from mezzanine.core.models import Displayable, Orderable, RichText, Ownable,\
    Slugged
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.related import ForeignKey
import datetime


class PageLike(Orderable, Displayable, RichText, AdminThumbMixin):
    titles = models.CharField(editable=False, max_length=1000, null=True)
    login_required = models.BooleanField(_("Login required"),
        default=False,
        help_text=_("If checked, only logged in users can view this page"))
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=upload_to("images", "images"),
        format="Image", max_length=255, null=True, blank=True)
    admin_thumb_field = "featured_image"

    class Meta:
        abstract = True


class Profile(models.Model, AdminThumbMixin):
    user = models.OneToOneField(User)
    date_of_birth = models.DateField(null=True, blank=True)
    title = models.CharField(null=True, blank=True, max_length=255)
    bio = models.TextField(null=True, blank=True)
    photo = FileField(verbose_name="Photo",
        upload_to=upload_to("sfpirgapp.Profile.photo", "photos"),
        format="Image", max_length=255, null=True, blank=True,
        help_text='User photo')
    admin_thumb_field = "photo"
    organization = ForeignKey('Organization', null=True, blank=True)


class Testimonial(PageLike, Ownable):
    category = ForeignKey('Category', related_name='testimonials')

    @models.permalink
    def get_absolute_url(self):
        return ('testimonial', (), {'slug': self.slug})



class DummyTable(models.Model):
    pass


def DummyEmptyResultSet():
    return DummyTable.objects.filter(pk=-1)


class Category(PageLike, Ownable):
    class Meta:
        verbose_name = u'Category'
        verbose_name_plural = u'Categories'

    @models.permalink
    def get_absolute_url(self):
        return ('category', (), {'slug': self.slug})


class ActionGroup(PageLike, Ownable):
    parent = None # To make it compatible with the side_menu template
    children = DummyEmptyResultSet() # To make it compatible with the side_menu template

    category = ForeignKey(Category, related_name='action_groups')

    @models.permalink
    def get_absolute_url(self):
        return ('action-group', (), {'slug': self.slug})


class Address(models.Model):
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)


class Organization(Slugged):
    mailing_address = ForeignKey(Address)
    mandate = models.TextField(null=True, blank=True,
                               verbose_name="Organization's Goal",
                               help_text="What is your organization's goal or mandate?")
    communities = models.TextField(null=True, blank=True,
                                   verbose_name='Communities you work with',
                                   help_text='What community or communities do you represent or work with?')
    sources_of_funding = models.TextField(verbose_name="Organization's sources of funding",
                                          help_text="What are your organization's principal sources of funding?")
    is_registered = models.BooleanField(default=False, verbose_name='Are you a registered non-profit?')
    website = models.URLField(null=True, blank=True, verbose_name='Website URL',
                              help_text='Website must begin with "http://"')
    contact = ForeignKey('Contact')


class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name='Contact Name',
                            help_text='Who can SFPIRG contact with questions about this projecct?')
    position = models.CharField(max_length=255, verbose_name='Contact Position',
                                help_text='What position do they hold in the organization?')
    email = models.EmailField(max_length=255, verbose_name='Contact Email')
    alt_email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='Alternative Email')
    phone = models.CharField(max_length=255, verbose_name='Contact Phone Number')
    on_mailing_list = models.BooleanField(default=True, verbose_name='Would you like to be added to our mailing list to receive periodic information about ARX?')

    def __unicode__(self):
        return self.name
    __str__ = __unicode__

    def as_p(self):
        retval = '<br/>'.join(['Name: %s' % self.name,
                  'Position: %s' % self.position,
                  'Email: %s %s' % (self.email, self.alt_email),
                  'Phone: %s' % self.phone])
        return '<p>%s</p>' % retval



class ProjectType(Slugged):
    pass


class ProjectSubject(Slugged):
    pass


class Project(Slugged, AdminThumbMixin):
    user = ForeignKey(User)
    liaison = ForeignKey(Contact)
    time_per_week = models.TextField(blank=True, null=True,
                                     verbose_name='How much time per week can the Contact/Liaison devote to the student?')
    support_method = models.TextField(blank=True, null=True,
                                      verbose_name='How will the Contact/Liaison provide direction and support to the project?')
    logo = FileField(verbose_name="Project Image",
        upload_to=upload_to("sfpirgapp.project", "images"),
        format="Image", max_length=255, null=True, blank=True,
        help_text='Please upload an image to represent the project, or your logo. If you do not have one, do not worry, just leave this section blank.')
    admin_thumb_field = "logo"
    description_short = models.TextField(blank=True, null=True,
                                   verbose_name='Research Question / Brief Project Description',
                                   help_text=('What is the central research question you want answered or what project would you like help with? '
                                   'This elevator pitch should be as brief as possible and should be designed to interest the student in your project. '
                                   'You will have a chance later to describe your project in greater detail.'))
    project_type = models.ManyToManyField(ProjectType)
    project_type_other = models.CharField(blank=True, null=True, max_length=255, verbose_name='Other Description',
                            help_text='If you checked "other", please briefly describe your project type')
    project_subject = models.ManyToManyField(ProjectSubject)
    project_subject_other = models.CharField(blank=True, null=True, max_length=255, verbose_name='Other Subject',
                                             help_text='If you checked "other", please briefly describe your project subject')
    size = models.CharField(null=True, blank=True, max_length=255, verbose_name='Size of Project',
                            help_text=('Please indicate the size of the project in quantifiable terms. '
                                       'e.g. word/page count, duration of radio show or video, number of hours'))
    length = models.CharField(null=True, blank=True, max_length=255, verbose_name='Length of Project',
                            help_text=('Please indicate how many months you expect this project to take. '
                                       'Keep in mind that if your project will take longer than one semester '
                                       'to complete, the pool of students who can do it will be limited to '
                                       'grad students and students who choose to undertake the project '
                                       'independently / not for course credit. Semesters run from Sept-Dec, Jan-Apr & May-Aug.'))
    description_long = models.TextField(blank=True, null=True,
                                   verbose_name='Project description',
                                   help_text=('Please provide a more detailed description of your project here, with particular focus on specific '
                                              'DELIVERABLES. For example, you might want a 10 page research paper on a topic, '
                                              'plus an executive summary, plus a powerpoint presentation to the organization\'s board of directors'))
    issues_addressed = models.TextField(blank=True, null=True,
                                   verbose_name='Issues Addressed by the Project',
                                   help_text=('Please describe the social / environmental issues that are addressed by this project'))
    results_plan = models.TextField(blank=True, null=True, verbose_name='Results Plan',
                                    help_text='How do you plan to use the results of this project?')
    larger_goal = models.TextField(blank=True, null=True, verbose_name='What larger goal is served by undertaking this project?',
                                    help_text='')
    researcher_qualities = models.TextField(blank=True, null=True, verbose_name='What Are You Looking For in a Student Researcher?',
                                    help_text='What skills or attributes do you hope the student researcher will possess?')
    date_created = models.DateTimeField(auto_now_add=True)
    date_start = models.DateField(blank=True)
    is_published = models.NullBooleanField(verbose_name='Publish this project',
                                           help_text='Leave this box unchecked to save the project as draft',
                                           null=True,
                                           blank=True,
                                           default=False)
    category = ForeignKey(Category, related_name='arx_projects')

    @models.permalink
    def get_absolute_url(self):
        return ('arx-project', (), {'slug': self.slug})

    @models.permalink
    def get_apply_url(self):
        return ('arx-project-apply', (), {'slug': self.slug})


class Application(models.Model):
    user = ForeignKey(User)
    project = ForeignKey(Project)
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)
    message = models.TextField()