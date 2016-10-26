# Acquire a list of DOCX files in a folder

# $File="C:\Foofolder\foofile.docx"
$Files=GET-CHILDITEM 'C:\Users\Jeremy\Documents\GitHub\ee4-FYP\reports\*.DOCX'
$Word=NEW-OBJECT –COMOBJECT WORD.APPLICATION
 

Foreach ($File in $Files) {

    # open a Word document, filename from the directory

    $Doc=$Word.Documents.Open($File.fullname)

 

    # Swap out DOCX with PDF in the Filename

$Name=($Doc.Fullname).replace("docx","pdf")

 

    # Save this File as a PDF in Word 2010/2013

    $Doc.saveas([ref] $Name, [ref] 17)

    $Doc.close()

}