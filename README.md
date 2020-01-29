# Application maker
 
Web scraping software that searches vacancies
Default search site: "https://no.jooble.org/jobb-ekstrahjelper%2Fbutikkselger-deltid/Stavanger?"
Target key: "ckey=ekstrahjelper%2fbutikkselger+deltid"
To change search site, find the appropriate search query, and inspect elements to find unique identifiers for desired links
Inspect the content of those links to find html id's of desired elements (in this case company)
Change application_template.docx to your desired template. Avoid changing MergeFields (e.g. «company»)
Run script and input required values
