from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        text = self.read_input()
        searched_string = "SANGUISORBA OFFICINALIS VAR. LONGIFOLIA RO"
        string_length = len(searched_string)
        step = int(float(len(text) / len(self.workers)))
        f = Solver.prefix(searched_string)

        # map
        mapped = []
        for i in xrange(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(text[i * step: i * step + step + string_length - 1], searched_string, f))
            
        print("Map finished")

        # reduce
        reduced = self.myreduce(mapped, text)
        print("Reduce finished: " + str(reduced))

        # output
        self.write_output(reduced)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(a, b, f):
        return Solver.kmp(b, a, f)
  

    @staticmethod
    @expose
    def myreduce(mapped, text):
        for i in xrange(0, len(mapped)):
            v = int(mapped[i].value)
            if(v != -1):
                return int(len(text)/len(mapped)*i + v)


    def read_input(self):
        f = open(self.input_file_name, 'r')
        input = f.read()
        f.close()
        return input

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()

    @staticmethod
    @expose
    def prefix(s):
        v = [0]*len(s)
        for i in range(1,len(s)):
            
            k = v[i-1]
            while k > 0 and s[k] != s[i]:
                k = v[k-1]
            if s[k] == s[i]:
                k = k + 1
            v[i] = k
        return v

    @staticmethod
    @expose
    def kmp(s,t,f):
        index = -1
        k = 0 #points to index in pattern
        for i in range(len(t)):
            while k > 0 and s[k] != t[i]:
                k = f[k-1] #if there were coincidences and they stopped, update the index in pattern according to prefix function 
            if s[k] == t[i]:
                k = k + 1 
            if k == len(s):
                index = i - len(s) + 1
                break
        return index