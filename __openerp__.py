{
	"name": "Academic Information System Day 3",
	"version": "1.0", 
	"depends": [
		"base",
		"account",
		"sale",
	],
	"author": "akhmad.daniel@gmail.com", 
	"category": "Education", 
	'website': 'http://www.vitraining.com',
	"description": """\
Academic Information System Day 3

""",
	"data": [
		"menu.xml",
		"course.xml",
		"session.xml",
		"attendee.xml",
		"partner.xml",
		"workflow.xml",
		"security/groups.xml",
		"security/ir.model.access.csv",
		"wizard/create_attendee_view.xml",
		"report/session.xml",
	],
	"installable": True,
	"auto_install": False,
    "application": True,
}
