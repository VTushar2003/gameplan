# Copyright (c) 2022, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

from urllib.parse import urljoin

import frappe
import requests
from bs4 import BeautifulSoup
from frappe.model.document import Document
from pypika.terms import ExistsCriterion

import gameplan
from gameplan.api import invite_by_email
from gameplan.gemoji import get_random_gemoji
from gameplan.mixins.archivable import Archivable
from gameplan.mixins.manage_members import ManageMembersMixin


class GPProject(ManageMembersMixin, Archivable, Document):
	on_delete_cascade = [
		"GP Task",
		"GP Discussion",
		"GP Project Visit",
		"GP Followed Project",
		"GP Page",
		"GP Pinned Project",
	]
	on_delete_set_null = ["GP Notification"]

	@staticmethod
	def get_list_query(query):
		Project = frappe.qb.DocType("GP Project")
		Member = frappe.qb.DocType("GP Member")
		member_exists = (
			frappe.qb.from_(Member)
			.select(Member.name)
			.where(Member.parenttype == "GP Project")
			.where(Member.parent == Project.name)
			.where(Member.user == frappe.session.user)
		)
		query = query.where(
			(Project.is_private == 0) | ((Project.is_private == 1) & ExistsCriterion(member_exists))
		)
		if gameplan.is_guest():
			GuestAccess = frappe.qb.DocType("GP Guest Access")
			project_list = GuestAccess.select(GuestAccess.project).where(
				GuestAccess.user == frappe.session.user
			)
			query = query.where(Project.name.isin(project_list))

		return query

	@staticmethod
	def get_list(query):
		Project = frappe.qb.DocType("GP Project")
		Member = frappe.qb.DocType("GP Member")
		member_exists = (
			frappe.qb.from_(Member)
			.select(Member.name)
			.where(Member.parenttype == "GP Project")
			.where(Member.parent == Project.name)
			.where(Member.user == frappe.session.user)
		)
		query = query.where(
			(Project.is_private == 0) | ((Project.is_private == 1) & ExistsCriterion(member_exists))
		)
		if gameplan.is_guest():
			GuestAccess = frappe.qb.DocType("GP Guest Access")
			project_list = GuestAccess.select(GuestAccess.project).where(
				GuestAccess.user == frappe.session.user
			)
			query = query.where(Project.name.isin(project_list))

		return query

	def as_dict(self, *args, **kwargs) -> dict:
		d = super().as_dict(*args, **kwargs)
		return d

	def before_insert(self):
		if not self.icon:
			self.icon = get_random_gemoji().emoji
		self.append("members", {"user": frappe.session.user})

	def update_discussions_count(self):
		total_discussions = frappe.db.count("GP Discussion", filters={"project": self.name})
		self.db_set("discussions_count", total_discussions)

	def update_tasks_count(self):
		total_tasks = frappe.db.count("GP Task", filters={"project": self.name})
		self.db_set("tasks_count", total_tasks)

	@frappe.whitelist()
	def move_to_team(self, team=None):
		if self.team == team:
			return
		self.team = team
		self.save()
		for doctype in ["GP Task", "GP Discussion"]:
			for name in frappe.db.get_all(doctype, {"project": self.name}, pluck="name"):
				doc = frappe.get_doc(doctype, name)
				doc.team = self.team
				doc.save()

	@frappe.whitelist()
	def get_merge_preview(self, project=None):
		"""Get a preview of what will happen when merging with another project"""
		if not project or self.name == project:
			frappe.throw("Invalid project for merge")
		if isinstance(project, str):
			project = int(project)
		if not frappe.db.exists("GP Project", project):
			frappe.throw(f'Invalid Project "{project}"')

		target_project = frappe.get_doc("GP Project", project)
		source_project_title = self.title

		# Get pods from both projects
		source_pods = frappe.get_all(
			"GP Pod", filters={"project": self.name}, fields=["name", "type", "title", "enabled"]
		)
		target_pods = frappe.get_all(
			"GP Pod", filters={"project": project}, fields=["name", "type", "title", "enabled"]
		)

		# Calculate new pod titles with prefix
		pods_to_add = []
		for pod in source_pods:
			# Create new title with source project prefix
			new_title = f"{source_project_title}: {pod.title}"

			# Check for title conflicts and add suffix if needed
			existing_titles = [p["title"] for p in target_pods] + [p["new_title"] for p in pods_to_add]
			counter = 2
			original_new_title = new_title
			while new_title in existing_titles:
				new_title = f"{original_new_title} ({counter})"
				counter += 1

			pods_to_add.append(
				{
					"type": pod.type,
					"original_title": pod.title,
					"new_title": new_title,
					"enabled": pod.enabled,
				}
			)

		# Get members from both projects
		source_members = [m.user for m in self.members]
		target_members = [m.user for m in target_project.members]
		members_to_add = [user for user in source_members if user not in target_members]

		# Get content counts that will be moved
		discussions_count = frappe.db.count("GP Discussion", {"project": self.name})
		tasks_count = frappe.db.count("GP Task", {"project": self.name})
		pages_count = frappe.db.count("GP Page", {"project": self.name})
		chat_messages_count = frappe.db.count("GP Chat Message", {"project": self.name})

		return {
			"source_project": {"name": self.name, "title": self.title},
			"target_project": {"name": target_project.name, "title": target_project.title},
			"pods_to_add": pods_to_add,
			"existing_target_pods": [{"type": p["type"], "title": p["title"]} for p in target_pods],
			"members_to_add": members_to_add,
			"content_counts": {
				"discussions": discussions_count,
				"tasks": tasks_count,
				"pages": pages_count,
				"chat_messages": chat_messages_count,
				"total": discussions_count + tasks_count + pages_count + chat_messages_count,
			},
		}

	@frappe.whitelist()
	def merge_with_project(self, project=None):
		if not project or self.name == project:
			return
		if isinstance(project, str):
			project = int(project)
		if not frappe.db.exists("GP Project", project):
			frappe.throw(f'Invalid Project "{project}"')

		# Get merge preview data before starting the merge
		merge_data = self.get_merge_preview(project)
		target_project = frappe.get_doc("GP Project", project)

		# Update existing pods instead of creating new ones
		source_pods = frappe.get_all(
			"GP Pod", filters={"project": self.name}, fields=["name", "type", "title"]
		)

		for i, pod_info in enumerate(merge_data["pods_to_add"]):
			# Find the corresponding source pod
			source_pod = source_pods[i]
			pod_doc = frappe.get_doc("GP Pod", source_pod["name"])

			# Update the pod to point to the target project with new title
			pod_doc.project = project
			pod_doc.title = pod_info["new_title"]
			pod_doc.save(ignore_permissions=True)

		# Handle member merging - add missing members to target project
		for user in merge_data["members_to_add"]:
			target_project.append("members", {"user": user})

		if merge_data["members_to_add"]:
			target_project.save(ignore_permissions=True)

		# Now perform the standard rename/merge which will handle all the remaining data migration
		return self.rename(project, merge=True, validate_rename=False, force=True)

	@frappe.whitelist()
	def invite_guest(self, email):
		invite_by_email(email, role="Gameplan Guest", projects=[self.name])

	@frappe.whitelist()
	def remove_guest(self, email):
		name = frappe.db.get_value("GP Guest Access", {"project": self.name, "user": email})
		if name:
			frappe.delete_doc("GP Guest Access", name)

	@frappe.whitelist()
	def track_visit(self):
		if frappe.flags.read_only:
			return

		values = {"user": frappe.session.user, "project": self.name}
		existing = frappe.db.get_value("GP Project Visit", values)
		if existing:
			visit = frappe.get_doc("GP Project Visit", existing)
			visit.last_visit = frappe.utils.now()
			visit.save(ignore_permissions=True)
		else:
			visit = frappe.get_doc(doctype="GP Project Visit")
			visit.update(values)
			visit.last_visit = frappe.utils.now()
			visit.insert(ignore_permissions=True)

	@property
	def is_followed(self):
		return bool(
			frappe.db.exists("GP Followed Project", {"project": self.name, "user": frappe.session.user})
		)

	@frappe.whitelist()
	def follow(self):
		if not self.is_followed:
			frappe.get_doc(doctype="GP Followed Project", project=self.name).insert(ignore_permissions=True)

	@frappe.whitelist()
	def unfollow(self):
		follow_id = frappe.db.get_value(
			"GP Followed Project", {"project": self.name, "user": frappe.session.user}
		)
		frappe.delete_doc("GP Followed Project", follow_id)

	@frappe.whitelist()
	def add_member(self, user):
		if user not in [d.user for d in self.members]:
			self.append("members", {"user": user})
			self.save()

	@frappe.whitelist()
	def join(self):
		self.add_member(frappe.session.user)

	@frappe.whitelist()
	def leave(self):
		user = frappe.session.user
		for member in self.members:
			if member.user == user:
				self.remove(member)
				self.save()
				break

	@frappe.whitelist()
	def mark_all_as_read(self):
		"""Mark all discussions as read using a project-level timestamp."""
		user = frappe.session.user
		project_name = self.name
		now = frappe.utils.now()

		project_visit_name = frappe.db.get_value("GP Project Visit", {"user": user, "project": project_name})
		if project_visit_name:
			project_visit_doc = frappe.get_doc("GP Project Visit", project_visit_name)
			project_visit_doc.set("mark_all_read_at", now)
			project_visit_doc.last_visit = now
			project_visit_doc.save(ignore_permissions=True)
		else:
			project_visit_doc = frappe.new_doc("GP Project Visit")
			project_visit_doc.user = user
			project_visit_doc.project = project_name
			project_visit_doc.last_visit = now
			project_visit_doc.set("mark_all_read_at", now)
			project_visit_doc.insert(ignore_permissions=True)


def get_meta_tags(url):
	response = requests.get(url, timeout=2, allow_redirects=True)
	soup = BeautifulSoup(response.text, "html.parser")
	title = soup.find("title").text.strip()

	image = None
	favicon = soup.find("link", rel="icon")
	if favicon:
		image = favicon["href"]

	if image and image.startswith("/"):
		image = urljoin(url, image)

	return {"title": title, "image": image}


@frappe.whitelist()
def get_joined_spaces():
	user = frappe.session.user
	projects = frappe.qb.get_query(
		"GP Project",
		filters={"members.user": user},
		fields=["name"],
	).run(as_dict=True, pluck="name")
	guest_access_projects = frappe.qb.get_query(
		"GP Guest Access", filters={"user": user}, fields=["project"]
	).run(as_dict=True, pluck="project")

	return list(map(str, set(projects + guest_access_projects)))


@frappe.whitelist()
def join_spaces(spaces: list[str] = None):
	if not spaces:
		return
	for space in spaces:
		frappe.get_doc("GP Project", space).join()


@frappe.whitelist()
def leave_spaces(spaces: list[str] = None):
	if not spaces:
		return
	for space in spaces:
		frappe.get_doc("GP Project", space).leave()


@frappe.whitelist()
def mark_all_as_read(spaces: list[str] = None):
	"""Mark all unread discussions as read for multiple spaces at once."""
	if not spaces:
		return
	for space in spaces:
		frappe.get_doc("GP Project", space).mark_all_as_read()


@frappe.whitelist()
def get_unread_count():
	from frappe.query_builder.functions import Count, Sum

	user = frappe.session.user
	joined_projects = get_joined_spaces()

	if not joined_projects:
		return {}

	gd = frappe.qb.DocType("GP Discussion").as_("gd")
	gdv = frappe.qb.DocType("GP Discussion Visit").as_("gdv")
	gpv = frappe.qb.DocType("GP Project Visit").as_("gpv")

	# Case 1: Projects with mark_all_read_at timestamp
	# Check if discussion's last_post_at is after the project's mark_all_read_at
	query1 = (
		frappe.qb.from_(gd)
		.select(gd.project, Count(gd.name).as_("unread_count"))
		.inner_join(gpv)
		.on((gd.project == gpv.project) & (gpv.user == user) & gpv.mark_all_read_at.isnotnull())
		.where(gd.last_post_at > gpv.mark_all_read_at)
		.groupby(gd.project)
	)

	# Case 2: Projects without mark_all_read_at (or NULL)
	# Fall back to individual discussion visit tracking
	query2 = (
		frappe.qb.from_(gd)
		.select(gd.project, Count(gd.name).as_("unread_count"))
		.left_join(gpv)
		.on((gd.project == gpv.project) & (gpv.user == user))
		.left_join(gdv)
		.on((gd.name == gdv.discussion) & (gdv.user == user))
		.where(
			(gpv.name.isnull() | gpv.mark_all_read_at.isnull())
			& (gdv.name.isnull() | (gd.last_post_at > gdv.last_visit))
		)
		.groupby(gd.project)
	)

	# Combine both queries using pypika's UNION operator
	union_query = query1 + query2

	# Create outer query to sum the unread counts per project
	combined = union_query.as_("combined")

	final_query = (
		frappe.qb.from_(combined)
		.select(combined.project, Sum(combined.unread_count).as_("unread_count"))
		.groupby(combined.project)
	)

	result = final_query.run(as_dict=True)
	unread_counts_dict = {row["project"]: row["unread_count"] for row in result}

	return unread_counts_dict
