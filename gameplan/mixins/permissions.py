# Copyright (c) 2025, Frappe Technologies Pvt Ltd and contributors


def has_permission(doc, ptype, user):
	if doc.doctype == "GP Page":
		if not doc.project and doc.owner != user:
			# private pages only accessible by owner
			return False

	if doc.doctype == "GP User Profile":
		if ptype == "write":
			# only user can edit their own profile
			return doc.user == user

	# returning True means fallback to default behaviour,
	# it doesn't mean we allow access
	return True
