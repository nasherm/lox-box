class GenerateAst:
    def __init__(self, args=['.']):
        if len(args) != 1:
            return
        self.outputDir = args[0]

    def run(self):
        self.defineAst(
            "Expr",
           [
               "Binary   ; left:Expr, operator:Token, right:Expr",
               "Grouping ; expression:Expr",
               "Literal  ; value:Any",
               "Unary    ; operator:Token, right:Expr"
           ])

    def stripWhitespace(self, s: str):
        import re
        return re.sub('[s+]','', s)

    def defineAst(self, baseName: str, types: list):
        path = f'{self.outputDir}/{baseName}.py'
        fileWriter = open(path, 'w')
        fileWriter.write('from typing import Any\n')
        fileWriter.write('from plox.plox.Token import Token\n')
        fileWriter.write(f'class {baseName}:\n\tpass\n')
        fileWriter.write(f'\tdef accept(self,visitor): pass\n')
        self.defineVisitor(fileWriter, baseName, types)
        for type in types:
            className, fields = [
                x.strip() for x in type.split(';')]
            self.defineType(fileWriter, baseName, className, fields)
        fileWriter.write('\n')
        fileWriter.close()

    def defineType(self, fileWriter, baseName, className, fields):
        fileWriter.write(f'class {className}({baseName}):\n\t')
        fileWriter.write(f'def __init__(self,{fields}):\n');
        for field in fields.split(','):
            name = field.split(':')[0]
            fileWriter.write(f'\t\tself.{name} = {name}\n')
        fileWriter.write(f'\tdef accept(self, visitor:Visitor):\n')
        fileWriter.write(f'\t\treturn visitor.visit{className}{baseName}(self)\n')
        fileWriter.write('\n')

    def defineVisitor(self, fileWriter, baseName, types):
        fileWriter.write('class Visitor:\n')
        for type in types:
            typeName = type.split(';')[0].strip()
            fileWriter.write(f'\tdef visit{typeName}{baseName}(self,{typeName}{baseName.lower()}:Expr): pass\n')
        fileWriter.write('\n')

GenerateAst().run()