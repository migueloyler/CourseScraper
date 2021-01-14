# CourseScraper
A Python Web-Scraper that generates an Outlook-Compatible HTML email that gets sent out to members of the Division of Clinical Research (DCR) at 
MGH to present the latest DCR-sponsored courses for individuals in the clinical research community.

Course scraper fetches courses from learn.partners.org/org/mgh-research-institute/date/ to generate an HTML email. This email will only include courses that
are scheduled to take place within the next three weeks from the day course scraper is run. Additionally, CourseScraper will include a max of 3 courses in the email
in order to keep the email concise as it is sent out on a weekly basis.
