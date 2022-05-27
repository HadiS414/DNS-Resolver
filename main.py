import dns.message
import dns.query
import time
import datetime

def findIP(request, ip):
    # create response using the request and IP in parameter
    response = dns.query.udp(request, ip)
    # if the response contains answer
    if response.answer:
        # print question section along with question
        print("Question Section: ")
        print(response.question[0])
        # return the IP in answer
        return response.answer[0]
    # if the response doesn't contain an answer
    else:
        # if the response contains additional
        if response.additional:
            # request for additional
            additional_request = dns.message.make_query(domain, dns.rdatatype.A)
            i = 0
            # loop to find an IP that is IPv4
            while response.additional[i].rdtype != 1:
                i += 1
            # if IP is IPv4
            if response.additional[i].rdtype == 1:
                # continue finding IP of the original domain
                return findIP(additional_request, str(response.additional[i][0]))    # recursive call
        # if the response doesn't contain additional, check authority
        else:
            # new root server request
            root_request = dns.message.make_query(str(response.authority[0][0]), dns.rdatatype.A)
            # find the IP of new domain given by authority
            authority_ip = findNameServerIP(str(response.authority[0][0]), root_request, "192.36.148.17")
            # request for authority
            authority_request = dns.message.make_query(domain, dns.rdatatype.A)
            # continue finding original domain IP using IP found from authority
            return findIP(authority_request, str(authority_ip[0]))       # recursive call


def findNameServerIP(auth_domain, request, IP):
    # create response using request and IP from parameter
    response = dns.query.udp(request, IP)
    # if response has an answer
    if response.answer:
        # return the IP in answer
        return response.answer[0]
    # if response doesn't contain an answer
    else:
        # if response contains an additional
        if response.additional:
            # request for additional
            additional_request = dns.message.make_query(auth_domain, dns.rdatatype.A)
            i = 0
            # loop to find an IP that is IPv4
            while response.additional[i].rdtype != 1:
                i += 1
            # if IP is IPv4
            if response.additional[i].rdtype == 1:
                # continue finding IP of new domain given by authority
                return findNameServerIP(auth_domain, additional_request, str(response.additional[i][0]))
        # if the response doesn't contain additional, check authority
        else:
            # new root server request
            root_request = dns.message.make_query(str(response.authority[0][0]), dns.rdatatype.A)
            # find the IP of new domain given by authority
            authority_ip = findNameServerIP(response.authority[0][0], root_request, "192.36.148.17")
            # request for authority
            authority_request = dns.message.make_query(auth_domain, dns.rdatatype.A)
            # continue finding domain IP using IP found from authority
            return findNameServerIP(auth_domain, authority_request, str(authority_ip[0]))


if __name__ == '__main__':
    # input for domain name
    domain = input("Enter a domain: mydig ")
    print("")
    # start time of request
    start = time.perf_counter()
    # root server request
    request = dns.message.make_query(domain, dns.rdatatype.A)
    # run function to find the IP of the domain
    answer = findIP(request, "192.36.148.17")
    print("")
    # print the answer section along with the answer
    print("Answer Section: ")
    print(answer)
    # end time of request
    end = time.perf_counter()
    print("")
    # calculate resolving query time by finding the difference of end and start time, then print
    print("Query time:", (end-start)*1000, "ms")
    # print date and time when request was made
    print("When:", datetime.datetime.now())

