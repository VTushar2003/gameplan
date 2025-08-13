# Copyright (c) 2025, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now

from gameplan.mixins.mentions import HasMentions
from gameplan.mixins.reactions import HasReactions
from gameplan.mixins.tags import HasTags


class GPChatMessage(HasMentions, HasReactions, HasTags, Document):
	# Class Configuration
	on_delete_set_null = ["GP Notification"]
	mentions_field = "content"
	tags_field = "content"

	def as_dict(self, *args, **kwargs):
		d = super().as_dict(*args, **kwargs)
		return d

	def validate(self):
		# Basic validation - ensure message has content
		if not self.content or not self.content.strip():
			frappe.throw("Message content is required")

		# Validate project tool belongs to the project
		if self.pod:
			tool_project = frappe.db.get_value("GP Pod", self.pod, "project")
			if not tool_project:
				frappe.throw("Project tool not found")
			if str(tool_project) != str(self.project):
				frappe.throw(
					f"Project tool does not belong to the selected project. "
					f"Tool project: {tool_project}, Expected: {self.project}"
				)

	def after_insert(self):
		# Notify mentions
		self.notify_mentions()

	def on_update(self):
		# Handle reactions notifications
		self.notify_reactions()

	@frappe.whitelist()
	def edit_message(self, content):
		"""Edit the message content"""
		self.content = content
		self.edited_at = now()
		self.save()
		return self

	def before_save(self):
		# Set team from project if not already set
		if self.project and not getattr(self, "team", None):
			team = frappe.db.get_value("GP Project", self.project, "team")
			if team:
				self.team = team
