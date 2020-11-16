from collections import namedtuple

sync_tokens = {";", "fimse", "fim", "$"}

Production = namedtuple("Production", ["left", "right"])

mgolgrammar = {
    "0": Production(left="P'", right=("P",)),
    "1": Production(left="P", right=("inicio", "V", "A",)),
    "2": Production(left="V", right=("varinicio", "LV",)),
    "3": Production(left="LV", right=("D", "LV",)),
    "4": Production(left="LV", right=("varfim", ";",)),
    "5": Production(left="D", right=("id", "TIPO", ";",)),
    "6": Production(left="TIPO", right=("inteiro",)),
    "7": Production(left="TIPO", right=("real",)),
    "8": Production(left="TIPO", right=("literal",)),
    "9": Production(left="A", right=("ES", "A",)),
    "10": Production(left="ES", right=("leia", "id", ";",)),
    "11": Production(left="ES", right=("escreva", "ARG", ";",)),
    "12": Production(left="ARG", right=("literal",)),
    "13": Production(left="ARG", right=("num",)),
    "14": Production(left="ARG", right=("id",)),
    "15": Production(left="A", right=("CMD", "A",)),
    "16": Production(left="CMD", right=("id", "rcb", "LD", ";",)),
    "17": Production(left="LD", right=("OPRD", "opm", "OPRD",)),
    "18": Production(left="LD", right=("OPRD",)),
    "19": Production(left="OPRD", right=("id",)),
    "20": Production(left="OPRD", right=("num",)),
    "21": Production(left="A", right=("COND", "A",)),
    "22": Production(left="COND", right=("CABEÇALHO", "CORPO",)),
    "23": Production(left="CABEÇALHO", right=("se", "(", "EXP_R", ")", "entao",)),
    "24": Production(left="EXP_R", right=("OPRD", "opr", "OPRD",)),
    "25": Production(left="CORPO", right=("ES", "CORPO",)),
    "26": Production(left="CORPO", right=("CMD", "CORPO",)),
    "27": Production(left="CORPO", right=("COND", "CORPO",)),
    "28": Production(left="CORPO", right=("fimse",)),
    "29": Production(left="A", right=("fim",)),
}