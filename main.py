import sys
from document import Document


def parse_document(path, output_path):
    """
    Parse document and write to csv
    :param path: Input utf8-encoded txt file path
    :param output_path: Output directory path
    :return: None
    """
    with open(path, 'r', encoding='utf-8') as f:
        content = f.readlines()

        doc = Document(content)

        doc.parse()
        print(doc.first_names)
        print(doc.last_name)
        print(doc.student_number)
        print(doc.birth_time)
        print(doc.total_credits_check)
        print(doc.credits)
        if doc.credits != doc.total_credits_check:
            print("HUOM! lasketut opintopisteet eivät täsmää! Todennäköisesti dokumentin lukemisessa virhe. ")
        doc.write_csv(output_path)


if __name__ == '__main__':
    parse_document(sys.argv[1], sys.argv[2])
