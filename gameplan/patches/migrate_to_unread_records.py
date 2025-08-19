# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and Contributors

import frappe
from frappe.model.document import bulk_insert


class UnreadRecordsMigrator:
	"""Migrates existing discussion visits to unread records system."""

	def __init__(self):
		self.discussion_project = {}
		self.user_discussion_visits = {}
		self.discussion_comments = {}
		self.private_project_members = {}
		self.user_project_visits = {}

	def execute(self):
		"""Main execution method for the migration."""
		self._load_data()
		gp_users = self._get_enabled_users()

		for user in gp_users:
			unread_records = self._generate_unread_records_for_user(user)
			if unread_records:
				self._save_unread_records(user, unread_records)

	def _load_data(self):
		"""Load all required data from database."""
		self._load_discussion_visits()
		self._load_discussions()
		self._load_comments()
		self._load_private_project_members()
		self._load_project_visits()

	def _get_enabled_users(self):
		"""Get all enabled GP users."""
		return frappe.qb.get_query(
			"GP User Profile",
			fields=["user"],
			filters={"enabled": 1},
		).run(pluck=True)

	def _load_discussion_visits(self):
		"""Load discussion visit records."""
		discussion_visits = frappe.qb.get_query(
			"GP Discussion Visit",
			fields=["name", "user", "discussion", "last_visit"],
		).run(as_dict=1)

		for visit in discussion_visits:
			key = (visit.user, str(visit.discussion))
			self.user_discussion_visits[key] = visit

	def _load_discussions(self):
		"""Load all discussions."""
		self.all_discussions = frappe.qb.get_query(
			"GP Discussion", fields=["name", "project", "owner", "creation", "last_post_at"]
		).run(as_dict=1)

		for discussion in self.all_discussions:
			self.discussion_project[str(discussion.name)] = discussion.project

	def _load_comments(self):
		"""Load comments and group by discussion."""
		all_comments = frappe.qb.get_query(
			"GP Comment",
			fields=["name", "reference_name as discussion", "owner", "creation"],
			filters={"reference_doctype": "GP Discussion"},
		).run(as_dict=1)

		for comment in all_comments:
			self.discussion_comments.setdefault(comment.discussion, []).append(comment)

	def _load_private_project_members(self):
		"""Load private project members for access control."""
		private_projects = frappe.get_all("GP Project", fields=["name"], filters={"is_private": 1})

		for project in private_projects:
			members = frappe.get_all(
				"GP Member", filters={"parent": project.name, "parenttype": "GP Project"}, pluck="user"
			)
			self.private_project_members[str(project.name)] = set(members)

	def _load_project_visits(self):
		"""Load project visit records."""
		project_visits = frappe.qb.get_query(
			"GP Project Visit",
			fields=["user", "project", "mark_all_read_at"],
			filters={"mark_all_read_at": ["is", "set"]},
		).run(as_dict=1)

		for visit in project_visits:
			key = (visit.user, visit.project)
			self.user_project_visits[key] = visit

	def _generate_unread_records_for_user(self, user):
		"""Generate unread records for a specific user."""
		unread_records = []
		discussion_counts = 0
		comment_counts = 0

		for discussion in self.all_discussions:
			if not self._should_process_discussion(user, discussion):
				continue

			last_timestamp = self._get_last_read_timestamp(user, discussion)

			if last_timestamp is None:
				# No visit record - create unread records for discussion and all comments
				discussion_record, comment_records = self._create_records_for_unvisited_discussion(
					user, discussion
				)
				unread_records.append(discussion_record)
				unread_records.extend(comment_records)
				discussion_counts += 1
				comment_counts += len(comment_records)
			else:
				# Create unread records only for unread comments
				comment_records = self._create_records_for_unread_comments(user, discussion, last_timestamp)
				unread_records.extend(comment_records)
				comment_counts += len(comment_records)

		if unread_records:
			print(f"Generated {len(unread_records)} unread records for user: {user}")
			print(f"Discussion counts: {discussion_counts}, Comment counts: {comment_counts}")

		return unread_records

	def _should_process_discussion(self, user, discussion):
		"""Check if discussion should be processed for the user."""
		# Skip discussions owned by the user
		if discussion.owner == user:
			return False

		# Check private project access
		if discussion.project in self.private_project_members:
			if user not in self.private_project_members[discussion.project]:
				return False

		return True

	def _get_last_read_timestamp(self, user, discussion):
		"""Get the last timestamp when the user read the discussion."""
		# Check discussion visit
		key = (user, str(discussion.name))
		visit = self.user_discussion_visits.get(key)
		last_visit_timestamp = visit.last_visit if visit else None

		# Check project-level mark all as read
		project_visit = self.user_project_visits.get((user, discussion.project))
		if project_visit and project_visit.mark_all_read_at:
			if discussion.creation <= project_visit.mark_all_read_at:
				# Discussion was marked as read at project level
				return discussion.creation

		mark_all_as_read_timestamp = project_visit.mark_all_read_at if project_visit else None

		# Return the latest timestamp
		return (
			max(last_visit_timestamp, mark_all_as_read_timestamp)
			if last_visit_timestamp and mark_all_as_read_timestamp
			else last_visit_timestamp or mark_all_as_read_timestamp
		)

	def _create_records_for_unvisited_discussion(self, user, discussion):
		"""Create unread records for a discussion that was never visited."""
		discussion_record = self._create_unread_record(
			user=user, discussion=discussion, creation=discussion.creation, owner=discussion.owner
		)

		comment_records = []
		comments = self.discussion_comments.get(str(discussion.name), [])

		for comment in comments:
			if comment.owner != user:  # Skip comments owned by the user
				comment_record = self._create_unread_record(
					user=user,
					discussion=discussion,
					comment=comment,
					creation=comment.creation,
					owner=comment.owner,
				)
				comment_records.append(comment_record)

		return discussion_record, comment_records

	def _create_records_for_unread_comments(self, user, discussion, last_timestamp):
		"""Create unread records for comments that are unread."""
		comment_records = []
		comments = self.discussion_comments.get(str(discussion.name), [])

		for comment in comments:
			if comment.owner != user and comment.creation > last_timestamp:
				comment_record = self._create_unread_record(
					user=user,
					discussion=discussion,
					comment=comment,
					creation=comment.creation,
					owner=comment.owner,
				)
				comment_records.append(comment_record)

		return comment_records

	def _create_unread_record(self, user, discussion, comment=None, creation=None, owner=None):
		"""Create a single unread record."""
		record_data = {
			"doctype": "GP Unread Record",
			"name": frappe.db.get_next_sequence_val("GP Unread Record"),
			"user": user,
			"discussion": str(discussion.name),
			"project": str(discussion.project),
			"is_unread": 1,
			"creation": creation,
			"modified": creation,
			"owner": owner,
		}

		if comment:
			record_data["comment"] = str(comment.name)

		return frappe.get_doc(record_data)

	def _save_unread_records(self, user, unread_records):
		"""Save unread records to database."""
		bulk_insert("GP Unread Record", unread_records, ignore_duplicates=True)


def execute():
	"""Entry point for the migration patch."""
	migrator = UnreadRecordsMigrator()
	migrator.execute()
