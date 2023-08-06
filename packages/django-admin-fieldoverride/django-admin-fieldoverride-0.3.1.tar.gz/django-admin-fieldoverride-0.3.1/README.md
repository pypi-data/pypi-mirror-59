# django-admin-fieldoverride
A system for allowing a local model to override readonly fields from other source, e.g., from an API (PBSMM, FMP)

## Background

For project that use external APIs (e.g, PBSMM or FMP), the content that is pulled is meant to be read-only.
However sometimes, producers want to override specific fields for specific instances: e.g., for a PBSMMEpisode record, they
might want to use a different description than the one that comes from the API.

Typically, things are set up so that there's a "local" model instance that has a 1:1 relationship to the record obtained from the API, 
e.g., for PBSMM there's a PBSMMEpisode model that has a description_long field.   One COULD just create all of the fields in the local
model, and then set up methods to peruse them when generating content in a view.   However that will quickly get messy because a) for most cases, an override won't be needed; and b) you end up coding all those extra fields "just in case" without absolutely knowing that they'll 
ever be used.

This makes the Admin full of cruft which gets in the way of content management.

### Enter Field Overrides

What if - instead - you had a single "override" field that has a FK to the "local" model instance, so that you only have to use it WHEN
you need to.

In this siutation, the Admin is simplified: you just have an Inline admin for ALL of the overrides for that record.

## How it works

You can get the list of fields for any model class through ._meta.fields.   Most of them probably will NOT want to be overridden 
(e.g., the id, and other things like creation dates, etc.).   So we'll have to come up with a way to filter those fields out.   
For the remaining set, it would be a dropdown field in the Admin along with a field for the override content.   Everything gets stored in 
a table that also keeps track of which model is involved (so some kind of generic foreign key).

When processing the record, i.e., a view to generate a detail page, or a REST API endpoint, you'd go through the list of override-able 
fields, check to see if there is an override, and use it, or fall back to the original field from the API data.

(Note that for a project like Roadshow that would involve TWO sources, FMP and PBSMM, but we can use this setup to handle the order of
precedence, AND we can also set it up that for any given overriden field that order can be different).

# Installation

# Creating the model map_override_fields method

Each model needs a map_override_fields method that returns a list of fields that can be overriden.  Each item in the list is a dict that
has the parameters of the override:

* field:  the name of the field when overridden, e.g., 'description'
* overrides: this is a list of the fields that would be overridden, e.g., ["fmp__description", "pbsmm__description_long"]

They're used to populate the choices for the fields in the Override model which also has the field for the overriding content.

SO FAR, the only way I can think to handle the fact that these fields can have different types (e.g., Text versus Integer), is to 
store everything as a TextField, and then on processing re-cast the content as needed.

# In the view

We'll probably want a mixin for this that sets things appropriately in the context.  

