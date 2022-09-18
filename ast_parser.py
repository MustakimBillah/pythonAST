import ast


class FunctionDef:
    def __init__(self, name, param, start, className):
        self.name = name
        self.param = param
        self.start = start
        self.className = className


class FunctionCall:
    def __init__(self, name, param, start, attr):
        self.name = name
        self.param = param
        self.start = start
        self.attr = attr


class objectMap:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent


functionDefs = []
functionCalls = []
className = ""
classes = []
objectMapper = []
obj = ""
parent = ""


class Visitor(ast.NodeVisitor):

    def visit_Assign(self, node: ast.AST):
        # pprint(ast.dump(node.value), indent=4)
        global parent, obj
        if isinstance(node.value, ast.Call):
            parent = node.value.func.id

        for item in node.targets:
            if isinstance(item, ast.Name):
                obj = item.id

        objectMapper.append(objectMap(obj, parent))
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.AST):
        # print("Class Name:", node.name)
        global className
        className = node.name
        classes.append(className)
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                # print(item.name)
                className = node.name

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.AST):
        paramName = []
        if isinstance(node, ast.FunctionDef):
            for arg in node.args.args:
                # print("Parameter name:", arg.arg)
                if not arg.arg == "self":
                    paramName.append(arg.arg)
        # pprint(node.lineno)
        lineNo = node.lineno
        # pprint(node._fields)
        # print("function name:", node.name)
        funcName = node.name
        functionDefs.append(FunctionDef(funcName, paramName, lineNo, className))
        self.generic_visit(node)

    def visit_Call(self, node: ast.AST):
        lineNo = node.lineno
        params = []
        funcName = ""
        funcAttr = ""
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                funcName = node.func.value.id
                funcAttr = node.func.attr
                for item in node.args:
                    params.append(ast.dump(item))

        if isinstance(node.func, ast.Name):
            funcName = node.func.id
            for item in node.args:
                params.append(ast.dump(item))

        functionCalls.append(FunctionCall(funcName, params, lineNo, funcAttr))
        self.generic_visit(node)


def main():
    with open('calculator.py') as f:
        code = f.read()

    node = ast.parse(code)
    # pprint(ast.dump(node, indent=4))
    Visitor().visit(node)

    # for item in functionDefs: print("Function Def Start Line :", item.start, ", Function Name :", item.name, ",
    # Function Param :", item.param, ", Class:", item.className, "param size:", len(item.param))

    for item in functionCalls:
        print("")
        tracked = 0
        if item.name:
            print("<<<--------------->>>")
            print("Function Call Start Line :", item.start)
            if item.attr:
                print("Function Name :", item.attr)
            else:
                print("Function Name :", item.name)
            print("Function Params :", item.param)
        # print("")

        if item.attr:
            for element in objectMapper:
                if element.name == item.name:
                    # print("Class Name :", element.parent)
                    for entry in functionDefs:
                        if entry.name == item.attr and entry.className == element.parent and len(item.param) == len(
                                item.param):
                            print("Class Name :", element.parent)
                            print("Start Line No :", entry.start)
                            print("Params :", entry.param)
                            tracked = 1
                            break
        elif item.name:
            for element in functionDefs:
                if item.name == element.className and element.name == "__init__" \
                        and len(element.param) == len(item.param):
                    print("Class Name :", element.className, "(Constructor)")
                    print("Start Line No :", element.start)
                    print("Params :", element.param)
                    tracked = 1
                elif item.name == element.name and len(element.param) == len(item.param):
                    print("Class Name :", element.className)
                    print("Start Line No :", element.start)
                    print("Params :", element.param)
                    tracked = 1

        if item.name and tracked == 0:
            print("Comments : builtins or unable to track!")

    print("")


if __name__ == '__main__':
    main()
