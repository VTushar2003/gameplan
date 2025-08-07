# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and Contributors

import frappe


def execute():
	"""Create default project tools for all existing projects based on existing content."""

	# Get all projects
	projects = frappe.get_all("GP Project", fields=["name", "title"])

	if not projects:
		return

	tools_created = {"Discussions": 0, "Tasks": 0, "Documents": 0}
	tools_skipped = {"Discussions": 0, "Tasks": 0, "Documents": 0}
	records_updated = {"Discussions": 0, "Tasks": 0, "Documents": 0}

	for project in projects:
		project_name = project["name"]

		# Check for existing discussions and create Discussions tool if found
		discussions_exist = frappe.db.exists("GP Discussion", {"project": project_name})
		if discussions_exist:
			tool_name = create_project_tool(project_name, "Discussions", "Discussions")
			if tool_name:
				if isinstance(tool_name, str):  # New tool was created
					tools_created["Discussions"] += 1
				else:  # Tool already existed
					tools_skipped["Discussions"] += 1

				# Update all discussions to link to this tool
				updated_count = update_records_with_tool("GP Discussion", project_name, tool_name)
				records_updated["Discussions"] += updated_count
			else:
				tools_skipped["Discussions"] += 1

		# Check for existing tasks and create Tasks tool if found
		tasks_exist = frappe.db.exists("GP Task", {"project": project_name})
		if tasks_exist:
			tool_name = create_project_tool(project_name, "Tasks", "Tasks")
			if tool_name:
				if isinstance(tool_name, str):  # New tool was created
					tools_created["Tasks"] += 1
				else:  # Tool already existed
					tools_skipped["Tasks"] += 1

				# Update all tasks to link to this tool
				updated_count = update_records_with_tool("GP Task", project_name, tool_name)
				records_updated["Tasks"] += updated_count
			else:
				tools_skipped["Tasks"] += 1

		# Check for existing pages and create Documents tool if found
		pages_exist = frappe.db.exists("GP Page", {"project": project_name})
		if pages_exist:
			tool_name = create_project_tool(project_name, "Documents", "Documents")
			if tool_name:
				if isinstance(tool_name, str):  # New tool was created
					tools_created["Documents"] += 1
				else:  # Tool already existed
					tools_skipped["Documents"] += 1

				# Update all pages to link to this tool
				updated_count = update_records_with_tool("GP Page", project_name, tool_name)
				records_updated["Documents"] += updated_count
			else:
				tools_skipped["Documents"] += 1

	# Print summary
	total_created = sum(tools_created.values())
	total_skipped = sum(tools_skipped.values())
	total_records_updated = sum(records_updated.values())

	print("Project Tools Migration Summary:")
	print(f"- Total tools created: {total_created}")
	print(f"- Total tools skipped (already existed): {total_skipped}")
	print(f"- Total records updated with tool links: {total_records_updated}")
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


def create_project_tool(project, tool_type, title):
	"""Create a project tool if it doesn't already exist."""

	# Check if tool already exists
	existing_tool = frappe.db.exists("GP Project Tool", {"project": project, "type": tool_type})

	if existing_tool:
		return existing_tool

	try:
		# Create new project tool
		project_tool = frappe.new_doc("GP Project Tool")
		project_tool.project = project
		project_tool.type = tool_type
		project_tool.title = title
		project_tool.enabled = 1  # Enable by default
		project_tool.insert(ignore_permissions=True)
		return project_tool.name

	except Exception:
		# Don't stop the entire process for one error
		return False


def update_records_with_tool(doctype, project, tool_name):
	"""Update all records of the specified doctype to link to the project tool."""
	try:
		# Get all records for this project that don't have a project_tool set
		records = frappe.get_all(doctype, {"project": project, "project_tool": ["is", "not set"]}, ["name"])

		# Use bulk update for efficiency
		if records:
			record_names = [record["name"] for record in records]
			frappe.db.set_value(doctype, {"name": ["in", record_names]}, "project_tool", tool_name)

		return len(records)

	except Exception as e:
		print(f"Error updating {doctype} records for project {project}: {str(e)}")
		return 0
