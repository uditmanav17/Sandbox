proteins_li = {
    "AUG": "Methionine",
    "UUU": "Phenylalanine",
    "UUC": "Phenylalanine",
    "UUA": "Leucine",
    "UUG": "Leucine",
    "UCU": "Serine",
    "UCC": "Serine",
    "UCA": "Serine",
    "UCG": "Serine",
    "UAU": "Tyrosine",
    "UAC": "Tyrosine",
    "UGU": "Cysteine",
    "UGC": "Cysteine",
    "UGG": "Tryptophan",
    # "UAA":"STOP", "UAG":"STOP", "UGA":"STOP",
}


def proteins(strand):
    protein_list = [strand[i : i + 3] for i in range(0, len(strand), 3)]
    protein_names = []
    for protein in protein_list:
        try:
            protein_names.append(proteins_li[protein])
        except KeyError as ve:
            break
    return protein_names
