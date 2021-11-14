# https://docs.microsoft.com/en-us/cpp/assembler/masm/directives-reference?view=msvc-160
X86_64_RET_STACK_CAP = 8192


class AsmGenerator:
    def __init__(self):
        self.assembly_prefix = []
        self.assembly_data = []
        self.assembly_code = []

        self.assembly_prefix.append(".686\n")
        self.assembly_prefix.append(".model flat, stdcall\n")
        self.assembly_prefix.append("option casemap : none\n")

        self.assembly_prefix.append("include    \\masm32\\include\\kernel32.inc\n")
        self.assembly_prefix.append("include    \\masm32\\include\\masm32.inc\n")
        self.assembly_prefix.append("include    \\masm32\\include\\msvcrt.inc\n")
        self.assembly_prefix.append("includelib \\masm32\\lib\\kernel32.lib\n")
        self.assembly_prefix.append("includelib \\masm32\\lib\\masm32.lib\n")
        self.assembly_prefix.append("includelib \\masm32\\lib\\msvcrt.lib\n")
        self.assembly_prefix.append("\n")
        self.assembly_prefix.append("printf PROTO C, :VARARG\n")

        self.assembly_data.append(".data\n")
        self.assembly_data.append("    num_msg db \"%d\", 13, 10, 0\n")
        self.assembly_data.append("    char_msg db \"%c\", 0\n")

        self.assembly_data.append("\n")
        self.assembly_data.append(".data?\n")
        self.assembly_data.append("    ret_stack dword %d dup(?)\n" % X86_64_RET_STACK_CAP)
        self.assembly_data.append("    ret_stack_end dword 1 dup(?)\n")
        self.assembly_data.append("    mem dword 8192 dup(?)\n")
        self.assembly_data.append("\n")

        self.assembly_code.append(".code\n")
        self.assembly_code.append("\n")
        self.assembly_code.append("main:\n")

    def add_assembly_arr(self, variable):
        self.assembly_data.append(f"    {variable.get_assembly_addr()} {variable.get_assembly_type()} {variable.get_array_size()} dup (0)\n")

    def add_assembly_var(self, variable):
        self.assembly_data.append(f"    {variable.get_assembly_addr()} {variable.get_assembly_type()} 0\n")

    def add_assembly_line(self, new_code: str):
        self.assembly_code.append(new_code+"\n")


asm_generator = AsmGenerator()
