from mailmerge import MailMerge

template = "mainFolder/application_template.docx"
document = MailMerge(template)
document.merge(date="27/01/20", company="Elkjop Os", company_address ="Osveien 1")

document.write('test1.docx')