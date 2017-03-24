# This might need to be it's own model with twin Many2Many Lookups to Nuggets and NuggetWrappers
GROUPS = {
    'article' : [
        ('quote_from_individual', 'Quote From Individual'), # Storyzy (This actual person you're researching)
        ('quote_from_company', 'Quote From Company'), # Storyzy (This is the company of the person you're researching)
        ('quote_about', 'Quote About') # Storyzy (This is any external person referring to either the individual or the company being researched)
    ],
    'testimonial' : [
        ('testimonial', 'Testimonial'), # Featured Customers
    ],
    'leadership' : [
        ('hires', 'Hires'), # PredictLeads vvv
        ('promotes', 'Promotes'),
        ('leaves', 'Leaves'),
        ('retires', 'Retires')
    ],

    'aquisition' : [
        ('acquires', 'Aquires'),
        ('merges_with', 'Merges With'),
        ('sells_assets_to', 'Sells Assets To')
    ],
    'expansion' : [
        ('expands_offices_to', 'Expands Offices To'),
        ('expands_offices_in', 'Expands Office In'),
        ('expands_facilities', 'Expands Facilities'),
        ('opens_new_location', 'Opens New Location'),
        ('increases_headcount_by', 'Increases Headcount By')
    ],
    'new_offering' : [
        ('launches', 'Launches'),
        ('integrates_with', 'Integrates With'),
        ('is_developing', 'Is Developing')
    ],
    'investment' : [
        ('receives_financing', 'Receives Financing'),
        ('invests_into', 'Invests Into'),
        ('goes_public', 'Goes Public')
    ],
    'cost_cutting' : [
        ('closes_offices', 'Closes Offices'),
        ('decreases_headcount_by', 'Decreases Headcount By')
    ],
    'partnership' : [
        ('partners_with', 'Partners With')
    ],
    'recognition' : [
        ('receives_award', 'Receives Award'),
        ('recognized_as', 'Recognized As'),
        ('signs_new_client', 'Signs New Client')
    ],
    'corporate_challenges' : [
        ('files_suit_against', 'Files Suit Against'),
        ('has_issues_with', 'Has Issues With')
    ],
    'job_position' : [
        ("none", "None"),
        ("administration", "Administration"),
        ("chairmen", "Chairmen"),
        ("health_care", "Health Care"),
        ("hospitality", "Hospitality"),
        ("engineering", "Engineering"),
        ("education", "Education"),
        ("maintenance", "Maintenance"),
        ("finance", "Finance"),
        ("information_technology", "Information Technology"),
        ("management", "Management"),
        ("operations", "Operations"),
        ("partnerships",  "Partnerships",),
        ("human_resources", "Human Resources"),
        ("publishing", "Publishing"),
        ("purchasing", "Purchasing"),
        ("sales", "Sales"),
        ("marketing", "Marketing"),
        ("transportation", "Transportation"),
        ("directors", "Directors"),
        ("design", "Design"),
        ("software_development", "Software Development"),
        ("general_technology", "General Technology"),
        ("business_analysis", "Business Analysis"),
        ("support", "Support"),
        ("data_analysis", "Data Analysis")
    ]
}
PIECE_GROUPS = zip(GROUPS.keys(), GROUPS.keys())
NUGGET_TEMPLATE_CATEGORIES = sorted(set(sum(GROUPS.values(), [])))

def category_to_group(category):
        for group, categories in GROUPS.items():
            if dict(categories).get(category) is not None:
                return group
        return 'article'