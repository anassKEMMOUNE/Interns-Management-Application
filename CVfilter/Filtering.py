import CVfilter.extraction as extraction
import os
import unidecode


def filterCV(content : dict, keywords : list) :
    listOfWords = content["tokenized"]
    attachedWords = content["untokenized"]
    keywords = [(unidecode.unidecode(text)).lower() for text in keywords]
    for kw in keywords :
        if kw in listOfWords or kw in attachedWords :
            continue
        else : 
            return False
    return True



def filterAll(directory : str, keywords : list = []) :
    filtered = []
    resumes =  os.listdir(directory)
    if len(resumes) == 0 :
        return "Empty directory"
    for res in resumes :
        print("Searching in resume : ",res)
        if (res.split(".")[-1] == "pdf") :
           if  filterCV(extraction.pdf_to_text(directory+'/'+res),keywords) : 
               filtered.append(res)
        elif res.split(".")[-1] == "png" or res.split(".")[-1] == "jog"  or res.split(".")[-1] == "jpeg"  :
            if filterCV(extraction.image_to_text(directory + '/' + res),keywords) :
                filtered.append(res)
        elif res.split(".")[-1] == "docx" :
            if filterCV(extraction.docx_to_text(directory + '/' + res),keywords) :
                filtered.append(res)

        else :
            continue 

    return filtered

print(filterAll("Resumes",keywords=['PHP',"blockchain"]))
print(filterAll("Resumes",keywords=['PHP']))


    
