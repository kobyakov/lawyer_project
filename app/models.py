from app import db
from webhelpers.text import urlify

ROLE_USER = 0
ROLE_ADMIN = 1

class Category(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(128, collation='utf8_general_ci'), index=True, unique=True)
	slug = db.Column(db.String(128, collation='utf8_general_ci'),index=True, unique=True)

	def __repr__(self):
		return '<category %r>' %(self.name)

	@property
	def slug(self):
		return urlify(self.name)

#class Type(models.Model):
#	type_category = models.ForeignKey(Category)
#	name = models.CharField(max_length=256)
#	slug = models.CharField(max_length=256, unique=True)
#
#	#def save(self, *args, **kwargs):
#	#	self.slug = slugify(self.name)
#	#	super(Category, self).save(*args, **kwargs)
#	
#	def __unicode__(self):
#		return self.name
#
#
#class Contract(models.Model):
#	contract_type = models.ForeignKey(Type)
#	name = models.CharField(max_length=256)
#	contract_template = models.URLField()
#
#	def __unicode__(self):
#		return self.name