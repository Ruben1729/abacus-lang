import subprocess


class AbacusCompiler:
    def __init__(self, file_path, asm_generator):
        self.asm_generator = asm_generator

        self.file_name = file_path[file_path.rfind("/"):file_path.rfind(".")]
        self.file_path = file_path[0:file_path.rfind("/")]

        self.file_asm = "%s.asm" % self.file_name
        self.file_obj = "%s.obj" % self.file_name
        self.file_exe = "%s.exe" % self.file_name

    def generate(self):
        out = open(self.file_path+self.file_asm, "w")

        for line in self.asm_generator.assembly_prefix:
            out.write(line)

        out.write("\n")

        for line in self.asm_generator.assembly_data:
            out.write(line)

        out.write("\n")

        for line in self.asm_generator.assembly_code:
            out.write(line)

        out.write("    exit_addr:\n")
        out.write("    invoke ExitProcess, 0\n")
        out.write("end main\n")
        out.close()

    def build(self):
        subprocess.run(["ml", "/c", "/Zd", "/coff", "."+self.file_asm], cwd=self.file_path, shell=True)

    def link(self):
        subprocess.run(["link", "/subsystem:console", "."+self.file_obj], cwd=self.file_path, shell=False)

    def execute(self):
        subprocess.Popen([r""+self.file_exe[1:len(self.file_exe)]], cwd=self.file_path, shell=True)