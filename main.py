import openpyxl
import tabulate
from emailer import send_email

path = "./data.xlsx"


def main():
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active
    name_email_list = []
    for row in sheet.iter_rows(values_only=True):
        if row[0] == "Name" or row[1] == "Email":  # skip header row
            continue
        name_email_list.append((row[0], row[1]))
    done, failed = send_email(name_email_list)
    if done:
        tabulated_done = tabulate.tabulate(
            [[mail] for mail in done],
            headers=[f"Emails: Success {len(done)}"],
            tablefmt="grid",
        )
        print(tabulated_done)
    if failed:
        tabulated_failed = tabulate.tabulate(
            [[mail] for mail in failed], headers=[f"Emails: Failed - {len(failed)}"]
        )
        print(tabulated_failed)
    workbook.close()


main()
