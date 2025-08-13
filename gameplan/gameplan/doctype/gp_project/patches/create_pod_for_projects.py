# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and Contributors

import frappe


def execute():
	"""Create default project pods for all existing projects based on existing content."""

	# Get all projects
	projects = frappe.get_all("GP Project", fields=["name", "title", "team"])

	if not projects:
		return

	tools_created = {"Discussions": 0, "Tasks": 0, "Documents": 0}
	tools_skipped = {"Discussions": 0, "Tasks": 0, "Documents": 0}
	records_updated = {"Discussions": 0, "Tasks": 0, "Documents": 0}

	for project in projects:
		project_name = project["name"]

		if project["team"]:
			team_title = frappe.db.get_value("GP Team", project["team"], "title")
			if team_title:
				new_project_title = f"{team_title}: {project['title']}"
				frappe.db.set_value(
					"GP Project", project_name, "title", new_project_title, update_modified=False
				)

		# Check for existing discussions and create Discussions pod if found
		discussions_exist = frappe.db.exists("GP Discussion", {"project": project_name})
		if discussions_exist:
			pod_name = create_project_pod(project_name, "Discussions", "Discussions")
			if pod_name:
				if isinstance(pod_name, str):  # New pod was created
					tools_created["Discussions"] += 1
				else:  # Pod already existed
					tools_skipped["Discussions"] += 1

				# Update all discussions to link to this pod
				updated_count = update_records_with_pod("GP Discussion", project_name, pod_name)
				records_updated["Discussions"] += updated_count
			else:
				tools_skipped["Discussions"] += 1

		# Check for existing tasks and create Tasks pod if found
		tasks_exist = frappe.db.exists("GP Task", {"project": project_name})
		if tasks_exist:
			pod_name = create_project_pod(project_name, "Tasks", "Tasks")
			if pod_name:
				if isinstance(pod_name, str):  # New pod was created
					tools_created["Tasks"] += 1
				else:  # Pod already existed
					tools_skipped["Tasks"] += 1

				# Update all tasks to link to this pod
				updated_count = update_records_with_pod("GP Task", project_name, pod_name)
				records_updated["Tasks"] += updated_count
			else:
				tools_skipped["Tasks"] += 1

		# Check for existing pages and create Documents pod if found
		pages_exist = frappe.db.exists("GP Page", {"project": project_name})
		if pages_exist:
			pod_name = create_project_pod(project_name, "Documents", "Documents")
			if pod_name:
				if isinstance(pod_name, str):  # New pod was created
					tools_created["Documents"] += 1
				else:  # Pod already existed
					tools_skipped["Documents"] += 1

				# Update all pages to link to this pod
				updated_count = update_records_with_pod("GP Page", project_name, pod_name)
				records_updated["Documents"] += updated_count
			else:
				tools_skipped["Documents"] += 1

	# Print summary
	total_created = sum(tools_created.values())
	total_skipped = sum(tools_skipped.values())
	total_records_updated = sum(records_updated.values())

	print("Project Pods Migration Summary:")
	print(f"- Total pods created: {total_created}")
	print(f"- Total pods skipped (already existed): {total_skipped}")
	print(f"- Total records updated with pod links: {total_records_updated}")
	print(
		f"- Discussions: {tools_created['Discussions']} created, "
		f"{tools_skipped['Discussions']} skipped, {records_updated['Discussions']} records updated"
	)
	print(
		f"- Tasks: {tools_created['Tasks']} created, "
		f"{tools_skipped['Tasks']} skipped, {records_updated['Tasks']} records updated"
	)
	print(
		f"- Documents: {tools_created['Documents']} created, "
		f"{tools_skipped['Documents']} skipped, {records_updated['Documents']} records updated"
	)


def create_project_pod(project, pod_type, title):
	"""Create a project pod if it doesn't already exist."""

	# Check if pod already exists
	existing_pod = frappe.db.exists("GP Pod", {"project": project, "type": pod_type})

	if existing_pod:
		return existing_pod

	try:
		# Create new project pod
		project_pod = frappe.new_doc("GP Pod")
		project_pod.project = project
		project_pod.type = pod_type
		project_pod.title = title
		project_pod.enabled = 1  # Enable by default
		project_pod.insert(ignore_permissions=True)
		return project_pod.name

	except Exception:
		# Don't stop the entire process for one error
		return False


def update_records_with_pod(doctype, project, pod_name):
	"""Update all records of the specified doctype to link to the project pod."""
	try:
		# Get all records for this project that don't have a pod set
		records = frappe.get_all(doctype, {"project": project, "pod": ["is", "not set"]}, ["name"])

		# Use bulk update for efficiency
		if records:
			record_names = [record["name"] for record in records]
			frappe.db.set_value(
				doctype, {"name": ["in", record_names]}, "pod", pod_name, update_modified=False
			)

		return len(records)

	except Exception as e:
		print(f"Error updating {doctype} records for project {project}: {str(e)}")
		return 0
