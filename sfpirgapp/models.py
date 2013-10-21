from django.db import models
from mezzanine.utils.models import AdminThumbMixin
from mezzanine.utils.models import upload_to
from mezzanine.core.fields import RichTextField
from django.contrib.auth.models import User
from mezzanine.core.models import Displayable, Orderable, RichText, Ownable,\
    Slugged
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.related import ForeignKey
import datetime
from sfpirgapp.fields import MyImageField
from mezzanine.pages.fields import MenusField
from django.conf import settings
#from django import forms


class PageLike(Orderable, Displayable, RichText, AdminThumbMixin):
    titles = models.CharField(editable=False, max_length=1000, null=True)
    login_required = models.BooleanField(_("Login required"),
        default=False,
        help_text=_("If checked, only logged in users can view this page"))
    featured_image = MyImageField(verbose_name=_("Featured Image"),
        upload_to=upload_to("images", "uploads/images"),
        format="Image", max_length=255, null=True, blank=True)
    admin_thumb_field = "featured_image"

    class Meta:
        abstract = True


class Profile(models.Model, AdminThumbMixin):
    organization = ForeignKey('Organization', null=True, blank=True)
    user = models.OneToOneField(User)
    date_of_birth = models.DateField(null=True, blank=True)
    title = models.CharField(null=True, blank=True, max_length=255)
    bio = models.TextField(null=True, blank=True)
    photo = MyImageField(verbose_name="Photo",
        upload_to=upload_to("sfpirgapp.Profile.photo", "uploads/profile-photos"),
        format="Image", max_length=255, null=True, blank=True,
        help_text='User photo')
    admin_thumb_field = "photo"
    on_mailing_list = models.BooleanField(default=True, verbose_name='Would you like to be added to our mailing list to receive periodic information about ARX?')


class Testimonial(PageLike):
    user = ForeignKey(User, null=True, blank=True, verbose_name=_("Author"), related_name="testimonials")
    category = ForeignKey('Category', related_name='testimonials')
    author_full_name = models.CharField(verbose_name='Your Full Name', max_length=255, null=True, blank=True)
    author_title = models.CharField(verbose_name='Your Title', max_length=255 ,null=True, blank=True)

    def get_author_full_name(self):
        if self.author_full_name:
            return self.author_full_name
        if self.user:
            return self.user.get_full_name() or self.user.username
        return ''

    def get_author_title(self):
        return self.author_title or (self.user and self.user.profile and self.user.profile.title) or ''

    @models.permalink
    def get_absolute_url(self):
        return ('testimonial', (), {'slug': self.slug})

    class Meta:
        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'


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

    announcements = RichTextField(null=True, blank=True,
                                  verbose_name='Announcements',
                                  help_text='Use this section to let people know about any upcoming events, volunteer opportunities, new initiatives - or just anything you want to draw attention to.')
    meetings = RichTextField(null=True, blank=True,
                                  verbose_name='Meetings',
                                  help_text='Let people know when & where you meet if you have regular meeting times. Don\'t forget you can book the SFPIRG lounge or meeting room to host your meetings.')
    contact_email = models.EmailField(null=True, blank=True, max_length=255,
                                      verbose_name='Contact Email')
    contact_phone = models.CharField(null=True, blank=True, max_length=255,
                                     verbose_name='Contact Telephone')
    links = RichTextField(null=True, blank=True,
                                  verbose_name='Links',
                                  help_text='Either to your website, or anywhere else you want to direct people to')
    facebook_url = models.URLField(null=True, blank=True, max_length=255)
    twitter = models.CharField(null=True, blank=True, max_length=255)
    google_plus_url = models.URLField(null=True, blank=True, max_length=255)
    mailing_list_url = models.URLField(null=True, blank=True, max_length=255,
                                       verbose_name='Link to Mailing List',
                                       help_text='You can create a free html email newsletter using mailchimp (www.mailchimp.com). Then people can automatically subscribe to your news. If you already have one, put in your Mailchimp List page address here. Visit mailchimp.com to get it quick')
    is_approved = models.BooleanField(default=False)
    in_menus = MenusField("Show in menus", blank=True, null=True)

    @property
    def richtextpage(self):
        return self

    def in_menu_template(self, template_name):
        if self.in_menus is not None:
            for i, l, t in settings.PAGE_MENU_TEMPLATES:
                if not unicode(i) in self.in_menus and t == template_name:
                    return False
        return True

    @models.permalink
    def get_absolute_url(self):
        return ('action-group', (), {'slug': self.slug})


class Address(models.Model):
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255, default='', blank=True, null=True)
    postal_code = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = u'Addresses'

    def __unicode__(self):
        return '%s %s %s %s' % (self.street, (self.street2 or ''), self.city, self.postal_code)
    __str__ = __unicode__


class Organization(Slugged):
    mailing_city = models.CharField(max_length=255, verbose_name='City')
    mailing_street = models.CharField(max_length=255, verbose_name='Street Address')
    mailing_street2 = models.CharField(max_length=255, default='', blank=True, null=True, verbose_name='Street Address (2nd line)')
    mailing_postal_code = models.CharField(max_length=255, verbose_name='Postal Code')

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
    contact_name = models.CharField(null=True, blank=True, max_length=255, verbose_name='Contact Name',
                            help_text='Who can SFPIRG contact with questions about this project?')
    contact_position = models.CharField(null=True, blank=True, max_length=255, verbose_name='Contact Position',
                                help_text='What position do they hold in the organization?')
    contact_email = models.EmailField(null=True, blank=True, max_length=255, verbose_name='Contact Email')
    contact_alt_email = models.EmailField(null=True, blank=True, max_length=255, verbose_name='Contact Alternative Email')
    contact_phone = models.CharField(null=True, blank=True, max_length=255, verbose_name='Contact Phone Number')


class Liaison(models.Model):
    name = models.CharField(max_length=255, verbose_name='Contact Name',
                            help_text='Who can SFPIRG contact with questions about this project?')
    position = models.CharField(max_length=255, verbose_name='Contact Position',
                                help_text='What position do they hold in the organization?')
    email = models.EmailField(max_length=255, verbose_name='Contact Email')
    alt_email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='Alternative Email')
    phone = models.CharField(max_length=255, verbose_name='Contact Phone Number')
    organization = ForeignKey(Organization, related_name='liaisons')

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
    liaison = ForeignKey(Liaison, blank=True, null=True,
                         help_text='Who can SFPIRG contact with questions about this project?')
    time_per_week = models.TextField(blank=True, null=True,
                                     verbose_name='How much time per week can the Contact/Liaison devote to the student?')
    support_method = models.TextField(blank=True, null=True,
                                      verbose_name='How will the Contact/Liaison provide direction and support to the project?')
    logo = MyImageField(verbose_name="Project Image",
        upload_to=upload_to("sfpirgapp.project", "uploads/project-images"),
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
    project_subject = models.ManyToManyField(ProjectSubject, verbose_name='Project Issues',
                                   help_text=('Please describe the social / environmental issues that are addressed by this project'))
    project_subject_other = models.CharField(blank=True, null=True, max_length=255, verbose_name='Other Issues',
                                             help_text='If you checked "other", please briefly describe your project subject')
    size = models.CharField(null=True, blank=True, max_length=255, verbose_name='Size of Project',
                            help_text=('Please indicate the size of the project in quantifiable terms. '
                                       'e.g. word/page count, duration of radio show or video, number of hours'))
    length = models.CharField(null=True, blank=True, max_length=255, verbose_name='Project Duration',
                            help_text=('Please indicate how many months you expect this project to take. '
                                       'Keep in mind that if your project will take longer than one semester '
                                       'to complete, the pool of students who can do it will be limited to '
                                       'grad students and students who choose to undertake the project '
                                       'independently / not for course credit. Semesters run from Sept-Dec, Jan-Apr & May-Aug.'))
    description_long = models.TextField(blank=True, null=True,
                                   verbose_name='About this Project',
                                   help_text=('Please provide a more detailed description of your project here, with particular focus on specific '
                                              'DELIVERABLES. For example, you might want a 10 page research paper on a topic, '
                                              'plus an executive summary, plus a powerpoint presentation to the organization\'s board of directors'))
    results_plan = models.TextField(blank=True, null=True, verbose_name='Use of Project Results',
                                    help_text='How do you plan to use the results of this project?')
    larger_goal = models.TextField(blank=True, null=True, verbose_name='Deliverables',
                                   help_text='What larger goal is served by undertaking this project?')
    researcher_qualities = models.TextField(blank=True, null=True, verbose_name='The Student Researcher Must Possess',
                                    help_text='What Are You Looking For in a Student Researcher?')
    date_created = models.DateTimeField(auto_now_add=True)
    date_start = models.DateField(blank=True, null=True)
    is_submitted = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_underway = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    is_completed_successfully = models.BooleanField(default=False)
    category = ForeignKey(Category, related_name='arx_projects')
    in_menus = MenusField("Show in menus", blank=True, null=True)

    @property
    def richtextpage(self):
        return self

    def in_menu_template(self, template_name):
        if self.in_menus is not None:
            for i, l, t in settings.PAGE_MENU_TEMPLATES:
                if not unicode(i) in self.in_menus and t == template_name:
                    return False
        return True

    @property
    def organization_title(self):
        try:
            return self.user.profile.organization.title
        except:
            return '[None]'

    @property
    def featured_image(self):
        return self.logo

    @property
    def content(self):
        return self.description_long

    @models.permalink
    def get_absolute_url(self):
        return ('arx-project', (), {'slug': self.slug})

    @models.permalink
    def get_apply_url(self):
        return ('arx-project-apply', (), {'slug': self.slug})

    @property
    def formatted_project_subject(self):
        subjects = [subj.title for subj in self.project_subject.all()]
        if subjects == ['Other']:
            return self.project_subject_other
        return ', '.join(subjects)

    def save(self, *args, **kwargs):
        # Can't save a state that violates consistency
        if self.is_approved and not self.is_submitted:
            return
        if ((self.is_completed_successfully or self.is_finished or self.is_underway)
                and not (self.is_approved and self.is_submitted)):
            return
        if ((self.is_completed_successfully or self.is_finished)
                and not (self.is_approved and self.is_submitted and self.is_underway)):
            return
        if self.is_completed_successfully and not self.is_finished:
            return
        return super(Project, self).save(*args, **kwargs)


class Application(models.Model):
    email = models.EmailField(null=True, blank=True, max_length=255, verbose_name='Your Email')
    project = ForeignKey(Project)
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)
    message = models.TextField()

    def __unicode__(self):
        return '%s: %s (%s...)' % (self.email, self.project.title, self.message[:20])

