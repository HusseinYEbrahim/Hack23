import base64, re, timeit 

def encodeb64(plaindata: str) -> str:
    unidata = plaindata.encode('utf-8')
    return base64.b64encode(unidata)

def decodeb64(hiddendata: str) -> str:
    databytes = base64.b64decode(hiddendata)
    return databytes.decode("unicode_escape")


def extractor(b64pcap: str) -> str:

    starttime = timeit.default_timer()
    
    pcap_txt = decodeb64(b64pcap)

    patterns= [r'\w+'] 
    extracted_data =  ""
    for p in patterns:
        extracted_data = re.findall(p, pcap_txt)

    ordered_message = ["1"]
    counter = 1
    while(True):
        b64count = encodeb64(str(counter))
        asciicount = b64count.decode("unicode_escape")
        asciicount = asciicount.replace("=", "")
        if asciicount in extracted_data[0:int(0.25*len(extracted_data))-1]:
            ordered_message.insert(extracted_data.index(asciicount), decodeb64(extracted_data[extracted_data.index(asciicount)+1]+"=="))
            counter += 1
        elif asciicount in extracted_data[int(0.25*len(extracted_data))-1:int(0.5*len(extracted_data))-1]:
            ordered_message.insert(extracted_data.index(asciicount), decodeb64(extracted_data[extracted_data.index(asciicount)+1]+"=="))
            counter += 1
        elif asciicount in extracted_data[int(0.5*len(extracted_data))-1:int(0.75*len(extracted_data))-1]:
            ordered_message.insert(extracted_data.index(asciicount), decodeb64(extracted_data[extracted_data.index(asciicount)+1]+"=="))
            counter += 1
        elif asciicount in extracted_data[int(0.75*len(extracted_data))-1:len(extracted_data)-1]:
            ordered_message.insert(extracted_data.index(asciicount), decodeb64(extracted_data[extracted_data.index(asciicount)+1]+"=="))
            counter += 1
        else:
            break

    ordered_message.pop(0)

    lapse = timeit.default_timer() - starttime
    print(lapse)
    
    return "".join(ordered_message)

def main():
    s1 = "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"
    print(extractor(s1))

if __name__ == "__main__":
    main()