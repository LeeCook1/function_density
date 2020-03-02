import io
import os
import sys
import ast
import tokenize

def tokenize_string(s):
    try:
        tk=tokenize.tokenize(io.BytesIO(s.encode('utf-8')).readline)
    except tokeniz.TokenError as e:
        pass
    return tk

class FuncLengthCalc:
    def __init__(self, code_path):
        self.code_path = self._check_path(code_path)
        self.func_calc = {}
        self._calc_function_length()
        
    def get_executable_count(self):
        return self.func_calc

    def _check_path(self, path):
        """
        Checks :param `path` to see if it has a valid directory. If not, sets 
        path to None

        Parameters:
            path (str): The csv location

        Returns:
            str: If the path directory is valid, returns :param `path` else None
        
        """
        if path is None:
            return None
        if not os.path.isfile(path):
            print("Directory for {} don't exist".format(path)) # Error
            return None
        return path

    def _calc_function_length(self):
        func_count = {}
        with open(self.code_path,"r") as source:
            tree = ast.parse(source.read())
            source.seek(0)
            lines = source.readlines()
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef,ast.AsyncFunctionDef)):
                    func_str = "".join(lines[node.lineno-1:node.end_lineno])
                    func_count[node.name] ={
                        'lines': self._get_exec_lines(func_str),
                        'child_funcs':self. _get_nested_func(node)
                    }
        self.func_calc = self._update_exec_lines(func_count)

    def _get_exec_lines(self,func_str): 
        func_count = 0
        for tok in tokenize_string(func_str):
            line = tok.line.replace('"','').replace("'","").strip()
            if tok.type == tokenize.NEWLINE and line != "":
                func_count += 1
        return func_count

    def _get_nested_func(self,node):
        return [child_node.name for child_node in ast.walk(node) \
                if isinstance(child_node, (ast.FunctionDef,ast.AsyncFunctionDef)) and \
                child_node.name != node.name]

    def _update_exec_lines(self,func_count_dict):
        updated_func_count = {}
        for func_name in func_count_dict:
            for child in func_count_dict[func_name]['child_funcs']:
                func_count_dict[func_name]['lines'] -= func_count_dict[child]['lines']
            updated_func_count[func_name] = func_count_dict[func_name]['lines'] - 1
        return updated_func_count
        
def main():
    code_calc1 = FuncLengthCalc(sys.argv[1]).get_executable_count()
    code_calc2 = FuncLengthCalc(sys.argv[2]).get_executable_count()
    print(code_calc1)
    print(code_calc2)
if __name__ == "__main__":
    main()        
