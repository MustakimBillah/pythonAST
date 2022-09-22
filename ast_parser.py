import ast
import glob


class FunctionDef:
    def __init__(self, name, param, start, parent_class, file_name):
        self.name = name
        self.param = param
        self.start = start
        self.className = parent_class
        self.file_name = file_name


class FunctionCall:
    def __init__(self, name, param, start, attr, file_name):
        self.name = name
        self.param = param
        self.start = start
        self.attr = attr
        self.file_name = file_name


class ObjectMap:
    def __init__(self, name, obj_parent, file_name):
        self.name = name
        self.parent = obj_parent
        self.file_name = file_name


class ImportMap:
    def __init__(self, class_name, func_name, file_name):
        self.class_name = class_name
        self.func_name = func_name
        self.file_name = file_name


functionDefs = []
functionCalls = []
className = ""
classes = []
objectMapper = []
objectMapperCleaned = []
obj = ""
parent = ""
currentFile = ""
importMap = []


class Visitor(ast.NodeVisitor):

    def visit_Import(self, node: ast.AST):
        for item in node.names:
            importMap.append(ImportMap(item.name, "", currentFile))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.AST):
        for item in node.names:
            importMap.append(ImportMap(node.module, item.name, currentFile))
        self.generic_visit(node)

    def visit_Assign(self, node: ast.AST):
        global parent, obj
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name):
                parent = node.value.func.id
            elif isinstance(node.value.func, ast.Attribute):
                parent = node.value.func.value.id

        for item in node.targets:
            if isinstance(item, ast.Name):
                obj = item.id

        objectMapper.append(ObjectMap(obj, parent, currentFile))
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.AST):
        global className
        className = node.name
        classes.append(className)
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                # print(item.name)
                className = node.name

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.AST):
        param_name = []
        if isinstance(node, ast.FunctionDef):
            for arg in node.args.args:
                if not arg.arg == "self":
                    param_name.append(arg.arg)
        line_no = node.lineno
        func_name = node.name
        functionDefs.append(FunctionDef(func_name, param_name, line_no, className, currentFile))
        self.generic_visit(node)

    def visit_Call(self, node: ast.AST):
        line_no = node.lineno
        params = []
        func_name = ""
        func_attr = ""
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                func_name = node.func.value.id
                func_attr = node.func.attr
                for item in node.args:
                    params.append(ast.dump(item))

        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            for item in node.args:
                params.append(ast.dump(item))

        functionCalls.append(FunctionCall(func_name, params, line_no, func_attr, currentFile))
        self.generic_visit(node)


def main():
    for file in glob.glob("*.py"):
        global currentFile
        currentFile = file
        if file != 'ast_parser.py':
            with open(file) as f:
                code = f.read()
            node = ast.parse(code)
            # print(ast.dump(node, indent=4))
            Visitor().visit(node)

    for item in objectMapper:
        match = 0
        for element in classes:
            if item.parent == element:
                match = 1
                break
        if match == 1:
            objectMapperCleaned.append(item)

    for item in functionCalls:
        print("")
        function_name = ""
        tracked = 0
        if item.name:
            print("<<<--------------->>>")
            print("Function Call Start Line :", item.start)
            print("Inside File :", item.file_name)
            if item.attr:
                print("Function Name :", item.attr, "|| called as :", item.name + "." + item.attr)
                function_name = item.attr
            else:
                print("Function Name :", item.name)
                function_name = item.name
            print("Function Params :", item.param)

        if item.attr:
            for element in objectMapperCleaned:
                if element.name == item.name:
                    for entry in functionDefs:
                        if entry.name == item.attr and entry.className == element.parent and len(item.param) == len(
                                entry.param):
                            if entry.file_name == item.file_name:
                                print("Class Name :", element.parent)
                                print("Class Source :", entry.file_name)
                                print("Start Line No :", entry.start)
                                print("Params :", entry.param)
                                tracked = 1
                                break

            if tracked == 0:
                for entry in functionDefs:
                    if entry.name == item.attr and len(entry.param) == len(item.param):
                        if entry.file_name == item.file_name:
                            print("Class Name :", entry.className)
                            print("Class Source :", entry.file_name)
                            print("Start Line No :", entry.start)
                            print("Params :", entry.param)
                            tracked = 1
                            break
                        else:
                            for tuples in importMap:
                                if tuples.func_name == function_name and tuples.class_name + ".py" == entry.file_name:
                                    print("Class Name :", tuples.class_name)
                                    print("Class Source :", entry.file_name)
                                    print("Start Line No :", entry.start)
                                    print("Params :", entry.param)
                                    tracked = 1
                                    break
                            if tracked == 0:
                                for tuples in importMap:
                                    if tuples.class_name + ".py" == entry.file_name and len(tuples.func_name) == 0:
                                        print("Class Name :", tuples.class_name)
                                        print("Class Source :", entry.file_name)
                                        print("Start Line No :", entry.start)
                                        print("Params :", entry.param)
                                        tracked = 1
                                        break

        elif item.name and tracked == 0:
            for element in functionDefs:
                if item.name == element.className and element.name == "__init__" \
                        and len(element.param) == len(item.param):
                    print("Class Name :", element.className, "(Constructor)")
                    print("Class Source :", element.file_name)
                    print("Start Line No :", element.start)
                    print("Params :", element.param)
                    tracked = 1
                    break
                elif item.name == element.name and len(element.param) == len(item.param):
                    if item.file_name == element.file_name:
                        print("Class Name :", element.className)
                        print("Class Source :", element.file_name)
                        print("Start Line No :", element.start)
                        print("Params :", element.param)
                        tracked = 1
                        break
                    else:
                        for tuples in importMap:
                            if tuples.func_name == function_name and tuples.class_name + ".py" == element.file_name:
                                print("Class Name :", tuples.class_name)
                                print("Class Source :", element.file_name)
                                print("Start Line No :", element.start)
                                print("Params :", element.param)
                                tracked = 1
                                break

        if item.name and tracked == 0:
            if tracked == 0:
                print("Comments : builtins or unable to track!")


if __name__ == '__main__':
    main()
