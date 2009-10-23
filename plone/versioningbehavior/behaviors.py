
from five import grok
from zope import schema
from zope.component import adapts
from zope.interface import Interface, implements, alsoProvides
from zope.annotation.interfaces import IAnnotations

from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.directives import dexterity
from plone.directives import form

from rwproperty import getproperty, setproperty

from plone.versioningbehavior import MessageFactory as _


class IVersionable(form.Schema):
    """ Behavior for enabling CMFEditions's versioning for dexterity
    content types. Be shure to enable versioning in the plone types
    control-panel for your content type.
    """
    changeNote = schema.TextLine(
            title = _(u'label_change_note', default=u'Change Note'),
            description = _(u'help_change_note', default=u'Enter a comment that describes the changes you made.'),
            required = False,
    )
alsoProvides(IVersionable, IFormFieldProvider)


class IVersioningSupport(Interface):
   """
   Marker Interface for the IVersionable behavior.
   """


class Versionable(object):
    """ The Versionable adapter prohibits dexterity from saving the changeNote
    on the context. It stores it in a request-annotation for later use in
    event-handlers
    """
    implements(IVersionable)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    @getproperty
    def changeNote(self):
        return ''

    @setproperty
    def changeNote(self, value):
        # store the value for later use (see events.py)
        annotation = IAnnotations(self.context.REQUEST)
        annotation['plone.versioningbehavior-changeNote'] = value

