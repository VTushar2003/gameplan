# Copyright (c) 2022, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from gameplan.mixins.mentions import HasMentions
from gameplan.mixins.reactions import HasReactions
from gameplan.mixins.tags import HasTags
from gameplan.search_sqlite import GameplanSearch, GameplanSearchIndexMissingError
from gameplan.utils import remove_empty_trailing_paragraphs


class GPComment(HasMentions, HasReactions, HasTags, Document):
	on_delete_set_null = ["GP Notification", "GP Discussion"]
	mentions_field = "content"
	tags_field = "content"

	def before_insert(self):
		if self.reference_doctype not in ["GP Discussion"]:
			return

		reference_doc = frappe.get_doc(self.reference_doctype, self.reference_name)
		if reference_doc.meta.has_field("closed_at"):
			if reference_doc.closed_at:
				frappe.throw("Cannot add comment to a closed discussion")

	def after_insert(self):
		self.update_discussion_meta()
		self.update_task_meta()

	def after_delete(self):
		self.update_discussion_meta()
		self.update_task_meta()

	def before_save(self):
		self.update_tags()

	def update_discussion_meta(self):
		if self.reference_doctype != "GP Discussion":
			return
		discussion = frappe.get_doc("GP Discussion", self.reference_name)
		discussion.update_last_post()
		discussion.update_post_count()
		discussion.update_participants_count()
		discussion.track_visit()
		discussion.save(ignore_permissions=True)

	def update_task_meta(self):
		if self.reference_doctype != "GP Task":
			return
		frappe.get_doc("GP Task", self.reference_name).update_comments_count()

	def validate(self):
		self.content = remove_empty_trailing_paragraphs(self.content)
		self.de_duplicate_reactions()

	def on_update(self):
		self.update_search_index()
		self.notify_mentions()
		self.notify_reactions()

	def on_trash(self):
		self.remove_search_index()

	def update_search_index(self):
		if self.reference_doctype in ["GP Discussion", "GP Task"]:
			try:
				search = GameplanSearch()
				search.index_doc(self)
			except GameplanSearchIndexMissingError:
				pass

	def remove_search_index(self):
		try:
			search = GameplanSearch()
			search.remove_doc(self)
		except GameplanSearchIndexMissingError:
			pass
