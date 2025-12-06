import sys
from datetime import date


def receive_input():
    print("Enter url list: ")
    url_list = sys.stdin.readlines()

    # default: berkeleyhousingstudy@gmail.com, lailavoss@berkeley.edu
    formatted_output_list = []
    for url in url_list:
        url = url.strip()
        print(f"\nEnter for {url}")
        email_one = input("Enter email 1: ") 
        email_two = input("Enter email 2: ")
        
        # if email_one == "":
        #     email_one = "berkeleyhousingstudy@gmail.com"
        # if email_two == "":
        #     email_two = "lailavoss@berkeley.edu"
        
        formatted_output = f"{url}:::{email_one}, {email_two}"
        formatted_output_list.append(formatted_output)

    final_output = "\n".join(formatted_output_list)
    print(f"Final Output:\n {final_output}")
    return formatted_output_list

def save_to_txt(formatted_output_list):
    today = date.today()
    with open(f'{today}_--_Emails.txt', 'a') as file:
        for line in formatted_output_list:
            file.write(line + '\n')
            
        
        file.close()

if __name__ == '__main__':
    formatted_output_list = receive_input()
    save_to_txt(formatted_output_list)