from typing import Optional, List
from _token import *
from ast import *

import llvmlite.ir as ll
import llvmlite.binding as llvm

i32 = ll.IntType(32)
void = ll.VoidType()


class CodeGen:
    def code_gen(self, unit: Optional[StatementListAST]):

        self.init_llvm()
        self.variable_dict = {}

        # main
        main_func = ll.FunctionType(void, [])
        self.module = ll.Module()
        func = ll.Function(self.module, main_func, name="main")
        entry = func.append_basic_block()

        self.builder = ll.IRBuilder()
        self.builder.position_at_end(entry)

        for ast in unit.asts:
            self._gen(ast)

        self.builder.ret_void()

        llvm_ir = str(self.module)
        llvm_ir_parsed = llvm.parse_assembly(llvm_ir)
        print("== LLVM IR ====================")
        with open('main.ll', 'w') as f:
            f.write(str(llvm_ir_parsed))

    def _gen(self, ast: BaseAST):
        if isinstance(ast, AssignmentAST):
            return self._generate_assignment(ast)
        if isinstance(ast, DigitAST):
            return self._generate_digit(ast)
        if isinstance(ast, PrintAST):
            return self._generate_print(ast)
        else:
            return

    def init_llvm(self):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

    def _generate_print(self, ast):
        fmt = "%d\n\0"
        p_value = ll.Constant(ll.IntType(32), 1)
        try:
            printf = self.module.get_global('printf')
        except KeyError:
            voidptr_ty = ll.IntType(8).as_pointer()
            c_fmt = ll.Constant(ll.ArrayType(ll.IntType(8), len(fmt)),
                                bytearray(fmt.encode("utf8")))
            global_fmt = ll.GlobalVariable(self.module, c_fmt.type, name="fstr")
            global_fmt.linkage = 'internal'
            global_fmt.global_constant = True
            global_fmt.initializer = c_fmt
            printf_ty = ll.FunctionType(ll.IntType(32), [voidptr_ty], var_arg=True)
            printf = ll.Function(self.module, printf_ty, name="printf")
            self.fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)

            if isinstance(ast.arg, VariableAST):
                p_value = self._load_variable(ast.arg.name)
            if isinstance(ast.arg, DigitAST):
                p_value = ll.Constant(ll.IntType(32), ast.arg.value)

        self.builder.call(printf, [self.fmt_arg, p_value])
        return

    def _generate_translation_unit(self):
        pass

    def _generate_assignment(self, ast: AssignmentAST):
        ptr = self.builder.alloca(ll.IntType(32))
        name = ast.variable.name

        if isinstance(ast.value, DigitAST):
            self.builder.store(self._generate_digit(ast.value), ptr)
        if isinstance(ast.value, VariableAST):
            self.builder.store(self._load_variable(ast.value.name), ptr)
        self.variable_dict[name] = ptr

    def _load_variable(self, name):
        return self.builder.load(self.variable_dict[name])

    def _generate_digit(self, ast: DigitAST):
        return ll.Constant(i32, ast.value)

    def _generate_binary_expression(self):
        pass


if __name__ == '__main__':
    import sys
    from parser import Parser

    args = sys.argv
    if len(args) < 2:
        print("no input")
    else:
        p = Parser(args[1])
        p.parse()
        print(p.unit.asts, p.variable_table)

        gen = CodeGen()
        gen.code_gen(p.unit)
