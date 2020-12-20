from copy import copy

# dicionário {chave:token, valor:tipo}
types = {
    "literal": "literal",
    "inteiro": "inteiro",
    "real": "real",
}




class Semantic:
    def __init__(self, symbol_table_reference):
        self.aux_stack = None
        self.code = [] # código em C
        self.semantic_error = False
        self.indent = 0
        self.Tx_count = -1
        self.semantic_rules = None
        self.create_semantic_rules()
        self.symbol_table_reference = symbol_table_reference
        self.translation_routines = ("5", "10", "11", "16", "17", "22", "23", "24")
        self.code_insert(snippet="/*------------------------------*/", indent=True)

    def set_type(self, ip):
        _type = types.get(ip["token"], ip["lexeme"])
        ip["type"] = _type
        return ip


    def init_stack(self):
        self.aux_stack = []
    
    def code_insert(self, snippet, position=None, indent=False):
        self.indent = self.indent + (1 if indent is True else 0)

        position = position if position is not None else len(self.code)
        snippet = "    "*self.indent + snippet + "\n"
        self.code.insert(position, snippet)

        self.indent = self.indent - (1 if indent is True else 0)


    def start_of_code(self):
        self.code_insert(snippet="#include <stdio.h>",         position=0)
        self.code_insert(snippet="typedef char literal[256];", position=1)
        self.code_insert(snippet="void main(void){",           position=2)
    
    def end_of_code(self):
        # self.code_insert("    exit(0);")
        self.code_insert("}")

    # Função que insere os códigos de declaração das variáveis temporárias
    def declare_temporary(self):
        for i in range(self.Tx_count, -1, -1):
            self.code_insert(snippet="int T"+str(i)+";", position=0, indent=True)
        self.code_insert(snippet="/*----Variaveis temporarias----*/", position=0, indent=True)

    def write_code(self):
        if not self.semantic_error:
            self.declare_temporary()
            self.start_of_code()
            self.end_of_code()
            with open("PROGRAMA.c", "w") as F:
                F.writelines(self.code)
        else:
            print("Erro Semântico encontrado. Abortando geração de código.")
            

    # função que mapeia os nomes dos tipos
    def map_type(self, data_type):
        if data_type == "inteiro":
            return "int"
        elif data_type == "real":
            return "double"
        elif data_type == "<-":
            return "="
        else:
            return data_type

    def run(self, prod_index, Alpha, validation, syntactic_error):
        # Definindo retorno padrão
        tmp = {"lexeme":str(Alpha), "token":str(Alpha), "type":"", "line":"", "column":""}

        # Seleciona a regração semântica que será executada
        # Se não existir regra para o índice passado, retorna None
        rule = self.semantic_rules.get(prod_index, None)

        # Se algum erro semântico ou sintático foi encontrado a regra é desativada
        # para as rotinas de tradução
        if syntactic_error or self.semantic_error:
            if prod_index in self.translation_routines:
                rule = None

        # Testa a regra seleciona
        if rule is not None:
            non_terminal = rule(Alpha=tmp, 
                                validation=validation, 
                                syntactic_error=syntactic_error)
        else:
            non_terminal = tmp

        return non_terminal

    # Cria um dicionário contendo as regras semânticas para acesso via índice
    # O índice corresponde ao índice da regra sintática
    def create_semantic_rules(self):
        self.semantic_rules = {}

        # P -> P 
        def rule0(**kwargs):
            
            return kwargs['Alpha']
        self.semantic_rules["0"] = rule0

        # P -> inicio V A
        def rule1(**kwargs):
            
            return kwargs['Alpha']
        self.semantic_rules["1"] = rule1

        # V -> varinicio LV
        def rule2(**kwargs):
            
            return kwargs['Alpha']
        self.semantic_rules["2"] = rule2

        # LV -> D LV
        def rule3(**kwargs):
            
            return kwargs['Alpha']
        self.semantic_rules["3"] = rule3

        # LV -> varfim;
        # Imprimir três linhas brancas no arquivo objeto
        def rule4(**kwargs):
            self.code_insert('\n\n\n', indent=True)
            
            return kwargs['Alpha']
        self.semantic_rules["4"] = rule4

        # D -> id TIPO;
        def rule5(**kwargs):
            id = kwargs["validation"].pop()
            TIPO = kwargs["validation"].pop()
            PT_V = kwargs["validation"].pop() # ponto_critico
            
            self.symbol_table_reference.ids[id["lexeme"]]["type"] = TIPO["type"]
            row = self.map_type(TIPO["type"]) + " " + id["lexeme"] + ";"
            self.code_insert(snippet=row, indent=True)
            # print(kwargs)
            # input()
            
            return kwargs['Alpha']
        self.semantic_rules["5"] = rule5

        # TIPO -> inteiro
        def rule6(**kwargs):
            inteiro = kwargs['validation'].pop()
            kwargs['Alpha']["type"] = inteiro["type"]
            
            return kwargs['Alpha']
        self.semantic_rules["6"] = rule6

        # TIPO -> real
        def rule7(**kwargs):
            real = kwargs['validation'].pop()
            kwargs['Alpha']["type"] = real["type"]
            
            return kwargs['Alpha']
        self.semantic_rules["7"] = rule7

        # TIPO -> literal
        def rule8(**kwargs):
            literal = kwargs['validation'].pop()
            kwargs['Alpha']["type"] = literal["type"]
            
            return kwargs['Alpha']
        self.semantic_rules["8"] = rule8

        # A -> ES A 
        def rule9(**kwargs):
            
            return kwargs['Alpha']
        self.semantic_rules["9"] = rule9

        # ES -> leia id;
        # Verificar se o campo tipo do identificador está preenchido indicando a
        # declaração do identificador (execução da regra semântica de número 6).
        def rule10(**kwargs):
            leia = kwargs["validation"].pop()
            id = kwargs["validation"].pop()
            PT_V = kwargs["validation"].pop() # ponto_critico
            if id["type"] == "literal":
                self.code_insert("scanf(\"%s\", " + id["lexeme"] + ");", indent=True)
                
                return kwargs["Alpha"]
            elif id["type"] == "inteiro":
                self.code_insert("scanf(\"%d\", &" + id["lexeme"] + ");", indent=True)
                
                return kwargs["Alpha"]
            elif id["type"] == "real":
                self.code_insert("scanf(\"%lf\", &" + id["lexeme"] + ");", indent=True)
                
                return kwargs["Alpha"]
            else:
                print("Erro na linha %d: Variável não declarada (%s)" % (leia["line"]+1, id["lexeme"]))
                self.semantic_error = True
        self.semantic_rules["10"] = rule10

        # ES -> escreva ARG;
        # Gerar código para o comando escreva no arquivo objeto
        def rule11(**kwargs):
            escreva = kwargs["validation"].pop()
            ARG = kwargs["validation"].pop()
            PT_V = kwargs["validation"].pop() # ponto_critico
            text = ""

            if ARG["type"] == "inteiro":
                text = "\"%d\\n\","+ARG["lexeme"]
            elif ARG["type"] == "real":
                text = "\"%lf\\n\","+ARG["lexeme"]
            elif ARG["type"] == "literal":
                text = "\"%s\\n\","+ARG["lexeme"]
            else:
                text = ARG["lexeme"] if not ARG["lexeme"][0]==ARG["lexeme"][-1]=="\"" else ARG["lexeme"][1:-1] # Retira as aspas caso ARG seja literal
                text = "\"" + text + "\\n\""
            self.code_insert("printf(" + text + ");",indent=True)
            
            return kwargs["Alpha"]
        self.semantic_rules["11"] = rule11
            
        # ARG -> literal
        # Copiar todos os atributos de literal para os atributos de ARG
        def rule1213(**kwargs):
            literal = kwargs['validation'].pop()
            kwargs['Alpha'] = copy(literal)
            
            return kwargs['Alpha']
        self.semantic_rules["12"] = rule1213
        self.semantic_rules["13"] = rule1213

        # ARG -> id  
        def rule14(**kwargs):
            id = kwargs["validation"].pop()

            # Verificar se o identificador foi declarado (execução da regra semântica de número 6).
            if id["type"] is not "":
                kwargs['Alpha'] = copy(id)  # (copia todos os atributos de id para os de ARG
                
                return kwargs["Alpha"]
            else:
                print("Erro na linha %d: Variável não declarada (%s)" % (id["line"]+1, id["lexeme"]))
                self.semantic_error = True
        self.semantic_rules["14"] = rule14

        # A -> CMD A
        def rule15(**kwargs):
            
            return kwargs['Alpha']
        self.semantic_rules["15"] = rule15

        # CMD -> id rcb LD;
        def rule16(**kwargs):
            id = kwargs["validation"].pop()
            rcb = kwargs["validation"].pop()
            LD = kwargs["validation"].pop()
            PT_V = kwargs["validation"].pop()

            # Verificar se id foi declarado (execução da regra semântica de número 6).
            if id["type"] is not "": 
                # Realizar verificação do tipo entre os operandos id e LD
                if id["type"] == LD["type"]:
                    text = id["lexeme"] +" "+ self.map_type(rcb["lexeme"]) +" "+ LD["lexeme"] + ";"
                    self.code_insert(snippet=text, indent=True)

                    return kwargs["Alpha"]
                else:
                    print("Erro na linha %d: Tipos diferentes para atribuição (%s e %s)" % (id["line"]+1, id["type"], LD["type"]))
                    self.semantic_error = True
            else:
                print("Erro na linha %d: Variável não declarada (%s)" % (id["line"]+1, id["lexeme"]))
                self.semantic_error = True
        self.semantic_rules["16"] = rule16

        # LD -> OPRD opm OPRD
        def rule17(**kwargs):
            OPRD1 = kwargs["validation"].pop()
            OPM = kwargs["validation"].pop()
            OPRD2 = kwargs["validation"].pop()

            # Verificar se tipo dos operandos são equivalentes e diferentes de literal
            if OPRD1["type"] == OPRD2["type"] != "literal": 
                self.Tx_count += 1
                kwargs["Alpha"]["lexeme"] = "T"+str(self.Tx_count)
                if OPRD1["type"]=="real" or OPRD2["type"]=="real":
                    kwargs["Alpha"]["type"] = "real"
                else:
                    kwargs["Alpha"]["type"] = "inteiro"
                text = "T{} = {} {} {};".format(self.Tx_count, OPRD1["lexeme"], OPM["lexeme"], OPRD2["lexeme"])
                self.code_insert(snippet=text, indent=True)

                return kwargs['Alpha']
            else:
                print("Erro na linha %d: Operandos com tipos incompatíveis (%s e %s)" % (OPRD1["line"]+1, OPRD1["type"], OPRD2["type"]))
                self.semantic_error = True
        self.semantic_rules["17"] = rule17

        # LD -> OPRD
        def rule18(**kwargs):
            OPRD = kwargs['validation'].pop()
            kwargs['Alpha'] = copy(OPRD)

            return kwargs['Alpha']
        self.semantic_rules["18"] = rule18

        # OPRD -> id
        def rule19(**kwargs):
            id = kwargs["validation"].pop()

            # Verificar se id foi declarado
            if id["type"] is not "": 
                kwargs["Alpha"] = copy(id)

                return kwargs["Alpha"]
            else:
                print("Erro na linha %d: Variável não declarada (%s)" % (id["line"]+1, id["lexeme"]))
                self.semantic_error = True
        self.semantic_rules["19"] = rule19

        # OPRD -> num
        def rule20(**kwargs):
            num = kwargs["validation"].pop()

            # Copiar todos os atributos de num para os atributos de OPRD
            kwargs["Alpha"] = copy(num)
            return kwargs["Alpha"]
        self.semantic_rules["20"] = rule20

        # A -> COND A
        def rule21(**kwargs):

            return kwargs['Alpha']
        self.semantic_rules["21"] = rule21

        # COND -> CABEÇALHO	
        # CORPO
        def rule22(**kwargs):
            self.indent -= 1
            self.code_insert(snippet="}", indent=True)

            return kwargs['Alpha']
        self.semantic_rules["22"] = rule22

        # CABEÇALHO -> se
        # (EXP_R)	então
        def rule23(**kwargs):
            se = kwargs["validation"].pop()
            parenthesis = kwargs["validation"].pop()
            EXP_R = kwargs["validation"].pop()
            parenthesis = kwargs["validation"].pop()
            entao = kwargs["validation"].pop()
            # Imprimir ( if (EXP_R.lexema) { ) no arquivo objeto.
            text = "if (" + EXP_R["lexeme"] + ") {"
            self.indent += 1
            self.code_insert(snippet=text, indent=True)
            return kwargs['Alpha']
        self.semantic_rules["23"] = rule23

        # EXP_R -> OPRD opr
        # OPRD
        def rule24(**kwargs):
            OPRD1 = kwargs["validation"].pop()
            opr = kwargs["validation"].pop()
            OPRD2 = kwargs["validation"].pop()
            
            # Verificar se os tipos de dados de OPRD são iguais ou equivalentes para a
            # realização de comparação relacional.
            if OPRD1["type"] in ("real","inteiro") and OPRD2["type"] in ("real","inteiro"):
                self.Tx_count += 1
                kwargs["Alpha"]["lexeme"] = "T"+str(self.Tx_count)
                text = "T{} = {} {} {};".format(self.Tx_count, OPRD1["lexeme"], opr["lexeme"], OPRD2["lexeme"])
                self.code_insert(snippet=text, indent=True)
                return kwargs['Alpha']
            else:
                print("Erro na linha %d: Operandos com tipos incompatíveis (%s e %s)." % (OPRD1["line"]+1, OPRD1["type"], OPRD2["type"]))
        self.semantic_rules["24"] = rule24

        # CORPO -> ES CORPO 
        def rule25(**kwargs):

            return kwargs['Alpha']
        self.semantic_rules["25"] = rule25

        # CORPO -> CMD	
        # CORPO
        def rule26(**kwargs):

            return kwargs['Alpha']
        self.semantic_rules["26"] = rule26

        # CORPO -> COND	
        # CORPO
        def rule27(**kwargs):

            return kwargs['Alpha']
        self.semantic_rules["27"] = rule27

        # CORPO -> fimse
        def rule28(**kwargs):

            return kwargs['Alpha']
        self.semantic_rules["28"] = rule28

        # A -> fim
        def rule29(**kwargs):

            return kwargs['Alpha']
        self.semantic_rules["29"] = rule29

