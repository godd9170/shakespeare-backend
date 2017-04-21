TEMPLATES = [
    { 
        "intro" : "Saw an article on {{Nugget.additionaldata.publisher}} that you were quoted in.  After reading the line \"{{Nugget.body}}\", I felt compelled to reach out to you directly.",
        "segue" : "The reason the article stood out for me is that it referred to something we strongly believe in.",
        "category" : "quote_from_individual",
        "subject" : "Your quote on {{Nugget.additionaldata.publisher}}"
    },
        { 
        "intro" : "I stumbled upon an article mentioning {{Nugget.piece.research.individual.company.name}}.  After reading {{Nugget.additionaldata.name}}'s quote \"{{Nugget.body}}\", I felt compelled to reach out to you directly.",
        "segue" : "The reason {{Nugget.additionaldata.name}}'s quote stood out is that it alluded to something we strongly believe in.",
        "category" : "quote_about",
        "subject" : "{{Nugget.additionaldata.name}} from {{Nugget.additionaldata.company}}'s quote on {{Nugget.piece.research.individual.company.name}}"
    },
        { 
        "intro" : "I stumbled upon an article where {{Nugget.additionaldata.name}} was quoted in {{Nugget.additionaldata.publisher}}.  After reading the line \"{{Nugget.body}}\", I felt compelled to reach out to you directly.",
        "segue" : "The reason {{Nugget.additionaldata.name}}'s quote stood out is that it alluded to something we strongly believe in.",
        "category" : "quote_from_company",
        "subject" : "{{Nugget.additionaldata.name}}'s quote on {{Nugget.additionaldata.publisher}}"
    },
        { 
        "intro" : "I was looking at the list of {{Nugget.additionaldata.recognition}} and saw that {{Nugget.piece.research.individual.company.name}} made the list.  Congratulations on the achievement.",
        "segue" : "We find that to continuously grow and challenge the norm, companies need to look for new ways of doing things.",
        "category" : "recognized_as",
        "subject" : "Your recent recognition as {{Nugget.additionaldata.recognition}}"
    },
        { 
        "intro" : "I was researching companies that recently got their {{Nugget.additionaldata.financing_type}} and came across an article mentioning {{Nugget.piece.research.individual.company.name}}.  Congratulations on your {{Nugget.additionaldata.amount}} round.",
        "segue" : "To reference Biggie, \"Mo' Money, Mo' Problems\", let's see if I can help.",
        "category" : "receives_financing",
        "subject" : "Your {{Nugget.additionaldata.amount}} round"
    },
        { 
        "intro" : "I was researching rapidly growing companies and came across an article referencing the {{Nugget.additionaldata.headcount}} people recently hired by {{Nugget.piece.research.individual.company.name}}.  Your headcount expansion compelled me to reach out to you directly.",
        "segue" : "We find that to take get new hires operartional quickly, companies need to look to new ways to do things.",
        "category" : "increases_headcount_by",
        "subject" : "Your {{Nugget.additionaldata.headcount}} new employees"
    },
        { 
        "intro" : "This article compelled me to reach out to you directly ({{Nugget.additionaldata.title}}).",
        "segue" : "We find that to take full advantage of new acquisitions, companies need to look for new ways to do things.",
        "category" : "acquires",
        "subject" : "Your recent Acquisition"
    },
        { 
        "intro" : "I came across an article that compelled me to reach out to you directly.  The article in question spoke to latest partnership you created ({{Nugget.additionaldata.title}}).",
        "segue" : "We find that to take full advantage of new partnerships, companies need to look for new ways to do things.",
        "category" : "partners_with",
        "subject" : "{{Nugget.additionaldata.title}}"
    },
        { 
        "intro" : "I came across an article that compelled me to reach out to you directly.  The article in question spoke to latest integration ({{Nugget.additionaldata.title}}).",
        "segue" : "We find that to take full advantage of new integrations, companies need to look for new ways to do things.",
        "category" : "integrates_with",
        "subject" : "{{Nugget.additionaldata.title}}"
    },
        { 
        "intro" : "I just finished reading an article named \"{{Nugget.additionaldata.title}}\" and needed to reach out to you directly.",
        "segue" : "We find that to take full advantage of new product launches, companies need to look for new ways to do things.",
        "category" : "launches",
        "subject" : "{{Nugget.additionaldata.title}}"
    },
        { 
        "intro" : "I was researching companies that recently hired a new {{Nugget.additionaldata.job_title}} and came across {{Nugget.piece.research.individual.company.name}}'s hire of {{Nugget.additionaldata.contact}}.",
        "segue" : "Adding new executives often means adding new ways to do things.",
        "category" : "hires",
        "subject" : "{{Nugget.additionaldata.contact}}"
    },
        { 
        "intro" : "I was researching companies that recently expanded to office locations and came across an article mentioning {{Nugget.piece.research.individual.company.name}} ({{Nugget.additionaldata.title}}).  After reading about your growth, I was compelled to reach out to you directly.",
        "segue" : "Expansions offer a world of possibility.",
        "category" : "expands_offices_to",
        "subject" : "Your expansion to {{Nugget.additionaldata.location}}"
    },
        { 
        "intro" : "I was researching companies with upcoming product launches and came across an article mentioning your {{Nugget.additionaldata.product}}.",
        "segue" : "We find that to take full advantage of new product launches, companies need to look for new ways to do things.",
        "category" : "is_developing",
        "subject" : "Your development of {{Nugget.additionaldata.product}}"
    },
        { 
        "intro" : "I was researching companies that recently went public and came accross article highlighting your IPO ({{Nugget.additionaldata.title}}).  Congratulations on your achievement.",
        "segue" : "To reference Biggie, \"Mo' Money, Mo' Problems\", so let's see if I can help.",
        "category" : "goes_public",
        "subject" : "Your {{Nugget.additionaldata.financing_type}}"
    },
        { 
        "intro" : "I was researching companies that were looking to expand their sales teams and came across {{Nugget.piece.research.individual.company.name}}'s posting for a {{Nugget.additionaldata.job_title}}.",
        "segue" : "We find that to get the most out of new sales hires, companies need to take advantage of new strategies.",
        "category" : "sales",
        "subject" : "Growing the {{Nugget.additionaldata.job_title}} team"
    },
        { 
        "intro" : "This article compelled me to reach out to you directly ({{Nugget.additionaldata.title}}).",
        "segue" : "We find that to take full advantage of new mergers, companies need to look for new ways to do things.",
        "category" : "merges_with",
        "subject" : "Your recent Merger"
    },
        { 
        "intro" : "I came across a testimonial {{Nugget.additionaldata.name}} from {{Nugget.additionaldata.company}} wrote about you.  It was the line \"{{Nugget.body}}\" that compelled me to reach out to you directly.",
        "segue" : "The reason {{Nugget.additionaldata.name}}'s testimonial stood out is because it resonated with something we strongly believe in.",
        "category" : "testimonial",
        "subject" : "{{Nugget.additionaldata.company}}"
    },
        { 
        "intro" : "I was researching companies that were looking to expand their engineering teams and came across {{Nugget.piece.research.individual.company.name}}.",
        "segue" : "We find that to get the most out of new engineers, companies need to take advantage of new strategies.",
        "category" : "engineering",
        "subject" : "Growing the {{Nugget.additionaldata.job_title}} team"
    },
        { 
        "intro" : "I was researching companies that were looking to expand their operations teams and came across {{Nugget.piece.research.individual.company.name}}.",
        "segue" : "We find that to get the most out of new leaders, companies need to take advantage of new strategies.",
        "category" : "operations",
        "subject" : "Growing the {{Nugget.additionaldata.job_title}} team"
    },
        { 
        "intro" : "I was researching companies that were looking to expand their HR teams and came across {{Nugget.piece.research.individual.company.name}}.",
        "segue" : "We find that to get the most out of new HR hires, companies need to take advantage of new strategies.",
        "category" : "human_resources",
        "subject" : "Growing the {{Nugget.additionaldata.job_title}} team"
    },
        { 
        "intro" : "I was researching companies that were looking to expand their BA teams and came across {{Nugget.piece.research.individual.company.name}}.",
        "segue" : "We find that to get the most out of new BAs, companies need to take advantage of new strategies.",
        "category" : "business_analysis",
        "subject" : "Growing the {{Nugget.additionaldata.job_title}} team"
    },
        { 
        "intro" : "I was researching companies that were looking to expand their dev teams and came across {{Nugget.piece.research.individual.company.name}}.",
        "segue" : "We find that to get most out of new developers, companies need to take advantage of new strategies.",
        "category" : "software_development",
        "subject" : "Growing the {{Nugget.additionaldata.job_title}} team"
    },
        { 
        "intro" : "I was researching companies that were looking to expand their finance teams and came across {{Nugget.piece.research.individual.company.name}}.",
        "segue" : "We find that to get most out of new hires in the finance team, companies need to take advantage of new strategies.",
        "category" : "finance",
        "subject" : "Growing the {{Nugget.additionaldata.job_title}} team"
    },
        { 
        "intro" : "I was looking at the list of {{Nugget.additionaldata.award}} and saw that {{Nugget.piece.research.individual.company.name}} made the list.  Congratulations on the achievement.",
        "segue" : "We find that to continuously grow and challenge the norm, companies need to look for new ways of doing things.",
        "category" : "receives_award",
        "subject" : "Your recent recognition as {{Nugget.additionaldata.award}}"
    },
        { 
        "intro" : "I was researching companies that were looking to expand their marketing teams and came across {{Nugget.piece.research.individual.company.name}}.",
        "segue" : "We find that to get the most out of new marketers, companies need to take advantage of new strategies.",
        "category" : "marketing",
        "subject" : "Growing the {{Nugget.additionaldata.job_title}} team"
    },
        { 
        "intro" : "I read about your latest expansion in {{Nugget.additionaldata.location}} and felt compelled me to reach out you directly.",
        "segue" : "New locations can be hard.",
        "category" : "opens_new_location",
        "subject" : "Your recent expansion to {{Nugget.additionaldata.location}}"
    },
        { 
        "intro" : "I was researching companies that were looking to expand their management teams and came across {{Nugget.piece.research.individual.company.name}}.",
        "segue" : "We find that to get the most out of new ops hires, companies need to take advantage of new strategies.",
        "category" : "management",
        "subject" : "Growing the {{Nugget.additionaldata.job_title}} team"
    },
        { 
        "intro" : "I was researching companies that recently opened new facilities and came across an article mentioning {{Nugget.piece.research.individual.company.name}} ({{Nugget.additionaldata.title}}).",
        "segue" : "Expansions offer a world of possibility.",
        "category" : "expands_facilities",
        "subject" : "Your expansion to {{Nugget.additionaldata.location}}"
    },
            { 
        "intro" : "I stumbled upon an article mentioning {{Nugget.piece.research.individual.company.name}}.  After reading {{Nugget.additionaldata.name}}'s quote \"{{Nugget.body}}\", I felt compelled to reach out to you directly.",
        "segue" : "The reason {{Nugget.additionaldata.name}}'s quote stood out is that it alluded to something we strongly believe in.",
        "category" : "quote_about",
        "subject" : "{{Nugget.additionaldata.name}}'s quote on {{Nugget.piece.research.individual.company.name}}"
    }
]