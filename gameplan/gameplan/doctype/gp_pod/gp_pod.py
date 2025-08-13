# Copyright (c) 2025, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class GPPod(Document):
	def before_insert(self):
		if not self.idx:
			if not self.title:
				self.title = self.type

			# Get the highest idx for this project and increment by 1
			max_idx = frappe.db.get_value(
				"GP Pod",
				{"project": self.project},
				[{"MAX": "idx"}],
			)
			self.idx = (max_idx or 0) + 1
